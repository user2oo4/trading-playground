from typing import Literal

class Order:
    def __init__(self, symbol: str, side: Literal['BUY', 'SELL'], quantity: int, price: float, order_type: str = 'market', limit_price = None):
        self.symbol = symbol
        self.side = side.upper() # 'BUY' or 'SELL'
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.limit_price = limit_price

    def __repr__(self):
        return (f"Order(symbol={self.symbol}, side={self.side}, quantity={self.quantity}, "
                f"price={self.price}, order_type={self.order_type}, limit_price={self.limit_price})")