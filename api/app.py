from flask import Flask, send_file, jsonify, send_from_directory
import os
import sys

app = Flask(__name__)

# ========== SIMPLE FILE SERVING ==========
@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    try:
        # Try different possible locations
        locations = [
            'index.html',
            'INDEX.HTML',
            os.path.join(os.getcwd(), 'index.html'),
            os.path.join(os.getcwd(), 'INDEX.HTML'),
            '/vercel/path0/index.html',
            '/var/task/index.html',
        ]
        
        for loc in locations:
            if os.path.exists(loc):
                print(f"✅ Found file at: {loc}")
                return send_file(loc)
        
        # If no file found, list what's there
        files = os.listdir(os.getcwd())
        return jsonify({
            'error': 'No index.html found',
            'files': files,
            'cwd': os.getcwd()
        }), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files"""
    try:
        # Try different locations
        locations = [
            path,
            path.upper(),
            path.lower(),
            os.path.join(os.getcwd(), path),
            '/vercel/path0/' + path,
            '/var/task/' + path,
        ]
        
        for loc in locations:
            if os.path.exists(loc):
                return send_file(loc)
        
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
    
    # Register each route file if it has the function
    route_modules = [login, register, admin, buy, activate, keys, stats, logs, generate_key]
    for module in route_modules:
        if hasattr(module, 'register_routes'):
            module.register_routes(app)
            print(f"✅ Loaded: {module.__name__}")
except Exception as e:
    print(f"⚠️ Error loading API routes: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)