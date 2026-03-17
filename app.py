import os
from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Get Neon DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Check Render environment variables!")

def get_db():
    # Connect to Neon Postgres
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        note = request.form.get("note")
        if note:
            cur.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
            conn.commit()

    cur.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cur.fetchall()  # returns list of dicts

    cur.close()
    conn.close()

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)