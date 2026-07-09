from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nyxis.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, username, email, is_admin, is_banned, created_at FROM users ORDER BY created_at DESC')
    users = c.fetchall()
    conn.close()

    return jsonify({
        'users': [{
            'id': u['id'],
            'username': u['username'],
            'email': u['email'],
            'is_admin': u['is_admin'] == 1,
            'is_banned': u['is_banned'] == 1,
            'created_at': u['created_at']
        } for u in users]
    })

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    action = data.get('action')

    conn = get_db()
    c = conn.cursor()

    if action == 'ban':
        c.execute('UPDATE users SET is_banned = 1 WHERE id = ?', (user_id,))
    elif action == 'unban':
        c.execute('UPDATE users SET is_banned = 0 WHERE id = ?', (user_id,))
    elif action == 'delete':
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()

    return jsonify({'success': True})