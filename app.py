from flask import Flask, request, abort
import sqlite3
import os
import hmac

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("messages.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return """
    <h1>My Website</h1>
    <form method="POST" action="/submit">
        <input name="name" placeholder="Your Name" required>
        <br><br>
        <textarea name="message"
        placeholder="Your Message" required></textarea>
        <br><br>
        <button type="submit">Submit</button>
    </form>
    """

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not message:
        abort(400)

    conn = sqlite3.connect("messages.db")
    conn.execute(
        "INSERT INTO messages (name, message) VALUES (?, ?)",
        (name, message)
    )
    conn.commit()
    conn.close()

    return "Thank you! Message saved successfully."

@app.route("/messages")
def messages():
    password = os.environ.get("MESSAGES_PASSWORD")
    auth = request.authorization

    if not password:
        abort(503)

    if not auth or not hmac.compare_digest(
        auth.password or "", password
    ):
        return abort(401)

    conn = sqlite3.connect("messages.db")
    data = conn.execute(
        "SELECT name, message FROM messages ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return "<h1>Messages</h1>" + "".join(
        f"<h3>{name}</h3><p>{message}</p><hr>"
        for name, message in data
    )

if __name__ == "__main__":
    app.run()
