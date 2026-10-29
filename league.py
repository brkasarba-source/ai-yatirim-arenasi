"""Bot ligi: her bota 1000 $ SANAL bütçe. Günlük çalışır, her bot her işlem gününü tam bir kez işler (tekrar çalıştırmak güvenli).
Karar günün KAPANIŞINDA verilir, ertesi günün AÇILIŞINDA uygulanır. Maliyet %0,15/işlem. Kesirli hisse serbest.
İki bot türü:
  sinyal  : hisse başına 0/1 sinyal. Sinyal 1 olunca hesap değerinin 1/N'i alınır, 0 olunca satılır; tutulan pozisyon dengelenmez.
  ağırlık : ajan günlük hedef portföy ağırlıkları üretir (FinRL, qlib, freqtrade). Hedeften %2'den fazla sapan pozisyon dengelenir.
Ajan modülleri agents/ klasöründedir; biri hata verirse o bot o gün atlanır, diğerleri etkilenmez.
Çıktı: league_state.json (kalıcı durum + tüm işlemler), league.json (özet)."""
import json, os, subprocess, sys, tempfile, traceback
import numpy as np, pandas as pd, yfinance as yf
import arena
from own_bot import sig_trend_ew

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STATE = os.environ.get("LEAGUE_STATE", os.path.join(HERE, "league_state.json"))
OUT = os.environ.get("LEAGUE_OUT", os.path.join(HERE, "league.json"))
INIT_DATE, BUDGET, COST = os.environ.get("LEAGUE_INIT", "2026-10-22"), 1000.0, 0.0015
TICKERS = arena.TICKERS
N = len(TICKERS)
BAND = 0.02  # ağırlık botları: hedeften bu kadar (hesap değerinin oranı) sapınca dengele

S = lambda name: arena.STRATS[name][1]
BOTS = {  # ad: dict(aile, tür, sinyal fonksiyonu | ajan modülü, AL nedeni, SAT nedeni)
    "Al-ve-tut (referans)": dict(fam="Referans", kind="signal", fn=arena.sig_bh, buy="Referans: başlangıçta eşit ağırlıklı al ve tut", sell="-"),
    "SMA 20/100": dict(fam="Kural tabanlı", kind="signal", fn=arena.sig_sma, buy="20 günlük ort. 100 günlük ort. üstüne çıktı (trend yukarı)", sell="20 günlük ort. 100 günlüğün altına indi (trend aşağı)"),
    "Bollinger": dict(fam="Kural tabanlı", kind="signal", fn=arena.sig_boll, buy="Fiyat alt Bollinger bandının altına düştü (aşırı satım)", sell="Fiyat orta banda geri döndü"),
    "RSI": dict(fam="Kural tabanlı", kind="signal", fn=arena.sig_rsi, buy="RSI 30'un altına indi (aşırı satım)", sell="RSI 60'ın üstüne çıktı"),
    "MACD": dict(fam="Kural tabanlı", kind="signal", fn=arena.sig_macd, buy="MACD sinyal çizgisini yukarı kesti", sell="MACD sinyal çizgisini aşağı kesti"),
    "Momentum 6 ay": dict(fam="Kural tabanlı", kind="signal", fn=arena.sig_mom, buy="Son 126 günlük getiri pozitif", sell="Son 126 günlük getiri negatife döndü"),
    "Lojistik ML": dict(fam="ML (walk-forward)", kind="signal", fn=S("ML: Lojistik (walk-forward)"), buy="Model yarın için yükseliş ihtimalini >%52 gördü", sell="Model yükseliş ihtimalini <=%52 gördü"),
    "Gradient Boosting ML": dict(fam="ML (walk-forward)", kind="signal", fn=S("ML: Gradient Boosting (walk-forward)"), buy="Model yarın için yükseliş ihtimalini >%52 gördü", sell="Model yükseliş ihtimalini <=%52 gördü"),
    "Trend EW (bizim bot)": dict(fam="Bizim bot", kind="signal", fn=sig_trend_ew, buy="Kapanış 200 günlük ort. üstünde ve 126 günlük getiri pozitif", sell="Kapanış 200 günlük ort. altına indi veya 126 günlük getiri negatife döndü"),
}
# Ajan botları: agents/<modül>.py içindeki targets(ad, cal, close, opn, start_date, tickers) -> hedef ağırlık DataFrame
for name, mod, fam in (("FinRL PPO", "finrl_agent", "RL ajanı (FinRL)"), ("FinRL A2C", "finrl_agent", "RL ajanı (FinRL)"),
                       ("qlib LightGBM", "qlib_agent", "ML (qlib)"), ("freqtrade RSI", "freqtrade_agent", "Kural tabanlı (freqtrade)")):
    if os.path.exists(os.path.join(HERE, "agents", mod + ".py")):
        BOTS[name] = dict(fam=fam, kind="weights", mod=mod, buy=f"{name} hedef ağırlığını artırdı", sell=f"{name} hedef ağırlığını azalttı")


