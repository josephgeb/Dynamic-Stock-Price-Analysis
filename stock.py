import requests
import pandas as pd

# Step 1: Fetch Stock Data from Alpha Vantage API
def fetch_stock_data(ticker):
    """
    Fetch daily stock data for a given ticker symbol from Alpha Vantage.
    Returns the stock data as a pandas DataFrame.
    """
    # Your Alpha Vantage API key
    api_key = '4A4GN5S7EHPZZO8P'
    
    # Alpha Vantage URL for Time Series Daily
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize=compact&datatype=json'
    
    # Make the API call
    response = requests.get(url)
    data = response.json()
    
    # Extract the 'Time Series (Daily)' data
    time_series = data['Time Series (Daily)']
    
    # Convert the time series data into a pandas DataFrame
    stock_data = pd.DataFrame.from_dict(time_series, orient='index')
    
    # Rename columns for clarity and convert them to numeric values
    stock_data.columns = ['open', 'high', 'low', 'close', 'volume']
    stock_data = stock_data.apply(pd.to_numeric)
    
    # Reverse the DataFrame to have the most recent date at the bottom
    stock_data = stock_data[::-1]
    
    # Reset index to have the date as a column
    stock_data.reset_index(inplace=True)
    stock_data.rename(columns={'index': 'date'}, inplace=True)
    
    return stock_data

# Fetch stock data for AAPL
df = fetch_stock_data('AAPL')

# Display the first few rows of the data
print(df.head())
