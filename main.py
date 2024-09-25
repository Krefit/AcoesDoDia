import pandas as pd
from stock_analysis import fetch_stock_data
from stocks_db import StocksDB  # Assuming your database class is saved in stocks_db.py
from datetime import datetime

def fetch_and_update_stock_data(ticker, db, interval="1m", period="5d"):
    """
    Fetches stock data using yfinance, checks the latest entry in the database, 
    and inserts new data if available.
    """
    # Fetch the stock's latest timestamp from the database
    latest_date = db.fetch_latest_timestamp(ticker)

    # Convert latest_date to a format that yfinance can use if it exists
    if latest_date:
        print(f"Fetching data starting from: {latest_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch stock data using yfinance with a 1-minute interval for the last 5 days
    stock_data = fetch_stock_data(ticker, interval=interval)

    # If no new data is available, exit early
    if stock_data.empty:
        print(f"No new data available for {ticker}.")
        return

    # Reset the index to have access to the 'Datetime' as a column
    stock_data = stock_data.reset_index()

    # Insert new records into the database
    for index, row in stock_data.iterrows():
        db.insert_stock(
            symbol=ticker,
            company_name=ticker,  # You can update this if you want to fetch the company name separately
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=row['Volume'],
            date=row['Datetime']  # 'Datetime' is now available after resetting the index
        )
    print(f"Inserted {len(stock_data)} new records for {ticker}.")


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
    tickers = ['AAPL', 'MSFT', 'GOOGL','PETR4.SA']

    # For each ticker, fetch and update the data
    for ticker in tickers:
        fetch_and_update_stock_data(ticker, db)
    
    

if __name__ == "__main__":
    main()
