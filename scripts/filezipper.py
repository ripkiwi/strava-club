import zipfile
import os
from config import RAW_CSV_DIR, LEADERBOARD_CSV_DIR, LEADERBOARD_PLOTS_DIR, TIMESTAMP, BASE_DIR
from pathlib import Path

# List of files to include
files_to_zip = [
    Path(RAW_CSV_DIR, f"raw_club_data_{TIMESTAMP}.csv"),
    Path(LEADERBOARD_CSV_DIR, f"leaderboard_{TIMESTAMP}.csv"),
    Path(LEADERBOARD_PLOTS_DIR, f"leaderboard_{TIMESTAMP}.png")
]

# Output zip path
zip_path = Path(BASE_DIR, f"zipped_output_{TIMESTAMP}.zip")

# Create the ZIP file
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files_to_zip:
        arcname = os.path.basename(file)
        zipf.write(file, arcname=arcname)

print(f"Created ZIP archive: {zip_path}")