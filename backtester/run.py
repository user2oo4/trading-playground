import os
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(REPO_DIR)

from backtester.order import Order
from backtester.order_fill import OrderFill
from backtester.portfolio import Portfolio
from backtester.execution import Execution
import pandas as pd
from pathlib import Path

class Backtester:
    def load_csv_data(self, data_path):
        data_path = Path(data_path)
        if not data_path.exists():
            raise FileNotFoundError(f"Data file {data_path} does not exist.")
        data = pd.read_csv(data_path, parse_dates=True, index_col='Date')
        return data

    def __init__(self, strategy, market_data, initial_balance=100000, slippage=0.001, fee_per_trade=1.0):
        self.strategy = strategy
        self.market_data = market_data
        symbols = list(market_data.keys())
        self.dates = market_data[symbols[0]].index
        self.portfolio = Portfolio(initial_balance)
        self.execution = Execution(slippage, fee_per_trade)
        self.metrics = []
    
    def run(self):
        for date in self.dates:
            # cut market data to current date
            # market data is dict (key: symbol, value: DataFrame)
            current_market_data = {symbol: df.loc[:date] for symbol, df in self.market_data.items()}
            orders = self.strategy.generate_signals(date, market_data=current_market_data)
            if not orders:
                continue
            # execute orders
            fills = self.execution.execute_order(orders, market_data=current_market_data)
            if not fills:
                continue
            # update portfolio with fills
            self.portfolio.update(fills)
            # calculate metrics
            total_value = self.portfolio.get_total_value(current_market_data)
            self.metrics.append({
                'date': date,
                'balance': self.portfolio.balance,
                'total_value': total_value,
                'positions': self.portfolio.positions.copy(),
                'avg_prices': self.portfolio.avg_prices.copy()
            })
    
    def get_metrics(self):
        return pd.DataFrame(self.metrics)