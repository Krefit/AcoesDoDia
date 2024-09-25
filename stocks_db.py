import psycopg2
from psycopg2 import sql, Error

class StocksDB:
    def __init__(self, host, port, database, user, password):
        """Inicializa a conexão com o banco de dados PostgreSQL."""
        try:
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            self.cur = self.conn.cursor()
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def insert_stock(self, symbol, company_name, open_price, high_price, low_price, close_price, volume, date):
        """
        Insere uma nova ação no banco de dados.
        """
        try:
            # Insert stock record with ON CONFLICT DO NOTHING to avoid duplicate inserts
            unique_id = f"{symbol}_{date}"
            insert_query = """
            INSERT INTO financial_data (ticker, unique_id, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (unique_id) DO NOTHING
            """
            self.cur.execute(insert_query, (symbol, unique_id, date, open_price, high_price, low_price, close_price, volume))
            self.conn.commit()

            if self.cur.rowcount > 0:
                print(f"Ação inserida com sucesso: {symbol} - Data: {date}")
            else:
                print(f"Ação com símbolo {symbol} e data {date} já existe no banco de dados.")
            return True

        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            print(f"Erro de integridade ao inserir ação: {symbol} - {date}. {e}")
            return False

        except Error as e:
            self.conn.rollback()
            print(f"Erro ao inserir ação no banco de dados: {e}")
            return False

    def fetch_latest_timestamp(self, ticker):
        """Retorna a última data de uma ação com o ticker fornecido."""
        try:
            sql_query = "SELECT MAX(date) FROM financial_data WHERE ticker = %s"
            self.cur.execute(sql_query, (ticker,))
            result = self.cur.fetchone()
            latest_date = result[0] if result else None

            if latest_date:
                print(f"Última data encontrada para o ticker {ticker}: {latest_date}")
            else:
                print(f"Nenhuma data encontrada para o ticker {ticker}.")
            
            return latest_date

        except Error as e:
            print(f"Erro ao buscar o último timestamp para o ticker {ticker}: {e}")
            return None

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexão com o banco de dados fechada.")

    def __del__(self):
        self.close()
