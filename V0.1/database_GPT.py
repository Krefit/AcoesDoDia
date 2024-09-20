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
        Se a ação com o mesmo símbolo e data já existir, ignora a inserção para evitar duplicatas.
        """
        try:
            # Tenta inserir a nova ação
            sql_query = """
            INSERT INTO stocks (symbol, company_name, open_price, high_price, low_price, close_price, volume, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cur.execute(sql_query, (symbol, company_name, open_price, high_price, low_price, close_price, volume, date))
            self.conn.commit()
            print(f"Ação inserida com sucesso: {symbol} - Data: {date}")
        except psycopg2.IntegrityError:
            # Caso de duplicata, rola de volta a transação e ignora a inserção
            self.conn.rollback()
            print(f"Ação com símbolo {symbol} e data {date} já existe no banco de dados. Ignorando inserção.")
        except Error as e:
            # Caso de erro genérico
            print(f"Erro ao inserir ação no banco de dados: {e}")
            self.conn.rollback()

    def get_all_stocks(self):
        """Retorna todas as ações armazenadas no banco de dados."""
        try:
            self.cur.execute("SELECT * FROM stocks")
            return self.cur.fetchall()
        except Error as e:
            print(f"Erro ao recuperar as ações do banco de dados: {e}")
            return []

    def close_connection(self):
        """Fecha o cursor e a conexão com o banco de dados."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexão com o banco de dados fechada.")
