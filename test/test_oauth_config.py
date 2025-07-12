#!/usr/bin/env python3
"""Test Google OAuth configuration without external requests"""

def test_oauth_config():
    print("🔍 Testing Google OAuth Configuration")
    print("=" * 50)
    
    try:
        from app import create_app
        app = create_app()
        
        with app.app_context():
            # Check configuration
            client_id = app.config.get('GOOGLE_CLIENT_ID')
            client_secret = app.config.get('GOOGLE_CLIENT_SECRET')
            
            print(f"Client ID configured: {'Yes' if client_id else 'No'}")
            print(f"Client Secret configured: {'Yes' if client_secret else 'No'}")
            
            if client_id and client_secret:
                print("✅ Google OAuth credentials are configured")
                
                # Test OAuth client registration
                from google_auth import oauth
                if hasattr(oauth, 'google'):
                    print("✅ Google OAuth client registered")
                else:
                    print("❌ Google OAuth client not registered")
                    
                # Test route access (without external calls)
                with app.test_client() as client:
                    # Test if route exists
                    response = client.get('/login/google', follow_redirects=False)
                    if response.status_code in [302, 200]:  # Redirect or OK
                        print("✅ Google login route is accessible")
                    else:
                        print(f"❌ Google login route error: {response.status_code}")
                        
            else:
                print("⚠️ Google OAuth credentials not configured")
                print("📝 To enable Google OAuth:")
                print("   1. Go to Google Cloud Console")
                print("   2. Create OAuth 2.0 credentials")
                print("   3. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")
                
        print("\n🎉 OAuth configuration test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_oauth_config()
