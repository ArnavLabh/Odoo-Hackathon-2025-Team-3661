#!/usr/bin/env python3
"""
Test script to verify Vercel deployment setup locally
"""

def test_vercel_deployment():
    print("🚀 Testing Vercel Deployment Setup")
    print("=" * 50)
    
    try:
        # Test 1: Import the API entry point
        print("1. Testing API entry point...")
        from api.index import app
        print("   ✅ API module imports successfully")
        
        # Test 2: Test app creation
        print("2. Testing Flask app...")
        with app.app_context():
            print("   ✅ Flask app context works")
            
        # Test 3: Test routes
        print("3. Testing routes...")
        with app.test_client() as client:
            # Test health check
            response = client.get('/health')
            if response.status_code == 200:
                print("   ✅ Health check works")
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
                
            # Test home page
            response = client.get('/')
            if response.status_code in [200, 302]:  # 302 for redirects
                print("   ✅ Home page responds")
            else:
                print(f"   ❌ Home page failed: {response.status_code}")
                
        # Test 4: Configuration
        print("4. Testing configuration...")
        config_ok = True
        if not app.config.get('SECRET_KEY'):
            print("   ⚠️ SECRET_KEY not set")
            config_ok = False
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            print("   ⚠️ DATABASE_URI not set")
            config_ok = False
            
        if config_ok:
            print("   ✅ Configuration looks good")
            
        print("\n🎉 Vercel deployment test completed!")
        print("📋 Next steps:")
        print("   1. git add .")
        print("   2. git commit -m 'Fix Vercel deployment'")
        print("   3. git push")
        print("   4. Check Vercel dashboard for deployment status")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check that all files are in correct locations")
        print("   2. Verify requirements.txt is complete")
        print("   3. Check for import errors")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_vercel_deployment()
