from flask import request, jsonify
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def register_routes(app):
    @app.route('/api/logs', methods=['GET'])
    def get_logs():
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            SELECT l.id, u.username, l.action, l.ip, l.timestamp
            FROM activity_logs l
            LEFT JOIN users u ON l.user_id = u.id
            ORDER BY l.timestamp DESC
            LIMIT 50
        ''')
        logs = c.fetchall()
        conn.close()

        return jsonify({
            'logs': [{
                'id': l['id'],
                'username': l['username'] or 'System',
                'action': l['action'],
                'ip': l['ip'],
                'timestamp': l['timestamp']
            } for l in logs]
        })