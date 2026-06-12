import imaplib
import email
import sqlite3
import json
from datetime import datetime

# Load email credentials
with open('config.json') as f:
    cfg = json.load(f)

EMAIL = cfg["email"]
PASSWORD = cfg["password"]

# Connect to Gmail via IMAP
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    print("📥 Connected to Gmail inbox successfully.")
except Exception as e:
    print("❌ Error connecting to Gmail:", e)
    exit()

# Fetch all emails (you can use 'UNSEEN' to get only unread)
status, data = mail.search(None, 'ALL')
mail_ids = data[0].split()

if not mail_ids:
    print("⚠️ No emails found to fetch.")
else:
    print(f"📩 Found {len(mail_ids)} emails to check.")

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    subject TEXT,
                    date TEXT,
                    message TEXT)''')

count = 0

# Loop through emails
for mail_id in mail_ids[-20:]:  # only check last 20 for speed
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            sender = msg["From"]
            subject = msg["Subject"]
            date = msg["Date"]

            # Decode the message body safely
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))
                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        try:
                            body += part.get_payload(decode=True).decode(errors='ignore')
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                except:
                    pass

            # Store only new unique emails
            cursor.execute("SELECT * FROM replies WHERE sender=? AND subject=? AND date=?", 
                           (sender, subject, date))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO replies (sender, subject, date, message) VALUES (?, ?, ?, ?)",
                               (sender, subject, date, body))
                conn.commit()
                count += 1

print(f"✅ {count} new replies stored successfully.")
conn.close()
mail.logout()
