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
                    stat_date = entry['stat_date']
                    circulating_fil = entry['circulating_fil']
                    mined_fil = entry['mined_fil']
                    vested_fil = entry['vested_fil']
                    reserve_disbursed_fil = entry['reserve_disbursed_fil']
                    locked_fil = entry['locked_fil']
                    burnt_fil = entry['burnt_fil']

                    # Calculate potential unlocked FIL
                    potential_unlocked_fil = circulating_fil - mined_fil

                    # Calculate FF/PL/Team Unlock (66.667% of potential unlocked FIL)
                    ff_pl_team_unlock = 0.66667 * potential_unlocked_fil

                    # Calculate daily FF/PL/Team Unlock (difference from previous day)
                    daily_ff_pl_team_unlock = ff_pl_team_unlock - prev_ff_pl_team_unlock

                    # Get FIL price from the loaded prices
                    fil_price = fil_prices[date]

                    # Calculate FF/PL Daily Value based on unlocked FIL and FIL price
                    ff_pl_daily_value = daily_ff_pl_team_unlock * fil_price

                    # Data processing succeeded, break out of the retry loop
                break  # Data processing succeeded, break out of the retry loop
            else:
                print("Error in API response:", data.get('message', 'Unknown error'))
                retries += 1
                time.sleep(60)

        except requests.exceptions.RequestException as e:
            print("Error making API request:", e)
            retries += 1
            time.sleep(60)

    # If retries reached the maximum limit, we can return None or raise an exception
    if retries == max_retries:
        print(f"Failed to fetch data for date: {formatted_date} after {max_retries} attempts.")
        return None, prev_ff_pl_team_unlock

    processed_data = {
        'stat_date': stat_date,
        'circulating_fil': circulating_fil,
        'mined_fil': mined_fil,
        'vested_fil': vested_fil,
        'reserve_disbursed_fil': reserve_disbursed_fil,
        'locked_fil': locked_fil,
        'burnt_fil': burnt_fil,
        'ff_pl_team_unlock': ff_pl_team_unlock,
        'daily_ff_pl_team_unlock': daily_ff_pl_team_unlock,
        'fil_price': fil_price,
        'ff_pl_daily_value': ff_pl_daily_value,
    }
    return processed_data, ff_pl_team_unlock  # Return the updated value for the next day

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
        prev_ff_pl_team_unlock = processed_data['ff_pl_team_unlock']
    processed_data_dict[date] = processed_data


# Define a function to write the processed data to a CSV file
def write_processed_data_to_csv(data, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['Stat Date', 'Circulating FIL', 'Mined FIL', 'Vested FIL', 'Reserve Disbursed FIL', 'Locked FIL', 'Burnt FIL', 'FF/PL/Team Unlock', 'Daily FF/PL/Team Unlock', 'FIL Price', 'FF/PL Daily Value']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for date, processed_data in data.items():
            row = {
                'Stat Date': processed_data['stat_date'],
                'Circulating FIL': processed_data['circulating_fil'],
                'Mined FIL': processed_data['mined_fil'],
                'Vested FIL': processed_data['vested_fil'],
                'Reserve Disbursed FIL': processed_data['reserve_disbursed_fil'],
                'Locked FIL': processed_data['locked_fil'],
                'Burnt FIL': processed_data['burnt_fil'],
                'FF/PL/Team Unlock': processed_data['ff_pl_team_unlock'],
                'Daily FF/PL/Team Unlock': processed_data['daily_ff_pl_team_unlock'],
                'FIL Price': processed_data['fil_price'],
                'FF/PL Daily Value': processed_data['ff_pl_daily_value'],
            }
            csv_writer.writerow(row)

# Save processed data to a new CSV file
write_processed_data_to_csv(processed_data_dict, 'processed_data.csv')
