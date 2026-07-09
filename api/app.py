from flask import Flask, send_from_directory, jsonify
import importlib
import os

app = Flask(__name__)

# ========== SERVE HTML PAGES - CASE INSENSITIVE ==========
def find_file(filename):
    """Find a file even if the case is wrong"""
    # Try exact match first
    if os.path.exists(filename):
        return filename
    
    # Try in current directory
    if os.path.exists(os.path.join(os.getcwd(), filename)):
        return os.path.join(os.getcwd(), filename)
    
    # Try uppercase version
    if os.path.exists(filename.upper()):
        return filename.upper()
    
    # Try lowercase version
    if os.path.exists(filename.lower()):
        return filename.lower()
    
    # Try in /vercel/path0
    vercel_path = '/vercel/path0'
    if os.path.exists(os.path.join(vercel_path, filename)):
        return os.path.join(vercel_path, filename)
    
    # Check all files in current directory
    try:
        for file in os.listdir(os.getcwd()):
            if file.lower() == filename.lower():
                return os.path.join(os.getcwd(), file)
    except:
        pass
    
    return None

@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    html_file = find_file('index.html')
    if html_file:
        return send_file(html_file)
    return jsonify({'error': 'index.html not found'}), 404

@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static files"""
    file_path = find_file(path)
    if file_path:
        return send_file(file_path)
    return jsonify({'error': f'File not found: {path}'}), 404

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