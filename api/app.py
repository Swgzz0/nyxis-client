from flask import Flask, send_file, jsonify
import os
import sys

app = Flask(__name__)

# ========== SIMPLE FILE SERVING - WORKS 100% ==========
@app.route('/')
def serve_index():
    """Serve the main index.html file from the ROOT folder"""
    try:
        # Get the root directory (where index.html actually lives)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Try different possible locations for index.html
        possible_files = [
            os.path.join(root_dir, 'index.html'),
            os.path.join(root_dir, 'INDEX.HTML'),
            os.path.join(os.getcwd(), 'index.html'),
            os.path.join(os.getcwd(), 'INDEX.HTML'),
            '/vercel/path0/index.html',
            '/vercel/path0/INDEX.HTML',
            '/var/task/index.html',
            '/var/task/INDEX.HTML',
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"✅ Found file: {file_path}")
                return send_file(file_path)
        
        # If no file found, show debug info
        files = os.listdir(os.getcwd())
        return jsonify({
            'error': 'index.html not found',
            'current_directory': os.getcwd(),
            'files': files,
            'root_directory': root_dir,
            'root_files': os.listdir(root_dir) if os.path.exists(root_dir) else []
        }), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files from the ROOT folder"""
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Try different possible locations
        possible_files = [
            os.path.join(root_dir, path),
            os.path.join(root_dir, path.upper()),
            os.path.join(root_dir, path.lower()),
            os.path.join(os.getcwd(), path),
            os.path.join('/vercel/path0', path),
            os.path.join('/var/task', path),
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                return send_file(file_path)
        
        return jsonify({'error': f'File not found: {path}'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== API ROUTES ==========
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'online', 'message': 'Nyxis API is running!'})

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

# ========== REGISTER YOUR OTHER API ROUTES ==========
try:
    from api import login, register, admin, buy, activate, keys, stats, logs, generate_key
    
    route_modules = [login, register, admin, buy, activate, keys, stats, logs, generate_key]
    for module in route_modules:
        if hasattr(module, 'register_routes'):
            module.register_routes(app)
            print(f"✅ Loaded: {module.__name__}")
except Exception as e:
    print(f"⚠️ Error loading API routes: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)