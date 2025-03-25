import yfinance as yf
import numpy as np

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """Fetch historical stock data using yfinance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

def calculate_moving_averages(data, short_window=10, long_window=50):
    """Calculate short-term and long-term moving averages."""
    data['SMA_10'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_50'] = data['Close'].rolling(window=long_window).mean()
    return data

def generate_signals(data):
    """Generate buy/sell signals based on moving averages."""
    data['Signal'] = 0
    data['Signal'][10:] = np.where(data['SMA_10'][10:] > data['SMA_50'][10:], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data
