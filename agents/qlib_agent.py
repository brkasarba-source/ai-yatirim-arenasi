"""qlib ajanı (Alpha158 + LightGBM) için lig adaptörü. Model models/qlib_lgbm.txt'te sabittir (eğitimi 2016-2022, train_qlib.py).
Her çalıştırmada yfinance verisi qlib ikili formatına çevrilir (qlib'in kendi dump_bin.py betiğiyle, vendor/ altında), Alpha158 özellikleri
hesaplanır ve her gün için en yüksek tahminli 5 hisse eşit ağırlıkla (%20) hedef olarak döner."""
import os, subprocess, sys, tempfile
import numpy as np, pandas as pd, yfinance as yf

os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODEL_FILE = os.path.join(ROOT, "models", "qlib_lgbm.txt")
TICKERS = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "JPM", "XOM"]
TOPK = 5


def build_provider(workdir):
    csv, out = os.path.join(workdir, "csv"), os.path.join(workdir, "qlib_data")
    os.makedirs(csv, exist_ok=True)
    raw = yf.download(TICKERS, start="2015-01-01", progress=False, auto_adjust=True)
    for t in TICKERS:
        d = raw.xs(t, axis=1, level=1).dropna().reset_index()
        d.columns = [c.lower() for c in d.columns]
        d["factor"] = 1.0
        d["vwap"] = (d["high"] + d["low"] + d["close"]) / 3
        d["date"] = d["date"].dt.strftime("%Y-%m-%d")
        d[["date", "open", "high", "low", "close", "volume", "factor", "vwap"]].to_csv(os.path.join(csv, f"{t}.csv"), index=False)
    subprocess.run([sys.executable, os.path.join(ROOT, "vendor", "dump_bin.py"), "dump_all", "--data_path", csv, "--qlib_dir", out, "--freq", "day",
                    "--date_field_name", "date", "--include_fields", "open,high,low,close,volume,factor,vwap"], check=True, capture_output=True)
    return out


def make_dataset(provider, test_start, test_end="2030-12-31"):
    import qlib
    from qlib.contrib.data.handler import Alpha158
    from qlib.data.dataset import DatasetH
    qlib.init(provider_uri=provider, region="us")
    handler = Alpha158(instruments=TICKERS, start_time="2015-01-01", end_time="2030-12-31", fit_start_time="2016-01-01", fit_end_time="2022-12-31")
    return DatasetH(handler, segments={"train": ("2016-01-01", "2022-12-31"), "valid": ("2023-01-01", "2024-12-31"), "test": (test_start, test_end)})


def targets(name, cal, close, opn, start_date, tickers):
    import lightgbm as lgb
    from qlib.contrib.model.gbdt import LGBModel
    with tempfile.TemporaryDirectory() as wd:
        provider = build_provider(wd)
        ds = make_dataset(provider, start_date)
        model = LGBModel(loss="mse")
        model.model = lgb.Booster(model_file=MODEL_FILE)
        pred = model.predict(ds, segment="test")
    p = pred.unstack("instrument").reindex(columns=TICKERS)
    rank = p.rank(axis=1, ascending=False, method="first")  # eşit tahminlerde her gün tam TOPK hisse seçilsin
    w = (rank <= TOPK).astype(float) / TOPK
    return w[tickers]
