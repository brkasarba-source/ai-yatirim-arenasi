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

import os as _os
if _os.path.exists("league.json"):
    lg = json.load(open("league.json", encoding="utf-8"))
    L += ["## Bot ligi: her bota 1000 $ sanal bütçe", "",
          f"Başlangıç {lg['start_date']} | son veri {lg['last_date']} | işlem günü {lg['days']}. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.", ""]
    if lg["days"] == 0:
        L += ["İlk işlem günü bekleniyor, tüm botlar nakitte.", ""]
    L += ["| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |", "|---|---:|---:|---:|---:|---:|"]
    for r in sorted(lg["board"], key=lambda x: -x["equity"]):
        L.append(f"| {r['bot']} | {r['equity']:.2f} | {r['return_pct']:.2f} | {r['maxdd_pct']:.2f} | {r['positions']} | {r['trades']} |")
    if lg["recent_trades"]:
        L += ["", "Son işlemler:", "", "| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |", "|---|---|---|---|---:|---:|---|"]
        for x in lg["recent_trades"][:12]:
            L.append(f"| {x['date']} | {x['bot']} | {x['side']} | {x['tic']} | {x['price']} | {x['value']} | {x['reason']} |")
    L += [""]
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

fq = _load("results/freqtrade_result.json")
if fq:
    L += ["## freqtrade (birlesik evren, 30 hisse)", "",
          "| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |", "|---|---:|---:|---:|---:|",
          f"| freqtrade RSI sablonu (hyperopt) | {fq['2025']['total_pct']} | {fq['2025']['sharpe_gunluk_cuzdan']} | {fq['2026']['total_pct']} | {fq['2026']['sharpe_gunluk_cuzdan']} |", "",
          "Hisseler Binance cift adlariyla etiketlendi (repos_tests/freqtrade/ft_mapping.json); icerideki veri hisse verisi. Yatirim tavsiyesi degildir.", ""]

fs = _load("results/finrl_seeds_summary.json")
if fs:
    o_ = fs["ozet"]
    L += ["## FinRL kararlilik testi (5 rastgele tohum, birlesik evren)", "",
          "| Ajan, yil | Tohum getirileri % | Ortalama | Std | Tum evren al-ve-tut'u gecen | ABD al-ve-tut'u gecen |", "|---|---|---:|---:|---:|---:|"]
    for k_, v_ in o_.items():
        L.append(f"| {k_.upper().replace('_', ' ')} | {', '.join(str(x) for x in v_['tohumlar'])} | {v_['ort']} | {v_['std']} | {v_['kazanan_tum_evren']}/5 | {v_['kazanan_abd']}/5 |")
    L += ["", "Referans (al-ve-tut %): tum evren 2025 +2.1, 2026 +0.4; sadece ABD 2025 +24.5, 2026 +15.5. Yatirim tavsiyesi degildir.", ""]

fh = _load("results/finrl_holdings_summary.json")
if fh:
    L += ["## FinRL ajanlari ne tutuyor? (5 tohum ortalamasi)", "",
          "| Ajan, yil | ABD agirligi % (tohum araligi) | BIST agirligi % | En cok tutulan hisseler |", "|---|---|---|---|"]
    for k_, v_ in fh.items():
        a_, b_ = v_["abd_pct"], v_["bist_pct"]
        top_ = ", ".join(f"{t} {p}" for t, p in v_["en_cok_tutulan"][:4])
        L.append(f"| {k_.upper().replace('_', ' ')} | {min(a_)}-{max(a_)} | {min(b_)}-{max(b_)} | {top_} |")
    L += ["", "Evrende BIST payi %67; ajanlar BIST'ten kacip buyuk ABD hisselerine yogunlasti. Yatirim tavsiyesi degildir.", ""]

ov = _load("results/own_bot_validation.json")
if ov:
    L += ["## Bizim bot (Trend EW): uzun geçmiş doğrulaması, 12 ETF, 2005-bugün", "",
          "Kurallar test öncesi sabitlendi. Yıllık getiri % / Sharpe / maks. düşüş %.", "",
          "| Dönem | Trend EW | Eşit ağırlık al-ve-tut | SPY al-ve-tut |", "|---|---|---|---|"]
    for k_, v_ in ov.items():
        f_ = lambda m_: f"{m_['cagr']} / {m_['sharpe']} / {m_['maxdd']}"
        L.append(f"| {k_} | {f_(v_['trend_ew'])} | {f_(v_['esit_agirlik_al_tut'])} | {f_(v_['spy_al_tut'])} |")
    L += ["", "Sonuç: düşüşleri çok iyi koruyor (2008'de -%7, SPY -%44) ama uzun vadede getiri geride (yıllık %4,2'ye karşı SPY %10,8). Yatırım tavsiyesi değildir.", ""]
open("STATUS.md", "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
