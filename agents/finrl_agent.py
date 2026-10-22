"""FinRL ajanları (PPO, A2C) için lig adaptörü. Modeller models/ altında sabittir (eğitimi 2016-2024, train_finrl.py).
Her çalıştırmada ajan, lig başlangıç tarihinden bugüne ortamda yeniden oynatılır (model sabit olduğundan sonuç tekrarlanabilir);
her günün karar sonrası portföy ağırlıkları hedef ağırlık olarak döner. Not: FinRL günün KAPANIŞINDA işlem yapar, lig ise
bu hedef ağırlıkları ertesi gün açılışında uygular."""
import os
import numpy as np, pandas as pd, yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(os.path.dirname(HERE), "models")
TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
INDS = ["macd", "boll_ub", "boll_lb", "rsi_30", "cci_30", "dx_30", "close_30_sma", "close_60_sma"]
COST = 0.0015


def build_df():
    from finrl.meta.preprocessor.preprocessors import FeatureEngineer
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
    return df.sort_values(["date", "tic"]).reset_index(drop=True)


def make_env(df, a, b, extra_day=False):
    from finrl.meta.preprocessor.preprocessors import data_split
    from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv
    d = data_split(df, a, b)
    if extra_day:  # son gerçek günde de işlem yapılabilsin diye bir sonraki güne kopya satır eklenir
        last = d["date"].max()
        nxt = d[d["date"] == last].copy()
        nxt["date"] = (pd.Timestamp(last) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        d = pd.concat([d, nxt]).sort_values(["date", "tic"])
        d.index = d["date"].factorize()[0]
    n = len(TICKERS)
    return StockTradingEnv(df=d, stock_dim=n, hmax=100, initial_amount=1_000_000, num_stock_shares=[0] * n,
                           buy_cost_pct=[COST] * n, sell_cost_pct=[COST] * n, state_space=1 + 2 * n + len(INDS) * n,
                           action_space=n, tech_indicator_list=INDS, reward_scaling=1e-4)


def targets(name, cal, close, opn, start_date, tickers):
    from stable_baselines3 import PPO, A2C
    algo = "ppo" if name.endswith("PPO") else "a2c"
    model = (PPO if algo == "ppo" else A2C).load(os.path.join(MODELS_DIR, f"finrl_{algo}"), device="cpu")
    df = build_df()
    last = df["date"].max()
    env = make_env(df, start_date, (pd.Timestamp(last) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), extra_day=True)
    n = len(TICKERS)
    state, _ = env.reset()
    dates = sorted(df[(df["date"] >= start_date)]["date"].unique())
    out = {}
    for ds in dates:
        px = np.array(state[1:1 + n])
        action, _ = model.predict(np.array(state), deterministic=True)
        state, _, term, trunc, _ = env.step(action)
        sh = np.array(state[1 + n:1 + 2 * n]); cash = state[0]
        eq = cash + float((px * sh).sum())
        out[pd.Timestamp(ds)] = dict(zip(TICKERS, (px * sh / eq).tolist()))
        if term or trunc:
            break
    return pd.DataFrame.from_dict(out, orient="index")[tickers]
