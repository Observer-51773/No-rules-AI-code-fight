ASCII Code Share Platform (Flask MVP)
-------------------------------------

Files added:
- platform.py
- requirements.txt
- templates/*.html
- static/style.css
- platform.db (created at first run)

Quick start (local)
1. Create a Python venv and activate it:
   python3 -m venv venv
   source venv/bin/activate   # windows: venv\Scripts\activate

2. Install deps:
   pip install -r requirements.txt

3. (Optional) set a secret key for sessions:
   export PLATFORM_SECRET_KEY="a_long_random_value"

4. Run the server:
   python platform.py

5. Open http://127.0.0.1:5000 in your browser.

Launch Game feature
- The Launch Game page (link in header) opens /launch-game. If you enable the /open-game endpoint the Launch Game button will POST /open-game and the server will attempt to run `python ai_arena.py` in the repo root.
- WARNING: the server-side open-game action spawns a process on the server. Only enable and use that on your local trusted machine.

Security notes:
- Passwords are hashed with Werkzeug.
- This is an example MVP — not production hardened (no CSRF tokens, no HTTPS enforcement, debug mode is on).
- Censorship is a simple blacklist: edit SENSITIVE_WORDS in platform.py to adjust.