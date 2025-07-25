import smtplib
import json
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# STEP 1: Load sender email credentials from config.json
with open('config.json') as f:
    cfg = json.load(f)

EMAIL = cfg["email"]
PASSWORD = cfg["password"]
SMTP_SERVER = cfg["smtp_server"]
SMTP_PORT = cfg["smtp_port"]
SUBJECT = cfg["subject"]

# STEP 2: Load recipient emails from email_list.txt
with open('email_list.txt') as f:
    RECIPIENTS = [email.strip() for email in f if email.strip()]

# STEP 3: Define function to send email
def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = SUBJECT

    body = "Hello,\n\nThis is an automated email sent using Python.\n\nBest,\nYour Name"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print(f"[{time.ctime()}] ✅ Email sent successfully.")
    except Exception as e:
        print(f"[{time.ctime()}] ❌ Failed to send email: {e}")

# STEP 4: Schedule the email to run daily at given time
schedule.every().day.at(cfg["schedule_time"]).do(send_email)

# STEP 5: Run once immediately, then wait for schedule
if __name__ == "__main__":
    print("🔄 Email scheduler started...")
    send_email()
    while True:
        schedule.run_pending()
        time.sleep(30)
