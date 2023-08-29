# Filecoin Daily Vesting Analysis Repository

This repository contains scripts to fetch and analyze the daily vesting of Filecoin tokens for the Filecoin Foundation and Protocol Labs. It comprises two main scripts:

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
\```bash
pip install requests
\```

### Fetch Filecoin Prices
\```bash
python prices.py
\```

### Update API Key
1. Open `supply.py` in your editor.
2. Update it with your SpaceScope API key where indicated.

### Analyze Daily Vesting
\```bash
python supply.py
\```

## Important Notes
- Ensure you have the appropriate permissions to read/write to the CSV files and that they're not being accessed by another application at the same time.
- Both scripts come with error-handling mechanisms for API request issues. If an error is detected during data fetch, the scripts will introduce delays and retry fetching the data to bypass rate-limiting concerns.

## License
This project is under the MIT License. For details, check the `LICENSE` file.


