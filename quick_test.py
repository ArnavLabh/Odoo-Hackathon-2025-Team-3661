#!/usr/bin/env python3
"""Quick test for public profile route issue"""

def test_route():
    print("Testing public profile route...")
    
    from app import create_app
    from models import User, db
    from auth_helpers import hash_password
    
    app = create_app()
    
    with app.app_context():
        # Create a test user if needed
        user = User.query.filter_by(id=1).first()
        if not user:
            user = User(
                name="Test User",
                email="test@example.com",
                password_hash=hash_password("test123"),
                is_public=True
            )
            db.session.add(user)
            db.session.commit()
            print(f"Created user with ID: {user.id}")
        
        # Test the route
        with app.test_client() as client:
            response = client.get(f'/public_profile/{user.id}')
            print(f"Status: {response.status_code}")
            
            if response.status_code == 404:
                print("404 - Checking route registration...")
                routes = [str(rule) for rule in app.url_map.iter_rules()]
                profile_routes = [r for r in routes if 'profile' in r]
                print("Profile routes:", profile_routes)

if __name__ == "__main__":
    test_route()
