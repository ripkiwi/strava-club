import requests
import json
import csv
import os
import locale
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

### Initialization

API_URL = os.getenv("STRAVA_API_URL") # References desired club.
TOKEN_URL ="https://www.strava.com/api/v3/oauth/token" # Leave unchanged

# Please reference 'https://www.strava.com/settings/api' for your API tokens.
# See README.md for more information on how to replace these.
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# Auto-detect delimiter for beautifying .CSV according to local standards.
decimal_point = locale.localeconv()['decimal_point']
delimited = ';' if decimal_point == ',' else ','

# Obtains the running directory for the .CSV to save to.
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_filename = os.path.join(script_dir, "output.csv")

# Make it so that script runs don't overwrite each other and are saved with the date.
timestamp = datetime.now().strftime("%Y%m%d")
csv_filename = os.path.join(script_dir, f"outputted-csv/strava_club_activities_{timestamp}.csv")


### Fetches the access token, or requests a new one using the refresh token.
def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )

    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print("Error fetching access token:", response.status_code, response.text)
        return None

### Using the access token, retrieves the requested data from the club.
def fetch_data(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        print("Error fetching data:", response.status_code, response.text)
        return None

### Recursively flattens the JSON so that each nested JSON structure gets their own column in the outputted .csv file.
def flatten_json(y, parent_key='', sep='.'):
    items = []
    for k, v in y.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    return dict(items)

### Main function, turns the JSON into a .CSV file.
def json_to_csv(json_data, csv_filename):
    if not json_data:
        print("No data available to convert to CSV.")
        return

    if isinstance(json_data, dict):
        json_data = [json_data]

    # Flatten all entries first (for a more beautified CSV)
    flattened_data = [flatten_json(entry) for entry in json_data]

    # We merge the first and last name into one column, and remove the respective merged columns.
    for entry in flattened_data:
        first_name = entry.get('athlete.firstname', '')
        last_name = entry.get('athlete.lastname','')
        entry['athlete_name'] = f"{first_name} {last_name}".strip()
        entry.pop('athlete.firstname', None)
        entry.pop('athlete.lastname', None)

    # Gather all possible keys (these will become the column headers)
    all_keys = set()
    for entry in flattened_data:
        all_keys.update(entry.keys())

    # Sort the column to have 'athlete_name' as first column.
    ordered_keys = ['athlete_name'] + sorted(k for k in all_keys if k != 'athlete_name')

    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ordered_keys, delimiter=delimited)
        writer.writeheader()
        writer.writerows(flattened_data)

    print(f"Strava Club CSV file '{csv_filename}' has been created successfully.")

### Validation and main runner, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    access_token = get_access_token()
    
    if access_token:
        data = fetch_data(access_token)
        if data:
            json_to_csv(data, csv_filename)