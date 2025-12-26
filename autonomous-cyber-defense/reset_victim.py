import os


VULNERABLE_CODE = """from flask import Flask, request, redirect, render_template_string
import sqlite3
import os
import subprocess

app = Flask(__name__)
DB_NAME = "bank.db"

LOGIN_HTML = \"\"\"
<html><body>
    <h2>🔐 Login to CyberBank</h2>
    <form method="GET" action="/login_check">
        User: <input type="text" name="username"><br>
        Pass: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
</body></html>
\"\"\"

ADMIN_HTML = \"\"\"
<html><body>
    <h2>🛠️ Admin Panel</h2>
    <form method="GET" action="/admin/ping">
        IP: <input type="text" name="ip"><input type="submit" value="Scan">
    </form>
    <h3>Tickets</h3> {tickets}
</body></html>
\"\"\"

@app.route('/')
def home():
    return LOGIN_HTML


@app.route('/login_check')
def login_check():
    username = request.args.get('username')
    password = request.args.get('password')
    

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # BAD CODE
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return f"<h1>Welcome, {user[1]}!</h1> Balance: ${user[3]} <br> <a href='/admin'>Go to Admin</a>"
        else:
            return "Login Failed"
    except Exception as e:
        return f"Database Error: {e}"

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM tickets")
    rows = cursor.fetchall()
    conn.close()
    tickets_html = "<ul>" + "".join([f"<li>{row[0]}</li>" for row in rows]) + "</ul>"
    return render_template_string(ADMIN_HTML.format(tickets=tickets_html))

@app.route('/admin/ping')
def ping():
    ip = request.args.get('ip')
    if not ip: return "No IP"
    
    cmd = f"ping -c 1 {ip}"
    try:
        return os.popen(cmd).read()
    except Exception as e:
        return str(e)

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    content = request.form.get('content')
    conn = sqlite3.connect(DB_NAME)
    conn.cursor().execute("INSERT INTO tickets (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""

def reset():
    print("🔄 RESETTING VICTIM TO SUPER VULNERABLE STATE (NO WAF)...")
    with open("victim/app.py", "w") as f:
        f.write(VULNERABLE_CODE)
    print("✅ Victim is broken.")

if __name__ == "__main__":
    reset()
