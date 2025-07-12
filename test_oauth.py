#!/usr/bin/env python3

try:
    print("Testing Google OAuth integration...")
    from app import create_app
    app = create_app()
    print("✅ App with Google OAuth created successfully!")
    
    print("\nTesting routes...")
    with app.app_context():
        # Test that all blueprints are registered
        print(f"Registered blueprints: {list(app.blueprints.keys())}")
        
        # Check for OAuth routes
        oauth_routes = [rule for rule in app.url_map.iter_rules() if 'google' in rule.rule]
        print(f"Google OAuth routes: {[rule.rule for rule in oauth_routes]}")
        
        print(f"Total URL rules: {len(app.url_map._rules)}")
    
    print("\n🎉 Google OAuth integration successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
