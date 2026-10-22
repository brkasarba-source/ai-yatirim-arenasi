"""finrl_combined.py ile ayni kurulum; ek olarak test donemlerinde her gun ajan portfoyundeki hisse agirliklarini kaydeder.
Calistir: C:/Users/Brk_A/finrl_env/Scripts/python.exe finrl_inspect.py 100000 <tohum>   -> finrl_hold_seed<tohum>.json"""
import json, sys
import numpy as np, pandas as pd
from finrl.meta.preprocessor.preprocessors import FeatureEngineer, data_split
from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv
from finrl.agents.stablebaselines3.models import DRLAgent

INDS = ["macd", "boll_ub", "boll_lb", "rsi_30", "cci_30", "dx_30", "close_30_sma", "close_60_sma"]
STEPS, SEED = int(sys.argv[1]), int(sys.argv[2])
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


def run_and_track(model, env):
    """Modeli test ortaminda calistirir; her gun hisse agirliklarini (portfoy degerine oran) ve nakit agirligini kaydeder."""
    state, _ = env.reset()
    W, C, eq = [], [], []
    done = False
    while not done:
        cash = state[0]; px = np.array(state[1:1 + n]); sh = np.array(state[1 + n:1 + 2 * n])
        tot = cash + (px * sh).sum()
        W.append((px * sh / tot).tolist()); C.append(float(cash / tot)); eq.append(float(tot))
        act, _ = model.predict(np.array(state), deterministic=True)
        state, _, term, trunc, _ = env.step(act)
        done = term or trunc
    return np.array(W), np.array(C), np.array(eq)


def stats(av):
    av = pd.Series(av).astype(float); r = av.pct_change().dropna()
    return {"total_pct": round(float((av.iloc[-1] / av.iloc[0] - 1) * 100), 1),
            "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2) if r.std() > 0 else 0,
            "maxdd": round(float((av / av.cummax() - 1).min() * 100), 1)}


is_bist = np.array([t.startswith("B_") for t in TICKERS])
res = {"seed": SEED, "adimlar": STEPS, "tickers": TICKERS}
for algo in ("ppo", "a2c"):
    agent = DRLAgent(env=make_env(*SPLITS["egitim"]).get_sb_env()[0])
    model = agent.get_model(algo, seed=SEED, model_kwargs=None if algo == "a2c" else {"n_steps": 512, "batch_size": 128})
    model = agent.train_model(model=model, tb_log_name=algo, total_timesteps=STEPS)
    res[algo] = {}
    for k in ("2025", "2026"):
        W, C, eq = run_and_track(model, make_env(*SPLITS[k]))
        res[algo][k] = {"stats": stats(eq), "nakit_agirlik_pct": round(float(C.mean() * 100), 1),
                        "abd_agirlik_pct": round(float(W[:, ~is_bist].sum(axis=1).mean() * 100), 1),
                        "bist_agirlik_pct": round(float(W[:, is_bist].sum(axis=1).mean() * 100), 1),
                        "hisse_agirlik_pct": {t: round(float(W[:, i].mean() * 100), 2) for i, t in enumerate(TICKERS)}}
        print(algo, k, res[algo][k]["stats"], "ABD", res[algo][k]["abd_agirlik_pct"], "BIST", res[algo][k]["bist_agirlik_pct"], "nakit", res[algo][k]["nakit_agirlik_pct"], flush=True)
json.dump(res, open(f"finrl_hold_seed{SEED}.json", "w", encoding="utf-8"), indent=1)
