"""FinRL PPO ve A2C ajanlarını ABD-10 evreninde 2016-2024 verisiyle (finrl_run.py ile aynı ayarlar) eğitip models/ altına kaydeder.
Çalıştır: C:/Users/Brk_A/finrl_env/Scripts/python.exe train_finrl.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agents.finrl_agent import build_df, make_env, MODELS_DIR
from finrl.agents.stablebaselines3.models import DRLAgent

STEPS = 60_000
df = build_df()
os.makedirs(MODELS_DIR, exist_ok=True)
for algo in ("ppo", "a2c"):
    env = make_env(df, "2016-01-01", "2025-01-01")
    agent = DRLAgent(env=env.get_sb_env()[0])
    model = agent.get_model(algo, seed=0, model_kwargs=None if algo == "a2c" else {"n_steps": 512, "batch_size": 128})
    model = agent.train_model(model=model, tb_log_name=algo, total_timesteps=STEPS)
    model.save(os.path.join(MODELS_DIR, f"finrl_{algo}"))
    print("kaydedildi:", algo, flush=True)
