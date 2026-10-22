#!/usr/bin/env bash
# Ajanlar bağımlılık çakışmasın diye her biri kendi sanal ortamında çalışır (agents/run_agent.py bunları çağırır).
# Kullanım: bash ci/setup_envs.sh finrl|qlib|freqtrade
set -ex
V="$HOME/.venvs"; N="$1"
mkdir -p "$V"
[ -x "$V/$N/bin/python" ] || python -m venv "$V/$N"
P="$V/$N/bin/python"
case "$N" in
  finrl)
    "$P" -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu
    "$P" -m pip install -q finrl gymnasium stable-baselines3 stockstats yfinance pandas numpy matplotlib scikit-learn exchange_calendars
    "$P" -m pip install -q "websockets>=13"
    # FinRL yalnızca içe aktarıyor (paper trading için); Linux'ta derlenemeyen paketlerin yerine boş yer tutucu modüller
    SP=$("$P" -c "import site;print(site.getsitepackages()[0])")
    for m in alpaca_trade_api wrds; do mkdir -p "$SP/$m"; echo "" > "$SP/$m/__init__.py"; done
    "$P" -c "from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv; from finrl.agents.stablebaselines3.models import DRLAgent; print('finrl import ok')"
    ;;
  qlib)
    "$P" -m pip install -q "setuptools<81" wheel
    "$P" -m pip install -q --no-build-isolation gym==0.26.2
    "$P" -m pip install -q pyqlib lightgbm yfinance
    "$P" -c "import qlib, lightgbm; print('qlib import ok')"
    ;;
  freqtrade)
    "$P" -m pip install -q freqtrade yfinance
    "$P" -c "import freqtrade, talib; print('freqtrade import ok')"
    ;;
esac
echo "ortam hazir: $N"
