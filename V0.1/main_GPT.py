import requests
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from datetime import datetime
from acao import Stock  # Importa a classe Stock
from stocks_db import StocksDB  # Importa a classe de conexão com o banco de dados

def print_stock_data(stocks):
    """Exibe informações sobre cada ação."""
    for stock in stocks:
        print(stock.get_info())
        print()

def create_stock_dataframe(stocks):
    """Cria um DataFrame a partir de uma lista de objetos Stock."""
    data = []
    for stock in stocks:
        for price in stock.historical_data_prices:
            data.append({
                'symbol': stock.symbol,
                'date': price['date'],
                'close': price['close'],
                'volume': price['volume']
            })
    return pd.DataFrame(data)

# Configuração do banco de dados
cn = StocksDB(
    host="localhost",
    port=5433,
    database="acao_dia",
    user="postgres",
    password="postgres"
)

# URL da API
url = 'https://brapi.dev/api/quote/PETR4?range=3mo&interval=1d&token=vTodNNnn1UMPvgBD1Vg7dB'
headers = {'Accept': 'application/brapi+json'}

# Faz a requisição GET à API
response = requests.get(url, headers=headers)

# Verifica se a resposta foi bem-sucedida
if response.status_code == 200:
    response_dict = response.json()
    results = response_dict.get("results", [])
    stock_list = []  # Lista para armazenar objetos Stock

    # Processa os resultados da API
    for result in results:
        symbol = result.get("symbol", "N/A")
        company_name = result.get("longName", "N/A")
        historical_data_prices = []

        for price in result.get("historicalDataPrice", []):
            date = price.get("date", "N/A")
            open_price = price.get("open", "N/A")
            high_price = price.get("high", "N/A")
            low_price = price.get("low", "N/A")
            close_price = price.get("close", "N/A")
            volume = price.get("volume", "N/A")
            
            # Tratamento da data, verificando se é timestamp ou string
            if isinstance(date, int):  # Se for timestamp (número inteiro)
                formatted_date = datetime.fromtimestamp(date).strftime('%d/%m/%Y')
            elif isinstance(date, str):  # Se for string (formato ISO)
                try:
                    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
                except ValueError:
                    formatted_date = date  # Usa o valor original se houver erro
            else:
                formatted_date = "N/A"

            # Adiciona os dados à lista de preços históricos
            historical_data_prices.append({
                "date": formatted_date,
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
                "volume": volume
            })

            # Insere no banco de dados
            cn.insert_stock(symbol, company_name, open_price, high_price, low_price, close_price, volume, formatted_date)

        # Cria o objeto Stock e adiciona à lista
        stock_obj = Stock(symbol=symbol, company_name=company_name, historical_data_prices=historical_data_prices)
        stock_list.append(stock_obj)

    # Exibe as informações das ações
    print_stock_data(stock_list)

    # Cria um DataFrame para visualização
    dados = create_stock_dataframe(stock_list)
    dados['date'] = pd.to_datetime(dados['date'], format='%d/%m/%Y')

    # Gráfico com seaborn
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='date', y='close', hue='volume', data=dados, palette="viridis", size='volume', sizes=(20, 200))
    plt.title(f"Preço de Fechamento das Ações de {stock_list[0].company_name}")
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Calcula e exibe o preço médio de fechamento
    for stock in stock_list:
        avg_close = stock.calculate_average_close_price()
        print(f"Preço médio de fechamento para {stock.symbol}: {avg_close}")

else:
    print(f"Falha ao recuperar os dados. Código de status: {response.status_code}")
