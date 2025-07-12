from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import User, Skill, UserSkill, SwapRequest, Feedback, db
from datetime import datetime
from functools import wraps

swaps = Blueprint('swaps', __name__)

# Helper functions
def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please login to access this page.', 'error')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Create Swap Request
@swaps.route('/request_swap/<int:to_user_id>', methods=['GET', 'POST'])
@login_required
def request_swap(to_user_id):
    current_user = get_current_user()
    to_user = User.query.get_or_404(to_user_id)
    
    if current_user.id == to_user_id:
        flash('You cannot request a swap with yourself.', 'error')
        # Stay on current page instead of redirecting
    
    if request.method == 'POST':
        offered_skill_id = request.form.get('offered_skill_id')
        wanted_skill_id = request.form.get('wanted_skill_id')
        
        # Validate skills
        offered_skill = UserSkill.query.filter_by(
            user_id=current_user.id, 
            skill_id=offered_skill_id, 
            type='offered'
        ).first()
        
        wanted_skill = UserSkill.query.filter_by(
            user_id=to_user_id, 
            skill_id=wanted_skill_id, 
            type='offered'
        ).first()
        
        if not offered_skill:
            flash('You must select a skill you offer.', 'error')
            # Stay on current page instead of redirecting
        
        if not wanted_skill:
            flash('Selected skill is not offered by this user.', 'error')
            # Stay on current page instead of redirecting
        
        # Check if request already exists
        existing_request = SwapRequest.query.filter_by(
            from_user_id=current_user.id,
            to_user_id=to_user_id,
            offered_skill_id=offered_skill_id,
            wanted_skill_id=wanted_skill_id,
            status='pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending request for this skill swap.', 'info')
            # Stay on current page instead of redirecting
        
        # Create swap request
        swap_request = SwapRequest(
            from_user_id=current_user.id,
            to_user_id=to_user_id,
            offered_skill_id=offered_skill_id,
            wanted_skill_id=wanted_skill_id,
            status='pending'
        )
        
        db.session.add(swap_request)
        db.session.commit()
        
        flash(f'Swap request sent to {to_user.name}!', 'success')
        # Just flash message, don't redirect
    
    # GET request - show form
    current_user_offered = UserSkill.query.filter_by(user_id=current_user.id, type='offered').all()
    to_user_offered = UserSkill.query.filter_by(user_id=to_user_id, type='offered').all()
    
    return render_template('swap_request.html', 
                         user=to_user,
                         to_user=to_user,
                         current_user=current_user, 
                         current_user_offered=current_user_offered,
                         to_user_offered=to_user_offered)

# Accept Swap Request
@swaps.route('/accept_swap/<int:request_id>')
@login_required
def accept_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user can accept this request
    if swap_request.to_user_id != current_user.id:
        flash('You can only accept requests sent to you.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'pending':
        flash('This request has already been processed.', 'info')
        return redirect(url_for('main.dashboard'))
    
    swap_request.status = 'accepted'
    db.session.commit()
    
    flash(f'Swap request accepted! You can now coordinate with {swap_request.requester.name}.', 'success')
    return redirect(url_for('swaps.swap_list'))

# Reject Swap Request
@swaps.route('/reject_swap/<int:request_id>')
@login_required
def reject_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user can reject this request
    if swap_request.to_user_id != current_user.id:
        flash('You can only reject requests sent to you.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'pending':
        flash('This request has already been processed.', 'info')
        return redirect(url_for('main.dashboard'))
    
    swap_request.status = 'rejected'
    db.session.commit()
    
    flash('Swap request rejected.', 'info')
    return redirect(url_for('swaps.swap_list'))

# Cancel Swap Request (for requesters)
@swaps.route('/cancel_swap/<int:request_id>')
@login_required
def cancel_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user can cancel this request
    if swap_request.from_user_id != current_user.id:
        flash('You can only cancel requests you sent.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'pending':
        flash('You can only cancel pending requests.', 'info')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(swap_request)
    db.session.commit()
    
    flash('Swap request cancelled.', 'info')
    return redirect(url_for('swaps.swap_list'))

# Complete Swap (mark as completed)
@swaps.route('/complete_swap/<int:request_id>')
@login_required
def complete_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user is part of this swap
    if swap_request.from_user_id != current_user.id and swap_request.to_user_id != current_user.id:
        flash('You are not part of this swap.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'accepted':
        flash('Only accepted swaps can be marked as completed.', 'error')
        return redirect(url_for('main.dashboard'))
    
    swap_request.status = 'completed'
    db.session.commit()
    
    flash('Swap marked as completed! You can now leave feedback.', 'success')
    return redirect(url_for('swaps.leave_feedback', request_id=request_id))

# Leave Feedback
@swaps.route('/feedback/<int:request_id>', methods=['GET', 'POST'])
@login_required
def leave_feedback(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user is part of this swap
    if swap_request.from_user_id != current_user.id and swap_request.to_user_id != current_user.id:
        flash('You are not part of this swap.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if swap_request.status != 'completed':
        flash('You can only leave feedback for completed swaps.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Check if user already left feedback
    existing_feedback = Feedback.query.filter_by(
        swap_id=request_id,
        reviewer_id=current_user.id
    ).first()
    
    if request.method == 'POST':
        if existing_feedback:
            flash('You have already left feedback for this swap.', 'info')
            return redirect(url_for('main.dashboard'))
        
        rating = request.form.get('rating')
        comment = request.form.get('comment', '')
        
        feedback = Feedback(
            swap_id=request_id,
            reviewer_id=current_user.id,
            rating=int(rating),
            comment=comment
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Determine who the other user is
    other_user = swap_request.receiver if current_user.id == swap_request.from_user_id else swap_request.requester
    
    return render_template('feedback.html', 
                         swap_request=swap_request, 
                         current_user=current_user,
                         other_user=other_user,
                         existing_feedback=existing_feedback)

# View All Swap Requests
@swaps.route('/my-swaps')
@login_required
def swap_list():
    current_user = get_current_user()
    
    # Get all swap requests (sent and received)
    sent_requests = SwapRequest.query.filter_by(from_user_id=current_user.id).order_by(SwapRequest.created_at.desc()).all()
    received_requests = SwapRequest.query.filter_by(to_user_id=current_user.id).order_by(SwapRequest.created_at.desc()).all()
    
    return render_template('swap_list.html',
                         current_user=current_user,
                         sent_requests=sent_requests,
                         received_requests=received_requests)

# View Swap Details
@swaps.route('/swap/<int:request_id>')
@login_required
def view_swap(request_id):
    swap_request = SwapRequest.query.get_or_404(request_id)
    current_user = get_current_user()
    
    # Verify user is part of this swap
    if swap_request.from_user_id != current_user.id and swap_request.to_user_id != current_user.id:
        flash('You are not part of this swap.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get feedback for this swap
    feedback_list = Feedback.query.filter_by(swap_id=request_id).all()
    
    return render_template('view_swap.html', 
                         swap_request=swap_request, 
                         feedback_list=feedback_list,
                         current_user=current_user)
