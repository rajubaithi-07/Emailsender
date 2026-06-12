import smtplib, json, schedule, time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open('config.json') as f:
    cfg = json.load(f)

EMAIL = cfg["email"]
PASSWORD = cfg["password"]
SMTP_SERVER = cfg["smtp_server"]
SMTP_PORT = cfg["smtp_port"]

with open('email_list.txt') as f:
    RECIPIENTS = [e.strip() for e in f if e.strip()]

def build_email_body():
    today = datetime.now().strftime("%d %B %Y")
    return f"""
Hello Team,

Daily Marketing Update for {today}.

Please reply with:
1️⃣ Purpose of Visit
2️⃣ Work Status
3️⃣ Area Covered
4️⃣ Photos (if any)
5️⃣ Sales % in your district

Regards,
Marketing Automation
"""

def send_marketing_email():
    subject = f"Daily Marketing Update – {datetime.now().strftime('%d %b %Y')}"
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = subject
    msg.attach(MIMEText(build_email_body(), 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print(f"[{time.ctime()}] ✅ Email sent successfully.")
    except Exception as e:
        print(f"[{time.ctime()}] ❌ Failed to send email: {e}")

schedule.every().day.at(cfg["schedule_time"]).do(send_marketing_email)

if __name__ == "__main__":
    print("🚀 Marketing Email Automation Started...")
    send_marketing_email()
    while True:
        schedule.run_pending()
        time.sleep(30)
