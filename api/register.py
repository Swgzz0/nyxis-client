from flask import Flask, request, jsonify
import hashlib
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()

    if not username or not password or not email:
        return jsonify({'success': False, 'error': 'All fields required'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400

    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    if c.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Username already exists'}), 400

    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    if c.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Email already registered'}), 400

    hashed = hash_password(password)
    c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashed, email))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Account created! Please login.'})