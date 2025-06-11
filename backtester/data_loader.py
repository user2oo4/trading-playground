import pandas as pd 
import datetime
import yfinance as yf # type: ignore
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CURRENT_DIR)

def load_data(symbols, start_date, end_date):
    """
    Load historical data for the given symbols between start_date and end_date.
    Args:
        symbols (list): List of stock symbols to load data for.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    Returns:
        dict: A dictionary where keys are symbols and values are DataFrames with historical data.
    """
    data = {}

    for symbol in symbols:
        current_data = yf.download(symbol, start=start_date, end=end_date)
        if current_data.empty:
            print(f"No data found for {symbol} between {start_date} and {end_date}.")
            continue
        data[symbol] = current_data
    for symbol in data:
        data[symbol].index = pd.to_datetime(data[symbol].index)
    
    file_name = f"data_{start_date}_{end_date}.csv"
    file_path = os.path.join(REPO_DIR, 'backtester', 'data', file_name)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    print_to_csv(data, file_path)
    print(f"Data loaded for symbols: {', '.join(symbols)}")
    return data

def print_to_csv(data, filename):
    with open(filename, 'w') as f:
        for symbol, df in data.items():
            df.to_csv(f, header=True if symbol == list(data.keys())[0] else False)
            f.write("\n")
    print(f"Data saved to {filename}")