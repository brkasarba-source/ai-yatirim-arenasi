"""Gercek qlib (Microsoft): Alpha158 ozellikleri + LightGBM. Egitim 2016-2022, dogrulama 2023-2024, test 2025 ve 2026.
Her gun tahmini en yuksek 5 hisse esit agirlikla tutulur (long-only), %0,15 maliyet.
Calistir: C:/Users/Brk_A/qlib_env/Scripts/python.exe qlib_run.py"""
import json
import numpy as np, pandas as pd
import qlib
from qlib.contrib.data.handler import Alpha158
from qlib.contrib.model.gbdt import LGBModel
from qlib.data.dataset import DatasetH

TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
COST, TOPK = 0.0015, 5


def main():
    qlib.init(provider_uri="C:/Users/Brk_A/qlib_data", region="us")

    handler = Alpha158(instruments=TICKERS, start_time="2015-01-01", end_time="2026-12-31",
                       fit_start_time="2016-01-01", fit_end_time="2022-12-31")
    ds = DatasetH(handler, segments={"train": ("2016-01-01", "2022-12-31"), "valid": ("2023-01-01", "2024-12-31"), "test": ("2025-01-01", "2026-12-31")})
    model = LGBModel(loss="mse", colsample_bytree=0.8, learning_rate=0.05, subsample=0.8, num_leaves=31, max_depth=6, num_threads=4, seed=0)
    model.fit(ds)
    pred = model.predict(ds, segment="test")
    label = ds.prepare("test", col_set="label").iloc[:, 0]

    from qlib.data import D
    close = D.features(TICKERS, ["$close"], start_time="2015-01-01", end_time="2026-12-31").iloc[:, 0].unstack(0)
    ret = close.pct_change()

    p = pred.unstack("instrument").reindex(columns=TICKERS)
    ic = p.corrwith(label.unstack("instrument").reindex(columns=TICKERS), axis=1, method="spearman").mean()
    rank = p.rank(axis=1, ascending=False)
    pos = (rank <= TOPK).astype(float) / TOPK                 # t gunu kararinin agirliklari
    held = pos.shift(2).reindex(ret.index).fillna(0)          # t+1 kapanisinda alinir, t+2 getirisini kazanir (qlib etiketiyle ayni)
    turn = held.diff().abs().sum(axis=1).fillna(0)
    port = (held * ret.reindex(held.index)).sum(axis=1) - turn * COST

    def stats(r):
        r = r.dropna(); eq = (1 + r).cumprod()
        return {"total_pct": round(float((eq.iloc[-1] - 1) * 100), 1),
                "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2),
                "maxdd": round(float((eq / eq.cummax() - 1).min() * 100), 1)}

    res = {"ic_ort": round(float(ic), 4), "topk": TOPK}
    for name, (a, b) in {"2025": ("2025-01-01", "2025-12-31"), "2026": ("2026-01-01", "2026-12-31")}.items():
        seg = port[(port.index >= a) & (port.index <= b)]
        bh = ret[(ret.index >= a) & (ret.index <= b)].mean(axis=1)
        bh.iloc[0] -= COST
        res[name] = {"qlib_lgbm_top5": stats(seg), "al_ve_tut": stats(bh)}
        print(name, res[name], flush=True)
    print("ortalama IC:", res["ic_ort"])
    json.dump(res, open("qlib_result.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
