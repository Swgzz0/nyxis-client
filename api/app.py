from flask import Flask, send_from_directory, jsonify
import importlib
import os

app = Flask(__name__)

# ========== SERVE HTML PAGES - VERCEL COMPATIBLE ==========
@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    try:
        # Try multiple possible paths for Vercel
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html'),
            os.path.join(os.getcwd(), 'index.html'),
            os.path.join('/vercel/path0', 'index.html'),
            'index.html'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return send_from_directory(os.path.dirname(path), 'index.html')
        
        # If none found, list files for debugging
        files = os.listdir(os.getcwd())
        return jsonify({
            'error': 'index.html not found',
            'current_dir': os.getcwd(),
            'files': files[:20]  # Show first 20 files
        }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files"""
    try:
        # Try multiple possible paths
        possible_dirs = [
            os.path.dirname(os.path.dirname(__file__)),
            os.getcwd(),
            '/vercel/path0'
        ]
        
        for dir_path in possible_dirs:
            file_path = os.path.join(dir_path, path)
            if os.path.exists(file_path):
                return send_from_directory(dir_path, path)
        
        return jsonify({'error': f'File not found: {path}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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