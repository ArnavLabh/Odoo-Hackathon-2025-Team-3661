#!/usr/bin/env python3
"""Test public_profile route"""

def test_public_profile_route():
    print("🧪 Testing Public Profile Route")
    print("=" * 40)
    
    try:
        from app import create_app
        from models import User, db
        
        app = create_app()
        
        with app.app_context():
            # Check if route is registered
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            public_profile_routes = [r for r in routes if 'public_profile' in r]
            
            print(f"Public profile routes found: {len(public_profile_routes)}")
            for route in public_profile_routes:
                print(f"  {route}")
            
            # Check users in database
            users = User.query.all()
            print(f"Total users in database: {len(users)}")
            
            if users:
                print(f"User IDs: {[u.id for u in users[:5]]}")
                
                # Test with first user
                test_user = users[0]
                print(f"Testing with user ID: {test_user.id}")
                
                with app.test_client() as client:
                    response = client.get(f'/public_profile/{test_user.id}')
                    print(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("✅ Public profile route works!")
                    elif response.status_code == 404:
                        print("❌ Route returns 404")
                    else:
                        print(f"❌ Unexpected status: {response.status_code}")
            else:
                print("No users found - creating test user...")
                
                # Create a test user
                test_user = User(
                    name="Test User",
                    email="test@example.com", 
                    is_public=True
                )
                db.session.add(test_user)
                db.session.commit()
                
                print(f"Created test user with ID: {test_user.id}")
                
                with app.test_client() as client:
                    response = client.get(f'/public_profile/{test_user.id}')
                    print(f"Response status: {response.status_code}")
                    
            # Test with non-existent user
            with app.test_client() as client:
                response = client.get('/public_profile/99999')
                print(f"Non-existent user (99999) status: {response.status_code}")
                
        print("\n🎉 Route testing completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_public_profile_route()
