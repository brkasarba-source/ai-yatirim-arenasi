"""Kendi botumuz: "Trend EW". KURALLAR TEST EDILMEDEN ONCE SABITLENDI, sonuca gore ayarlanmadi:
  Bir varlik ancak (kapanis > 200 gunluk ortalama) VE (126 gunluk getiri > 0) ise tutulur; aksi halde o dilim nakitte.
  Her varlik esit dilim (1/N). Karar kapanista, uygulama ertesi gun. Maliyet: islem basina %0,15.
Dogrulama: yanlilik icermeyen (hayatta kalma yanliligi olmayan) 12 ETF evreninde 2005-bugun (2008, 2020, 2022 dususlerini icerir).
Calistir: python own_bot.py"""
import json
import numpy as np, pandas as pd, yfinance as yf

COST = 0.0015
ETFS = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "IEF", "GLD", "XLE", "XLF", "XLV", "XLU"]


def sig_trend_ew(df):
    c = df.Close
    return ((c > c.rolling(200).mean()) & (c.pct_change(126) > 0)).astype(float)


def metrics(r):
    r = r.dropna(); eq = (1 + r).cumprod(); yrs = len(r) / 252
    return {"cagr": round(float(eq.iloc[-1] ** (1 / yrs) - 1) * 100, 1), "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2),
            "maxdd": round(float((eq / eq.cummax() - 1).min() * 100), 1), "total": round(float((eq.iloc[-1] - 1) * 100), 0)}


def main():
    px = yf.download(ETFS, start="2003-06-01", progress=False, auto_adjust=True)
    legs, bh = [], []
    for t in ETFS:
        df = px.xs(t, axis=1, level=1).dropna()
        pos = sig_trend_ew(df).shift(1).fillna(0)
        r = pos * df.Close.pct_change() - pos.diff().abs().fillna(0) * COST
        legs.append(r.rename(t)); bh.append(df.Close.pct_change().rename(t))
    bot = pd.concat(legs, axis=1).mean(axis=1)
    ew = pd.concat(bh, axis=1).mean(axis=1)
    spy = px.xs("SPY", axis=1, level=1).Close.pct_change()
    start = "2005-01-01"
    out = {}
    windows = {"2005-bugun": (start, "2030-01-01"), "2008 krizi": ("2008-01-01", "2009-03-31"), "2020 cokusu": ("2020-01-01", "2020-06-30"),
               "2022 dususu": ("2022-01-01", "2022-12-31"), "2023-bugun": ("2023-01-01", "2030-01-01")}
    for k, (a, b) in windows.items():
        sel = lambda s: s[(s.index >= a) & (s.index <= b)]
        out[k] = {"trend_ew": metrics(sel(bot)), "esit_agirlik_al_tut": metrics(sel(ew)), "spy_al_tut": metrics(sel(spy))}
        print(k, "| bot", out[k]["trend_ew"], "| EW", out[k]["esit_agirlik_al_tut"], "| SPY", out[k]["spy_al_tut"])
    json.dump(out, open("own_bot_validation.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
