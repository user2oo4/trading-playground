# trading-playground

A modular Python framework for simulating, backtesting, and developing trading strategies.

## Features

- **Backtesting Engine:** Simulate trading strategies on historical data with customizable parameters.
- **Strategy Interface:** Easily implement and plug in your own trading strategies.
- **Data Loader:** Download and manage historical market data (supports yfinance and S&P 500 tickers).
- **Portfolio Management:** Track balances, positions, and performance metrics.
- **Execution Simulation:** Models slippage and trading fees.
- **Results Export:** Save backtest results and metrics to CSV for further analysis.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/trading-playground.git
    cd trading-playground
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Download Data:**
    ```sh
    python backtester/data_loader.py
    ```
    This will download historical data for selected tickers.

2. **Run a Backtest:**
    ```sh
    python backtester/driver.py
    ```
    This will run all strategies defined in `driver.py` on the downloaded data and save results to the `backtester/results` folder.

3. **Develop Your Own Strategy:**
    - Create a new strategy class in the `strategies` folder, inheriting from `StrategyInterface`.
    - Implement the `generate_signals` method.

## Project Structure

```
trading-playground/
│
├── backtester/
│   ├── data_loader.py
│   ├── driver.py
│   ├── execution.py
│   ├── order.py
│   ├── order_fill.py
│   ├── portfolio.py
│   ├── run.py
│   └── strategy_interface.py
│
├── strategies/
│   ├── mean_reversion.py
│   └── reverse_mean_reversion.py
│
├── requirements.txt
└── README.md
```

## Dependencies

- `pandas`
- `yfinance`
- `numpy`
- (see `requirements.txt` for full list)
