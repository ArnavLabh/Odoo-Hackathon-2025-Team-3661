from app import create_app
from models import User, db
from auth_helpers import hash_password

app = create_app()
print('App created')

with app.app_context():
    # Create test user if needed
    user = User.query.first()
    if not user:
        user = User(
            name='Test User',
            email='test@test.com',
            password_hash=hash_password('test'),
            is_public=True
        )
        db.session.add(user)
        db.session.commit()
    
    print(f'Test user ID: {user.id}')
    
    # Test the route
    with app.test_client() as client:
        response = client.get(f'/public_profile/{user.id}')
        print(f'Status: {response.status_code}')
        if response.status_code != 200:
            print(f'Response data: {response.data.decode()}')
