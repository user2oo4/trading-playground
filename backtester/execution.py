# Receive orders from the strategy
# Execute and generate order fills
# Update portfolio with order fills
from order import Order
from order_fill import OrderFill
from portfolio import Portfolio

class Execution:
    def __init__(self, slippage=0.0, fee_per_trade=0.0):
        self.slippage = slippage
        self.fee_per_trade = fee_per_trade
    
    def execute_order(self, orders, market_data):
        # return list of OrderFill objects
        fills = []
        for order in orders:
            symbol = order.symbol
            side = order.side
            quantity = order.quantity
            price = market_data[symbol]['Close'][-1]
            if order.order_type == 'market':
                fill_price = price * (1 + self.slippage) if side == 'BUY' else price * (1 - self.slippage)
            elif order.order_type == 'limit':
                fill_price = order.limit_price
            else:
                raise ValueError(f"Unsupported order type: {order.order_type}")
            fill = OrderFill(symbol, side, quantity, fill_price, self.fee_per_trade)
            fills.append(fill)

        return fills