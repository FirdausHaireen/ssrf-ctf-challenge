from flask import Flask, request, redirect

app = Flask(__name__)

FLAG = "pkb{be_the_admin}"

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
    bypass_key = request.headers.get("X-Internal-Bypass")
    if bypass_key == "127.0.0.1":
        return f"<h3>Welcome, Admin!</h3><p>Flag: {FLAG}</p>"
    return "403 Forbidden – You must be internal admin."

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /dev-notes", 200, {"Content-Type": "text/plain"}

@app.route("/dev-notes")
def dev_notes():
    return '''
        <h2>Internal Dev Notes</h2>
        <p>Temporary admin passcode for testing: <code>LetMeIn123</code></p>
        #don't forget to use X-Internal-Bypass to access the admin page
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)



