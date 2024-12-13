import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    return conn

db_connection = init_db()

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # Vulnerable query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor = db_connection.cursor()
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return "Login successful!"
    return "Invalid credentials!"

if __name__ == '__main__':
    app.run(debug=True)

