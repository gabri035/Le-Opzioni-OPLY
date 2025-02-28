import numpy as np
from datatrader.strategy.base import Strategies
from datatrader.compat import queue
from coint_bollinger_strategy import CointegrationBollingerBandsStrategy
from coint_bollinger_backtest import main
from Config import Config

events_queue = queue.Queue()
tickers = "AAPL,AGC"
weights = np.array([1.0, -1.213])
lookback = 15
entry_z = 1.5
exit_z = 0.5
base_quantity = 10000
strategy = CointegrationBollingerBandsStrategy(
    tickers, events_queue,
    lookback, weights,
    entry_z, exit_z, base_quantity
)
strategy = Strategies(strategy)

main(Config(),True,tickers,"ciao")