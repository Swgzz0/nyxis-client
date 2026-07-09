from flask import Flask, request, jsonify
import sqlite3
import secrets
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_key():
    return f"NYX-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"

@app.route('/api/generate-key', methods=['POST'])
def generate_key_route():
    data = request.json
    username = data.get('username')
    plan = data.get('plan')

    if not username:
        return jsonify({'success': False, 'error': 'Username required'}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if not user:
        conn.close()
        return jsonify({'success': False, 'error': 'User not found'}), 404

    durations = {'weekly': 7, 'monthly': 30, 'lifetime': 3650}
    days = durations.get(plan, 30)
    end_date = (datetime.now() + timedelta(days=days)).isoformat()

    key = generate_key()

    c.execute('''
        INSERT INTO subscriptions (user_id, key, plan, end_date)
        VALUES (?, ?, ?, ?)
    ''', (user['id'], key, plan, end_date))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'key': key, 'plan': plan, 'username': username})