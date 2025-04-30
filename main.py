import os
import subprocess
import sys
import logging
from pathlib import Path
from scripts.config import RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR, CUSTOM_CSV_DIR

# Configures basic logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ensure_directories():
    for path in [RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR]:
        os.makedirs(path, exist_ok=True)
    logging.info("All output directories existing ensured.")

def run_scripts():
    script_path = Path("scripts", "strava-club-activity-to-csv.py")
    logging.info(f"Running script: {script_path}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        logging.error(f"Script failed with exit code: {result.returncode}")
    else:
        logging.info("Script ran and generated data CSV successfully.")

    script_path = Path("scripts", "strava-leaderboard-generator.py")
    logging.info(f"Running script: {script_path}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        logging.error(f"Script failed with exit code: {result.returncode}")
    else:
        logging.info("Script ran and generated leaderboard successfully.")

    script_path = Path("scripts", "filezipper.py")
    logging.info(f"Running script: {script_path}")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        logging.error(f"Script failed with exit code: {result.returncode}")
    else:
        logging.info("Script ran and generated .zip successfully.")
        print("Script finished running succesfully.")

def run_custom_script():
    os.makedirs(CUSTOM_CSV_DIR, exist_ok=True)
    logging.info("Custom output directory existing ensured.")

    script_path = os.path.join("scripts", "custom.py")
    logging.info(f"Running script: {script_path}")
    result = subprocess.run(["python", script_path])
    if result.returncode != 0:
        logging.error(f"Custom script failed with exit code: {result.returncode}")
    else:
        logging.info("Custom script ran and generated .CSV successfully.")

def run_send_mail_script():
    script_path = os.path.join("scripts", "send-mail.py")
    logging.info(f"Running script: {script_path}")
    result = subprocess.run(["python", script_path])
    if result.returncode != 0:
        logging.error(f"Send mail failed with exit code: {result.returncode}")
    else:
        logging.info("Mail succesfully sent.")

def main():
    ensure_directories()
    run_scripts()

    ### Please uncomment following code if you want to use a custom script.
    # run_custom_script()

    ### OPTIONAL: Please comment following code if you don't want mails to be sent.
    # run_send_mail_script()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("An unexpected error has occured.")
        raise