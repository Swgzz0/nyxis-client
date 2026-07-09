from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/activate', methods=['POST'])
def activate():
    data = request.json
    key = data.get('key')
    user_id = data.get('user_id')

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM subscriptions WHERE key = ?', (key,))
    sub = c.fetchone()

    if not sub:
        conn.close()
        return jsonify({'success': False, 'error': 'Invalid key'}), 404

    if sub['user_id'] != user_id:
        conn.close()
        return jsonify({'success': False, 'error': 'Key does not belong to this user'}), 403

    if datetime.fromisoformat(sub['end_date']) < datetime.now():
        return jsonify({'success': False, 'error': 'Key expired'}), 400

    conn.close()
    return jsonify({'success': True, 'message': 'Key activated!'})