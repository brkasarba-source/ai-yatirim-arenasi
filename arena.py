"""Ortak backtest arenasi: ayni veri, ayni komisyon/kayma, gunluk sinyal ertesi gun uygulanir -> arena.json
Not: GitHub repolarinin kodu dogrudan calistirilmaz; her repo ailesinin tipik strateji turu ayni kurallarla test edilir."""
import json
import numpy as np, pandas as pd, yfinance as yf
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
START, OOS_START = "2016-01-01", "2024-01-01"
COST = 0.0010 + 0.0005  # komisyon + kayma, pozisyon degisiminde


def rsi(c, n=14):
    d = c.diff(); up = d.clip(lower=0).rolling(n).mean(); dn = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + up / dn)


def sig_bh(df): return pd.Series(1.0, index=df.index)
def sig_sma(df): c = df.Close; return (c.rolling(20).mean() > c.rolling(100).mean()).astype(float)
def sig_rsi(df):
    r = rsi(df.Close); s = pd.Series(np.nan, index=df.index)
    s[r < 30] = 1; s[r > 60] = 0
    return s.ffill().fillna(0)
def sig_mom(df): return (df.Close.pct_change(126) > 0).astype(float)
def sig_boll(df):
    c = df.Close; m = c.rolling(20).mean(); sd = c.rolling(20).std(); s = pd.Series(np.nan, index=df.index)
    s[c < m - 2 * sd] = 1; s[c > m] = 0
    return s.ffill().fillna(0)
def sig_macd(df):
    c = df.Close; macd = c.ewm(span=12).mean() - c.ewm(span=26).mean()
    return (macd > macd.ewm(span=9).mean()).astype(float)


def features(df):
    c = df.Close; f = pd.DataFrame(index=df.index)
    for n in (1, 5, 10, 21, 63): f[f"r{n}"] = c.pct_change(n)
    f["vol21"] = c.pct_change().rolling(21).std(); f["rsi"] = rsi(c) / 100
    f["sma"] = c / c.rolling(50).mean() - 1
    return f


def ml_signal(df, model_cls, kwargs):
    """Walk-forward: her yil basinda gecmis veriyle egit, o yil tahmin et (gelecek sizintisi yok)."""
    f = features(df); y = (df.Close.pct_change().shift(-1) > 0).astype(int)
    sig = pd.Series(0.0, index=df.index)
    for yr in sorted(set(df.index.year)):
        te = f.index.year == yr; tr = (f.index < pd.Timestamp(f"{yr}-01-01")) & f.notna().all(axis=1)
        if tr.sum() < 500: continue
        m = model_cls(**kwargs).fit(f[tr].values, y[tr].values)
        p = m.predict_proba(f[te].fillna(0).values)[:, 1]
        sig[te] = (p > 0.52).astype(float)
    return sig


STRATS = {
    "Buy & Hold (referans)": ("Referans", sig_bh),
    "SMA 20/100 Kesişim": ("freqtrade tipi klasik", sig_sma),
    "RSI Ortalamaya Dönüş": ("freqtrade tipi klasik", sig_rsi),
    "Bollinger Dönüş": ("freqtrade tipi klasik", sig_boll),
    "MACD Trend": ("freqtrade tipi klasik", sig_macd),
    "6 Ay Momentum": ("qlib / faktör tipi", sig_mom),
    "ML: Lojistik (walk-forward)": ("qlib / ai-hedge-fund tipi ML", lambda d: ml_signal(d, LogisticRegression, dict(max_iter=500))),
    "ML: Gradient Boosting (walk-forward)": ("qlib / FinRL tipi ML", lambda d: ml_signal(d, GradientBoostingClassifier, dict(n_estimators=60, max_depth=2, random_state=0))),
}


def metrics(r):
    r = r.dropna()
    if len(r) < 50: return None
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    sharpe = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else 0
    dd = (eq / eq.cummax() - 1).min()
    return {"cagr": round(cagr * 100, 1), "sharpe": round(float(sharpe), 2), "maxdd": round(dd * 100, 1)}


def main():
    px = yf.download(TICKERS, start=START, progress=False, auto_adjust=True)
    out = {"tickers": TICKERS, "oos_start": OOS_START, "cost_bps": COST * 1e4, "strategies": {}, "curves": {}}
    for name, (fam, fn) in STRATS.items():
        rets = []
        for t in TICKERS:
            df = px.xs(t, axis=1, level=1).dropna()
            pos = fn(df).shift(1).fillna(0)  # ertesi gun uygula
            r = pos * df.Close.pct_change() - pos.diff().abs().fillna(0) * COST
            rets.append(r.rename(t))
        port = pd.concat(rets, axis=1).mean(axis=1)  # esit agirlikli sepet
        full, oos = port, port[port.index >= OOS_START]
        train = port[port.index < OOS_START]
        out["strategies"][name] = {"family": fam, "full": metrics(full), "train": metrics(train), "oos": metrics(oos)}
        eq = (1 + oos.fillna(0)).cumprod()
        out["curves"][name] = [round(float(v), 4) for v in eq.iloc[::5]]
        out["dates"] = [d.strftime("%Y-%m-%d") for d in eq.index[::5]]
        print(name, out["strategies"][name]["oos"])
    json.dump(out, open("arena.json", "w", encoding="utf-8"), ensure_ascii=False)


if __name__ == "__main__":
    main()
