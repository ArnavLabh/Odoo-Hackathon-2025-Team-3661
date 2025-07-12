from flask import Blueprint, request, redirect, url_for, session, flash, current_app
from authlib.integrations.flask_client import OAuth
from models import User, db
import json
import requests

auth = Blueprint('auth', __name__)

# Initialize OAuth
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth with the Flask app"""
    oauth.init_app(app)
    
    # Register Google OAuth
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

# Helper functions
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@auth.route('/login/google')
def google_login():
    """Initiate Google OAuth login"""
    if not current_app.config.get('GOOGLE_CLIENT_ID'):
        flash('Google OAuth is not configured. Please contact administrator.', 'error')
        return redirect(url_for('main.login'))
    
    # Create redirect URI
    redirect_uri = url_for('auth.google_authorized', _external=True)
    
    # Redirect to Google OAuth
    return oauth.google.authorize_redirect(redirect_uri)

@auth.route('/login/google/authorized')
def google_authorized():
    """Handle Google OAuth callback"""
    try:
        # Get the authorization token
        token = oauth.google.authorize_access_token()
        
        if not token:
            flash('Access denied or authorization failed.', 'error')
            return redirect(url_for('main.login'))
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if not user_info:
            # Fallback: manually fetch user info
            resp = oauth.google.parse_id_token(token)
            user_info = resp
        
        # Extract user data
        google_id = user_info.get('sub')
        email = user_info.get('email')
        name = user_info.get('name', '')
        picture = user_info.get('picture', '')
        
        if not email:
            flash('Unable to get email from Google. Please try again.', 'error')
            return redirect(url_for('main.login'))
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # User exists - update Google info and log them in
            if not hasattr(user, 'google_id') or not user.google_id:
                # Add google_id field if it doesn't exist
                user.google_id = google_id
            
            if picture and not user.photo_url:
                user.photo_url = picture
                
            db.session.commit()
            
            # Log the user in
            session['user_id'] = user.id
            flash(f'Welcome back, {user.name}!', 'success')
            
        else:
            # Create new user
            new_user = User(
                name=name or email.split('@')[0],  # Fallback to email username
                email=email,
                password_hash='',  # Empty for OAuth users
                google_id=google_id,
                photo_url=picture,
                is_public=True  # Default to public for OAuth users
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Log the new user in
            session['user_id'] = new_user.id
            flash(f'Welcome to Skill Swap, {new_user.name}! Your account has been created.', 'success')
        
        # Redirect to dashboard
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        current_app.logger.error(f'Google OAuth error: {str(e)}')
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('main.login'))

@auth.route('/unlink/google')
def unlink_google():
    """Unlink Google account from user profile"""
    user = get_current_user()
    
    if not user:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
    
    if not user.password_hash:
        flash('Cannot unlink Google account. Please set a password first to maintain account access.', 'error')
        return redirect(url_for('main.edit_profile'))
    
    # Remove Google OAuth data
    user.google_id = None
    db.session.commit()
    
    flash('Google account has been unlinked from your profile.', 'success')
    return redirect(url_for('main.edit_profile'))

@auth.route('/link/google')
def link_google():
    """Link Google account to existing user profile"""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
    
    # Store that this is a linking request
    session['linking_account'] = True
    
    # Redirect to Google OAuth
    redirect_uri = url_for('auth.google_authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# Helper route to check OAuth status
@auth.route('/oauth/status')
def oauth_status():
    """Check OAuth configuration status"""
    user = get_current_user()
    
    status = {
        'google_configured': bool(current_app.config.get('GOOGLE_CLIENT_ID')),
        'user_logged_in': bool(user),
        'user_has_google': bool(user and hasattr(user, 'google_id') and user.google_id),
        'user_has_password': bool(user and user.password_hash)
    }
    
    return status
