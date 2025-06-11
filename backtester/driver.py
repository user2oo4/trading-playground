# Run backtester, can be used when actually having strategies
import os
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(REPO_DIR)

from backtester.run import Backtester
from strategies.mean_reversion import MeanReversionStrategy
from strategies.reverse_mean_reversion import ReverseMeanReversionStrategy
import backtester.data_loader as dl

symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
# symbols = symbols[:1]
start_date = '2020-01-01'
end_date = '2023-01-01'

print("Retrieving market data...")

market_data = dl.load_data(symbols, start_date, end_date)
# print(type(market_data))
# print(market_data['AAPL'].head())
# exit(0)

print("Market data loaded successfully.")

strategies = [MeanReversionStrategy(symbol=symbol, threshold=2.0) for symbol in symbols]
strategies += [ReverseMeanReversionStrategy(symbol=symbol, threshold=2.0) for symbol in symbols]
for strategy in strategies:
    print("Running backtester for strategy:", strategy.__class__.__name__)
    print(f"Symbol: {strategy.symbol}")
    backtester = Backtester(strategy=strategy,
                            market_data=market_data,
                            initial_balance=100000,
                            slippage=0.001,
                            fee_per_trade=1.0)
    backtester.run()
    metrics = backtester.get_metrics()
    print(f"Metrics for {strategy.__class__.__name__} on {strategy.symbol}:")
    print(metrics.tail())
    file_name = strategy.__class__.__name__ + '_' + strategy.symbol + '_metrics.csv'
    file_path = os.path.join(REPO_DIR, 'backtester', 'results', file_name)
    metrics.to_csv(file_path, index=False)