import math
import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CURRENT_DIR)
BACKTESTER_DIR = os.path.join(REPO_DIR, 'backtester')
import sys
sys.path.append(REPO_DIR)

from backtester.run import Backtester
from backtester.strategy_interface import StrategyInterface as Strategy
from backtester.order import Order

class MeanReversionStrategy(Strategy):
    def __init__(self, symbol, long_window=20, short_window=5, threshold=1.0):
        self.symbol = symbol
        self.long_window = long_window
        self.short_window = short_window
        self.threshold = threshold
        self.position = 0 # 0 or 1

    def generate_signals(self, timestamp, market_data):
        price = market_data[self.symbol]['Close']
        print('len = ', len(price))
        if price is None or len(price) < self.long_window:
            return []
        
        long_ma = price[-self.long_window:].mean().iloc[0]
        short_ma = price[-self.short_window:].mean().iloc[0]
        print(f"Timestamp: {timestamp}, Long MA: {long_ma}, Short MA: {short_ma}, Position: {self.position}")
        orders = []
        if short_ma < long_ma - self.threshold:
            quantity = math.log2((long_ma - short_ma))
            quantity = int(quantity)
            if quantity <= 0:
                return []
            # If moving down, buy
            orders.append(Order(self.symbol, 'BUY', quantity, 'market'))
            print("Buying signal generated.")
            self.position += quantity
        elif short_ma > long_ma + self.threshold:
            quantity = math.log2((short_ma - long_ma))
            quantity = int(quantity)
            quantity = min(quantity, self.position)
            if quantity <= 0:
                return []
            # If moving up, sell
            orders.append(Order(self.symbol, 'SELL', quantity, 'market'))
            print("Selling signal generated.")
            self.position -= quantity
        return orders


