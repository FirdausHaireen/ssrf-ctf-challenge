from flask import Flask, request, abort
import requests
import socket
import re

app = Flask(__name__)

BLOCKED_IPS = [
    "127.", "0.", "169.254.", "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
    "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.",
    "172.28.", "172.29.", "172.30.", "172.31."
]

@app.route("/")
def index():
    return '''
        <h2>SSRF Challenge: The Hidden Gateway</h2>
        <form action="/preview" method="GET">
            <label>Enter a URL to fetch:</label><br>
            <input type="text" name="url" size="50" placeholder="http://example.com"/><br><br>
            <input type="submit" value="Fetch"/>
        </form>
    '''

def is_private_ip(ip):
    for blocked in BLOCKED_IPS:
        if ip.startswith(blocked):
            return True
    return False

@app.route("/preview")
def preview():
    target_url = request.args.get("url")
    if not target_url:
        return "Missing URL", 400

    try:
        # Parse domain
        match = re.match(r"^https?://([^/:]+)", target_url)
        if not match:
            return "Invalid URL", 400
        hostname = match.group(1)

        # Resolve IP
        ip = socket.gethostbyname(hostname)
        if is_private_ip(ip):
            return "Access denied: Private IPs are blocked!", 403

        # Request the URL
        r = requests.get(target_url, timeout=3)
        return f"<pre>{r.text}</pre>"
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/super-admin")
def secret_admin():
    return "Flag: FLAG{ssrf_bypass_wizard}"
