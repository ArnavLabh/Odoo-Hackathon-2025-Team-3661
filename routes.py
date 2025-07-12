from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import User, Skill, UserSkill, SwapRequest, Feedback, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

# Home page
@main.route('/')
def index():
    recent_users = User.query.filter_by(is_public=True, is_banned=False).limit(6).all()
    return render_template('index.html', recent_users=recent_users)

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
        password_hash = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            location=location,
            availability=availability
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        flash('Registration successful! Welcome to Skill Swap!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            if user.is_banned:
                flash('Your account has been banned. Please contact support.', 'error')
                return redirect(url_for('main.login'))
            
            session['user_id'] = user.id
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

# User Profile Routes
@main.route('/profile')
def profile():
    if not is_logged_in():
        flash('Please login to view your profile.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    offered_skills = UserSkill.query.filter_by(user_id=user.id, type='offered').all()
    wanted_skills = UserSkill.query.filter_by(user_id=user.id, type='wanted').all()
    
    return render_template('profile.html', user=user, offered_skills=offered_skills, wanted_skills=wanted_skills)

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not is_logged_in():
        flash('Please login to edit your profile.', 'error')
        return redirect(url_for('main.login'))
    
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

# Skills Management Routes
@main.route('/manage_skills')
def manage_skills():
    if not is_logged_in():
        flash('Please login to manage your skills.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    all_skills = Skill.query.all()
    user_offered = [us.skill_id for us in UserSkill.query.filter_by(user_id=user.id, type='offered').all()]
    user_wanted = [us.skill_id for us in UserSkill.query.filter_by(user_id=user.id, type='wanted').all()]
    
    return render_template('manage_skills.html', skills=all_skills, user_offered=user_offered, user_wanted=user_wanted)

@main.route('/add_skill', methods=['POST'])
def add_skill():
    if not is_logged_in():
        return jsonify({'error': 'Please login first'}), 401
    
    skill_name = request.form.get('skill_name')
    skill_type = request.form.get('skill_type')  # 'offered' or 'wanted'
    
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
    else:
        flash(f'Skill "{skill_name}" is already in your {skill_type} skills.', 'info')
    
    return redirect(url_for('main.manage_skills'))

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

# Browse and Search Routes
@main.route('/browse')
def browse():
    search_query = request.args.get('search', '')
    skill_filter = request.args.get('skill', '')
    
    # Base query for public, non-banned users
    query = User.query.filter_by(is_public=True, is_banned=False)
    
    # Apply search filters
    if search_query:
        query = query.filter(User.name.contains(search_query))
    
    if skill_filter:
        # Find users who offer this skill
        skill = Skill.query.filter_by(name=skill_filter).first()
        if skill:
            user_ids = [us.user_id for us in UserSkill.query.filter_by(skill_id=skill.id, type='offered').all()]
            query = query.filter(User.id.in_(user_ids))
    
    users = query.all()
    all_skills = Skill.query.all()
    
    return render_template('browse.html', users=users, skills=all_skills, search_query=search_query, skill_filter=skill_filter)

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

# Dashboard
@main.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please login to view your dashboard.', 'error')
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    
    # Get swap requests
    sent_requests = SwapRequest.query.filter_by(from_user_id=user.id).all()
    received_requests = SwapRequest.query.filter_by(to_user_id=user.id).all()
    
    return render_template('dashboard.html', user=user, sent_requests=sent_requests, received_requests=received_requests)
