# Durum

## Bot ligi: her bota 1000 $ sanal bütçe

Başlangıç 2026-10-22 | son veri 2026-11-04 | işlem günü 9. Karar kapanışta, uygulama ertesi gün açılışta, maliyet %0,15.

| Bot | Değer $ | Getiri % | Maks. düşüş % | Pozisyon | İşlem |
|---|---:|---:|---:|---:|---:|
| Bollinger | 1008.88 | 0.89 | -2.25 | 7 | 7 |
| SMA 20/100 | 1005.05 | 0.50 | -2.63 | 8 | 8 |
| MACD | 1000.99 | 0.10 | -0.71 | 2 | 10 |
| Al-ve-tut (referans) | 1000.54 | 0.05 | -3.96 | 10 | 10 |
| Momentum 6 ay | 999.18 | -0.08 | -2.29 | 8 | 12 |
| Trend EW (bizim bot) | 998.33 | -0.17 | -2.30 | 8 | 12 |
| FinRL PPO | 995.41 | -0.46 | -0.64 | 5 | 11 |
| RSI | 990.91 | -0.91 | -2.68 | 4 | 4 |
| freqtrade RSI | 989.53 | -1.05 | -1.33 | 4 | 4 |
| Gradient Boosting ML | 988.86 | -1.11 | -3.62 | 7 | 23 |
| Lojistik ML | 986.62 | -1.34 | -4.08 | 9 | 9 |
| FinRL A2C | 979.51 | -2.05 | -4.39 | 9 | 50 |
| qlib LightGBM | 973.86 | -2.61 | -4.85 | 5 | 45 |

Son işlemler:

| Tarih | Bot | İşlem | Hisse | Fiyat $ | Tutar $ | Neden |
|---|---|---|---|---:|---:|---|
| 2026-11-04 | qlib LightGBM | SAT | AMZN | 264.82 | 208.48 | qlib LightGBM hedef ağırlığını azalttı (hedef %0.0) |
| 2026-11-04 | qlib LightGBM | SAT | GOOGL | 283.51 | 198.0 | qlib LightGBM hedef ağırlığını azalttı (hedef %0.0) |
| 2026-11-04 | qlib LightGBM | SAT | TSLA | 379.8 | 180.04 | qlib LightGBM hedef ağırlığını azalttı (hedef %0.0) |
| 2026-11-04 | qlib LightGBM | SAT | JPM | 346.0 | 197.59 | qlib LightGBM hedef ağırlığını azalttı (hedef %0.0) |
| 2026-11-04 | qlib LightGBM | AL | SPY | 762.99 | 195.7 | qlib LightGBM hedef ağırlığını artırdı (hedef %20.0) |
| 2026-11-04 | qlib LightGBM | AL | QQQ | 688.43 | 195.7 | qlib LightGBM hedef ağırlığını artırdı (hedef %20.0) |
| 2026-11-04 | qlib LightGBM | AL | AAPL | 341.57 | 195.7 | qlib LightGBM hedef ağırlığını artırdı (hedef %20.0) |
| 2026-11-04 | qlib LightGBM | AL | XOM | 174.26 | 194.68 | qlib LightGBM hedef ağırlığını artırdı (hedef %20.0) |
| 2026-11-04 | freqtrade RSI | AL | AMZN | 264.82 | 98.98 | freqtrade RSI hedef ağırlığını artırdı (hedef %10.0) |
| 2026-11-04 | Trend EW (bizim bot) | AL | NVDA | 203.5 | 99.41 | Kapanış 200 günlük ort. üstünde ve 126 günlük getiri pozitif |
| 2026-11-04 | MACD | SAT | XOM | 174.26 | 97.15 | MACD sinyal çizgisini aşağı kesti |
| 2026-11-04 | Gradient Boosting ML | SAT | NVDA | 203.5 | 96.45 | Model yükseliş ihtimalini <=%52 gördü |

**Son veri:** 2026-11-04 | **Takip gunu:** 10 | **Baslangic:** 2026-10-22

Al-ve-tut referansi: %-2.11. Referansi gecen: Bollinger Dönüş, RSI Ortalamaya Dönüş, MACD Trend, SMA 20/100 Kesişim, 6 Ay Momentum.

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| Bollinger Dönüş | -0.44 | -2.67 | 4/10 hisse |
| RSI Ortalamaya Dönüş | -0.80 | -2.67 | 4/10 hisse |
| MACD Trend | -0.81 | -0.59 | 3/10 hisse |
| SMA 20/100 Kesişim | -1.23 | -2.61 | 7/10 hisse |
| 6 Ay Momentum | -1.75 | -2.25 | 5/10 hisse |
| Buy & Hold (referans) | -2.11 | -3.95 | 10/10 hisse |
| ML: Gradient Boosting (walk-forward) | -2.55 | -3.32 | 5/10 hisse |
| ML: Lojistik (walk-forward) | -3.39 | -4.00 | 8/10 hisse |

Son sinyal tarihi: 2026-11-04. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

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
