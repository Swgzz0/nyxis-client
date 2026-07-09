# api/app.py
from flask import Flask
import importlib

app = Flask(__name__)

# List of all your route files
route_files = [
    'activate', 'admin', 'buy', 'generate_key',
    'keys', 'login', 'logs', 'register', 'stats'
]

# Register each route file with the main app
for file in route_files:
    try:
        module = importlib.import_module(f'api.{file}')
        if hasattr(module, 'register_routes'):
            module.register_routes(app)
        elif hasattr(module, 'app'):
            # Copy the app instance's routes if they exist
            for rule in module.app.url_map.iter_rules():
                # Add the rule from the sub-app to the main app
                app.add_url_rule(
                    rule.rule,
                    endpoint=rule.endpoint,
                    view_func=module.app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
        print(f"✅ Loaded: {file}")
    except Exception as e:
        print(f"❌ Failed to load {file}: {e}")

if __name__ == "__main__":
    app.run()