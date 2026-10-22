"""qlib LightGBM modelini ABD-10 evreninde eğitip models/qlib_lgbm.txt olarak kaydeder (qlib_run.py ile aynı ayarlar).
Çalıştır: MLFLOW_ALLOW_FILE_STORE=true C:/Users/Brk_A/qlib_env/Scripts/python.exe train_qlib.py"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    from agents.qlib_agent import build_provider, make_dataset, MODEL_FILE
    from qlib.contrib.model.gbdt import LGBModel
    with tempfile.TemporaryDirectory() as wd:
        provider = build_provider(wd)
        ds = make_dataset(provider, "2025-01-01")
        model = LGBModel(loss="mse", colsample_bytree=0.8, learning_rate=0.05, subsample=0.8, num_leaves=31, max_depth=6, num_threads=4, seed=0)
        model.fit(ds)
        os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
        model.model.save_model(MODEL_FILE)
    print("kaydedildi:", MODEL_FILE)


if __name__ == "__main__":
    main()
