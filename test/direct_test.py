import os
import sys

# Set working directory
os.chdir(r'C:\Arnav\Coding\Odoo-Hackathon-2025\Odoo-Hackathon-2025-Team-3661')

try:
    from app import create_app
    from models import User, db
    from auth_helpers import hash_password
    
    print("Creating Flask app...")
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if test user exists
        test_user = User.query.filter_by(email='test@test.com').first()
        if not test_user:
            print("Creating test user...")
            test_user = User(
                name='Test User',
                email='test@test.com',
                password_hash=hash_password('test123'),
                is_public=True,
                bio='Test user for debugging'
            )
            db.session.add(test_user)
            db.session.commit()
        
        print(f"Test user exists with ID: {test_user.id}")
        
        # Test the route
        print("Testing public_profile route...")
        with app.test_client() as client:
            response = client.get(f'/public_profile/{test_user.id}')
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ Route works! Page loaded successfully.")
            elif response.status_code == 404:
                print("✗ 404 Error - Route not found")
                print("Available routes:")
                for rule in app.url_map.iter_rules():
                    if 'profile' in rule.rule.lower():
                        print(f"  {rule.rule} -> {rule.endpoint}")
            else:
                print(f"Response data: {response.data.decode()[:500]}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
