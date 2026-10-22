# Durum

Takip 2026-10-22 tarihinde basladi. Ilk islem gunu verisi bekleniyor.

| Strateji | Getiri % | Maks. dusus % | Sepet pozisyonu (son sinyal) |
|---|---:|---:|---:|
| Buy & Hold (referans) | 0.00 | 0.00 | 10/10 hisse |
| SMA 20/100 Kesişim | 0.00 | 0.00 | 8/10 hisse |
| RSI Ortalamaya Dönüş | 0.00 | 0.00 | 0/10 hisse |
| Bollinger Dönüş | 0.00 | 0.00 | 3/10 hisse |
| MACD Trend | 0.00 | 0.00 | 4/10 hisse |
| 6 Ay Momentum | 0.00 | 0.00 | 8/10 hisse |
| ML: Lojistik (walk-forward) | 0.00 | 0.00 | 9/10 hisse |
| ML: Gradient Boosting (walk-forward) | 0.00 | 0.00 | 8/10 hisse |

Son sinyal tarihi: 2026-10-21. Sanal portfoy, gercek para yok. Yatirim tavsiyesi degildir.

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
