import requests
import json
import csv
import os
import hashlib
from pathlib import Path
from config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, API_URL, RAW_CSV_DIR, CSV_DELIMITER, TIMESTAMP

### Strava API URL, leave unchanged.
TOKEN_URL ="https://www.strava.com/api/v3/oauth/token"

# Output .CSV path and name. Removing the timestamp will make it so that all data from the earliest possible point will be consistently saved.
csv_filename = Path(RAW_CSV_DIR, f"raw_club_data_{TIMESTAMP}.csv")

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
        print(f"Error fetching access token: {response.status_code}")
        print(f"Error details: {response.text}")
        return None

### Generates a unique hash per row. This is used to check for duplicates, considering Strava's API is too limited.
def generate_row_hash(entry: dict, fields_to_use: list) -> str:
    key_string = '|'.join(str(entry.get(field, '')) for field in fields_to_use)
    return hashlib.sha256(key_string.encode('utf-8')).hexdigest()

### Using the access token, retrieves the requested data from the club.
def fetch_data(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        print(f"Succesfully fetched following data from API: {response.text}")
        return response.json()  # Parse JSON response
    else:
        print(f"Error fetching data from API: {response.status_code}")
        print(f"Error details: {response.text}")
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

### Loads existing unique IDs, skipping them to avoid duplicates.
def load_existing_ids(csv_filename):
    existing_ids = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=CSV_DELIMITER)
            for row in reader:
                if 'unique_id' in row:
                    existing_ids.add(row['unique_id'])
    return existing_ids

### Main function, turns the JSON into a .CSV file.
def json_to_csv(json_data, csv_filename):
    if not json_data:
        print("No data available to convert to CSV.")
        return

    if isinstance(json_data, dict):
        json_data = [json_data]

    # Flatten all entries first (for a more beautified CSV)
    flattened_data = [flatten_json(entry) for entry in json_data]

    # Decides which fields contribute to the unique hash.
    hash_fields = ['athlete.firstname','distance''elapsed_time','moving_time']

    # Generate unique hash 'unique_id' for each row.
    for entry in flattened_data:
        entry['unique_id'] = generate_row_hash(entry, hash_fields)
        entry['date_added'] = TIMESTAMP

    # We merge the first and last name into one column, and remove the respective merged columns.
    for entry in flattened_data:
        first_name = entry.get('athlete.firstname', '')
        last_name = entry.get('athlete.lastname','')
        entry['athlete_name'] = f"{first_name} {last_name}".strip()
        entry.pop('athlete.firstname', None)
        entry.pop('athlete.lastname', None)

    # Load existing unique IDs from the file.
    existing_ids = load_existing_ids(csv_filename)

    # Filter out any duplicates.
    new_data = [entry for entry in flattened_data if entry['unique_id'] not in existing_ids]

    if not new_data:
        print("There was no new unique data to write.")
        return

    # Gather all possible keys (these will become the column headers)
    all_keys = set()
    for entry in new_data:
        all_keys.update(entry.keys())

    # Sort the column to have 'athlete_name' as first column.
    ordered_keys = ['athlete_name'] + sorted(k for k in all_keys if k != 'athlete_name')

    # Validation for added columns.
    if 'unique_id' not in ordered_keys:
        ordered_keys.append('unique_id')
    if 'date_added' not in ordered_keys:
        ordered_keys.append('date_added')


    with open(csv_filename, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ordered_keys, delimiter=CSV_DELIMITER)
        writer.writeheader()
        writer.writerows(flattened_data)

    print(f"Strava Club CSV file '{csv_filename}' has been created/appended successfully.")

### Validation and main runner, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    access_token = get_access_token()
    
    if access_token:
        data = fetch_data(access_token)
        if data:
            json_to_csv(data, csv_filename)