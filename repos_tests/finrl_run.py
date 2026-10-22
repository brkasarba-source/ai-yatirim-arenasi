"""Gercek FinRL (AI4Finance) ile calistirma: PPO ve A2C ajanlari 2016-2024 verisiyle egitilir,
2025 ve 2026'da (ajanin hic gormedigi donemler) ayni 10 hisse/ETF ve %0,15 maliyetle test edilir.
Calistir: C:/Users/Brk_A/finrl_env/Scripts/python.exe finrl_run.py"""
import json, sys
import numpy as np, pandas as pd, yfinance as yf
from finrl.meta.preprocessor.preprocessors import FeatureEngineer, data_split
from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv
from finrl.agents.stablebaselines3.models import DRLAgent

TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
INDS = ["macd", "boll_ub", "boll_lb", "rsi_30", "cci_30", "dx_30", "close_30_sma", "close_60_sma"]
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 60_000
COST = 0.0015
SPLITS = {"egitim": ("2016-01-01", "2025-01-01"), "2025": ("2025-01-01", "2026-01-01"), "2026": ("2026-01-01", "2027-01-01")}

raw = yf.download(TICKERS, start="2015-01-01", progress=False, auto_adjust=True)
rows = []
for t in TICKERS:
    d = raw.xs(t, axis=1, level=1).dropna().reset_index()
    d.columns = [c.lower() for c in d.columns]
    d["tic"] = t
    d["date"] = d["date"].dt.strftime("%Y-%m-%d")
    rows.append(d[["date", "open", "high", "low", "close", "volume", "tic"]])
df = pd.concat(rows).sort_values(["date", "tic"]).reset_index(drop=True)
df = FeatureEngineer(use_technical_indicator=True, tech_indicator_list=INDS, use_turbulence=False, user_defined_feature=False).preprocess_data(df)
df = df.sort_values(["date", "tic"]).reset_index(drop=True)
df.index = df["date"].factorize()[0]

n = len(TICKERS)
def make_env(a, b):
    d = data_split(df, a, b)
    return StockTradingEnv(df=d, stock_dim=n, hmax=100, initial_amount=1_000_000, num_stock_shares=[0] * n,
                           buy_cost_pct=[COST] * n, sell_cost_pct=[COST] * n, state_space=1 + 2 * n + len(INDS) * n,
                           action_space=n, tech_indicator_list=INDS, reward_scaling=1e-4)

def stats(av):
    av = av.astype(float); r = av.pct_change().dropna()
    return {"total_pct": round(float((av.iloc[-1] / av.iloc[0] - 1) * 100), 1),
            "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 2) if r.std() > 0 else 0,
            "maxdd": round(float((av / av.cummax() - 1).min() * 100), 1)}

def buy_hold(a, b):
    d = data_split(df, a, b).pivot(index="date", columns="tic", values="close")
    eq = (d / d.iloc[0]).mean(axis=1) * 1_000_000 * (1 - COST)
    return stats(eq)

res = {"adimlar": STEPS, "buy_hold": {k: buy_hold(*SPLITS[k]) for k in ("2025", "2026")}}
for algo in ("ppo", "a2c"):
    agent = DRLAgent(env=make_env(*SPLITS["egitim"]).get_sb_env()[0])
    model = agent.get_model(algo, seed=0, model_kwargs=None if algo == "a2c" else {"n_steps": 512, "batch_size": 128})
    model = agent.train_model(model=model, tb_log_name=algo, total_timesteps=STEPS)
    res[algo] = {}
    for k in ("2025", "2026"):
        av, acts = DRLAgent.DRL_prediction(model=model, environment=make_env(*SPLITS[k]))
        res[algo][k] = stats(av["account_value"])
        print(algo, k, res[algo][k], "| al&tut:", res["buy_hold"][k], flush=True)
json.dump(res, open("finrl_result.json", "w", encoding="utf-8"), indent=1)
