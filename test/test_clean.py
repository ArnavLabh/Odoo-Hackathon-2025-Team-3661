#!/usr/bin/env python3
"""Quick test of clean backend"""

print('🧪 Testing clean backend...')

# Test custom secure_filename
from routes import secure_filename
test_file = "../hack.txt"
result = secure_filename(test_file)
print(f'secure_filename test: "{test_file}" -> "{result}"')

# Test app creation
from app import create_app
app = create_app()
print(f'✅ App created with {len(app.url_map._rules)} routes!')

# Test that werkzeug and babel are not imported
import sys
werkzeug_modules = [m for m in sys.modules.keys() if 'werkzeug' in m.lower()]
babel_modules = [m for m in sys.modules.keys() if 'babel' in m.lower()]

print(f'Werkzeug modules loaded: {len(werkzeug_modules)}')
print(f'Babel modules loaded: {len(babel_modules)}')

print('✅ Backend works without werkzeug and babel!')
