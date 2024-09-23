import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker, interval):
    """Fetches stock data from yfinance."""
    print(yf.download(ticker, interval=interval, period="5d"))
    return yf.download(ticker, interval=interval, period="5d")

def analyze_stock_data(data):
    """Performs your desired analysis on the stock data."""
    # Add your analysis logic here
    # For example, calculate moving averages, RSI, etc.
    # ...
    print(data.head())