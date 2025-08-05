from flask import Flask, request, redirect
import requests
import re

app = Flask(__name__)

BLOCKED_KEYWORDS = ["127.0.0.1", "localhost", "0.0.0.0"]

@app.route('/')
def home():
    return '''
        <h2>SSRF Challenge: Peek Inside</h2>
        <p>Try accessing an internal-only page using the URL preview tool!</p>
        <form method="GET" action="/preview">
            <input type="text" name="url" size="50" placeholder="http://example.com"/><br><br>
            <input type="submit" value="Preview">
        </form>
    '''

@app.route('/preview')
def preview():
    url = request.args.get("url")

    if not url:
        return "No URL provided", 400

    for keyword in BLOCKED_KEYWORDS:
        if keyword in url:
            return "Access Denied! Internal URLs are blocked.", 403

    try:
        resp = requests.get(url, timeout=3)
        return f"<h4>Preview Output:</h4><pre>{resp.text}</pre>"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

@app.route('/internal/admin')
def internal_admin():
    return "Internal Admin Only! Flag: FLAG{ssrf_preview_succeeded}"