def load(start_date, wanted):
    px = yf.download(TICKERS, start=arena.START, progress=False, auto_adjust=True)
    cal = px["Close"]["SPY"].dropna().index
    close, opn = px["Close"].reindex(cal).ffill(), px["Open"].reindex(cal)
    opn = opn.fillna(close)
    targets = {}
    for name in wanted:
        cfg = BOTS[name]
        try:
            if cfg["kind"] == "signal":
                cols = {t: cfg["fn"](px.xs(t, axis=1, level=1).dropna()).reindex(cal).ffill().fillna(0) for t in TICKERS}
                targets[name] = pd.DataFrame(cols)
            else:
                py = os.environ.get({"finrl_agent": "FINRL_PY", "qlib_agent": "QLIB_PY", "freqtrade_agent": "FREQTRADE_PY"}[cfg["mod"]], sys.executable)
                out = os.path.join(tempfile.mkdtemp(), "w.csv")
                res = subprocess.run([py, os.path.join(HERE, "agents", "run_agent.py"), name, cfg["mod"], start_date, out], capture_output=True, text=True, cwd=HERE)
                if res.returncode != 0:
                    raise RuntimeError(res.stdout[-800:] + res.stderr[-1500:])
                targets[name] = pd.read_csv(out, index_col=0, parse_dates=True).reindex(cal).ffill().fillna(0)
        except Exception:
            print(f"UYARI: {name} atlandı:\n{traceback.format_exc(limit=3)}", flush=True)
    return cal, close, opn, targets


def trade(b, ds, t, side, shares, price, reason):
    val = shares * price; fee = val * COST
    if side == "SAT":
        b["cash"] += val - fee
        rest = b["pos"].get(t, 0.0) - shares
        if rest <= 1e-9:
            b["pos"].pop(t, None)
        else:
            b["pos"][t] = rest
    else:
        b["cash"] -= val + fee
        b["pos"][t] = b["pos"].get(t, 0.0) + shares
    b["trades"].append({"date": ds, "tic": t, "side": side, "shares": round(float(shares), 6), "price": round(float(price), 2),
                        "value": round(float(val), 2), "fee": round(float(fee), 2), "reason": reason})


def step_signal(b, cfg, ds, o):
    pos, pend = b["pos"], b["pending"]
    eq_open = b["cash"] + sum(sh * o[t] for t, sh in pos.items())
    for t in [t for t in list(pos) if pend.get(t, 0) == 0]:
        trade(b, ds, t, "SAT", pos[t], o[t], cfg["sell"])
    for t in TICKERS:
        if pend.get(t, 0) == 1 and t not in pos:
            amt = min(eq_open / N, b["cash"] / (1 + COST))
            if amt >= 1.0:
                trade(b, ds, t, "AL", amt / o[t], o[t], cfg["buy"])


