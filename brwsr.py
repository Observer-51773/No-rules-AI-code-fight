#!/usr/bin/env python3
"""
brwsr.py - Minimal Flask "code share" platform (ASCII/2D-styled UI)
Run: python brwsr.py
Visit: http://127.0.0.1:5000
"""
from datetime import datetime
import os
import re
import shlex
import sqlite3
import subprocess
import sys
from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from markupsafe import Markup
from werkzeug.security import check_password_hash, generate_password_hash

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "platform.db")
SECRET_KEY = os.environ.get("PLATFORM_SECRET_KEY", "change-this-secret-in-prod")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = SECRET_KEY

SENSITIVE_WORDS = [
    "password", "ssn", "credit card", "cvv", "private_key",
    "exploit", "malware", "virus", "bomb", "kill", "assassin",
]

def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        language TEXT,
        code TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    db.commit()

with app.app_context():
    init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

def censor_text(text):
    def repl(match):
        return "*" * len(match.group(0))
    for word in SENSITIVE_WORDS:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", flags=re.IGNORECASE)
        text = pattern.sub(repl, text)
    return text

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = get_db()
    row = db.execute("SELECT id, username FROM users WHERE id = ?", (uid,)).fetchone()
    return row

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Please provide both username and password.", "error")
            return redirect(url_for("index"))
        db = get_db()
        existing = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            if check_password_hash(existing["password_hash"], password):
                session["user_id"] = existing["id"]
                flash("Login successful.", "ok")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid password.", "error")
                return redirect(url_for("index"))
        else:
            phash = generate_password_hash(password)
            now = datetime.utcnow().isoformat()
            cur = db.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)", (username, phash, now))
            db.commit()
            session["user_id"] = cur.lastrowid
            flash("Account created and logged in.", "ok")
            return redirect(url_for("dashboard"))
    return render_template("index.html", user=current_user())

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user = current_user()
    db = get_db()
    if request.method == "POST":
        if not user:
            flash("Please login to publish code.", "error")
            return redirect(url_for("index"))
            
        title = request.form.get("title", "").strip() or "untitled"
        language = request.form.get("language", "").strip() or "txt"
        code = request.form.get("code", "").rstrip()
        if not code:
            flash("Cannot submit empty code.", "error")
            return redirect(url_for("dashboard"))
        
        db.execute("INSERT INTO posts (user_id, title, language, code, created_at) VALUES (?, ?, ?, ?, ?)",
                   (user["id"], censor_text(title), censor_text(language), censor_text(code), datetime.utcnow().isoformat()))
        db.commit()
        flash("Code published and queued for AI dataset training!", "ok")
        return redirect(url_for("dashboard"))

    posts = db.execute("""
        SELECT p.id,p.title,p.language,p.code,p.created_at,u.username
        FROM posts p JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT 100
    """).fetchall()
    return render_template("dashboard.html", user=user, posts=posts)

@app.route("/user/<username>")
def user_posts(username):
    db = get_db()
    user_row = db.execute("SELECT id, username, created_at FROM users WHERE username = ?", (username,)).fetchone()
    if not user_row:
        flash("User not found", "error")
        return redirect(url_for("index")) 
    posts = db.execute("SELECT p.id, p.title, p.language, p.code, p.created_at, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.user_id = ? ORDER BY p.created_at DESC", (user_row["id"],)).fetchall()
    return render_template("user_posts.html", profile=user_row, posts=posts, user=current_user())

@app.route("/save-code", methods=["POST"])
def save_code():
    user = current_user()
    data = request.get_json(silent=True) or request.form
    code_content = data.get("code", "").strip()
    title = data.get("title", "Dataset Code Submission").strip()
    language = data.get("language", "python").strip()

    if not code_content:
        return jsonify({"ok": False, "msg": "Code is empty"}), 400

    db = get_db()
    user_id = user["id"] if user else 1
    db.execute("INSERT INTO posts (user_id, title, language, code, created_at) VALUES (?, ?, ?, ?, ?)",
               (user_id, censor_text(title), censor_text(language), censor_text(code_content), datetime.utcnow().isoformat()))
    db.commit()
    return jsonify({"ok": True, "msg": "Code successfully ingested into training dataset!"})

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "ok")
    return redirect(url_for("index"))

@app.route("/open-game", methods=["GET", "POST"])
def open_game():
    try:
        python_exec = shlex.quote(sys.executable)
        cmd = f"{python_exec} ai_arena.py"
        subprocess.Popen(shlex.split(cmd), cwd=APP_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"ok": True, "msg": "AI Arena launched successfully."}), 200
    except Exception as e:
        return jsonify({"ok": False, "msg": f"Failed to start game: {str(e)}"}), 500

@app.template_filter("pre")
def pre_filter(s):
    if s is None:
        return ""
    return Markup("<pre class='code-block'>") + Markup.escape(s) + Markup("</pre>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

