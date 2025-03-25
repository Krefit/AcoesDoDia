import psycopg2
from psycopg2 import sql, Error

class StocksDB:
    def __init__(self, host, port, database, user, password):
        """Connect to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cur = self.conn.cursor()
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def fetch_latest_timestamp(self, ticker):
        """Fetch the latest timestamp for a given stock ticker."""
        try:
            query = "SELECT MAX(date) FROM financial_data WHERE ticker = %s"
            self.cur.execute(query, (ticker,))
            result = self.cur.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error fetching latest timestamp: {e}")
            return None

    def insert_stock(self, symbol, date, open_price, high_price, low_price, close_price, volume):
        """Insert stock data into the database."""
        try:
            query = """
            INSERT INTO financial_data (ticker, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """
            self.cur.execute(query, (symbol, date, open_price, high_price, low_price, close_price, volume))
            self.conn.commit()
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            print(f"Integrity error: {e}")
        except Error as e:
            self.conn.rollback()
            print(f"Error inserting stock data: {e}")
