"""Long-only stratejilere piyasa dusus filtresi (risk kapatma). Filtreler OLCUMDEN ONCE sabitlendi, parametre aramasi yok:
  A: SPY kapanisi 200 gunluk ortalamanin altindaysa nakite gec
  B: SPY son 126 gunluk zirveden %8'den fazla dusmusse nakite gec
Filtre sinyal gibi kapanista hesaplanir, ertesi gun uygulanir. Donemler: 2016-2024 (2022 ayi dahil), 2025, 2026 (bugune kadar)."""
import json
import numpy as np, pandas as pd, yfinance as yf
import arena

PERIODS = {"2018-2024": ("2018-01-01", "2024-12-31"), "2025": ("2025-01-01", "2025-12-31"), "2026 (bugune kadar)": ("2026-01-01", "2026-12-31")}


def filters(spy):
    c = spy.Close
    return {"filtresiz": pd.Series(1.0, index=c.index),
            "A: SPY>SMA200": (c > c.rolling(200).mean()).astype(float),
            "B: dusus<%8": (c / c.rolling(126).max() - 1 > -0.08).astype(float)}


def main():
    px = yf.download(arena.TICKERS, start=arena.START, progress=False, auto_adjust=True)
    spy = px.xs("SPY", axis=1, level=1).dropna()
    flt = filters(spy)
    res = {}
    for name, (fam, fn) in arena.STRATS.items():
        for fname, f in flt.items():
            legs = []
            for t in arena.TICKERS:
                df = px.xs(t, axis=1, level=1).dropna()
                pos = (fn(df) * f.reindex(df.index).fillna(0)).shift(1).fillna(0)
                legs.append((pos * df.Close.pct_change() - pos.diff().abs().fillna(0) * arena.COST).rename(t))
            port = pd.concat(legs, axis=1).mean(axis=1)
            row = {}
            for label, (a, b) in PERIODS.items():
                seg = port[(port.index >= a) & (port.index <= b)]
                m = arena.metrics(seg)
                row[label] = {"total_pct": round(float(((1 + seg.fillna(0)).prod() - 1) * 100), 1), "sharpe": m["sharpe"], "maxdd": m["maxdd"]}
            res[f"{name} | {fname}"] = row
    json.dump(res, open("backtest_filter.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for label in PERIODS:
        print(f"\n=== {label} ===  (toplam getiri %, Sharpe, maks dusus %)")
        for k, v in sorted(res.items(), key=lambda kv: -kv[1][label]["sharpe"])[:9]:
            s = v[label]; print(f'{k:56s} {s["total_pct"]:7.1f} {s["sharpe"]:6.2f} {s["maxdd"]:7.1f}')
        bh = res["Buy & Hold (referans) | filtresiz"][label]
        print(f'{"[referans] Buy & Hold filtresiz":56s} {bh["total_pct"]:7.1f} {bh["sharpe"]:6.2f} {bh["maxdd"]:7.1f}')


if __name__ == "__main__":
    main()
