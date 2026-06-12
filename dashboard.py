from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def fetch_replies():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, subject, date, message FROM replies ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    data = fetch_replies()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
