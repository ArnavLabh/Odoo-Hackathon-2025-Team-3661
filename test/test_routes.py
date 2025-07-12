#!/usr/bin/env python3

try:
    # Test if routes file can be imported without errors
    print("Testing routes import...")
    from routes import main
    print(f"✓ Routes imported successfully. Blueprint name: {main.name}")
    
    # Test if app can be created
    print("Testing app creation...")
    from app import create_app
    app = create_app()
    print("✓ App created successfully")
    
    # Check if the public_profile route is registered
    print("Checking routes...")
    found_route = False
    for rule in app.url_map.iter_rules():
        if 'public_profile' in rule.rule:
            print(f"✓ Found route: {rule.rule} -> {rule.endpoint}")
            found_route = True
    
    if not found_route:
        print("✗ public_profile route not found!")
        print("All routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} -> {rule.endpoint}")
    
    # Test with app context
    with app.app_context():
        from models import db
        db.create_all()
        print("✓ Database tables created")
        
        # Test the route directly
        with app.test_client() as client:
            # Test with a likely non-existent user first
            response = client.get('/public_profile/999')
            print(f"Test request to /public_profile/999: Status {response.status_code}")
            
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
