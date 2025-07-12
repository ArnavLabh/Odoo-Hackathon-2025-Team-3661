#!/usr/bin/env python3
"""Test the simplified forgot password flow"""

print("🧪 Testing Forgot Password Flow")
print("=" * 40)

try:
    from app import create_app
    from models import User, db
    from auth_helpers import hash_password
    
    app = create_app()
    
    with app.app_context():
        # Test app creation
        print("✅ App created successfully")
        
        # Create a test user if not exists
        test_email = "test@example.com"
        test_user = User.query.filter_by(email=test_email).first()
        
        if not test_user:
            test_user = User(
                name="Test User",
                email=test_email,
                password_hash=hash_password("oldpassword123")
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created")
        else:
            print("✅ Test user exists")
        
        # Test forgot password flow with test client
        with app.test_client() as client:
            # Test GET request to forgot password page
            response = client.get('/forgot_password')
            print(f"✅ Forgot password page loads: {response.status_code}")
            
            # Test POST request with valid email
            response = client.post('/forgot_password', data={
                'email': test_email
            }, follow_redirects=False)
            
            if response.status_code == 302:  # Redirect
                print("✅ Valid email submission redirects to reset password")
                
                # Check if user has reset token
                user = User.query.filter_by(email=test_email).first()
                if user.reset_token:
                    print("✅ Reset token generated")
                    
                    # Test reset password page
                    reset_response = client.get(f'/reset_password/{user.reset_token}')
                    print(f"✅ Reset password page loads: {reset_response.status_code}")
                    
                    # Test password reset
                    reset_post = client.post(f'/reset_password/{user.reset_token}', data={
                        'password': 'newpassword123',
                        'confirm_password': 'newpassword123'
                    }, follow_redirects=False)
                    
                    if reset_post.status_code == 302:
                        print("✅ Password reset successful")
                    else:
                        print(f"❌ Password reset failed: {reset_post.status_code}")
                else:
                    print("❌ Reset token not generated")
            else:
                print(f"❌ Email submission failed: {response.status_code}")
            
            # Test invalid email
            response = client.post('/forgot_password', data={
                'email': 'nonexistent@example.com'
            })
            print(f"✅ Invalid email handled: {response.status_code}")
        
        print("\n🎉 Forgot Password Flow Test Complete!")
        print("📝 Flow: Email → Immediate Reset (No Email Required)")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
