"""qlib (Alpha158 + LightGBM), birlesik evren: 10 ABD + 20 BIST (USD). Egitim 2016-2022, dogrulama 2023-2024, test 2025-2026.
Her gun tahmini en yuksek 10 hisse esit agirlikla tutulur. Maliyet: ABD %0,15, BIST %0,25 (devir uzerinden).
Calistir: MLFLOW_ALLOW_FILE_STORE=true C:/Users/Brk_A/qlib_env/Scripts/python.exe qlib_combined.py"""
import json
import numpy as np, pandas as pd
import qlib
from qlib.contrib.data.handler import Alpha158
from qlib.contrib.model.gbdt import LGBModel
from qlib.data.dataset import DatasetH

TOPK = 10


def main():
    qlib.init(provider_uri="C:/Users/Brk_A/qlib_data_comb", region="us")
    from qlib.data import D
    tickers = sorted(pd.read_csv("panel_usd.csv", usecols=["tic"])["tic"].unique())
    tickers_q = [t.upper() for t in tickers]
    cost = pd.Series({t.upper(): (0.0025 if t.startswith("B_") else 0.0015) for t in tickers})

    handler = Alpha158(instruments=tickers_q, start_time="2015-01-01", end_time="2026-12-31",
                       fit_start_time="2016-01-01", fit_end_time="2022-12-31")
    ds = DatasetH(handler, segments={"train": ("2016-01-01", "2022-12-31"), "valid": ("2023-01-01", "2024-12-31"), "test": ("2025-01-01", "2026-12-31")})
    model = LGBModel(loss="mse", colsample_bytree=0.8, learning_rate=0.05, subsample=0.8, num_leaves=31, max_depth=6, num_threads=4, seed=0)
    model.fit(ds)
    pred = model.predict(ds, segment="test")
    label = ds.prepare("test", col_set="label").iloc[:, 0]

    close = D.features(tickers_q, ["$close"], start_time="2015-01-01", end_time="2026-12-31").iloc[:, 0].unstack(0)
    ret = close.astype("float64").pct_change()
    p = pred.unstack("instrument").reindex(columns=tickers_q)
    ic = p.corrwith(label.unstack("instrument").reindex(columns=tickers_q), axis=1, method="spearman").mean()
    rank = p.rank(axis=1, ascending=False)
    pos = (rank <= TOPK).astype(float) / TOPK
    held = pos.shift(2).reindex(ret.index).fillna(0)
    turn_cost = (held.diff().abs().fillna(0) * cost.reindex(held.columns)).sum(axis=1)
    port = (held * ret.reindex(held.index)).sum(axis=1) - turn_cost

    def stats(r):
        r = r.dropna(); eq = (1 + r).cumprod()
        return {"total_pct": round(float((eq.iloc[-1] - 1) * 100), 1), "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2),
                "maxdd": round(float((eq / eq.cummax() - 1).min() * 100), 1)}

    def bh(a, b, cols):
        r = ret[(ret.index >= a) & (ret.index <= b)][cols].mean(axis=1)
        r.iloc[0] -= cost.reindex(cols).mean()
        return stats(r)

    us = [t for t in tickers_q if not t.startswith("B_")]; bist = [t for t in tickers_q if t.startswith("B_")]
    sel = port.reindex(port.index)
    # secilen hisselerin ABD/BIST dagilimi
    w = held[(held.index >= "2025-01-01")].mean()
    res = {"ic_ort": round(float(ic), 4), "topk": TOPK, "ortalama_agirlik_bist_pct": round(float(w[bist].sum() / w.sum() * 100), 1)}
    for name, (a, b) in {"2025": ("2025-01-01", "2025-12-31"), "2026": ("2026-01-01", "2026-12-31")}.items():
        seg = port[(port.index >= a) & (port.index <= b)]
        res[name] = {"qlib_lgbm_top10": stats(seg), "al_ve_tut_tum_evren": bh(a, b, tickers_q), "al_ve_tut_sadece_abd": bh(a, b, us), "al_ve_tut_sadece_bist": bh(a, b, bist)}
        print(name, res[name], flush=True)
    print("ortalama IC:", res["ic_ort"], "| BIST agirligi %:", res["ortalama_agirlik_bist_pct"])
    json.dump(res, open("qlib_combined_result.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
