"""Bot ligi: her bota 1000 $ SANAL bütçe. Gunluk calisir, her islem gunu tam bir kez islenir (tekrar calistirmak guvenli).
Kural: karar gunun KAPANISINDA verilir, ertesi gunun ACILISINDA uygulanir. Maliyet %0,15/islem. Kesirli hisse serbest.
Her sinyal-1 hissede hesap degerinin 1/N'i kadar pozisyon; sinyal 0 olunca satilir; tutulan pozisyon yeniden dengelenmez.
Cikti: league_state.json (kalici durum + tum islemler), league.json (ozet)."""
import json, os
import numpy as np, pandas as pd, yfinance as yf
import arena
from own_bot import sig_trend_ew

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.environ.get("LEAGUE_STATE", os.path.join(HERE, "league_state.json"))
OUT = os.environ.get("LEAGUE_OUT", os.path.join(HERE, "league.json"))
INIT_DATE, BUDGET, COST = os.environ.get("LEAGUE_INIT", "2026-10-22"), 1000.0, 0.0015  # %0,15 maliyet
TICKERS = arena.TICKERS
N = len(TICKERS)

BOTS = {  # ad: (aile, sinyal fonksiyonu, AL nedeni, SAT nedeni)
    "Al-ve-tut (referans)": ("Referans", arena.sig_bh, "Referans: baslangicta esit agirlikli al ve tut", "-"),
    "SMA 20/100": ("Kural tabanli", arena.sig_sma, "20 gunluk ort. 100 gunluk ort. ustune cikti (trend yukari)", "20 gunluk ort. 100 gunlugun altina indi (trend asagi)"),
    "Bollinger": ("Kural tabanli", arena.sig_boll, "Fiyat alt Bollinger bandinin altina dustu (asiri satim)", "Fiyat orta banda geri dondu"),
    "RSI": ("Kural tabanli", arena.sig_rsi, "RSI 30'un altina indi (asiri satim)", "RSI 60'in ustune cikti"),
    "Momentum 6 ay": ("Kural tabanli", arena.sig_mom, "Son 126 gunluk getiri pozitif", "Son 126 gunluk getiri negatife dondu"),
    "Lojistik ML": ("ML (walk-forward)", arena.STRATS["ML: Lojistik (walk-forward)"][1], "Model yarin icin yukselis ihtimalini >%52 gordu", "Model yukselis ihtimalini <=%52 gordu"),
    "Trend EW (bizim bot)": ("Bizim bot", sig_trend_ew, "Kapanis 200 gunluk ort. ustunde ve 126 gunluk getiri pozitif", "Kapanis 200 gunluk ort. altina indi veya 126 gunluk getiri negatife dondu"),
}


def load():
    px = yf.download(TICKERS, start=arena.START, progress=False, auto_adjust=True)
    cal = px["Close"]["SPY"].dropna().index
    close, opn = px["Close"].reindex(cal).ffill(), px["Open"].reindex(cal)
    opn = opn.fillna(close)
    sigs = {}
    for name, (_, fn, _, _) in BOTS.items():
        cols = {}
        for t in TICKERS:
            df = px.xs(t, axis=1, level=1).dropna()
            cols[t] = fn(df).reindex(cal).ffill().fillna(0)
        sigs[name] = pd.DataFrame(cols)
    return cal, close, opn, sigs


def main():
    cal, close, opn, sigs = load()
    if os.path.exists(STATE):
        st = json.load(open(STATE, encoding="utf-8"))
    else:
        d0 = max(d for d in cal if d <= pd.Timestamp(INIT_DATE)).strftime("%Y-%m-%d")
        st = {"start_date": d0, "last_date": d0, "budget": BUDGET, "bots": {}}
        for name in BOTS:
            st["bots"][name] = {"cash": BUDGET, "pos": {}, "pending": {t: float(sigs[name].loc[d0, t]) for t in TICKERS},
                                "trades": [], "equity": [[d0, BUDGET]]}
    new_days = [d for d in cal if d.strftime("%Y-%m-%d") > st["last_date"]]
    for d in new_days:
        ds = d.strftime("%Y-%m-%d")
        for name, (fam, fn, why_buy, why_sell) in BOTS.items():
            b = st["bots"][name]; pend = b["pending"]; pos = b["pos"]
            o = opn.loc[d]
            eq_open = b["cash"] + sum(sh * o[t] for t, sh in pos.items())
            for t in [t for t in list(pos) if pend.get(t, 0) == 0]:  # once satislar
                sh = pos.pop(t); val = sh * o[t]; fee = val * COST
                b["cash"] += val - fee
                b["trades"].append({"date": ds, "tic": t, "side": "SAT", "shares": round(sh, 6), "price": round(float(o[t]), 2), "value": round(val, 2), "fee": round(fee, 2), "reason": why_sell})
            for t in TICKERS:  # sonra alislar
                if pend.get(t, 0) == 1 and t not in pos:
                    amt = min(eq_open / N, b["cash"] / (1 + COST))
                    if amt < 1.0:
                        continue
                    sh = amt / o[t]; fee = amt * COST
                    b["cash"] -= amt + fee; pos[t] = sh
                    b["trades"].append({"date": ds, "tic": t, "side": "AL", "shares": round(sh, 6), "price": round(float(o[t]), 2), "value": round(amt, 2), "fee": round(fee, 2), "reason": why_buy})
            eq_close = b["cash"] + sum(sh * close.loc[d, t] for t, sh in pos.items())
            b["equity"].append([ds, round(float(eq_close), 2)])
            b["pending"] = {t: float(sigs[name].loc[d, t]) for t in TICKERS}
        st["last_date"] = ds
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1)

    last = pd.Timestamp(st["last_date"])
    board = []
    for name, (fam, *_ ) in BOTS.items():
        b = st["bots"][name]; eq = b["equity"][-1][1]
        vals = pd.Series([e[1] for e in b["equity"]])
        board.append({"bot": name, "family": fam, "equity": round(eq, 2), "return_pct": round((eq / BUDGET - 1) * 100, 2), "cash": round(b["cash"], 2),
                      "positions": len(b["pos"]), "trades": len(b["trades"]), "maxdd_pct": round(float((vals / vals.cummax() - 1).min() * 100), 2),
                      "holding": {t: round(sh * float(close.loc[last, t]), 2) for t, sh in b["pos"].items()}})
    recent = sorted([dict(x, bot=n) for n, b in st["bots"].items() for x in b["trades"]], key=lambda x: (x["date"], x["bot"]), reverse=True)[:30]
    curves = {n: b["equity"] for n, b in st["bots"].items()}
    json.dump({"start_date": st["start_date"], "last_date": st["last_date"], "days": len(next(iter(curves.values()))) - 1, "board": board, "recent_trades": recent, "curves": curves},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print("son gun:", st["last_date"], "| yeni gun:", len(new_days))
    for r in sorted(board, key=lambda x: -x["equity"]):
        print(f'{r["bot"]:24s} ${r["equity"]:8.2f}  {r["return_pct"]:6.2f}%  pozisyon {r["positions"]:2d}  islem {r["trades"]}')


if __name__ == "__main__":
    main()
