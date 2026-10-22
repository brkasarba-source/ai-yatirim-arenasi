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
import os


def _load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


fr, ql = _load("results/finrl_result.json"), _load("results/qlib_result.json")
if fr and ql:
    L += ["## Gercek repolar: FinRL ve qlib (2025 ve 2026 testi)", "",
          "Egitim 2016-2024 (qlib: 2016-2022), ajanlarin hic gormedigi donemlerde test. Ayni 10 hisse/ETF, %0,15 maliyet.", "",
          "| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |", "|---|---:|---:|---:|---:|"]
    rows_ = [("Al-ve-tut (FinRL donemi)", fr["buy_hold"]), ("FinRL PPO", fr["ppo"]), ("FinRL A2C", fr["a2c"]),
             ("Al-ve-tut (qlib donemi)", {y: ql[y]["al_ve_tut"] for y in ("2025", "2026")}),
             ("qlib LightGBM ilk 5", {y: ql[y]["qlib_lgbm_top5"] for y in ("2025", "2026")})]
    for n_, d_ in rows_:
        L.append(f"| {n_} | {d_['2025']['total_pct']} | {d_['2025']['sharpe']} | {d_['2026']['total_pct']} | {d_['2026']['sharpe']} |")
    L += ["", f"qlib ortalama IC: {ql['ic_ort']} (sifira yakin: model hisseleri ayirt edemedi).",
          "Sonuc: hicbiri iki yilda tutarli bicimde al-ve-tut'u gecemedi. FinRL egitimi kisa (60 bin adim, tek tohum); qlib 10 hisselik kucuk evrende zayif bir test. Kodlar: repos_tests/", ""]

fc, qc = _load("results/finrl_combined_result.json"), _load("results/qlib_combined_result.json")
if fc and qc:
    L += ["## Birlesik evren: 10 ABD + 20 BIST (hepsi USD)", "",
          "| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |", "|---|---:|---:|---:|---:|"]
    def _r(n_, a_, b_):
        L.append(f"| {n_} | {a_['total_pct']} | {a_['sharpe']} | {b_['total_pct']} | {b_['sharpe']} |")
    for k_, n_ in (("tum_evren", "Al-ve-tut, tum evren"), ("sadece_abd", "Al-ve-tut, sadece ABD"), ("sadece_bist", "Al-ve-tut, sadece BIST (USD)")):
        _r(n_, fc["buy_hold"]["2025"][k_], fc["buy_hold"]["2026"][k_])
    _r("FinRL PPO", fc["ppo"]["2025"], fc["ppo"]["2026"])
    _r("FinRL A2C", fc["a2c"]["2025"], fc["a2c"]["2026"])
    _r("qlib LightGBM ilk 10", qc["2025"]["qlib_lgbm_top10"], qc["2026"]["qlib_lgbm_top10"])
    L += ["", f"qlib IC: {qc['ic_ort']}, ortalama BIST agirligi: %{qc['ortalama_agirlik_bist_pct']}. FinRL tek tohum, 100 bin adim. Yatirim tavsiyesi degildir.", ""]
open("STATUS.md", "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
