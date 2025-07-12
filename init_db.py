#!/usr/bin/env python3
"""
Database initialization script for production
Run this once after deploying to create tables
"""

import os
from app import create_app
from models import db

def init_production_db():
    """Initialize production database tables"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🗄️ Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print table info
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📦 Created {len(tables)} tables: {', '.join(tables)}")
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = init_production_db()
    if not success:
        exit(1)
