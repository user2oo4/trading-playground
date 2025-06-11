from order import Order
from order_fill import OrderFill
from portfolio import Portfolio
from execution import Execution
import pandas as pd
from pathlib import Path

class Backtester:
    def load_csv_data(self, data_path):
        data_path = Path(data_path)
        if not data_path.exists():
            raise FileNotFoundError(f"Data file {data_path} does not exist.")
        data = pd.read_csv(data_path, parse_dates=True, index_col='Date')
        return data

    def __init__(self, strategy, data_path, initial_balance=100000, slippage=0.001, fee_per_trade=1.0):
        self.strategy = strategy
        self.market_data = self.load_csv_data(data_path)
        self.dates = self.market_data.index
        self.portfolio = Portfolio(initial_balance)
        self.execution = Execution(slippage, fee_per_trade)
        self.metrics = []
    
    def run(self):
        for date in self.dates:
            daily_data = self.market_data.loc[date]
            # get orders from strategy
            orders = self.strategy.generate_orders(daily_data, self.portfolio)
            if not orders:
                continue
            # execute orders
            fills = self.execution.execute_order(orders, daily_data)
            # update portfolio with fills
            self.portfolio.update(fills)
            # calculate metrics
            total_value = self.portfolio.get_total_value(self.market_data)
            self.metrics.append({
                'date': date,
                'balance': self.portfolio.balance,
                'total_value': total_value,
                'positions': self.portfolio.positions.copy(),
                'avg_prices': self.portfolio.avg_prices.copy()
            })
    
    def get_metrics(self):
        return pd.DataFrame(self.metrics)