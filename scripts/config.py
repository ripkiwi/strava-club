import os
from dotenv import load_dotenv

### Root project directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

### Environment variables directory.
ENV_DIR = os.path.join(BASE_DIR, 'config', '.env')
load_dotenv(ENV_DIR)

### Environment variables access.
### Please reference 'https://www.strava.com/settings/api' for your API tokens.
### See README.md for more information on how to replace these.
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
API_URL = os.getenv("STRAVA_API_URL")

### Commonly used paths.
RAW_CSV_DIR = os.path.join(BASE_DIR, "output/raw-data-csv")
LEADERBOARD_CSV_DIR = os.path.join(BASE_DIR, "output/leaderboard-csv")
LEADERBOARD_PLOTS_DIR = os.path.join(BASE_DIR, "output/leaderboard-plots")