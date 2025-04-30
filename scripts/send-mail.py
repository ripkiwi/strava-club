import smtplib
import os
import glob
from dotenv import load_dotenv
from config import BASE_DIR
from email.message import EmailMessage

### Environment variables directory.
ENV_DIR = os.path.join(BASE_DIR, 'config', '.env')
load_dotenv(ENV_DIR)

EMAIL_ADDRESS = os.getenv("GMAIL_MAIL")
EMAIL_PASSWORD = os.getenv("GMAIL_PASS")
RECIPIENT = os.getenv("GMAIL_RECIPIENT")

msg = EmailMessage()
msg["Subject"] = "Strava Weekly API Content"
msg["From"] = EMAIL_ADDRESS
msg["To"] = RECIPIENT
msg.set_content("Please view attachment, thank you.")

# Find the most recent zipped_output_*.zip in BASE_DIR
matching_zips = sorted(
    glob.glob(os.path.join(BASE_DIR, "zipped_output_*.zip")),
    key=os.path.getmtime,
    reverse=True
)

if not matching_zips:
    raise FileNotFoundError("No .zip file found in the root directory.")

zip_path = matching_zips[0]

with open(zip_path, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="zip",
        filename=os.path.basename(zip_path)
    )

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)