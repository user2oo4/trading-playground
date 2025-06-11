import os
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(REPO_DIR)

import pandas as pd

from backtester.order_fill import OrderFill

class Portfolio:
    def __init__(self, initial_balance):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = {}
        self.avg_prices = {}  # average entry prices for positions
        self.trade_history = [] # list of OrderFill objets
    
    def _buy(self, symbol, quantity, fill_price, fee):
        print("Buying:", symbol, "Quantity:", quantity, "Fill Price:", fill_price, "Fee:", fee)
        if symbol not in self.positions:
            self.positions[symbol] = 0
            self.avg_prices[symbol] = 0.0
        
        total_cost = quantity * fill_price + fee
        print(type(total_cost))
        print(type(self.balance))
        if total_cost > self.balance:
            raise ValueError(f"Insufficient balance to buy {quantity} of {symbol} at {fill_price}.")
        
        self.balance -= total_cost
        self.positions[symbol] += quantity
        total_quantity = self.positions[symbol]
        current_avg_price = self.avg_prices[symbol]
        new_avg_price = (current_avg_price * (total_quantity - quantity) + fill_price * quantity) / total_quantity
        self.avg_prices[symbol] = new_avg_price
        self.trade_history.append(OrderFill(symbol, 'BUY', quantity, fill_price, fee))
    
    def _sell(self, symbol, quantity, fill_price, fee):
        print("Selling:", symbol, "Quantity:", quantity, "Fill Price:", fill_price, "Fee:", fee)
        if symbol not in self.positions or self.positions[symbol] < quantity:
            raise ValueError(f"Insufficient position to sell {quantity} of {symbol}.")
        
        total_revenue = quantity * fill_price - fee
        self.balance += total_revenue
        self.positions[symbol] -= quantity
        
        if self.positions[symbol] == 0:
            del self.avg_prices[symbol]
            del self.positions[symbol]

    def update(self, fills):
        for fill in fills:
            print("Processing fill:", fill)
            symbol = fill.symbol
            side = fill.side
            quantity = fill.quantity
            fill_price = fill.fill_price
            fee = fill.fee
            
            if side == 'BUY':
                self._buy(symbol, quantity, fill_price, fee)
            elif side == 'SELL':
                self._sell(symbol, quantity, fill_price, fee)
    
    def get_total_value(self, market_data):
        total_value = self.balance
        for symbol, quantity in self.positions.items():
            if symbol in market_data:
                current_price = market_data[symbol]['Close'].iloc[-1]
                if isinstance(current_price, pd.core.series.Series):
                    current_price = float(current_price.iloc[0])
                total_value += quantity * current_price
        return total_value
    
    def get_metrics(self):
        """pnL, returns, etc,"""
        value = self.get_total_value()
        pnl = value - self.initial_balance
        returns = pnl / self.initial_balance
        return {
            'balance': self.balance,
            'total_value': value,
            'pnl': pnl,
            'returns': returns,
            'positions': self.positions,
            'avg_prices': self.avg_prices
        }

    