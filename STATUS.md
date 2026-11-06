# Durum

## Bot ligi: her bota 1000 $ sanal bütçe

Başlangıç 2026-10-22 | son veri 2026-11-05 | işlem günü 10. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.

| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |
|---|---:|---:|---:|---:|---:|
| FinRL PPO | 995.41 | -0.46 | -0.64 | 5 | 11 |
| Bollinger | 990.24 | -0.98 | -2.25 | 4 | 10 |
| freqtrade RSI | 989.53 | -1.05 | -1.33 | 4 | 4 |
| MACD | 981.80 | -1.82 | -2.62 | 3 | 11 |
| FinRL A2C | 979.51 | -2.05 | -4.39 | 9 | 50 |
| Momentum 6 ay | 976.33 | -2.37 | -3.74 | 5 | 15 |
| Trend EW (bizim bot) | 975.38 | -2.46 | -3.60 | 5 | 15 |
| qlib LightGBM | 973.86 | -2.61 | -4.85 | 5 | 45 |
| RSI | 970.00 | -3.00 | -3.50 | 4 | 4 |
| SMA 20/100 | 969.37 | -3.06 | -4.90 | 7 | 9 |
| Gradient Boosting ML | 961.89 | -3.81 | -4.67 | 5 | 29 |
| Al-ve-tut (referans) | 953.49 | -4.65 | -6.68 | 10 | 10 |
| Lojistik ML | 948.39 | -5.16 | -6.27 | 8 | 10 |

Son işlemler:

| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |
|---|---|---|---|---:|---:|---|
| 2026-11-05 | Trend EW (bizim bot) | SAT | QQQ | 683.12 | 97.28 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-05 | Trend EW (bizim bot) | SAT | TSLA | 374.12 | 94.99 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-05 | Trend EW (bizim bot) | SAT | NVDA | 196.07 | 95.78 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-05 | SMA 20/100 | SAT | QQQ | 683.12 | 97.28 | 20 günlük ort. 100 günlüğün altına indi (trend aşağı) |
| 2026-11-05 | Momentum 6 ay | SAT | QQQ | 683.12 | 97.28 | Son 126 günlük getiri negatife döndü |
| 2026-11-05 | Momentum 6 ay | SAT | TSLA | 374.12 | 95.23 | Son 126 günlük getiri negatife döndü |
| 2026-11-05 | Momentum 6 ay | SAT | NVDA | 196.07 | 90.63 | Son 126 günlük getiri negatife döndü |
| 2026-11-05 | MACD | AL | AMZN | 271.43 | 100.02 | MACD sinyal çizgisini yukarı kesti |
| 2026-11-05 | Lojistik ML | SAT | MSFT | 554.94 | 107.18 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-05 | Gradient Boosting ML | SAT | SPY | 765.47 | 100.73 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-05 | Gradient Boosting ML | SAT | XOM | 171.06 | 92.55 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-05 | Gradient Boosting ML | SAT | MSFT | 554.94 | 106.13 | Model yükseliş ihtimalini <=%52 gördü |

**Son veri:** 2026-11-05 | **Takip gunu:** 11 | **Baslangic:** 2026-10-22

Al-ve-tut referansi: %-6.71. Referansi gecen: MACD Trend, Bollinger Dönüş, RSI Ortalamaya Dönüş, 6 Ay Momentum, SMA 20/100 Kesişim, ML: Gradient Boosting (walk-forward).

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| MACD Trend | -2.53 | -2.24 | 2/10 hisse |
| Bollinger Dönüş | -2.71 | -2.67 | 6/10 hisse |
| RSI Ortalamaya Dönüş | -2.94 | -3.47 | 4/10 hisse |
| 6 Ay Momentum | -3.37 | -3.05 | 5/10 hisse |
| SMA 20/100 Kesişim | -4.61 | -4.70 | 6/10 hisse |
| ML: Gradient Boosting (walk-forward) | -5.07 | -4.14 | 6/10 hisse |
| Buy & Hold (referans) | -6.71 | -6.61 | 10/10 hisse |
| ML: Lojistik (walk-forward) | -7.20 | -6.23 | 9/10 hisse |

Son sinyal tarihi: 2026-11-05. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

## Gercek repolar: FinRL ve qlib (2025 ve 2026 testi)

Egitim 2016-2024 (qlib: 2016-2022), ajanlarin hic gormedigi donemlerde test. Ayni 10 hisse/ETF, %0,15 maliyet.

| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |
|---|---:|---:|---:|---:|
| Al-ve-tut (FinRL donemi) | 24.5 | 1.03 | 15.5 | 1.29 |
| FinRL PPO | 22.6 | 1.05 | 4.7 | 0.42 |
| FinRL A2C | 15.5 | 0.56 | -3.1 | -0.02 |
| Al-ve-tut (qlib donemi) | 26.3 | 1.06 | 17.3 | 1.35 |
| qlib LightGBM ilk 5 | -9.1 | -0.16 | 0.3 | 0.11 |

