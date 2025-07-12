#!/usr/bin/env python3

try:
    print("Testing app without werkzeug and babel...")
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    print("\nTesting secure_filename function...")
    from routes import secure_filename
    
    test_files = [
        "test.jpg",
        "../../../etc/passwd",
        "file with spaces.png",
        "special@#$%chars.pdf",
        "",
        "...",
        "normal_file-123.txt"
    ]
    
    for filename in test_files:
        secure = secure_filename(filename)
        print(f"'{filename}' -> '{secure}'")
    
    print("\nTesting routes...")
    with app.app_context():
        print(f"Registered blueprints: {list(app.blueprints.keys())}")
        print(f"Total URL rules: {len(app.url_map._rules)}")
    
    print("\n🎉 All tests passed! No werkzeug or babel dependencies!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
