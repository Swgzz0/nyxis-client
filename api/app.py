from flask import Flask, send_from_directory, jsonify
import importlib
import os

app = Flask(__name__)

# Get the root directory (one level up from api folder)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== SERVE HTML PAGES ==========
@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    try:
        return send_from_directory(ROOT_DIR, 'index.html')
    except Exception as e:
        return f"Error serving index.html: {e}"

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files"""
    try:
        return send_from_directory(ROOT_DIR, path)
    except Exception as e:
        return jsonify({'error': f'File not found: {path}', 'details': str(e)}), 404

# ========== API HEALTH CHECK ==========
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'online', 'message': 'Nyxis API is running!'})

# ========== REGISTER ALL API ROUTES ==========
route_files = [
    'activate', 'admin', 'buy', 'generate_key',
    'keys', 'login', 'logs', 'register', 'stats'
]

for file in route_files:
    try:
        module = importlib.import_module(f'api.{file}')
        if hasattr(module, 'register_routes'):
            module.register_routes(app)
            print(f"✅ Loaded: {file}")
    except Exception as e:
        print(f"❌ Failed to load {file}: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)