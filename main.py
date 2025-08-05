from flask import Flask, request, redirect

app = Flask(__name__)

FLAG = "FLAG{proxy_header_admin_bypass_success}"

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").lower()
        if username == "admin":
            return redirect("/admin-login")
        else:
            return f"Welcome, {username}. You're not admin. No flag for you."
    return '''
        <h2>Login</h2>
        <form method="POST">
            Username: <input type="text" name="username">
            <button type="submit">Login</button>
        </form>
    '''

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        passcode = request.form.get("passcode", "")
        if passcode != "LetMeIn123":
            return "Invalid passcode. Access denied."
        return redirect("/admin")
    return '''
        <h2>Admin Login</h2>
        <form method="POST">
            Passcode: <input type="password" name="passcode">
            <button type="submit">Login</button>
        </form>
    '''

@app.route("/admin")
def admin():
    # Trust boundary flaw: IP spoof via header
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip == "127.0.0.1":
        return f"<h3>Welcome, Admin!</h3><p>Flag: {FLAG}</p>"
    return "403 Forbidden – You must be internal admin."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
