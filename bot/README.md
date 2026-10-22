# Arena SMA 20/100 – TradingView + webhook paper bot

Sanal hesapla çalışır, gerçek emir göndermez. Başlangıç bakiyesi 100.000 $, işlem başı %10, maliyet %0,15.

## Neden bu strateji
Arenada hiçbir strateji al-ve-tut getirisini geçemedi. SMA 20/100 Sharpe'ta ML stratejilerinin yanında en tutarlısıydı (1,29) ve düşüşü azalttı (-%15, referans -%24). Lojistik ML Pine'a taşınamaz (Python modeli gerekir). Bu bot bir getiri vaadi değil, boru hattını (sinyal → webhook → sanal hesap) test eder.

## Kurulum
1. **Alıcı:** `set WEBHOOK_SECRET=kendi-gizli-kelimen` ardından `python receiver.py` (PowerShell: `$env:WEBHOOK_SECRET="..."`).
2. **Dışarı aç:** TradingView yalnızca 80/443 portuna ve public URL'ye gönderir. `cloudflared tunnel --url http://localhost:8080` veya `ngrok http 8080` ile https adresi al.
3. **Pine:** TradingView > Pine Editor'a `strategy.pine` içeriğini yapıştır, "Add to chart". Günlük (1D) grafikte AAPL, MSFT vb. aç. `Webhook secret` girişine aynı gizli kelimeyi yaz.
4. **Alert:** Alert oluştur → Condition: bu strateji, "Order fills only" → Notifications: Webhook URL = `https://<tünel-adresin>/webhook` → Message kutusuna `{{strategy.order.alert_message}}` yaz. Webhook için ücretli TradingView planı gerekir.
5. **İzle:** `https://<tünel-adresin>/status` veya `http://localhost:8080/status`. Kayıt `paper_ledger.json` dosyasında.

## Sınırlar
- Sinyal bar kapanışında gelir; alıcı fiyatı alert anındaki `close` ile işler (arenadaki ertesi gün açılış varsayımından biraz farklı).
- Gizli kelime Pine girişinde ve alert mesajında görünür; sadece paper için uygundur.
- Canlı paraya geçmeden önce en az birkaç hafta paper sonuçlarını arenayla karşılaştır. Bu finansal tavsiye değildir.
