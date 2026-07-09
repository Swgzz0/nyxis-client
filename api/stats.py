from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM subscriptions WHERE status = "active"')
    active_subs = c.fetchone()[0]

    conn.close()

    return jsonify({
        'total_users': total_users,
        'active_subscriptions': active_subs
    })