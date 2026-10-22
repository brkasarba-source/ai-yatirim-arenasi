"""Birlesik evren: 10 ABD hisse/ETF + 20 BIST hissesi, hepsi USD cinsinden (BIST fiyati / USDTRY).
Tatil gunleri ileri doldurulur (getiri 0). Cikti: panel_usd.csv (FinRL) ve qlib_data_comb (qlib).
Calistir: C:/Users/Brk_A/qlib_env/Scripts/python.exe universe.py"""
import os, subprocess, sys
import pandas as pd, yfinance as yf

US = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
BIST = ["THYAO", "GARAN", "AKBNK", "ISCTR", "YKBNK", "KCHOL", "SAHOL", "EREGL", "TUPRS", "ASELS",
        "BIMAS", "SISE", "FROTO", "TOASO", "PGSUS", "TCELL", "ARCLK", "PETKM", "KRDMD", "SASA"]
START = "2015-01-01"
CSV, OUT = "C:/Users/Brk_A/qlib_csv_comb", "C:/Users/Brk_A/qlib_data_comb"

us = yf.download(US, start=START, progress=False, auto_adjust=True)
bi = yf.download([b + ".IS" for b in BIST], start=START, progress=False, auto_adjust=True)
fx = yf.download("USDTRY=X", start=START, progress=False, auto_adjust=True)["Close"].iloc[:, 0]

frames = {}
for t in US:
    frames[t] = us.xs(t, axis=1, level=1)[["Open", "High", "Low", "Close", "Volume"]]
for b in BIST:
    d = bi.xs(b + ".IS", axis=1, level=1)[["Open", "High", "Low", "Close", "Volume"]].dropna(how="all")
    rate = fx.reindex(d.index, method="ffill")
    for c in ("Open", "High", "Low", "Close"):
        d[c] = d[c] / rate
    frames["B_" + b] = d  # ayirt etmek icin onek

cal = sorted(set().union(*[set(f.dropna().index) for f in frames.values()]))
cal = pd.DatetimeIndex(cal)
rows, bad = [], []
for tic, f in frames.items():
    f = f.reindex(cal).ffill()
    f = f.dropna()
    if f.index[0] > pd.Timestamp("2016-06-01") or len(f) < 2000:
        bad.append(tic); continue
    f = f.reset_index().rename(columns={"index": "date", "Date": "date"})
    f.columns = [c.lower() for c in f.columns]
    f["tic"] = tic
    rows.append(f)
panel = pd.concat(rows)
panel["date"] = pd.to_datetime(panel["date"]).dt.strftime("%Y-%m-%d")
# her hisse ayni tarihleri paylasmali
common = set.intersection(*[set(g["date"]) for _, g in panel.groupby("tic")])
panel = panel[panel["date"].isin(common)].sort_values(["date", "tic"])
panel.to_csv("panel_usd.csv", index=False)
print("atlanan:", bad, "| hisse:", panel["tic"].nunique(), "| gun:", len(common), "|", min(common), "->", max(common))

os.makedirs(CSV, exist_ok=True)
for tic, g in panel.groupby("tic"):
    g = g.copy(); g["factor"] = 1.0; g["vwap"] = (g["high"] + g["low"] + g["close"]) / 3
    g[["date", "open", "high", "low", "close", "volume", "factor", "vwap"]].to_csv(f"{CSV}/{tic}.csv", index=False)
subprocess.run([sys.executable, "C:/Users/Brk_A/qlib_src/scripts/dump_bin.py", "dump_all", "--data_path", CSV, "--qlib_dir", OUT, "--freq", "day",
                "--date_field_name", "date", "--include_fields", "open,high,low,close,volume,factor,vwap"], check=True, capture_output=True)
print("qlib verisi hazir:", len(os.listdir(OUT + "/features")), "enstruman")
