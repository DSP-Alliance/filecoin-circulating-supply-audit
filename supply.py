import requests
import csv
import time
from datetime import datetime, timedelta

# Replace with your actual API key
api_key = 'YOUR_API_KEY_HERE'

url = "https://api.spacescope.io/v2/circulating_supply/circulating_supply"
headers = {
    'authorization': f'Bearer {api_key}'
}

# Load FIL prices from the CSV file
def load_film_prices_from_csv(csv_filename):
    fil_prices = {}
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            original_date = row['Date']
            original_date_object = datetime.strptime(original_date, '%Y-%m-%d')
            fil_price = float(row['FIL Price'])
            fil_prices[original_date_object] = fil_price
    return fil_prices

# This function will return the total vested amount for the foundation or labs until a given date
def calculate_vested_amount(start_date, current_date, total_amount, vesting_years):
    days_since_start = (current_date - start_date).days
    total_days = vesting_years * 365
    vested_amount = min(total_amount * days_since_start / total_days, total_amount)
    return vested_amount

def daily_vested_amount(start_date, current_date, total_amount, vesting_years):
    days_since_start = (current_date - start_date).days
    yesterday_vested = calculate_vested_amount(start_date, current_date - timedelta(days=1), total_amount, vesting_years)
    today_vested = calculate_vested_amount(start_date, current_date, total_amount, vesting_years)
    return today_vested - yesterday_vested

# Function to process data for a specific date
def process_data_for_date(date, prev_ff_pl_team_unlock):
    formatted_date = date.strftime('%Y-%m-%d')  # Convert date to ISO 8601 format
    params = {
        'start_date': formatted_date,
        'end_date': formatted_date
    }
    max_retries = 3  # setting a maximum retry limit
    retries = 0

    while retries < max_retries:
        print(f"Fetching data for date: {formatted_date}")
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if response.status_code == 200 and data['code'] == 0 and len(data['data']) > 0:
                for entry in data['data']:
                    circulating_fil = entry['circulating_fil']
                    mined_fil = entry['mined_fil']
                    burnt_fil = entry['burnt_fil']

                    # Calculate potential unlocked FIL
                    potential_unlocked_fil = circulating_fil - mined_fil - burnt_fil
                    start_date = datetime.strptime("2020-10-15", '%Y-%m-%d')

                    foundation_allocation = 0.05 * 2_000_000_000  # 5% of 2B FIL
                    labs_allocation = 0.15 * 2_000_000_000  # 15% of 2B FIL

                    # Calculate the daily vested FIL for Filecoin Foundation and Protocol Labs
                    foundation_daily_vest = daily_vested_amount(start_date, date, foundation_allocation, 6)
                    labs_daily_vest = daily_vested_amount(start_date, date, labs_allocation, 6)

                    # Now calculate the FF/PL/Team Unlock for the day
                    daily_ff_pl_team_unlock = foundation_daily_vest + labs_daily_vest

                    # Get FIL price from the loaded prices
                    fil_price = fil_prices[date]

                    # Calculate FF/PL Daily Value based on unlocked FIL and FIL price
                    ff_pl_daily_value = daily_ff_pl_team_unlock * fil_price

                break
            else:
                print("Error in API response:", data.get('message', 'Unknown error'))
                retries += 1
                time.sleep(60)
        except requests.exceptions.RequestException as e:
            print("Error making API request:", e)
            retries += 1
            time.sleep(60)

    if retries == max_retries:
        print(f"Failed to fetch data for date: {formatted_date} after {max_retries} attempts.")
        return None, prev_ff_pl_team_unlock

    processed_data = {
        'stat_date': formatted_date,
        'circulating_fil': circulating_fil,
        'mined_fil': mined_fil,
        'burnt_fil': burnt_fil,
        'daily_ff_pl_team_unlock': daily_ff_pl_team_unlock,
        'fil_price': fil_price,
        'ff_pl_daily_value': ff_pl_daily_value,
    }
    return processed_data, daily_ff_pl_team_unlock

# Load FIL prices from CSV
fil_prices = load_film_prices_from_csv('fil_prices.csv')

# Initialize previous day's FF/PL/Team Unlock
prev_ff_pl_team_unlock = 0

# Create a dictionary to store processed data
processed_data_dict = {}

# Loop through FIL prices dates and process data
for date in fil_prices:
    processed_data, prev_ff_pl_team_unlock = process_data_for_date(date, prev_ff_pl_team_unlock)
    if processed_data:  # Only update if we successfully got the data for that date
        processed_data_dict[date] = processed_data

# Define a function to write the processed data to a CSV file
def write_processed_data_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['Stat Date', 'Circulating FIL', 'Mined FIL', 'Burnt FIL', 'Daily FF/PL/Team Unlock', 'FIL Price', 'FF/PL Daily Value']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for date, processed_data in data.items():
            row = {
                'Stat Date': processed_data['stat_date'],
                'Circulating FIL': processed_data['circulating_fil'],
                'Mined FIL': processed_data['mined_fil'],
                'Burnt FIL': processed_data['burnt_fil'],
                'Daily FF/PL/Team Unlock': processed_data['daily_ff_pl_team_unlock'],
                'FIL Price': processed_data['fil_price'],
                'FF/PL Daily Value': processed_data['ff_pl_daily_value'],
            }
            csv_writer.writerow(row)

# Save processed data to a new CSV file
write_processed_data_to_csv(processed_data_dict, 'processed_data.csv')
