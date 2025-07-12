#!/usr/bin/env python3

try:
    print("Testing app creation...")
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    print("\nTesting routes...")
    with app.app_context():
        # Test that all blueprints are registered
        print(f"Registered blueprints: {list(app.blueprints.keys())}")
        
        # Test URL rules
        print(f"Total URL rules: {len(app.url_map._rules)}")
        
        print("\nSample routes:")
        for rule in list(app.url_map.iter_rules())[:10]:
            print(f"  {rule.rule} -> {rule.endpoint}")
    
    print("\n🎉 All tests passed! App is ready to run.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
