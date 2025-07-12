#!/usr/bin/env python3
from app import create_app
from models import User

app = create_app()

with app.app_context():
    print("Testing routes...")
    
    # Check if routes exist
    for rule in app.url_map.iter_rules():
        if 'swap' in rule.rule:
            print(f"Route: {rule.rule} -> {rule.endpoint}")
    
    # Check users count
    users = User.query.limit(5).all()
    print(f"\nFirst 5 users:")
    for user in users:
        print(f"  {user.id}: {user.name}")
    
    # Test the specific route that's causing 404
    with app.test_client() as client:
        response = client.get('/swap_request/1')
        print(f"\nGET /swap_request/1: Status {response.status_code}")
        
        if response.status_code == 302:
            print(f"Redirected to: {response.location}")
        elif response.status_code != 200:
            print(f"Response: {response.data.decode()[:200]}...")
