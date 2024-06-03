
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

def fetch_ethereum_data(symbol, market):
    load_dotenv()
    # Get the API key from the environment variable
    api_key = os.getenv('AlphaVantage_API_key')
    # Construct the URL for the Alpha Vantage API call
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={api_key}'
    # Load environment variables from .env file

    # Make the API request and get the JSON response
    response = requests.get(url).json()

    # Extract the daily time series data from the JSON response
    time_series_key = 'Time Series (Digital Currency Daily)'
    if time_series_key not in response:
        print(f"Error fetching data: {response}")
        return None

    time_series_data = response[time_series_key]

    # Convert the nested dictionary to a DataFrame
    ethereum_api_data = pd.DataFrame.from_dict(time_series_data, orient='index')

    # Convert the index to datetime
    ethereum_api_data.index = pd.to_datetime(ethereum_api_data.index)

    # Rename the index to 'Date'
    ethereum_api_data.index.name = 'Date'
    
    # Rename columns for easier access
    ethereum_api_data.columns = [
        '1. Open',
        '2. High',
        '3. Low',
        '4. Close',
        '5. Volume'
    ]

    # Convert columns to numeric values
    ethereum_api_data = ethereum_api_data.apply(pd.to_numeric)

    # Filter the DataFrame to include only the last 6 months of data
    six_months_ago = datetime.now() - timedelta(days=6*30)  # approximate 6 months
    ethereum_api_data = ethereum_api_data[ethereum_api_data.index >= six_months_ago]

    return ethereum_api_data

# Load environment variables from .env file
#load_dotenv()

# Get the API key from the environment variable
#api_key = os.getenv('AlphaVantage_API_key')
symbol="ETH"
market="USD"
# Fetch and process the cryptocurrency data
df = fetch_ethereum_data(symbol, market)

# Check if the DataFrame is valid
if df is None:
    raise ValueError("Data fetching returned None. Please check the fetch_ethereum_data function.")
if df.empty:
    raise ValueError("Data fetching returned an empty DataFrame. Please check the fetch_ethereum_data function.")

print(f"Fetched DataFrame:\n{df.head()}\n[Total Rows: {df.shape[0]}]")
