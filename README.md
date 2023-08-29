# Filecoin Daily Vesting Analysis Repository

This repository contains scripts to fetch and analyze the daily vesting of Filecoin tokens for the Filecoin Foundation and Protocol Labs. It comprises two main scripts:

### How "Daily FF/PL/Team Unlock" is Calculated

1. **Potential Unlocked FIL**: Calculated by subtracting mined and burnt FIL from circulating FIL, giving an idea of how much FIL has been potentially unlocked.
   
2. **Daily FF/PL/Team Unlock**: Represents the difference in the total unlocked FIL for FF/PL/Team between two consecutive days. It indicates the amount of FIL that got unlocked on a particular day.

3. **FIL Price**: This is fetched for each day to calculate the dollar value of the daily unlocked FIL.

4. **FF/PL Daily Value**: Represents the dollar value of the "Daily FF/PL/Team Unlock". It's calculated by multiplying the "Daily FF/PL/Team Unlock" with the "FIL Price" for the day.

### CSV Output Explained

- **Stat Date**: The date for which the data is being reported.
- **Circulating FIL**: The total amount of FIL tokens in circulation on that day.
- **Mined FIL**: Amount of FIL mined up to that date.
- **Burnt FIL**: Amount of FIL that has been burnt up to that date.
- **Daily FF/PL/Team Unlock**: Amount of FIL tokens that were unlocked on that day for the Filecoin Foundation, Protocol Labs, and their team.
- **FIL Price**: The price of FIL token in USD on that day.
- **FF/PL Daily Value**: The total value in USD of the FIL tokens that were unlocked on that day for the Filecoin Foundation, Protocol Labs, and their team.
  
## Scripts

1. **`prices.py`** - Fetches daily Filecoin prices from CoinGecko.
2. **`supply.py`** - Analyzes daily vesting based on the prices fetched from `prices.py`.

## Overview

### 1. `prices.py`

- Connects to the CoinGecko API.
- Retrieves daily Filecoin prices for a specified date range.
- Saves the prices for further analysis.

### 2. `supply.py`

- Loads the Filecoin prices saved by `prices.py`.
- Connects to the SpaceScope API to fetch data related to the circulating supply of Filecoin tokens.
- Performs calculations to determine the daily vesting amounts.
- Outputs the processed data to a CSV file.

## Prerequisites

- **Python Version:** Python 3.x
- **Required Python packages:** `requests`, `csv`
- **API Key:** A valid API key for the SpaceScope API (only for `supply.py`).

## Setup & Execution

### Install Required Packages

pip install requests


### Fetch Filecoin Prices

python prices.py


### Update API Key
1. Open `supply.py` in your editor.
2. Update it with your SpaceScope API key where indicated.

### Analyze Daily Vesting

python supply.py


## Important Notes
- Ensure you have the appropriate permissions to read/write to the CSV files and that they're not being accessed by another application at the same time.
- Both scripts come with error-handling mechanisms for API request issues. If an error is detected during data fetch, the scripts will introduce delays and retry fetching the data to bypass rate-limiting concerns.

## License
This project is under the MIT License. For details, check the `LICENSE` file.


