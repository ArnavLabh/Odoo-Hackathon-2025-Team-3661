#!/usr/bin/env python3
"""
Script to manually fix admin login by recreating the admin user with proper bcrypt hash
"""
import sqlite3
import bcrypt

def hash_password(password):
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

# Connect to database
conn = sqlite3.connect('instance/skillswap.db')
cursor = conn.cursor()

# Delete existing admin user if any
cursor.execute("DELETE FROM user WHERE email = 'admin@skillswap.com'")

# Create new admin user with proper bcrypt hash
admin_password = "admin123"
admin_hash = hash_password(admin_password)

cursor.execute("""
    INSERT INTO user (name, email, password_hash, is_admin, is_public, is_banned, created_at, last_login)
    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
""", ("Admin", "admin@skillswap.com", admin_hash, True, False, False))

conn.commit()

# Verify the user was created
cursor.execute("SELECT id, name, email, is_admin FROM user WHERE email = 'admin@skillswap.com'")
admin = cursor.fetchone()

if admin:
    print(f"✅ Admin user created successfully!")
    print(f"ID: {admin[0]}")
    print(f"Name: {admin[1]}")
    print(f"Email: {admin[2]}")
    print(f"Is Admin: {admin[3]}")
    print(f"\nLogin credentials:")
    print(f"Email: admin@skillswap.com")
    print(f"Password: admin123")
else:
    print("❌ Failed to create admin user")

conn.close()
