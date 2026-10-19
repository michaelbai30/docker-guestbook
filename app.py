import html
import json
import os
import socket
from datetime import datetime

import redis
from flask import Flask, redirect, request

app = Flask(__name__)
db = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379, decode_responses=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip() or "Anonymous"
        message = request.form.get("message", "").strip()
        if message:
            entry = {"name": name, "message": message, "time": datetime.now().strftime("%b %d, %I:%M %p")}
            db.lpush("messages", json.dumps(entry))
        return redirect("/")

    visits = db.incr("visits")
    entries = [json.loads(m) for m in db.lrange("messages", 0, 49)]
    items = "".join(
        f"<li><b>{html.escape(e['name'])}</b> <small>{e['time']}</small><br>{html.escape(e['message'])}</li>"
        for e in entries
    ) or "<li>No messages yet. Be the first!</li>"

    return f"""
    <html><head><title>Docker Guestbook</title>
    <style>
      body {{ font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px; }}
      input, textarea {{ width: 100%; padding: 8px; margin: 4px 0; box-sizing: border-box; }}
      button {{ padding: 8px 16px; }}
      li {{ margin-bottom: 12px; }}
      small {{ color: gray; }}
    </style></head>
    <body>
      <h1>Docker Guestbook</h1>
      <p>Page visits: {visits} &middot; Served by container <code>{socket.gethostname()}</code></p>
      <form method="post">
        <input name="name" placeholder="Your name">
        <textarea name="message" placeholder="Leave a message" required></textarea>
        <button type="submit">Sign the guestbook</button>
      </form>
      <h2>Messages</h2>
      <ul>{items}</ul>
    </body></html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.environ.get("FLASK_DEBUG") == "1")