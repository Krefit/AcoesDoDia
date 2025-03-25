from stock_analysis import fetch_stock_data, calculate_moving_averages, generate_signals
from stocks_db import StocksDB
from backtrading import backtest, run_backtest

def main():
    # Initialize the database connection
    db = StocksDB(
        host="localhost",
        port=5433,
        database="acoesdias",
        user="postgres",
        password="postgres"
    )

    # List of tickers you want to track
    tickers = [ 'PETR4.SA']#,'AAPL', 'MSFT', 'GOOGL']

    # Fetch, update, and backtest each ticker
    for ticker in tickers:
        print(f"\nFetching data for {ticker}...")
        data = fetch_stock_data(ticker, period="1y", interval="1d")

        if not data.empty:
            # Calculate moving averages and generate signals
            data = calculate_moving_averages(data)
            data = generate_signals(data)
            
            # Insert new data into the database if needed (optional depending on your needs)
            latest_date = db.fetch_latest_timestamp(ticker)
            if latest_date:
                print(f"Last date in the database for {ticker}: {latest_date}")
            
            # Perform backtesting on the data
            run_backtest(ticker, data)

if __name__ == "__main__":
    main()
