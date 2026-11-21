# Durum

## Bot ligi: her bota 1000 $ sanal bütçe

Başlangıç 2026-10-22 | son veri 2026-11-20 | işlem günü 21. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.

| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |
|---|---:|---:|---:|---:|---:|
| FinRL PPO | 995.41 | -0.46 | -0.64 | 5 | 11 |
| freqtrade RSI | 989.53 | -1.05 | -1.33 | 4 | 4 |
| FinRL A2C | 979.51 | -2.05 | -4.39 | 9 | 50 |
| qlib LightGBM | 973.86 | -2.61 | -4.85 | 5 | 45 |
| MACD | 958.99 | -4.10 | -4.88 | 2 | 18 |
| SMA 20/100 | 957.62 | -4.24 | -6.05 | 5 | 11 |
| Bollinger | 949.84 | -5.02 | -6.21 | 6 | 14 |
| Trend EW (bizim bot) | 943.10 | -5.69 | -6.79 | 3 | 23 |
| Momentum 6 ay | 941.37 | -5.86 | -7.19 | 4 | 22 |
| RSI | 921.93 | -7.81 | -8.28 | 5 | 5 |
| Lojistik ML | 900.14 | -9.99 | -11.04 | 8 | 16 |
| Gradient Boosting ML | 893.92 | -10.61 | -11.40 | 8 | 66 |
| Al-ve-tut (referans) | 884.19 | -11.58 | -13.46 | 10 | 10 |

Son işlemler:

| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |
|---|---|---|---|---:|---:|---|
| 2026-11-20 | Trend EW (bizim bot) | SAT | JPM | 319.89 | 96.06 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-20 | Trend EW (bizim bot) | SAT | AMZN | 253.48 | 89.54 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-20 | Momentum 6 ay | SAT | AMZN | 253.48 | 89.63 | Son 126 günlük getiri negatife döndü |
| 2026-11-20 | MACD | SAT | AAPL | 352.87 | 97.29 | MACD sinyal çizgisini aşağı kesti |
| 2026-11-20 | Lojistik ML | AL | TSLA | 370.43 | 93.24 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-20 | Gradient Boosting ML | SAT | AMZN | 253.48 | 91.98 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-20 | Gradient Boosting ML | AL | MSFT | 493.74 | 92.17 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-20 | Gradient Boosting ML | AL | GOOGL | 274.5 | 92.17 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-20 | Gradient Boosting ML | AL | JPM | 319.89 | 92.17 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-20 | Gradient Boosting ML | AL | XOM | 158.83 | 92.17 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-19 | Trend EW (bizim bot) | SAT | SPY | 737.46 | 97.05 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-19 | Trend EW (bizim bot) | AL | AMZN | 272.56 | 96.28 | Kapanış 200 günlük ort. üstünde ve 126 günlük getiri pozitif |

**Son veri:** 2026-11-20 | **Takip gunu:** 22 | **Baslangic:** 2026-10-22

Al-ve-tut referansi: %-13.81. Referansi gecen: MACD Trend, SMA 20/100 Kesişim, 6 Ay Momentum, Bollinger Dönüş, RSI Ortalamaya Dönüş, ML: Gradient Boosting (walk-forward), ML: Lojistik (walk-forward).

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| MACD Trend | -4.83 | -4.55 | 0/10 hisse |
| SMA 20/100 Kesişim | -5.92 | -6.02 | 5/10 hisse |
| 6 Ay Momentum | -6.36 | -6.06 | 4/10 hisse |
| Bollinger Dönüş | -7.27 | -6.90 | 8/10 hisse |
| RSI Ortalamaya Dönüş | -8.39 | -8.90 | 6/10 hisse |
| ML: Gradient Boosting (walk-forward) | -9.43 | -8.76 | 8/10 hisse |
| ML: Lojistik (walk-forward) | -12.76 | -11.85 | 8/10 hisse |
| Buy & Hold (referans) | -13.81 | -13.72 | 10/10 hisse |

Son sinyal tarihi: 2026-11-20. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

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
