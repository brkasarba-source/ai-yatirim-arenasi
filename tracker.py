"""Gunluk forward-test takipcisi (ucretsiz: yfinance + yerel dosyalar).
Her calistirmada: fiyatlari ceker, arena stratejilerinin sinyallerini hesaplar, FORWARD_START'tan beri
sanal sepet degerini yeniden uretir (tum sinyaller sadece gecmis veriyle hesaplandigi icin tekrar calistirmak guvenlidir)
ve her gunun sinyal kararini signals_log.csv'ye BIR KEZ ekler (degistirilmez kayit).
Cikti: tracker.json (egriler + metrikler)"""
import csv, json, os
import numpy as np, pandas as pd, yfinance as yf
import arena

FORWARD_START = "2026-10-22"
SIGNAL_START = "2026-10-21"  # 21 Ekim kapanisinda verilen karar 22 Ekim getirisini belirler
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    px = yf.download(arena.TICKERS, start=arena.START, progress=False, auto_adjust=True)
    rets, today_pos = {}, []
    for name, (fam, fn) in arena.STRATS.items():
        legs = []
        for t in arena.TICKERS:
            df = px.xs(t, axis=1, level=1).dropna()
            raw = fn(df)
            pos = raw.shift(1).fillna(0)
            r = pos * df.Close.pct_change() - pos.diff().abs().fillna(0) * arena.COST
            legs.append(r.rename(t))
            today_pos.append((df.index[-1].strftime("%Y-%m-%d"), name, t, float(raw.iloc[-1])))
        rets[name] = pd.concat(legs, axis=1).mean(axis=1)
    fwd = {n: r[r.index >= FORWARD_START] for n, r in rets.items()}
    dates = fwd[next(iter(fwd))].index
    out = {"forward_start": FORWARD_START, "last_date": dates[-1].strftime("%Y-%m-%d") if len(dates) else None,
           "days": len(dates), "curves": [], "metrics": []}
    eq = {n: (1 + r.fillna(0)).cumprod() for n, r in fwd.items()}
    for d in dates:
        out["curves"].append({"date": d.strftime("%Y-%m-%d"), **{n: round(float(eq[n].loc[d]), 4) for n in eq}})
    for n, r in fwd.items():
        m = arena.metrics(r) if len(r) >= 50 else None
        out["metrics"].append({"strategy": n, "family": arena.STRATS[n][0],
                               "return_pct": round(float(eq[n].iloc[-1] - 1) * 100, 2) if len(r) else 0.0,
                               "maxdd_pct": round(float((eq[n] / eq[n].cummax() - 1).min()) * 100, 2) if len(r) else 0.0,
                               "sharpe": m["sharpe"] if m else None})
    json.dump(out, open(os.path.join(HERE, "tracker.json"), "w", encoding="utf-8"), ensure_ascii=False)

    log = os.path.join(HERE, "signals_log.csv")
    done = set()
    if os.path.exists(log):
        with open(log, encoding="utf-8") as f:
            done = {row[0] for row in csv.reader(f)}
    new = [p for p in today_pos if p[0] not in done and p[0] >= SIGNAL_START]
    with open(log, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for p in new:
            w.writerow(p)
    print("son gun:", out["last_date"], "| forward gun:", out["days"], "| yeni sinyal satiri:", len(new))
    for m in out["metrics"]:
        print(f'{m["strategy"]:40s} getiri %{m["return_pct"]:6.2f}  dusus %{m["maxdd_pct"]:6.2f}')


if __name__ == "__main__":
    main()
