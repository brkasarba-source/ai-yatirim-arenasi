# AI yatırım arenası

Ücretsiz forward-test: 8 strateji (klasik + ML) 10 ABD hissesi/ETF'inde aynı maliyet kurallarıyla sanal olarak takip edilir. GitHub Actions hafta içi her gün çalışır ve [STATUS.md](STATUS.md) dosyasını günceller.

- `arena.py`: strateji tanımları ve geçmiş backtest
- `tracker.py`: günlük forward takip, `signals_log.csv` değişmez sinyal kaydı
- `report.py`: telefonda okunacak `STATUS.md`
- `bot/`: TradingView Pine Script + webhook paper bot

Sanal portföy, gerçek para yok. Yatırım tavsiyesi değildir.
