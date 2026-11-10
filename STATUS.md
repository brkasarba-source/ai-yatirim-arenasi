# Durum

## Bot ligi: her bota 1000 $ sanal bütçe

Başlangıç 2026-10-22 | son veri 2026-11-09 | işlem günü 12. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.

| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |
|---|---:|---:|---:|---:|---:|
| Bollinger | 1006.07 | 0.61 | -2.25 | 6 | 12 |
| FinRL PPO | 995.41 | -0.46 | -0.64 | 5 | 11 |
| SMA 20/100 | 991.58 | -0.84 | -4.90 | 6 | 10 |
| freqtrade RSI | 989.53 | -1.05 | -1.33 | 4 | 4 |
| MACD | 986.89 | -1.31 | -2.62 | 2 | 12 |
| Momentum 6 ay | 983.68 | -1.63 | -3.92 | 5 | 15 |
| Trend EW (bizim bot) | 982.74 | -1.73 | -3.77 | 5 | 15 |
| FinRL A2C | 979.51 | -2.05 | -4.39 | 9 | 50 |
| Al-ve-tut (referans) | 977.71 | -2.23 | -6.68 | 10 | 10 |
| RSI | 976.75 | -2.32 | -3.50 | 4 | 4 |
| qlib LightGBM | 973.86 | -2.61 | -4.85 | 5 | 45 |
| Lojistik ML | 972.03 | -2.80 | -6.27 | 9 | 11 |
| Gradient Boosting ML | 969.64 | -3.04 | -4.67 | 5 | 37 |

Son işlemler:

| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |
|---|---|---|---|---:|---:|---|
| 2026-11-09 | Gradient Boosting ML | SAT | NVDA | 173.07 | 87.31 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-09 | Gradient Boosting ML | SAT | TSLA | 360.25 | 99.91 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-09 | Gradient Boosting ML | AL | AMZN | 269.32 | 96.82 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-06 | SMA 20/100 | SAT | NVDA | 191.1 | 90.57 | 20 günlük ort. 100 günlüğün altına indi (trend aşağı) |
| 2026-11-06 | MACD | SAT | TSLA | 348.92 | 88.07 | MACD sinyal çizgisini aşağı kesti |
| 2026-11-06 | Lojistik ML | AL | MSFT | 525.69 | 95.44 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-06 | Gradient Boosting ML | SAT | AMZN | 259.81 | 104.4 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-06 | Gradient Boosting ML | SAT | JPM | 333.15 | 91.88 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-06 | Gradient Boosting ML | AL | SPY | 734.82 | 96.77 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-06 | Gradient Boosting ML | AL | MSFT | 525.69 | 96.77 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-06 | Gradient Boosting ML | AL | TSLA | 348.92 | 96.77 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-06 | Bollinger | AL | TSLA | 348.92 | 99.73 | Fiyat alt Bollinger bandının altına düştü (aşırı satım) |

**Son veri:** 2026-11-09 | **Takip gunu:** 13 | **Baslangic:** 2026-10-22

Al-ve-tut referansi: %-4.34. Referansi gecen: Bollinger Dönüş, MACD Trend, RSI Ortalamaya Dönüş, 6 Ay Momentum, SMA 20/100 Kesişim, ML: Gradient Boosting (walk-forward).

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| Bollinger Dönüş | -1.02 | -2.67 | 6/10 hisse |
| MACD Trend | -2.15 | -2.37 | 3/10 hisse |
| RSI Ortalamaya Dönüş | -2.24 | -3.47 | 4/10 hisse |
| 6 Ay Momentum | -2.65 | -3.22 | 5/10 hisse |
| SMA 20/100 Kesişim | -2.87 | -4.70 | 6/10 hisse |
| ML: Gradient Boosting (walk-forward) | -3.09 | -4.14 | 3/10 hisse |
| Buy & Hold (referans) | -4.34 | -6.61 | 10/10 hisse |
| ML: Lojistik (walk-forward) | -4.99 | -6.23 | 8/10 hisse |

Son sinyal tarihi: 2026-11-09. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

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
