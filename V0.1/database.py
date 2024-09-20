import psycopg2

class StocksDB:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()

    def insert_stock(self, symbol, company_name, open_price, high_price, low_price, close_price, volume, date):
        # Check if the stock symbol and date already exist
        self.cur.execute("SELECT COUNT(*) FROM stocks WHERE symbol = %s AND date = %s", (symbol, date))
        count = self.cur.fetchone()[0]
        if count > 0:
            #print(f"Stock with symbol {symbol} and date {date} already exists in the database.")
            return

        # Insert the new stock
        sql = "INSERT INTO stocks (symbol, company_name, open_price, high_price, low_price, close_price, volume, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(sql, (symbol, company_name, open_price, high_price, low_price, close_price, volume, date))
        self.conn.commit()
        print(f"Inserted new stock with symbol {symbol} and date {date}.")

    def get_all_stocks(self):
        self.cur.execute("SELECT * FROM stocks")
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()
