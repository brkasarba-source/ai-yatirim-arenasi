# Durum

## Bot ligi: her bota 1000 $ sanal bütçe

Başlangıç 2026-10-22 | son veri 2026-11-19 | işlem günü 20. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.

| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |
|---|---:|---:|---:|---:|---:|
| FinRL PPO | 995.41 | -0.46 | -0.64 | 5 | 11 |
| freqtrade RSI | 989.53 | -1.05 | -1.33 | 4 | 4 |
| FinRL A2C | 979.51 | -2.05 | -4.39 | 9 | 50 |
| qlib LightGBM | 973.86 | -2.61 | -4.85 | 5 | 45 |
| SMA 20/100 | 973.50 | -2.65 | -4.90 | 5 | 11 |
| Bollinger | 972.74 | -2.73 | -3.95 | 6 | 14 |
| MACD | 964.42 | -3.56 | -4.34 | 3 | 17 |
| Momentum 6 ay | 949.76 | -5.02 | -6.36 | 5 | 21 |
| Trend EW (bizim bot) | 948.83 | -5.12 | -6.22 | 5 | 21 |
| RSI | 941.07 | -5.89 | -6.38 | 5 | 5 |
| Lojistik ML | 935.42 | -6.46 | -7.55 | 7 | 15 |
| Gradient Boosting ML | 924.61 | -7.54 | -8.36 | 5 | 61 |
| Al-ve-tut (referans) | 923.61 | -7.64 | -9.60 | 10 | 10 |

Son işlemler:

| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |
|---|---|---|---|---:|---:|---|
| 2026-11-19 | Trend EW (bizim bot) | SAT | SPY | 737.46 | 97.05 | Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü |
| 2026-11-19 | Trend EW (bizim bot) | AL | AMZN | 272.56 | 96.28 | Kapanış 200 günlük ort. üstünde ve 126 günlük getiri pozitif |
| 2026-11-19 | RSI | AL | XOM | 161.33 | 96.04 | RSI 30'un altına indi (aşırı satım) |
| 2026-11-19 | Momentum 6 ay | SAT | SPY | 737.46 | 97.05 | Son 126 günlük getiri negatife döndü |
| 2026-11-19 | Momentum 6 ay | AL | AMZN | 272.56 | 96.38 | Son 126 günlük getiri pozitif |
| 2026-11-19 | Gradient Boosting ML | SAT | MSFT | 519.5 | 95.63 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-19 | Gradient Boosting ML | SAT | GOOGL | 294.3 | 97.05 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-19 | Gradient Boosting ML | SAT | TSLA | 389.91 | 94.47 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-19 | Gradient Boosting ML | SAT | JPM | 326.38 | 93.01 | Model yükseliş ihtimalini <=%52 gördü |
| 2026-11-19 | Gradient Boosting ML | AL | QQQ | 671.09 | 94.22 | Model yarın için yükseliş ihtimalini >%52 gördü |
| 2026-11-19 | Bollinger | AL | JPM | 326.38 | 99.28 | Fiyat alt Bollinger bandının altına düştü (aşırı satım) |
| 2026-11-18 | MACD | SAT | JPM | 327.52 | 98.35 | MACD sinyal çizgisini aşağı kesti |

**Son veri:** 2026-11-19 | **Takip gunu:** 21 | **Baslangic:** 2026-10-22

Al-ve-tut referansi: %-9.77. Referansi gecen: MACD Trend, SMA 20/100 Kesişim, Bollinger Dönüş, 6 Ay Momentum, RSI Ortalamaya Dönüş, ML: Gradient Boosting (walk-forward), ML: Lojistik (walk-forward).

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| MACD Trend | -4.16 | -3.88 | 2/10 hisse |
| SMA 20/100 Kesişim | -4.42 | -4.70 | 5/10 hisse |
| Bollinger Dönüş | -4.56 | -4.18 | 6/10 hisse |
| 6 Ay Momentum | -5.69 | -5.38 | 4/10 hisse |
| RSI Ortalamaya Dönüş | -6.09 | -6.61 | 5/10 hisse |
| ML: Gradient Boosting (walk-forward) | -6.26 | -5.57 | 8/10 hisse |
| ML: Lojistik (walk-forward) | -8.88 | -7.93 | 8/10 hisse |
| Buy & Hold (referans) | -9.77 | -9.68 | 10/10 hisse |

Son sinyal tarihi: 2026-11-19. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

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
