from flask import request, jsonify
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def register_routes(app):
    @app.route('/api/keys/<int:user_id>', methods=['GET'])
    def get_keys(user_id):
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT key, plan, start_date, end_date, status FROM subscriptions WHERE user_id = ? ORDER BY start_date DESC', (user_id,))
        keys = c.fetchall()
        conn.close()

        return jsonify({
            'keys': [{
                'key': k['key'],
                'plan': k['plan'],
                'start_date': k['start_date'],
                'end_date': k['end_date'],
                'status': k['status']
            } for k in keys]
        })