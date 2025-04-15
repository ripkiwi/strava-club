import os
import subprocess
from scripts.config import RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR

def ensure_directories():
    for path in [RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR]:
        os.makedirs(path, exist_ok=True)
    print("All output directories existing ensured.")

def run_scripts():
    script_path = os.path.join("scripts", "strava-leaderboard-generator.py")
    print(f"Running script: {script_path}")
    result = subprocess.run(["python", script_path])
    if result.returncode != 0:
        print(f"Script failed with exit code: {result.returncode}")
    else:
        print("Script ran and generated successfully.")

def main():
    ensure_directories()
    run_scripts()

if __name__ == "__main__":
    main()
