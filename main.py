from flask import Flask, request, abort
import requests
import re

app = Flask(__name__)

# SSRF filter: deny common internal IPs
BLOCKED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0"
]

def is_blocked(url):
    for host in BLOCKED_HOSTS:
        if host in url:
            return True
    return False

@app.route("/")
def index():
    return '''
    <h2>🕵️ SSRF Challenge - Level 2</h2>
    <p>Enter a URL to fetch:</p>
    <form method="POST" action="/fetch">
        <input name="url" style="width:300px"/>
        <button type="submit">Fetch</button>
    </form>
    '''

@app.route("/fetch", methods=["POST"])
def fetch():
    url = request.form.get("url")

    # Simple filtering to block common localhost references
    if is_blocked(url.lower()):
        return "❌ Access to that host is blocked."

    try:
        res = requests.get(url, timeout=3)
        return f"<pre>{res.text}</pre>"
    except Exception as e:
        return f"<b>Error:</b> {e}"

# Internal endpoint, only accessible via SSRF with token
@app.route("/internal")
def internal():
    token = request.headers.get("X-Secret-Token")
    if token == "SSRF-MASTER":
        return "🎉 FLAG{bypass_success_and_secret_token}"
    return abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
