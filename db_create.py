import sqlite3
import os

# Set the path for the database
db_path = os.path.join(os.path.dirname(__file__), 'submissions.db')

# Check if the database file exists, create it if not
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor =   conn.cursor()
    cursor.execute('''
        CREATE TABLE submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            reflections TEXT NOT NULL,
            timestamp DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()