import os
import locale
import subprocess
import glob
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

### !!! THIS WHOLE SCRIPT IS STILL A PROTOTYPE, THERE WILL BE BUGS, COMPILATION ERRORS AND THE LIKE. !!! ###

# Auto-detect delimiter for beautifying .CSV according to local standards.
decimal_point = locale.localeconv()['decimal_point']
delimited = ';' if decimal_point == ',' else ','

# Obtains the running directory for the .CSV to save to.
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_filename = os.path.join(script_dir, "output.csv")

### TODO: Run fetch script
def run_fetch_script():
    fetch_script = os.path.join(script_dir, 'strava-club-activity-to-csv.py')
    result = subprocess.run(["python", fetch_script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Error running strava-club-activity-to-csv.py:", result.stderr)
        exit(1)

### Loads the latest outputted .CSV file.
def get_latest_csv():
    csv_files = sorted(glob.glob(os.path.join(script_dir, "outputted-csv/strava_club_activities_*.csv")), reverse=True)
    return csv_files[0] if csv_files else None

### Generates the leaderboard.
def generate_leaderboard(csv_path):
    df = pd.read_csv(csv_path, delimiter=delimited)

    # Example demonstration values, the leaderboard can be created for other values such as elevation gain too.
    leaderboard = df.groupby('athlete_name').agg({
        'distance': 'sum',
        'moving_time': 'sum',
    }).reset_index()

    # TODO: this might need some fine tuning.
    leaderboard['distance_km'] = (leaderboard['distance'] / 1000).round(2)
    leaderboard['moving_time_h'] = (leaderboard['moving_time'] / 3600).round(2)
    leaderboard = leaderboard.drop(columns=['distance', 'moving_time'])

    leaderboard = leaderboard.sort_values(by='distance_km', ascending=False)
    return leaderboard

### We store the leaderboard .CSV locally.
def save_leaderboard_csv(df, date_str):
    path = os.path.join(script_dir, f"leaderboard-csv/leaderboard_{date_str}.csv")
    df.to_csv(path, sep=delimited, index=False)
    print(f"Saved leaderboard .CSV to {path}.")

### TODO: Visualization


### Validation and main runner, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    run_fetch_script()

    latest_csv = get_latest_csv()
    if not latest_csv:
        print("No CSV found.")
        exit()

    date_tag = datetime.now().strftime('%Y%m%d')
    leaderboard_df = generate_leaderboard(latest_csv)
    save_leaderboard_csv(leaderboard_df, date_tag)