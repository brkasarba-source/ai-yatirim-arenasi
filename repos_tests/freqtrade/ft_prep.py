"""panel_usd.csv -> freqtrade veri formati. Freqtrade yalniz borsa ciftleri kabul ettigi icin her hisse, gercek bir Binance spot
cift adiyla ETIKETLENIR; icerideki veri hisse verisidir (kripto verisi degil). Esleme ft_mapping.json'da.
Calistir: C:/Users/Brk_A/ft_env/Scripts/python.exe ft_prep.py"""
import json, os
import pandas as pd

PAIRS = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'LTC/USDT', 'ADA/USDT', 'XRP/USDT', 'XLM/USDT', 'TRX/USDT', 'ETC/USDT', 'VET/USDT', 'LINK/USDT', 'THETA/USDT',
         'ATOM/USDT', 'ALGO/USDT', 'DOGE/USDT', 'XTZ/USDT', 'HBAR/USDT', 'BCH/USDT', 'SOL/USDT', 'MANA/USDT', 'SAND/USDT', 'DOT/USDT', 'EGLD/USDT',
         'UNI/USDT', 'AVAX/USDT', 'AAVE/USDT', 'NEAR/USDT', 'FIL/USDT', 'AXS/USDT', 'ICP/USDT']
df = pd.read_csv("panel_usd.csv")
tics = sorted(df["tic"].unique(), key=lambda t: (t.startswith("B_"), t))  # once ABD, sonra BIST
assert len(tics) == len(PAIRS)
mapping = dict(zip(tics, PAIRS))
out = "ft_user/data/binance"; os.makedirs(out, exist_ok=True)
for tic, pair in mapping.items():
    g = df[df.tic == tic].copy()
    g["date"] = pd.to_datetime(g["date"], utc=True)
    g = g[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
    g.to_feather(f"{out}/{pair.replace('/', '_')}-1d.feather")
json.dump(mapping, open("ft_mapping.json", "w"), indent=1)
print(mapping)
