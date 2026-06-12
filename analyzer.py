import sqlite3
import pandas as pd
from datetime import datetime

# Connect to DB
conn = sqlite3.connect('database.db')

# Load all reports
df = pd.read_sql_query("SELECT * FROM daily_reports", conn)

# Convert dates
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.strftime('%B')

# Analyze
summary = df.groupby(['emp_email', 'month']).size().reset_index(name='total_reports')

print("📅 Monthly Report Summary")
print(summary)

# Save as Excel
filename = f"monthly_summary_{datetime.now().strftime('%B_%Y')}.xlsx"
summary.to_excel(filename, index=False)
print(f"✅ Saved summary as {filename}")
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_reports ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
