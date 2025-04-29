import os
import subprocess
import sys
from pathlib import Path
from scripts.config import RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR, CUSTOM_CSV_DIR

def ensure_directories():
    for path in [RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR]:
        os.makedirs(path, exist_ok=True)
    print("All output directories existing ensured.")

def run_scripts():
    script_path = Path("scripts", "strava-club-activity-to-csv.py")
    print(f"Running script: {script_path}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"Script failed with exit code: {result.returncode}")
    else:
        print("Script ran and generated data CSV successfully.")

    script_path = Path("scripts", "strava-leaderboard-generator.py")
    print(f"Running script: {script_path}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"Script failed with exit code: {result.returncode}")
    else:
        print("Script ran and generated leaderboard successfully.")

### Please uncomment following code if you want to use a custom script.
# def run_custom_script():
#     os.makedirs(CUSTOM_CSV_DIR, exist_ok=True)
#     print("Custom output directory existing ensured.")

#     script_path = os.path.join("scripts", "custom.py")
#     print(f"Running script: {script_path}")
#     result = subprocess.run(["python", script_path])
#     if result.returncode != 0:
#         print(f"Custom script failed with exit code: {result.returncode}")
#     else:
#         print("Custom script ran and generated successfully.")

def main():
    ensure_directories()
    run_scripts()

    # Following line should also be uncommented for usage of custom script.
    # run_custom_script()

if __name__ == "__main__":
    main()