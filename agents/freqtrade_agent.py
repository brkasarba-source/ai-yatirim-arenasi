"""freqtrade ajanı için lig adaptörü: gerçek freqtrade backtest motoru çalıştırılır.
Freqtrade yalnızca borsa çiftleriyle çalıştığı için her hisse bir Kraken çift adıyla ETİKETLENİR (içerideki veri hisse verisidir).
Strateji: freqtrade'in "advanced" şablonu (RSI), 2016-2024'te hyperopt ile optimize edilmiş parametreler (StockSample.json).
Her çalıştırmada lig başlangıç tarihinden bugüne backtest çalıştırılır; bir hissenin işlemi açıkken (günün kapanışında) hedef ağırlık 1/N olur.
Not: freqtrade girişleri mum açılışında yapar; lig bu hedefi bir sonraki gün açılışında uygular (bir gün gecikmeli)."""
import glob, json, os, subprocess, sys, tempfile
import numpy as np, pandas as pd, yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAPPING = {"SPY": "BTC/USDT", "QQQ": "ETH/USDT", "AAPL": "XRP/USDT", "MSFT": "ADA/USDT", "NVDA": "LTC/USDT",
           "AMZN": "SOL/USDT", "GOOGL": "DOT/USDT", "TSLA": "DOGE/USDT", "JPM": "LINK/USDT", "XOM": "ATOM/USDT"}


def write_data():
    out = os.path.join(ROOT, "freqtrade_user", "data", "kraken")
    os.makedirs(out, exist_ok=True)
    raw = yf.download(list(MAPPING), start="2015-01-01", progress=False, auto_adjust=True)
    for t, pair in MAPPING.items():
        g = raw.xs(t, axis=1, level=1).dropna().reset_index()
        g.columns = [c.lower() for c in g.columns]
        g["date"] = pd.to_datetime(g["date"], utc=True)
        g[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True).to_feather(os.path.join(out, f"{pair.replace('/', '_')}-1d.feather"))


def targets(name, cal, close, opn, start_date, tickers):
    write_data()
    tr_dir = tempfile.mkdtemp()
    start = start_date.replace("-", "")
    cmd = [sys.executable, "-m", "freqtrade", "backtesting", "--config", os.path.join(ROOT, "freqtrade_config.json"), "--userdir", os.path.join(ROOT, "freqtrade_user"),
           "--strategy", "StockSample", "--timerange", f"{start}-", "--fee", "0.0015", "--export", "trades", "--export-directory", tr_dir]
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("freqtrade backtest basarisiz:\n" + res.stdout[-1500:] + res.stderr[-1500:])
    from freqtrade.data.btanalysis import load_backtest_data
    last = json.load(open(os.path.join(tr_dir, ".last_result.json")))["latest_backtest"]
    trades = load_backtest_data(os.path.join(tr_dir, last))
    inv = {v: k for k, v in MAPPING.items()}
    w = pd.DataFrame(0.0, index=cal, columns=tickers)
    idx = cal.tz_localize("UTC") if cal.tz is None else cal
    for _, t in trades.iterrows():
        tic = inv.get(t["pair"])
        if tic is None:
            continue
        o = pd.Timestamp(t["open_date"]).tz_convert("UTC").normalize(); c = pd.Timestamp(t["close_date"]).tz_convert("UTC").normalize()
        if str(t.get("exit_reason", "")) == "force_exit":
            c = pd.Timestamp("2100-01-01", tz="UTC")  # backtest sonunda zorla kapanan = hala acik
        mask = (idx >= o) & (idx < c)
        w.loc[mask, tic] = 1.0 / len(tickers)
    return w
