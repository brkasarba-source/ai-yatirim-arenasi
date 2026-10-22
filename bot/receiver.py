"""TradingView webhook -> sanal (paper) hesap. Sadece standart kutuphane. Gercek para/broker yok.
Calistir:  set WEBHOOK_SECRET=...   python receiver.py     (port 8080)
GET /status ile hesap durumu, POST /webhook ile sinyal."""
import hmac, json, os, threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SECRET = os.environ.get("WEBHOOK_SECRET", "")
LEDGER = os.environ.get("LEDGER_FILE", "paper_ledger.json")
START_CASH, ALLOC, COST = 100_000.0, 0.10, 0.0015  # bakiye, islem basi bakiye orani, komisyon+kayma
lock = threading.Lock()


def load():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER, encoding="utf-8"))
    return {"cash": START_CASH, "positions": {}, "trades": []}


def save(s):
    json.dump(s, open(LEDGER, "w", encoding="utf-8"), indent=1)


def equity(s):
    return s["cash"] + sum(p["qty"] * p["last"] for p in s["positions"].values())


def apply(s, sym, action, price):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if action == "buy":
        if sym in s["positions"]:
            return "zaten pozisyonda"
        budget = min(equity(s) * ALLOC, s["cash"])
        qty = budget / (price * (1 + COST))
        if qty <= 0:
            return "nakit yok"
        s["cash"] -= qty * price * (1 + COST)
        s["positions"][sym] = {"qty": qty, "entry": price, "last": price}
        s["trades"].append({"t": now, "sym": sym, "side": "buy", "qty": qty, "price": price})
        return "alindi"
    if action == "sell":
        p = s["positions"].pop(sym, None)
        if not p:
            return "pozisyon yok"
        s["cash"] += p["qty"] * price * (1 - COST)
        pnl = p["qty"] * (price * (1 - COST) - p["entry"] * (1 + COST))
        s["trades"].append({"t": now, "sym": sym, "side": "sell", "qty": p["qty"], "price": price, "pnl": round(pnl, 2)})
        return "satildi"
    return "bilinmeyen action"


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path != "/status":
            return self._send(404, {"error": "not found"})
        with lock:
            s = load()
            self._send(200, {"equity": round(equity(s), 2), "cash": round(s["cash"], 2), "positions": s["positions"], "trades": s["trades"][-20:]})

    def do_POST(self):
        if self.path != "/webhook":
            return self._send(404, {"error": "not found"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except ValueError:
            return self._send(400, {"error": "bad json"})
        if not SECRET or not hmac.compare_digest(str(body.get("secret", "")), SECRET):
            return self._send(403, {"error": "forbidden"})
        try:
            sym, action, price = str(body["symbol"]).upper(), str(body["action"]).lower(), float(body["price"])
            assert price > 0
        except (KeyError, ValueError, AssertionError):
            return self._send(400, {"error": "missing/invalid symbol, action, price"})
        with lock:
            s = load()
            res = apply(s, sym, action, price)
            if sym in s["positions"]:
                s["positions"][sym]["last"] = price
            save(s)
        print(datetime.now().isoformat(timespec="seconds"), sym, action, price, "->", res, flush=True)
        self._send(200, {"result": res, "equity": round(equity(s), 2)})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not SECRET:
        raise SystemExit("WEBHOOK_SECRET ortam degiskenini ayarla.")
    port = int(os.environ.get("PORT", 8080))
    print("Paper bot dinliyor: port", port)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
