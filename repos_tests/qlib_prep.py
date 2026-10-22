"""yfinance fiyatlarini qlib ikili formatina cevirir (qlib'in kendi dump_bin.py betigiyle)."""
import os, subprocess, sys
import yfinance as yf

TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
CSV = "C:/Users/Brk_A/qlib_csv"; OUT = "C:/Users/Brk_A/qlib_data"
os.makedirs(CSV, exist_ok=True)
raw = yf.download(TICKERS, start="2015-01-01", progress=False, auto_adjust=True)
for t in TICKERS:
    d = raw.xs(t, axis=1, level=1).dropna().reset_index()
    d.columns = [c.lower() for c in d.columns]
    d["factor"] = 1.0
    d["vwap"] = (d["high"] + d["low"] + d["close"]) / 3
    d["date"] = d["date"].dt.strftime("%Y-%m-%d")
    d[["date", "open", "high", "low", "close", "volume", "factor", "vwap"]].to_csv(f"{CSV}/{t}.csv", index=False)
subprocess.run([sys.executable, "C:/Users/Brk_A/qlib_src/scripts/dump_bin.py", "dump_all", "--data_path", CSV, "--qlib_dir", OUT,
                "--freq", "day", "--date_field_name", "date", "--include_fields", "open,high,low,close,volume,factor,vwap"], check=True)
print("tamam", len(os.listdir(OUT + "/features")), "enstruman")
