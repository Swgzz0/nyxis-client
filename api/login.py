from flask import request, jsonify
import hashlib
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_routes(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'}), 400

        conn = get_db()
        c = conn.cursor()
        hashed = hash_password(password)
        c.execute('SELECT id, username, password, email, is_admin, is_banned FROM users WHERE username = ?', (username,))
        user = c.fetchone()

        if not user:
            conn.close()
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        if user['password'] != hashed:
            conn.close()
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        if user['is_banned'] == 1:
            conn.close()
            return jsonify({'success': False, 'error': 'Account banned'}), 403

        conn.close()
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'is_admin': user['is_admin'] == 1
            }
        })