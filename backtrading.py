import pandas as pd
import matplotlib.pyplot as plt

def backtest(data, initial_capital=10000):
    """Simulate a backtest using buy/sell signals and calculate portfolio performance."""
    positions = pd.DataFrame(index=data.index)
    positions['Stock'] = 100 * data['Signal']  # Buy/sell 100 shares

    portfolio = pd.DataFrame(index=data.index)
    portfolio['Holdings'] = positions['Stock'] * data['Close']
    portfolio['Cash'] = initial_capital - (positions['Stock'] * data['Close']).cumsum()
    portfolio['Total'] = portfolio['Holdings'] + portfolio['Cash']
    portfolio['Returns'] = portfolio['Total'].pct_change()
    return portfolio

def run_backtest(ticker, data):
    """Run the backtest and display results."""
    portfolio = backtest(data)

    # Calculate total return
    total_return = (portfolio['Total'][-1] / portfolio['Total'][0]) - 1
    print(f"Total Return for {ticker}: {total_return * 100:.2f}%")

    # Plot the portfolio and signals
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label=f'{ticker} Price')
    plt.plot(data['SMA_10'], label='SMA 10')
    plt.plot(data['SMA_50'], label='SMA 50')
    plt.plot(data[data['Position'] == 1].index, data['Close'][data['Position'] == 1], "^", markersize=10, color="g", lw=0, label='Buy Signal')
    plt.plot(data[data['Position'] == -1].index, data['Close'][data['Position'] == -1], "v", markersize=10, color="r", lw=0, label='Sell Signal')
    plt.title(f'{ticker} Backtest Results')
    plt.legend(loc='best')
    plt.show()
