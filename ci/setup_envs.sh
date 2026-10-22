#!/usr/bin/env bash
# Ajanlar bağımlılık çakışmasın diye her biri kendi sanal ortamında çalışır (agents/run_agent.py bunları çağırır).
set -e
mkdir -p "$HOME/.venvs"
for n in finrl qlib freqtrade; do [ -x "$HOME/.venvs/$n/bin/python" ] || python -m venv "$HOME/.venvs/$n"; done
V="$HOME/.venvs"
"$V/finrl/bin/pip" install -q torch --index-url https://download.pytorch.org/whl/cpu
"$V/finrl/bin/pip" install -q finrl gymnasium stable-baselines3 stockstats yfinance pandas numpy matplotlib scikit-learn alpaca-trade-api exchange_calendars wrds
"$V/finrl/bin/pip" install -q "websockets>=13"
"$V/qlib/bin/pip" install -q pyqlib lightgbm yfinance
"$V/freqtrade/bin/pip" install -q freqtrade yfinance
echo "ortamlar hazir"
