"""FinRL, birlesik evren (10 ABD + 20 BIST, hepsi USD). Egitim 2016-2024, test 2025 ve 2026.
Maliyet: ABD %0,15, BIST %0,25. Referans: ayni evrenin esit agirlikli al-ve-tut'u (+ yalniz ABD ve yalniz BIST).
Calistir: C:/Users/Brk_A/finrl_env/Scripts/python.exe finrl_combined.py [adim] [tohum]"""
import json, sys
import numpy as np, pandas as pd
from finrl.meta.preprocessor.preprocessors import FeatureEngineer, data_split
from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv
from finrl.agents.stablebaselines3.models import DRLAgent

INDS = ["macd", "boll_ub", "boll_lb", "rsi_30", "cci_30", "dx_30", "close_30_sma", "close_60_sma"]
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0
SPLITS = {"egitim": ("2016-01-01", "2025-01-01"), "2025": ("2025-01-01", "2026-01-01"), "2026": ("2026-01-01", "2027-01-01")}

df = pd.read_csv("panel_usd.csv")
TICKERS = sorted(df["tic"].unique())
COSTS = [0.0025 if t.startswith("B_") else 0.0015 for t in TICKERS]
df = FeatureEngineer(use_technical_indicator=True, tech_indicator_list=INDS, use_turbulence=False, user_defined_feature=False).preprocess_data(df)
df = df.sort_values(["date", "tic"]).reset_index(drop=True)
df.index = df["date"].factorize()[0]
n = len(TICKERS)


def make_env(a, b):
    d = data_split(df, a, b)
    return StockTradingEnv(df=d, stock_dim=n, hmax=500, initial_amount=1_000_000, num_stock_shares=[0] * n,
                           buy_cost_pct=COSTS, sell_cost_pct=COSTS, state_space=1 + 2 * n + len(INDS) * n,
                           action_space=n, tech_indicator_list=INDS, reward_scaling=1e-4)


def stats(av):
    av = pd.Series(av).astype(float); r = av.pct_change().dropna()
    return {"total_pct": round(float((av.iloc[-1] / av.iloc[0] - 1) * 100), 1),
            "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2) if r.std() > 0 else 0,
            "maxdd": round(float((av / av.cummax() - 1).min() * 100), 1)}


def buy_hold(a, b, sel=None):
    d = data_split(df, a, b).pivot(index="date", columns="tic", values="close")
    cols = [c for c in d.columns if sel is None or sel(c)]
    cost = np.mean([COSTS[TICKERS.index(c)] for c in cols])
    eq = (d[cols] / d[cols].iloc[0]).mean(axis=1) * (1 - cost)
    return stats(eq)


res = {"seed": SEED, "adimlar": STEPS, "hisse_sayisi": n, "buy_hold": {}}
for k in ("2025", "2026"):
    res["buy_hold"][k] = {"tum_evren": buy_hold(*SPLITS[k]), "sadece_abd": buy_hold(*SPLITS[k], lambda c: not c.startswith("B_")),
                          "sadece_bist": buy_hold(*SPLITS[k], lambda c: c.startswith("B_"))}
    print("al-ve-tut", k, res["buy_hold"][k], flush=True)
for algo in ("ppo", "a2c"):
    agent = DRLAgent(env=make_env(*SPLITS["egitim"]).get_sb_env()[0])
    model = agent.get_model(algo, seed=SEED, model_kwargs=None if algo == "a2c" else {"n_steps": 512, "batch_size": 128})
    model = agent.train_model(model=model, tb_log_name=algo, total_timesteps=STEPS)
    res[algo] = {}
    for k in ("2025", "2026"):
        av, acts = DRLAgent.DRL_prediction(model=model, environment=make_env(*SPLITS[k]))
        res[algo][k] = stats(av["account_value"])
        print(algo, k, res[algo][k], flush=True)
json.dump(res, open("finrl_combined_result.json" if SEED == 0 and len(sys.argv) <= 2 else f"finrl_seed{SEED}.json", "w", encoding="utf-8"), indent=1)
