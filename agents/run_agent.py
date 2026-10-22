"""Bir ajanı kendi Python ortamında çalıştırıp hedef ağırlıkları CSV'ye yazar. Kullanım:
python agents/run_agent.py "<bot adı>" <modül> <başlangıç tarihi> <çıkış.csv>"""
import importlib, os, sys
import pandas as pd, yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]


def main():
    name, mod, start, out = sys.argv[1:5]
    px = yf.download(TICKERS, start="2015-01-01", progress=False, auto_adjust=True)
    cal = px["Close"]["SPY"].dropna().index
    w = importlib.import_module("agents." + mod).targets(name, cal, None, None, start, TICKERS)
    w.reindex(columns=TICKERS).to_csv(out)
    print("hedef ağırlıklar yazıldı:", out, w.shape)


if __name__ == "__main__":
    main()
