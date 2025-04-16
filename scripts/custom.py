import os
import subprocess
import glob
import pandas as pd
import matplotlib.pyplot as plt
from config import BASE_DIR, CSV_DELIMITER, TIMESTAMP

### Loads the latest outputted .CSV file.
def get_latest_csv():
    csv_files = sorted(glob.glob(os.path.join(BASE_DIR, "output/raw-data-csv/raw_club_data_*.csv")), reverse=True)
    return csv_files[0] if csv_files else None

### Generates the leaderboard.
def generate_custom_csv(csv_path):
    df = pd.read_csv(csv_path, delimiter=CSV_DELIMITER)

    # Example demonstration values, these are the values for leaderboard.
    # Feel free to change it to accommondate your custom needs.
    leaderboard = df.groupby('athlete_name').agg({
        'distance': 'sum',
        'moving_time': 'sum',
    }).reset_index()

    leaderboard['distance_km'] = (leaderboard['distance'] / 1000).round(3)
    leaderboard['moving_time_m'] = (leaderboard['moving_time'] / 60).round(2)
    leaderboard = leaderboard.drop(columns=['distance', 'moving_time'])

    leaderboard = leaderboard.sort_values(by='distance_km', ascending=False)
    return leaderboard

### We store the custom .CSV locally.
def save_custom_csv(df):
    path = os.path.join(BASE_DIR, f"output/custom/custom_{TIMESTAMP}.csv")
    df.to_csv(path, sep=CSV_DELIMITER, index=False)
    print(f"Saved custom .CSV to {path}.")

### We visualize the data to be easier for general user consumption.
def visualize_custom_csv(df):
    # Important note, these values depend on the previous function.
    df = df.sort_values(by='distance_km', ascending=False)

    athletes = df['athlete_name']
    distances = df['distance_km']
    times = df['moving_time_m']

    fig, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(athletes, distances, color='skyblue', label='Distance (km)')
    ax1.set_ylabel('Distance (km)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(athletes, times, color='darkorange', marker='o', label='Moving Time (h)')
    ax2.set_ylabel('Moving Time (m))', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    plt.title(f'Strava Leaderboard – {TIMESTAMP}')
    fig.tight_layout()

    # Save plot
    output_path = os.path.join(BASE_DIR, f'output/custom/custom_{TIMESTAMP}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"Saved custom plot to {output_path}.")
    plt.close()


### Validation and main runner, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    # run_fetch_script()

    latest_csv = get_latest_csv()
    if not latest_csv:
        print("No CSV found.")
        exit()

    leaderboard_df = generate_custom_csv(latest_csv)
    save_custom_csv(leaderboard_df)
    visualize_custom_csv(leaderboard_df)