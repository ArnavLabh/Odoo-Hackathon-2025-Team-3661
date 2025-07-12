from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import User, Skill, UserSkill, SwapRequest, Feedback, db
from auth_helpers import (
    hash_password, check_password, is_logged_in, get_current_user,
    login_user, logout_user, login_required, admin_required
)
from datetime import datetime, timedelta
import os
import re
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

main = Blueprint('main', __name__)

# Helper functions
def secure_filename(filename):
    """
    Simple secure filename function to replace werkzeug dependency.
    Removes/replaces unsafe characters from filename.
    """
    if not filename:
        return ''
    
    # Remove path separators and other dangerous characters
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    
    # Remove leading dots and spaces
    filename = filename.lstrip('. ')
    
    # Ensure it's not empty after cleaning
    if not filename:
        return 'unnamed_file'
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

# Home page
@main.route('/')
def index():
    recent_users = User.query.filter_by(is_public=True, is_banned=False).limit(6).all()
    return render_template('index.html', recent_users=recent_users)

# Dashboard route (shows user dashboard with recent activity)
@main.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    
    # Get recent swap requests (sent and received)
    sent_requests = SwapRequest.query.filter_by(from_user_id=user.id).order_by(SwapRequest.created_at.desc()).limit(5).all()
    received_requests = SwapRequest.query.filter_by(to_user_id=user.id).order_by(SwapRequest.created_at.desc()).limit(5).all()
    
    # Get user's skills
    offered_skills = UserSkill.query.filter_by(user_id=user.id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user.id, type='wanted').all()
    
    # Get recent feedback received
    recent_feedback = db.session.query(Feedback).join(SwapRequest).filter(
        ((SwapRequest.from_user_id == user.id) | (SwapRequest.to_user_id == user.id)) &
        (Feedback.reviewer_id != user.id)
    ).order_by(Feedback.id.desc()).limit(3).all()
    
    return render_template('dashboard.html', 
                         user=user,
                         sent_requests=sent_requests,
                         received_requests=received_requests,
                         offered_skills=offered_skills,
                         wanted_skills=wanted_skills,
                         recent_feedback=recent_feedback)

