import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    # Hardcoded credentials
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    return conn

db_connection = init_db()

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # Vulnerable query: susceptible to SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = db_connection.cursor()
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        # Reflecting user input in response (XSS vulnerability)
        return render_template_string(f"<h1>Welcome, {username}!</h1>")
    return "Invalid credentials!"

@app.route('/exec_query', methods=['POST'])
def exec_query():
    # Allowing users to run arbitrary SQL queries (Critical vulnerability)
    query = request.form.get('query')
    cursor = db_connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    # Insecure API configurations
    app.run(debug=True, host="0.0.0.0")

