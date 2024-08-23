import requests
from database import StocksDB
from datetime import datetime

# Store API URL
url = 'https://brapi.dev/api/quote/PETR4?range=3mo&interval=1d&token=vTodNNnn1UMPvgBD1Vg7dB'
cn = StocksDB(
    host="localhost",
    port=5433,
    database="acao_dia",
    user="postgres",
    password="postgres"
)

# Assign the headers
headers = {'Accept': 'application/brapi+json'}

# Send a GET request to the API
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Load the JSON response into a dictionary
    response_dict = response.json()

    # Access the "results" key in the response
    results = response_dict.get("results", [])

    # Create a list to store stock data
    stock_data = []

    # Extract symbol, company name, and historical data prices from each result
    for result in results:
        #symbol, company_name, open_price, high_price, low_price, close_price, volume, date
        symbol = result.get("symbol", "N/A")
        company_name = result.get("longName", "N/A")
        historical_data_prices = result.get("historicalDataPrice", [])

        # Extract historical data prices as a list of dictionaries
        prices = []
        for price in historical_data_prices:
            
            date = price.get("date", "N/A")
            open_price = price.get("open", "N/A")
            high_price = price.get("high", "N/A")
            low_price = price.get("low", "N/A")
            close_price = price.get("close", "N/A")
            volume = price.get("volume", "N/A")
            formatted_date = datetime.fromtimestamp(date).strftime('%d/%m/%Y')
            prices.append({"date": formatted_date, "value": open_price})
            cn.insert_stock(symbol, company_name, open_price, high_price, low_price, close_price, volume, formatted_date)

        stock_data.append({"symbol": symbol, "company_name": company_name, "prices": prices})
        

    # Print the stock data
    for stock in stock_data:
        print(f"Symbol: {stock['symbol']}, Company Name: {stock['company_name']}")
        for price in stock['prices']:
            print(f"Date: {price['date']}, Open Price: {price['value']}")
        print()

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")