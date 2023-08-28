import requests
import csv
import time
from datetime import datetime, timedelta

# Function to fetch FIL price from CoinGecko API for a specific date
def get_filecoin_price(date):
    url = f"https://api.coingecko.com/api/v3/coins/filecoin/history"
    params = {
        "date": date.strftime('%d-%m-%Y'),
        "localization": "false"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and 'market_data' in data:
        return data['market_data']['current_price']['usd']
    return None

# Function to fetch FIL prices for a range of dates
def fetch_filecoin_prices(start_date, end_date):
    prices = {}
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        fil_price = get_filecoin_price(current_date)
        if fil_price is not None:
            prices[formatted_date] = fil_price
            print(f"FIL Price for {formatted_date}: {fil_price}")
        else:
            print(f"Error fetching FIL price for {formatted_date}")
            # Introduce a delay to avoid rate limiting and retry fetching the price
            time.sleep(60)
            continue
        
        current_date += timedelta(days=1)
        # Introduce a delay to avoid rate limiting
        time.sleep(10)
    
    return prices

# Define the date range you want to fetch data for
start_date = datetime(2020, 10, 15)
end_date = datetime.now()

# Fetch FIL prices
prices = fetch_filecoin_prices(start_date, end_date)
