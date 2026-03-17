from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_ok1gGMxZtK2p@ep-rapid-field-amqp1ddj-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/", methods=["GET","POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        note = request.form["note"]

        cur.execute(
            "INSERT INTO notes (content) VALUES (%s)",
            (note,)
        )
        conn.commit()

    cur.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)