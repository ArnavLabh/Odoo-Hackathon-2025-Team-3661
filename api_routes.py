from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, create_access_token
from models import User, Skill, UserSkill, SwapRequest, Feedback, db
from auth_helpers import get_current_user, get_current_user_jwt, check_password
import json

api = Blueprint('api', __name__)

# API Authentication Routes
@api.route('/api/auth/login', methods=['POST'])
def api_login():
    """API login endpoint that returns JWT tokens"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.password_hash and check_password(password, user.password_hash):
        if user.is_banned:
            return jsonify({'error': 'Account banned'}), 403
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api.route('/api/auth/profile')
@jwt_required()
def api_profile():
    """Get current user profile via JWT"""
    user = get_current_user_jwt()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'location': user.location,
        'availability': user.availability,
        'is_public': user.is_public
    })

# Helper functions  
def is_logged_in():
    return 'user_id' in session

# API Routes for AJAX calls
@api.route('/api/skills/search')
def search_skills():
    """Search skills for autocomplete"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    skills = Skill.query.filter(Skill.name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([{'id': skill.id, 'name': skill.name} for skill in skills])

@api.route('/api/users/search')
def search_users():
    """Search users by name"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    users = User.query.filter(
        User.name.ilike(f'%{query}%'),
        User.is_public == True,
        User.is_banned == False
    ).limit(10).all()
    
    return jsonify([{
        'id': user.id, 
        'name': user.name,
        'location': user.location,
        'photo_url': user.photo_url
    } for user in users])

@api.route('/api/user/<int:user_id>/skills')
def get_user_skills(user_id):
    """Get user's skills"""
    user = User.query.get_or_404(user_id)
    
    if not user.is_public and (not is_logged_in() or get_current_user().id != user_id):
        return jsonify({'error': 'Profile is private'}), 403
    
    offered_skills = UserSkill.query.filter_by(user_id=user_id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user_id, type='wanted').all()
    
    return jsonify({
        'offered': [{'id': us.skill.id, 'name': us.skill.name} for us in offered_skills],
        'wanted': [{'id': us.skill.id, 'name': us.skill.name} for us in wanted_skills]
    })

@api.route('/api/swap/<int:swap_id>/status', methods=['POST'])
def update_swap_status(swap_id):
    """Update swap request status via API"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    swap = SwapRequest.query.get_or_404(swap_id)
    current_user = get_current_user()
    new_status = request.json.get('status')
    
    # Verify user can update this swap
    if swap.to_user_id != current_user.id and swap.from_user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    if new_status in ['accepted', 'rejected'] and swap.to_user_id == current_user.id:
        swap.status = new_status
        db.session.commit()
        return jsonify({'status': 'success', 'new_status': new_status})
    elif new_status == 'cancelled' and swap.from_user_id == current_user.id:
        db.session.delete(swap)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Swap cancelled'})
    
    return jsonify({'error': 'Invalid status update'}), 400

@api.route('/api/stats/dashboard')
def dashboard_stats():
    """Get dashboard statistics"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    user = get_current_user()
    
    stats = {
        'offered_skills_count': UserSkill.query.filter_by(user_id=user.id, type='offered').count(),
        'wanted_skills_count': UserSkill.query.filter_by(user_id=user.id, type='wanted').count(),
        'sent_requests_count': SwapRequest.query.filter_by(from_user_id=user.id).count(),
        'received_requests_count': SwapRequest.query.filter_by(to_user_id=user.id).count(),
        'completed_swaps_count': SwapRequest.query.filter(
            ((SwapRequest.from_user_id == user.id) | (SwapRequest.to_user_id == user.id)) &
            (SwapRequest.status == 'completed')
        ).count(),
        'pending_requests_count': SwapRequest.query.filter_by(to_user_id=user.id, status='pending').count()
    }
    
    return jsonify(stats)

@api.route('/api/notifications/unread')
def unread_notifications():
    """Get count of unread notifications"""
    if not is_logged_in():
        return jsonify({'error': 'Authentication required'}), 401
    
    user = get_current_user()
    
    # Count pending swap requests received
    pending_count = SwapRequest.query.filter_by(to_user_id=user.id, status='pending').count()
    
    # Count recent status updates on sent requests
    recent_updates = SwapRequest.query.filter(
        (SwapRequest.from_user_id == user.id) & 
        (SwapRequest.status.in_(['accepted', 'rejected', 'completed']))
    ).count()
    
    return jsonify({
        'pending_requests': pending_count,
        'recent_updates': recent_updates,
        'total_unread': pending_count + recent_updates
    })
