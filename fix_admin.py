#!/usr/bin/env python3
from app import create_app
from models import User, db
from auth_helpers import hash_password, check_password

app = create_app()

with app.app_context():
    # Find the admin user
    admin_user = User.query.filter_by(email="admin@skillswap.com").first()
    
    if admin_user:
        print(f"Found admin user: {admin_user.name} ({admin_user.email})")
        print(f"Current password hash: {admin_user.password_hash[:50]}...")
        
        # Create a new bcrypt hash
        new_password = "admin123"
        new_hash = hash_password(new_password)
        
        print(f"New password hash: {new_hash[:50]}...")
        
        # Update the admin user
        admin_user.password_hash = new_hash
        db.session.commit()
        
        print("✅ Admin password updated successfully!")
        
        # Test the new password
        if check_password(new_password, new_hash):
            print("✅ Password verification works!")
        else:
            print("❌ Password verification failed!")
            
    else:
        print("Admin user not found, creating new one...")
        new_hash = hash_password("admin123")
        admin_user = User(
            name="Admin",
            email="admin@skillswap.com", 
            password_hash=new_hash,
            is_admin=True,
            is_public=False
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ New admin user created!")
    
    print(f"\nTo login:")
    print(f"Email: admin@skillswap.com")
    print(f"Password: admin123")
