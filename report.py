"""tracker.json + signals_log.csv -> STATUS.md (telefondan okunacak kisa durum raporu)"""
import csv, json
from collections import defaultdict

t = json.load(open("tracker.json", encoding="utf-8"))
m = sorted(t["metrics"], key=lambda r: -r["return_pct"])
base = next((r for r in t["metrics"] if r["strategy"].startswith("Buy")), None)

last_sig, tickers = {}, defaultdict(set)
with open("signals_log.csv", encoding="utf-8") as f:
    rows = list(csv.reader(f))
if rows:
    d = max(r[0] for r in rows)
    for dt, strat, tick, pos in rows:
        if dt == d:
            tickers[strat].add(tick)
            last_sig[strat] = last_sig.get(strat, 0) + float(pos)
    sig_date = d
else:
    sig_date = "-"

L = ["# Durum", ""]
if t["days"] == 0:
    L += [f"Takip {t['forward_start']} tarihinde basladi. Ilk islem gunu verisi bekleniyor.", ""]
else:
    L += [f"**Son veri:** {t['last_date']} | **Takip gunu:** {t['days']} | **Baslangic:** {t['forward_start']}", ""]
    if base:
        beat = [r["strategy"] for r in m if r["return_pct"] > base["return_pct"] and r is not base]
        L += [f"Al-ve-tut referansi: %{base['return_pct']:.2f}. Referansi gecen: {', '.join(beat) if beat else 'yok'}.", ""]
L += ["| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |", "|---|---:|---:|---:|"]
for r in m:
    n = len(tickers[r["strategy"]]) or 1
    pos = f"{int(last_sig.get(r['strategy'], 0))}/{n} hisse"
    L.append(f"| {r['strategy']} | {r['return_pct']:.2f} | {r['maxdd_pct']:.2f} | {pos} |")
L += ["", f"Son sinyal tarihi: {sig_date}. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.", ""]
open("STATUS.md", "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
