"""2025 testi: strateji sinyalleri sadece gecmis veriyle uretilir (ML her yil basinda onceki verilerle yeniden egitilir).
Long-only ve long/short (+1/-1) karsilastirilir. 2025 = dogrulama, 2026 (bugune kadar) = dokunulmamis ikinci test.
Maliyet: pozisyon degisiminde %0,15 (long->short donusu 2 birim), short icin yillik %1 odunc maliyeti."""
import json
import numpy as np, pandas as pd, yfinance as yf
import arena

BORROW = 0.01 / 252
PERIODS = {"2025": ("2025-01-01", "2025-12-31"), "2026 (bugune kadar)": ("2026-01-01", "2026-12-31")}


def run(pos, close):
    pos = pos.shift(1).fillna(0)  # sinyal kapanista, uygulama ertesi gun
    r = pos * close.pct_change() - pos.diff().abs().fillna(0) * arena.COST - (pos < 0) * BORROW
    return pos, r


def trades(pos, close):
    """Pozisyon bloklari: giris/cikis tarihi, yon, getiri."""
    out, cur, entry_i = [], 0, None
    idx = close.index
    for i in range(len(pos)):
        p = pos.iloc[i]
        if p != cur:
            if cur != 0 and entry_i is not None:
                ret = (close.iloc[i] / close.iloc[entry_i] - 1) * cur - 2 * arena.COST
                out.append((idx[entry_i], idx[i], cur, ret))
            cur, entry_i = p, (i if p != 0 else None)
    if cur != 0 and entry_i is not None:
        ret = (close.iloc[-1] / close.iloc[entry_i] - 1) * cur - arena.COST
        out.append((idx[entry_i], idx[-1], cur, ret))
    return out


def main():
    px = yf.download(arena.TICKERS, start=arena.START, progress=False, auto_adjust=True)
    res = {}
    for name, (fam, fn) in arena.STRATS.items():
        for mode in ("long", "long/short"):
            legs, tr_all = [], []
            for t in arena.TICKERS:
                df = px.xs(t, axis=1, level=1).dropna()
                sig = fn(df)
                raw = sig if mode == "long" else 2 * sig - 1
                pos, r = run(raw, df.Close)
                legs.append(r.rename(t))
                tr_all += [(t, *x) for x in trades(pos, df.Close)]
            port = pd.concat(legs, axis=1).mean(axis=1)
            row = {}
            for label, (a, b) in PERIODS.items():
                seg = port[(port.index >= a) & (port.index <= b)]
                m = arena.metrics(seg)
                tr = [x for x in tr_all if pd.Timestamp(a) <= x[1] <= pd.Timestamp(b)]
                rets = np.array([x[4] for x in tr]) if tr else np.array([])
                row[label] = {
                    "total_pct": round(float(((1 + seg.fillna(0)).prod() - 1) * 100), 1),
                    "sharpe": m["sharpe"] if m else None, "maxdd": m["maxdd"] if m else None,
                    "trades": len(tr), "win_rate": round(float((rets > 0).mean() * 100), 0) if len(rets) else None,
                    "avg_trade_pct": round(float(rets.mean() * 100), 2) if len(rets) else None,
                }
            res[f"{name} | {mode}"] = row
    json.dump(res, open("backtest_ls.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for label in PERIODS:
        print(f"\n=== {label} ===")
        print(f'{"strateji | yon":52s} {"getiri%":>8s} {"sharpe":>7s} {"dusus%":>7s} {"islem":>6s} {"kazanc%":>8s}')
        for k, v in sorted(res.items(), key=lambda kv: -kv[1][label]["total_pct"]):
            s = v[label]
            print(f'{k:52s} {s["total_pct"]:8.1f} {s["sharpe"] or 0:7.2f} {s["maxdd"] or 0:7.1f} {s["trades"]:6d} {s["win_rate"] or 0:8.0f}')


if __name__ == "__main__":
    main()
