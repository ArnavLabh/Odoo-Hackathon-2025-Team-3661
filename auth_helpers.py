from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from flask import session, current_app
from models import User
from functools import wraps
import bcrypt
from datetime import datetime

def hash_password(password):
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def check_password(password, hashed_password):
    """Check if password matches the hashed password"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user_tokens(user):
    """Create JWT tokens for a user"""
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def is_logged_in():
    """Check if user is logged in via session or JWT"""
    # Check session-based auth (for web interface)
    if 'user_id' in session:
        return True
    
    # For API/JWT auth, this would be handled by @jwt_required decorator
    return False

def get_current_user():
    """Get current user from session or JWT"""
    # Session-based auth
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    
    return None

def get_current_user_jwt():
    """Get current user from JWT token (for API routes)"""
    try:
        user_id = get_jwt_identity()
        if user_id:
            return User.query.get(user_id)
    except:
        pass
    return None

def login_user(user, remember=False):
    """Login user with session and optionally create JWT tokens"""
    # Session-based login for web interface
    session['user_id'] = user.id
    
    # Update last login
    user.last_login = datetime.now()
    from models import db
    db.session.commit()
    
    # Create JWT tokens for API access
    tokens = create_user_tokens(user)
    return tokens

def logout_user():
    """Logout user from session"""
    session.pop('user_id', None)

def login_required(f):
    """Decorator for routes that require login (session-based)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            from flask import flash, redirect, url_for
            flash('Please login to access this page.', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            from flask import flash, redirect, url_for
            flash('Please login to access this page.', 'error')
            return redirect(url_for('main.login'))
        
        user = get_current_user()
        if not user or not user.is_admin:
            from flask import flash, redirect, url_for
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
