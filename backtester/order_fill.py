from typing import Literal

class OrderFill:
    def __init__(self, symbol: str, side: Literal['BUY', 'SELL'], quantity: int, fill_price: float, fee: float=0.0):
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.fill_price = fill_price
        self.fee = fee

    def __repr__(self):
        return f"<Fill {self.side} {self.quantity} {self.symbol} @ {self.fill_price} (${self.fee:.2f} fee)>"