qlib ortalama IC: 0.01 (sifira yakin: model hisseleri ayirt edemedi).
Sonuc: hicbiri iki yilda tutarli bicimde al-ve-tut'u gecemedi. FinRL egitimi kisa (60 bin adim, tek tohum); qlib 10 hisselik kucuk evrende zayif bir test. Kodlar: repos_tests/

## Birlesik evren: 10 ABD + 20 BIST (hepsi USD)

| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |
|---|---:|---:|---:|---:|
| Al-ve-tut, tum evren | 2.1 | 0.2 | 0.4 | 0.12 |
| Al-ve-tut, sadece ABD | 24.5 | 1.01 | 15.5 | 1.27 |
| Al-ve-tut, sadece BIST (USD) | -9.1 | -0.22 | -7.1 | -0.2 |
| FinRL PPO | 9.7 | 0.48 | 10.4 | 0.56 |
| FinRL A2C | 24.7 | 1.04 | 8.0 | 0.64 |
| qlib LightGBM ilk 10 | -48.6 | -2.97 | -29.2 | -2.14 |

qlib IC: -0.006, ortalama BIST agirligi: %62.3. FinRL tek tohum, 100 bin adim. Yatirim tavsiyesi degildir.

## freqtrade (birlesik evren, 30 hisse)

| Model | 2025 getiri % | 2025 Sharpe | 2026 getiri % | 2026 Sharpe |
|---|---:|---:|---:|---:|
| freqtrade RSI sablonu (hyperopt) | 3.61 | 0.29 | 2.56 | 0.28 |

Hisseler Binance cift adlariyla etiketlendi (repos_tests/freqtrade/ft_mapping.json); icerideki veri hisse verisi. Yatirim tavsiyesi degildir.

## FinRL kararlilik testi (5 rastgele tohum, birlesik evren)

| Ajan, yil | Tohum getirileri % | Ortalama | Std | Tum evren al-ve-tut'u gecen | ABD al-ve-tut'u gecen |
|---|---|---:|---:|---:|---:|
| PPO 2025 | 9.7, 13.8, 53.9, 14.8, 2.6 | 19.0 | 18.0 | 5/5 | 1/5 |
| PPO 2026 | 10.4, 11.5, 8.6, 9.2, 19.9 | 11.9 | 4.1 | 5/5 | 1/5 |
| A2C 2025 | 24.7, 16.1, 31.0, 16.0, 18.2 | 21.2 | 5.8 | 5/5 | 2/5 |
| A2C 2026 | 8.0, 9.8, 9.4, 16.7, 21.4 | 13.1 | 5.1 | 5/5 | 2/5 |

Referans (al-ve-tut %): tum evren 2025 +2.1, 2026 +0.4; sadece ABD 2025 +24.5, 2026 +15.5. Yatirim tavsiyesi degildir.

## FinRL ajanlari ne tutuyor? (5 tohum ortalamasi)

| Ajan, yil | ABD agirligi % (tohum araligi) | BIST agirligi % | En cok tutulan hisseler |
|---|---|---|---|
| PPO 2025 | 91.4-98.7 | 0.7-7.5 | AAPL 15.7, AMZN 15.4, GOOGL 14.8, MSFT 14.6 |
| PPO 2026 | 93.0-98.9 | 0.4-6.0 | QQQ 18.2, AMZN 15.7, AAPL 15.0, MSFT 14.6 |
| A2C 2025 | 96.4-98.3 | 1.2-3.0 | MSFT 26.5, QQQ 17.3, GOOGL 10.3, AAPL 9.3 |
| A2C 2026 | 95.7-98.4 | 0.9-3.5 | MSFT 21.9, QQQ 19.8, GOOGL 13.3, JPM 9.0 |

Evrende BIST payi %67; ajanlar BIST'ten kacip buyuk ABD hisselerine yogunlasti. Yatirim tavsiyesi degildir.

## Bizim bot (Trend EW): uzun geçmiş doğrulaması, 12 ETF, 2005-bugün

Kurallar test öncesi sabitlendi. Yıllık getiri % / Sharpe / maks. düşüş %.

| Dönem | Trend EW | Eşit ağırlık al-ve-tut | SPY al-ve-tut |
|---|---|---|---|
| 2005-bugun | 4.2 / 0.58 / -11.2 | 9.4 / 0.69 / -41.1 | 10.8 / 0.64 / -55.2 |
| 2008 krizi | -3.8 / -0.94 / -7.2 | -25.5 / -0.74 / -40.0 | -37.1 / -0.92 / -51.9 |
| 2020 cokusu | -5.3 / -0.68 / -9.9 | -5.2 / 0.01 / -27.5 | -6.4 / 0.08 / -33.7 |
| 2022 dususu | -5.3 / -1.08 / -6.1 | -9.6 / -0.52 / -17.5 | -18.2 / -0.71 / -24.5 |
| 2023-bugun | 6.3 / 0.88 / -6.9 | 15.0 / 1.37 / -11.2 | 21.5 / 1.38 / -18.8 |

Sonuç: düşüşleri çok iyi koruyor (2008'de -%7, SPY -%44) ama uzun vadede getiri geride (yıllık %4,2'ye karşı SPY %10,8). Yatırım tavsiyesi değildir.
