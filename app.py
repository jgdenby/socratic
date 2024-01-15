from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Render the webpage with Title and Reflections text boxes
    return render_template('./index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submissions and save to the database
    title = request.form['title']
    reflections = request.form['reflections']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to the database (SQLite example)
    db_path = os.path.join(os.path.dirname(__file__), 'submissions.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO submissions (title, reflections, timestamp) VALUES (?, ?, ?)',
                   (title, reflections, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/download/<timestamp>')
def download(timestamp):
    # Retrieve content from the database and create a text file for download
    conn = sqlite3.connect('submissions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, reflections FROM submissions WHERE timestamp = ?', (timestamp,))
    result = cursor.fetchone()
    conn.close()

    if result:
        content = f"Title: {result[0]}\nReflections: {result[1]}"
        return Response(content, mimetype="text/plain", headers={"Content-Disposition": f"attachment;filename={timestamp}.txt"})
    else:
        return "Submission not found."

if __name__ == '__main__':
    app.run(debug=True)
