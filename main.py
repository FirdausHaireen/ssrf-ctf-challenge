
from flask import Flask, request, redirect, make_response, render_template_string

app = Flask(__name__)

FLAG = "FLAG{logic_flaw_bypass_success}"

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
        # No real validation - logic flaw!
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
    is_admin = request.cookies.get("is_admin", "false")
    if is_admin == "true":
        return f"<h3>Welcome, Admin!</h3><p>Flag: {FLAG}</p>"
    return "403 Forbidden – You're not an admin."

@app.route("/set-admin")
def set_admin_cookie():
    resp = make_response("Admin cookie set! Now visit /admin")
    resp.set_cookie("is_admin", "true")
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
