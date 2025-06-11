# Run backtester, can be used when actually having strategies
import os
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(REPO_DIR)

from backtester.run import Backtester

# from strategies.<strategy_name> import <Strategy> 
# data_path = os.path.join(REPO_DIR, 'backtester', 'data', 'data_2020-01-01_2023-01-01.csv')
# strategy = ...
 
backtester = Backtester(strategy=None, data_path=None, initial_balance=100000, slippage=0.001, fee_per_trade=1.0)
backtester.run()
metrics = backtester.get_metrics()
print(metrics.tail())
# Save metrics to CSV
# file_name = strategy.__class__.__name__ + '_metrics.csv'
# file_path = os.path.join(REPO_DIR, 'backtester', 'results', file_name)
# metrics.to_csv(file_path, index=False)
# print(f"Metrics saved to {file_path}")