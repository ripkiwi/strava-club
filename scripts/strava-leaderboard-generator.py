import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from config import BASE_DIR, CSV_DELIMITER, TIMESTAMP

# Configures basic logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

### Loads the latest outputted .CSV file.
def get_latest_csv():
    csv_files = sorted(Path(BASE_DIR).glob("output/raw-data-csv/raw_club_data*.csv"), reverse=True)
    logging.info("Found the latest .CSV, progressing script...")
    return csv_files[0] if csv_files else None

### Generates the leaderboard.
def generate_leaderboard(csv_path):
    df = pd.read_csv(csv_path, delimiter=CSV_DELIMITER)

    # Ensure numeric types
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['moving_time'] = pd.to_numeric(df['moving_time'], errors='coerce')

    # Example demonstration values, the leaderboard can be created for other values such as elevation gain too.
    leaderboard = df.groupby('athlete_name').agg({
        'distance': 'sum',
        'moving_time': 'sum',
    }).reset_index()

    leaderboard['distance_km'] = (leaderboard['distance'] / 1000).round(3)
    leaderboard['moving_time_m'] = (leaderboard['moving_time'] / 60).round(2)
    leaderboard = leaderboard.drop(columns=['distance', 'moving_time'])

    leaderboard = leaderboard.sort_values(by='distance_km', ascending=False)
    logging.info("Leaderboard generated, progressing script...")
    return leaderboard

### We store the leaderboard .CSV locally.
def save_leaderboard_csv(df):
    path = Path(BASE_DIR, f"output/leaderboard-csv/leaderboard_{TIMESTAMP}.csv")
    df.to_csv(path, sep=CSV_DELIMITER, index=False)
    logging.info(f"Saved leaderboard .CSV to {path}.")

### We visualize the data to be easier for general user consumption.
def visualize_leaderboard(df):
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
    ax2.set_ylabel('Moving Time (m)', color='darkorange')
    ax2.tick_params(axis='y', labelcolor='darkorange')

    # Add labels with values on the line dots for clarity.
    for i, (x, y) in enumerate(zip(athletes, times)):
        ax2.annotate(f'{y:.1f}', (x, y), textcoords="offset points", xytext=(0, 8), 
                     ha='center', color='darkorange', fontsize=9)

    plt.title(f'Strava Leaderboard – {TIMESTAMP}')
    fig.tight_layout()

    # Save plot
    output_path = Path(BASE_DIR) / 'output' / 'leaderboard-plots' / f'leaderboard_{TIMESTAMP}.png'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    logging.info(f"Succesfully leaderboard plot to {output_path}.")
    plt.close()

### Validation and main runner, ensures that we only move forward if each step succeeds.
if __name__ == "__main__":
    latest_csv = get_latest_csv()
    if not latest_csv:
        logging.error("No CSV found, exiting...")
        exit()

    leaderboard_df = generate_leaderboard(latest_csv)
    save_leaderboard_csv(leaderboard_df)
    visualize_leaderboard(leaderboard_df)