def step_weights(b, cfg, ds, o):
    pos, pend = b["pos"], b["pending"]
    eq_open = b["cash"] + sum(sh * o[t] for t, sh in pos.items())
    for t in TICKERS:  # önce satışlar
        cur = pos.get(t, 0.0) * o[t]; want = pend.get(t, 0.0) * eq_open
        if cur > 0 and (want < 1.0 or cur - want > BAND * eq_open):
            sh = pos[t] if want < 1.0 else (cur - want) / o[t]
            trade(b, ds, t, "SAT", sh, o[t], cfg["sell"] + f" (hedef %{pend.get(t, 0) * 100:.1f})")
    for t in TICKERS:  # sonra alışlar
        cur = pos.get(t, 0.0) * o[t]; want = pend.get(t, 0.0) * eq_open
        if want - cur > BAND * eq_open:
            amt = min(want - cur, b["cash"] / (1 + COST))
            if amt >= 1.0:
                trade(b, ds, t, "AL", amt / o[t], o[t], cfg["buy"] + f" (hedef %{pend.get(t, 0) * 100:.1f})")


def main():
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else None
    start_date = st["start_date"] if st else INIT_DATE
    cal, close, opn, targets = load(start_date, list(BOTS))
    if st is None:
        d0 = max(d for d in cal if d <= pd.Timestamp(INIT_DATE)).strftime("%Y-%m-%d")
        st = {"start_date": d0, "budget": BUDGET, "bots": {}}
    d0 = st["start_date"]
    for b in st["bots"].values():  # eski durum biçimi: bot başına last_date yoktu
        b.setdefault("last_date", st.get("last_date", d0))
    for name in BOTS:
        if name in targets and name not in st["bots"]:
            st["bots"][name] = {"cash": BUDGET, "pos": {}, "pending": {t: float(targets[name].loc[d0, t]) for t in TICKERS},
                                "trades": [], "equity": [[d0, BUDGET]], "last_date": d0}
    st.pop("last_date", None)
    n_days = 0
    for name, cfg in BOTS.items():
        if name not in targets:
            continue
        b = st["bots"][name]; stepf = step_signal if cfg["kind"] == "signal" else step_weights
        for d in [d for d in cal if d.strftime("%Y-%m-%d") > b["last_date"]]:
            ds = d.strftime("%Y-%m-%d")
            stepf(b, cfg, ds, opn.loc[d])
            b["equity"].append([ds, round(float(b["cash"] + sum(sh * close.loc[d, t] for t, sh in b["pos"].items())), 2)])
            b["pending"] = {t: float(targets[name].loc[d, t]) for t in TICKERS}
            b["last_date"] = ds; n_days += 1
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1)

    last_all = max(b["last_date"] for b in st["bots"].values())
    board = []
    for name, cfg in BOTS.items():
        if name not in st["bots"]:
            continue
        b = st["bots"][name]; eq = b["equity"][-1][1]; vals = pd.Series([e[1] for e in b["equity"]])
        board.append({"bot": name, "family": cfg["fam"], "equity": round(eq, 2), "return_pct": round((eq / BUDGET - 1) * 100, 2), "cash": round(b["cash"], 2),
                      "positions": len(b["pos"]), "trades": len(b["trades"]), "maxdd_pct": round(float((vals / vals.cummax() - 1).min() * 100), 2),
                      "last_date": b["last_date"], "trade_list": b["trades"][::-1]})
    recent = sorted([dict(x, bot=n) for n, b in st["bots"].items() for x in b["trades"]], key=lambda x: (x["date"], x["bot"]), reverse=True)[:30]
    curves = {n: b["equity"] for n, b in st["bots"].items()}
    days = max(len(c) for c in curves.values()) - 1
    json.dump({"start_date": st["start_date"], "last_date": last_all, "days": days, "board": board, "recent_trades": recent, "curves": curves},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print("son gun:", last_all, "| islenen bot-gun:", n_days, "| bot sayisi:", len(board))
    for r in sorted(board, key=lambda x: -x["equity"]):
        print(f'{r["bot"]:24s} ${r["equity"]:8.2f}  {r["return_pct"]:6.2f}%  pozisyon {r["positions"]:2d}  islem {r["trades"]}')


if __name__ == "__main__":
    main()
