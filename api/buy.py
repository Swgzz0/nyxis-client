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

@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.json
    user_id = data.get('user_id')
    plan = data.get('plan')

    durations = {'weekly': 7, 'monthly': 30, 'lifetime': 3650}
    days = durations.get(plan, 30)
    end_date = (datetime.now() + timedelta(days=days)).isoformat()
    key = generate_key()

    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO subscriptions (user_id, key, plan, end_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, key, plan, end_date))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'key': key, 'plan': plan, 'end_date': end_date})