# User Authentication Routes
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location', '')
        availability = request.form.get('availability', '')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('main.register'))
        
        # Create new user
        password_hash = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            location=location,
            availability=availability
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Login the user
        tokens = login_user(new_user)
        flash('Registration successful! Welcome to Skill Swap!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Check if user has a password (not OAuth-only)
            if not user.password_hash:
                flash('This account was created with Google. Please use "Continue with Google" to login.', 'info')
                return render_template('login.html')
            
            if check_password(password, user.password_hash):
                if user.is_banned:
                    flash('Your account has been banned. Please contact support.', 'error')
                    return redirect(url_for('main.login'))
                
                # Login the user
                tokens = login_user(user)
                flash(f'Welcome back, {user.name}!', 'success')
                
                # Redirect admins to admin dashboard
                if user.is_admin:
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid email or password.', 'error')
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

# User Profile Routes
@main.route('/profile')
@login_required
def profile():
    user = get_current_user()
    offered_skills = UserSkill.query.filter_by(user_id=user.id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user.id, type='wanted').all()
    
    return render_template('profile.html', user=user, offered_skills=offered_skills, wanted_skills=wanted_skills)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = get_current_user()
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.location = request.form.get('location')
        user.availability = request.form.get('availability')
        user.is_public = 'is_public' in request.form
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Save to static/uploads directory
                upload_dir = os.path.join('static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, f"{user.id}_{filename}")
                file.save(file_path)
                user.photo_url = f"uploads/{user.id}_{filename}"
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('edit_profile.html', user=user)

# Additional Profile Routes
@main.route('/public_profile/<int:user_id>')
def public_profile(user_id):
    """View another user's public profile"""
    try:
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('main.browse'))
        
        if not user.is_public and (not is_logged_in() or get_current_user().id != user_id):
            flash('This profile is private.', 'error')
            return redirect(url_for('main.browse'))
        
        if user.is_banned:
            flash('This user is not available.', 'error')
            return redirect(url_for('main.browse'))
        
        offered_skills = UserSkill.query.filter_by(user_id=user_id, type='offered').all()
        wanted_skills = UserSkill.query.filter_by(user_id=user_id, type='wanted').all()
        
        # Get user's feedback/ratings (simplified)
        user_feedback = []
        avg_rating = 0
        
        can_request_swap = is_logged_in() and get_current_user().id != user_id
        current_user = get_current_user() if is_logged_in() else None
        
        return render_template('public_profile.html', 
                             user=user, 
                             current_user=current_user,
                             offered_skills=offered_skills, 
                             wanted_skills=wanted_skills,
                             can_request_swap=can_request_swap,
                             feedback=user_feedback,
                             avg_rating=avg_rating)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect(url_for('main.browse'))

# Skills Management Routes
@main.route('/manage_skills')
def manage_skills():
    if not is_logged_in():
        flash('Please login to manage your skills.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    all_skills = Skill.query.all()
    offered_skills = UserSkill.query.filter_by(user_id=user.id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user.id, type='wanted').all()
    user_offered = [us.skill_id for us in offered_skills]
    user_wanted = [us.skill_id for us in wanted_skills]
    
    return render_template('manage_skills.html', 
                         skills=all_skills, 
                         offered_skills=offered_skills,
                         wanted_skills=wanted_skills,
                         user_offered=user_offered, 
                         user_wanted=user_wanted)

@main.route('/add_skill', methods=['POST'])
def add_skill():
    if not is_logged_in():
        return jsonify({'error': 'Please login first'}), 401
    
    skill_name = request.form.get('skill_name')
    skill_type = request.form.get('skill_type')  # 'offered' or 'wanted'
    
    if not skill_name or not skill_type:
        return jsonify({'error': 'Missing skill name or type'}), 400
    
    # Create skill if it doesn't exist
    skill = Skill.query.filter_by(name=skill_name).first()
    if not skill:
        skill = Skill(name=skill_name)
        db.session.add(skill)
        db.session.commit()
    
    # Add user skill if not already exists
    user_skill = UserSkill.query.filter_by(
        user_id=session['user_id'], 
        skill_id=skill.id, 
        type=skill_type
    ).first()
    
    if not user_skill:
        user_skill = UserSkill(
            user_id=session['user_id'],
            skill_id=skill.id,
            type=skill_type
        )
        db.session.add(user_skill)
        db.session.commit()
        flash(f'Skill "{skill_name}" added to your {skill_type} skills!', 'success')
        return jsonify({'success': True, 'message': f'Skill "{skill_name}" added successfully!'})
    else:
        flash(f'Skill "{skill_name}" is already in your {skill_type} skills.', 'info')
        return jsonify({'error': f'Skill "{skill_name}" is already in your {skill_type} skills.'}), 400

@main.route('/remove_skill/<int:skill_id>/<skill_type>')
def remove_skill(skill_id, skill_type):
    if not is_logged_in():
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
    
    user_skill = UserSkill.query.filter_by(
        user_id=session['user_id'],
        skill_id=skill_id,
        type=skill_type
    ).first()
    
    if user_skill:
        db.session.delete(user_skill)
        db.session.commit()
        flash('Skill removed successfully!', 'success')
    
    return redirect(url_for('main.manage_skills'))

# Skill Swap Core Routes
@main.route('/swap_request/<int:to_user_id>')
def swap_request_form(to_user_id):
    """Show swap request form"""
    if not is_logged_in():
        flash('Please login to make swap requests.', 'error')
        return redirect(url_for('main.login'))
    
    current_user = get_current_user()
    to_user = User.query.get(to_user_id)
    
    if not to_user:
        flash('User not found.', 'error')
        return redirect(url_for('main.browse'))
    
    if current_user.id == to_user_id:
        flash('You cannot request a swap with yourself.', 'error')
        return redirect(url_for('main.browse'))
    
    # Get current user's offered skills and target user's offered skills
    current_user_offered = UserSkill.query.filter_by(user_id=current_user.id, type='offered').all()
    to_user_offered = UserSkill.query.filter_by(user_id=to_user_id, type='offered').all()
    
    return render_template('swap_request.html', 
                         user=to_user,
                         to_user=to_user,
                         current_user=current_user,
                         current_user_offered=current_user_offered,
                         to_user_offered=to_user_offered)

@main.route('/swap_list')
def swap_list():
    """View all user's swap requests"""
    if not is_logged_in():
        flash('Please login to view your swaps.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    
    # Get all swap requests (sent and received)
    sent_requests = SwapRequest.query.filter_by(from_user_id=user.id).order_by(SwapRequest.created_at.desc()).all()
    received_requests = SwapRequest.query.filter_by(to_user_id=user.id).order_by(SwapRequest.created_at.desc()).all()
    
    return render_template('swap_list.html', 
                         sent_requests=sent_requests, 
                         received_requests=received_requests)

@main.route('/feedback_form/<int:swap_id>')
def feedback_form(swap_id):
    """Show feedback form for a completed swap"""
    if not is_logged_in():
        flash('Please login to leave feedback.', 'error')
        return redirect(url_for('main.login'))
    
    swap_request = SwapRequest.query.get_or_404(swap_id)
    current_user = get_current_user()
    
    # Verify user is part of this swap
    if swap_request.from_user_id != current_user.id and swap_request.to_user_id != current_user.id:
        flash('You are not part of this swap.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'completed':
        flash('You can only leave feedback for completed swaps.', 'error')
        return redirect(url_for('main.swap_list'))
    
    # Check if user already left feedback
    existing_feedback = Feedback.query.filter_by(
        swap_id=swap_id,
        reviewer_id=current_user.id
    ).first()
    
    if existing_feedback:
        flash('You have already left feedback for this swap.', 'info')
        return redirect(url_for('main.swap_list'))
    
    # Determine who the other user is
    other_user = swap_request.receiver if current_user.id == swap_request.from_user_id else swap_request.requester
    
    return render_template('feedback_form.html', 
                         swap_request=swap_request, 
                         other_user=other_user)

@main.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for a swap"""
    if not is_logged_in():
        return redirect(url_for('main.login'))
    
    swap_id = request.form.get('swap_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')
    
    current_user = get_current_user()
    swap_request = SwapRequest.query.get_or_404(swap_id)
    
    # Verify user is part of this swap
    if swap_request.from_user_id != current_user.id and swap_request.to_user_id != current_user.id:
        flash('You are not part of this swap.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Check if feedback already exists
    existing_feedback = Feedback.query.filter_by(
        swap_id=swap_id,
        reviewer_id=current_user.id
    ).first()
    
    if existing_feedback:
        flash('You have already left feedback for this swap.', 'info')
        return redirect(url_for('main.swap_list'))
    
    feedback = Feedback(
        swap_id=swap_id,
        reviewer_id=current_user.id,
        rating=int(rating),
        comment=comment
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('main.swap_list'))

# Browse and Search Routes
@main.route('/browse')
def browse():
    search_query = request.args.get('search', '')
    skill_filter = request.args.get('skill', '')
    availability_filter = request.args.get('availability', '')
    location_filter = request.args.get('location', '')
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of users per page
    
    # Base query for public, non-banned users
    query = User.query.filter_by(is_public=True, is_banned=False)
    
    # Apply search filters
    if search_query:
        query = query.filter(User.name.ilike(f'%{search_query}%'))
    
    # Apply skill filter
    if skill_filter:
        # Find users who offer this skill
        skill = Skill.query.filter_by(name=skill_filter).first()
        if skill:
            user_ids = [us.user_id for us in UserSkill.query.filter_by(skill_id=skill.id, type='offered').all()]
            if user_ids:
                query = query.filter(User.id.in_(user_ids))
    
    # Apply availability filter
    if availability_filter:
        query = query.filter(User.availability.ilike(f'%{availability_filter}%'))
    
    # Apply location filter
    if location_filter:
        query = query.filter(User.location.ilike(f'%{location_filter}%'))
    
    # Apply sorting
    if sort_by == 'rating':
        # This would require a more complex query with joins to calculate average ratings
        # For simplicity, we'll just sort by name for now
        query = query.order_by(User.name)
    elif sort_by == 'active':
        # Sort by last login time
        query = query.order_by(User.last_login.desc())
    elif sort_by == 'skills':
        # This would require a subquery to count skills
        # For simplicity, we'll sort by name
        query = query.order_by(User.name)
    else:  # newest
        query = query.order_by(User.created_at.desc())
    
    # Execute query with pagination
    total_users = query.count()
    total_pages = (total_users + per_page - 1) // per_page  # Ceiling division
    offset = (page - 1) * per_page
    users = query.offset(offset).limit(per_page).all()
    
    # Get all skills for the filter dropdown
    all_skills = Skill.query.all()
    
    # Get all unique availability values
    availabilities = db.session.query(User.availability).distinct().all()
    availabilities = [a[0] for a in availabilities if a[0]]
    
    # Get all unique locations
    locations = db.session.query(User.location).distinct().all()
    locations = [l[0] for l in locations if l[0]]
    
    # Current time for online status
    now = datetime.now()
    
    # Get current user for conditional display
    current_user = get_current_user() if is_logged_in() else None
    
    return render_template('browse.html', 
                          users=users, 
                          skills=all_skills,
                          availabilities=availabilities,
                          locations=locations,
                          search_query=search_query, 
                          skill_filter=skill_filter,
                          availability_filter=availability_filter,
                          location_filter=location_filter,
                          sort_by=sort_by,
                          current_page=page,
                          total_pages=total_pages,
                          total_users=total_users,
                          now=now,
                          current_user=current_user)

@main.route('/user/<int:user_id>')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if not user.is_public and (not is_logged_in() or get_current_user().id != user_id):
        flash('This profile is private.', 'error')
        return redirect(url_for('main.browse'))
    
    offered_skills = UserSkill.query.filter_by(user_id=user_id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user_id, type='wanted').all()
    
    can_request_swap = is_logged_in() and get_current_user().id != user_id
    
    return render_template('view_user.html', user=user, offered_skills=offered_skills, wanted_skills=wanted_skills, can_request_swap=can_request_swap)

@main.route('/search_results')
def search_results():
    """Advanced search and filter results"""
    search_query = request.args.get('search', '')
    skill_filter = request.args.get('skill', '')
    location_filter = request.args.get('location', '')
    availability_filter = request.args.get('availability', '')
    
    # Base query for public, non-banned users
    query = User.query.filter_by(is_public=True, is_banned=False)
    
    # Apply search filters
    if search_query:
        query = query.filter(User.name.contains(search_query))
    
    if location_filter:
        query = query.filter(User.location.contains(location_filter))
        
    if availability_filter:
        query = query.filter(User.availability == availability_filter)
    
    if skill_filter:
        # Find users who offer this skill
        skill = Skill.query.filter_by(name=skill_filter).first()
        if skill:
            user_ids = [us.user_id for us in UserSkill.query.filter_by(skill_id=skill.id, type='offered').all()]
            query = query.filter(User.id.in_(user_ids))
    
    users = query.all()
    all_skills = Skill.query.all()
    
    # Get unique locations and availabilities for filter options
    locations = db.session.query(User.location).filter(User.location.isnot(None), User.location != '').distinct().all()
    availabilities = db.session.query(User.availability).filter(User.availability.isnot(None), User.availability != '').distinct().all()
    
    return render_template('search_results.html', 
                         users=users, 
                         skills=all_skills,
                         locations=[l[0] for l in locations],
                         availabilities=[a[0] for a in availabilities],
                         search_query=search_query, 
                         skill_filter=skill_filter,
                         location_filter=location_filter,
                         availability_filter=availability_filter)

# Privacy and Settings
@main.route('/privacy_toggle', methods=['GET', 'POST'])
def privacy_toggle():
    """Toggle user profile privacy settings"""
    if not is_logged_in():
        flash('Please login to change privacy settings.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    
    if request.method == 'POST':
        user.is_public = 'is_public' in request.form
        db.session.commit()
        
        status = "public" if user.is_public else "private"
        flash(f'Your profile is now {status}.', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('privacy_toggle.html', user=user)

# Notifications (Optional)
@main.route('/notifications')
def notifications():
    """View user notifications"""
    if not is_logged_in():
        flash('Please login to view notifications.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    
    # Get recent swap requests and updates
    recent_received = SwapRequest.query.filter_by(to_user_id=user.id).order_by(SwapRequest.created_at.desc()).limit(10).all()
    recent_sent = SwapRequest.query.filter_by(from_user_id=user.id).filter(SwapRequest.status != 'pending').order_by(SwapRequest.created_at.desc()).limit(10).all()
    
    # Get recent feedback
    recent_feedback = db.session.query(Feedback).join(SwapRequest).filter(
        ((SwapRequest.from_user_id == user.id) | (SwapRequest.to_user_id == user.id)) &
        (Feedback.reviewer_id != user.id)
    ).order_by(Feedback.id.desc()).limit(5).all()
    
    return render_template('notifications.html', 
                         recent_received=recent_received,
                         recent_sent=recent_sent,
                         recent_feedback=recent_feedback)

# Password Reset Routes
@main.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expires = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            
            db.session.commit()
            
            # Since we don't have email system, directly redirect to reset password
            flash('Please reset your password below.', 'info')
            return redirect(url_for('main.reset_password', token=reset_token))
        else:
            flash('No account found with that email address.', 'error')
            return render_template('forgotpassword.html')
    
    return render_template('forgotpassword.html')

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.now():
        flash('Invalid or expired reset token. Please request a new password reset.', 'error')
        return redirect(url_for('main.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('Please fill in both password fields.', 'error')
            return render_template('reset_password.html', token=token, user=user)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token, user=user)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('reset_password.html', token=token, user=user)
        
        # Update password
        user.password_hash = hash_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        
        db.session.commit()
        
        flash(f'Password reset successful for {user.name}! You can now login with your new password.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('reset_password.html', token=token, user=user)
    
    # TODO: Implement actual email sending
    # Example with SMTP (requires email server configuration):
    
    msg = MIMEMultipart()
    msg['From'] = 'noreply@skillswap.com'
    msg['To'] = email
    msg['Subject'] = 'Password Reset Request - Skill Swap'
    
    body = f"""
    Hello,
    
    You have requested to reset your password for Skill Swap.
    
    Click the following link to reset your password:
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you did not request this reset, please ignore this email.
    
    Best regards,
    Skill Swap Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Configure your SMTP settings here
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('your-email@gmail.com', 'your-app-password')
    # server.send_message(msg)
    # server.quit()
    

# Error handlers
@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
