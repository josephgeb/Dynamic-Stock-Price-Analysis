import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Step 1: Fetch Stock Data from Alpha Vantage API
def fetch_stock_data(ticker):
    """
    Fetch daily stock data for a given ticker symbol from Alpha Vantage.
    Returns the stock data as a pandas DataFrame.
    """
    # Your Alpha Vantage API key
    api_key = '4A4GN5S7EHPZZO8P'  # Update with your own key
    
    # Alpha Vantage URL for Time Series Daily
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=compact&datatype=json'
    
    # Make the API call
    response = requests.get(url)
    data = response.json()
    
    # Check if the response contains the expected data
    if 'Time Series (Daily)' not in data:
        print("Error fetching data or reaching API limit.")
        return pd.DataFrame()
    
    # Extract the 'Time Series (Daily)' data
    time_series = data['Time Series (Daily)']
    
    # Convert the time series data into a pandas DataFrame
    stock_data = pd.DataFrame.from_dict(time_series, orient='index')
    
    # Rename columns for clarity and convert them to numeric values
    stock_data.columns = ['open', 'high', 'low', 'close', 'volume']
    stock_data = stock_data.apply(pd.to_numeric, errors='coerce')
    
    # Reverse the DataFrame to have the most recent date at the bottom
    stock_data = stock_data[::-1]
    
    # Reset index to have the date as a column
    stock_data.reset_index(inplace=True)
    stock_data.rename(columns={'index': 'date'}, inplace=True)
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    
    return stock_data

# Step 2: Calculate Simple Moving Averages (SMA)
def calculate_moving_averages(stock_data, short_window=50, long_window=200):
    """
    Calculate short and long simple moving averages for trend analysis.
    """
    stock_data['SMA50'] = stock_data['close'].rolling(window=short_window).mean()
    stock_data['SMA200'] = stock_data['close'].rolling(window=long_window).mean()
    
    return stock_data

# Step 3: Generate Buy/Sell Alerts Based on Moving Averages
def generate_alerts(stock_data):
    """
    Generate buy/sell signals based on SMA crossovers.
    A 'Buy' signal is generated when SMA50 crosses above SMA200.
    A 'Sell' signal is generated when SMA50 crosses below SMA200.
    """
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(stock_data)):
        if stock_data['SMA50'][i] > stock_data['SMA200'][i] and stock_data['SMA50'][i - 1] <= stock_data['SMA200'][i - 1]:
            buy_signals.append((stock_data['date'][i], stock_data['close'][i]))
        elif stock_data['SMA50'][i] < stock_data['SMA200'][i] and stock_data['SMA50'][i - 1] >= stock_data['SMA200'][i - 1]:
            sell_signals.append((stock_data['date'][i], stock_data['close'][i]))
    
    return buy_signals, sell_signals

# Step 4: Plot the Data and Alerts
def plot_stock_data(stock_data, buy_signals, sell_signals):
    """
    Plot stock closing prices along with SMA50 and SMA200.
    Plot buy/sell signals.
    """
    plt.figure(figsize=(12, 6))
    
    # Plot closing prices
    plt.plot(stock_data['date'], stock_data['close'], label='Close Price', color='blue', alpha=0.5)
    
    # Plot moving averages
    plt.plot(stock_data['date'], stock_data['SMA50'], label='SMA50', color='orange', alpha=0.75)
    plt.plot(stock_data['date'], stock_data['SMA200'], label='SMA200', color='green', alpha=0.75)
    
    # Track if labels have been added to avoid duplication
    buy_label_added = False
    sell_label_added = False

    # Plot buy signals
    for buy_signal in buy_signals:
        if not buy_label_added:
            plt.scatter(buy_signal[0], buy_signal[1], marker='^', color='green', s=100, label='Buy Signal')
            buy_label_added = True
        else:
            plt.scatter(buy_signal[0], buy_signal[1], marker='^', color='green', s=100)
    
    # Plot sell signals
    for sell_signal in sell_signals:
        if not sell_label_added:
            plt.scatter(sell_signal[0], sell_signal[1], marker='v', color='red', s=100, label='Sell Signal')
            sell_label_added = True
        else:
            plt.scatter(sell_signal[0], sell_signal[1], marker='v', color='red', s=100)
    
    # Format date on x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)

    plt.title('Stock Price and Moving Averages with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Step 5: Main Execution
if __name__ == "__main__":
    # Fetch stock data for AAPL
    df = fetch_stock_data('AAPL')
    
    if not df.empty:
        # Calculate moving averages (SMA50 and SMA200)
        df = calculate_moving_averages(df)
        
        # Generate buy and sell alerts
        buy_signals, sell_signals = generate_alerts(df)
        
        # Display the first few rows of stock data
        print(df.head())
        
        # Plot the stock data along with buy/sell signals
        plot_stock_data(df, buy_signals, sell_signals)
