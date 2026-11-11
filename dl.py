"""yfinance indirme yardimcisi: tek is parcacigi + eksik hisse olursa tekrar dene (yfinance 'database is locked' hatasi gecici bos veri donduruyordu)."""
import time
import yfinance as yf


def download(tickers, start, tries=5, **kw):
    tickers = list(tickers)
    for i in range(tries):
        px = yf.download(tickers, start=start, progress=False, auto_adjust=True, threads=False, **kw)
        ok = not px.empty and all(px["Close"][t].dropna().size > 0 for t in tickers)
        if ok:
            return px
        print(f"UYARI: indirme eksik, tekrar deneniyor ({i + 1}/{tries})", flush=True)
        time.sleep(5 * (i + 1))
    raise RuntimeError("yfinance verisi eksik geldi: " + ",".join(tickers))
