import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CURRENT_DIR)
BACKTESTER_DIR = os.path.join(REPO_DIR, 'backtester')
import sys
sys.path.append(REPO_DIR)

from backtester.run import Backtester
from backtester.strategy_interface import Strategy
from backtester.order import Order

class ReverseMeanReversionStrategy(Strategy):
    def __init__(self, symbol, long_window=20, short_window=5, threshold=1.0):
        self.symbol = symbol
        self.long_window = long_window
        self.short_window = short_window
        self.threshold = threshold
        self.position = 0 # 0 or 1

    def generate_orders(self, timestamp, market_data):
        price = market_data[self.symbol]['Close']
        if price is None or len(price) < self.long_window:
            return []
        
        long_ma = price[-self.long_window:].mean()
        short_ma = price[-self.short_window:].mean()
        orders = []
        if short_ma < long_ma - self.threshold and self.position == 1:
            # If moving down, sell
            orders.append(Order(self.symbol, 'SELL', 1, 'market'))
            self.position = 1
        elif short_ma > long_ma + self.threshold and self.position == 0:
            # If moving up, buy
            orders.append(Order(self.symbol, 'BUY', 1, 'market'))
            self.position = 0


