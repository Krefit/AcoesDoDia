# acao.py file
class Stock:
    def __init__(self, symbol, company_name, historical_data_prices=None):
        self.symbol = symbol
        self.company_name = company_name
        self.historical_data_prices = historical_data_prices if historical_data_prices else []

    def get_info(self):
        info = f"Stock Information:\n\tSymbol: {self.symbol}\n\tCompany Name: {self.company_name}"
        if self.historical_data_prices:
            info += "\n\tHistorical Data Prices:"
            for price_data in self.historical_data_prices:
                price_date = price_data.get("date", "N/A")
                price_value = price_data.get("value", "N/A")
                info += f"\n\t\tDate: {price_date}, Value: {price_value}"
        return info