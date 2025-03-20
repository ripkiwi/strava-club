import requests
import json
import csv

# Private (Kevin Burgers) data for Strava API.
CLIENT_ID = "151932"
CLIENT_SECRET = "97245c9f09928690c552fe67b93176f245015b1f"
REFRESH_TOKEN = "1837d19a3d55c278d32ac9a163a551398cd60cbd"

API_URL = "https://www.strava.com/api/v3/clubs/1392745/activities"
TOKEN_URL ="https://www.strava.com/api/v3/oauth/token"

#ACCESS_TOKEN = "70009fe1d7514e3128980eae5b02123dee026f3b" #Legacy, will keep for documenting purposes.

# Fetches the access token, or requests a new one using the refresh token.
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

# Using the access token, retrieves the requested data from the club.
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

# Attempts conversion from JSON response into a .csv
#TODO: currently does not look nice, demo build.
def json_to_csv(json_data, csv_filename="C:/Users/kevin/Desktop/output.csv"):
    if not json_data:
        print("No data available to convert to CSV.")
        return

    if isinstance(json_data, dict):  
        json_data = [json_data]  

    keys = json_data[0].keys() if json_data else []

    # Write data to CSV, ChatGPT code, have to check it
    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(json_data)

    print(f"CSV file '{csv_filename}' has been created successfully.")

# Validation, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    access_token = get_access_token()
    
    if access_token:
        data = fetch_data(access_token)
        if data:
            json_to_csv(data)