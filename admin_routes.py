from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import User, Skill, UserSkill, SwapRequest, Feedback, db
from datetime import datetime, timedelta
import json

admin = Blueprint('admin', __name__)

# Helper functions for admin
def is_admin():
    """Check if current user is admin"""
    if 'user_id' not in session:
        return False
    user = User.query.get(session['user_id'])
    return user and user.is_admin

def admin_required(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Admin Dashboard
@admin.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    """Admin overview dashboard"""
    # Get platform statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_banned=False).count()
    banned_users = User.query.filter_by(is_banned=True).count()
    public_profiles = User.query.filter_by(is_public=True, is_banned=False).count()
    
    total_skills = Skill.query.count()
    total_swaps = SwapRequest.query.count()
    pending_swaps = SwapRequest.query.filter_by(status='pending').count()
    completed_swaps = SwapRequest.query.filter_by(status='completed').count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    new_users_week = User.query.filter(User.id >= week_ago).count()
    new_swaps_week = SwapRequest.query.filter(SwapRequest.created_at >= week_ago).count()
    
    # Top skills
    skill_usage = db.session.query(
        Skill.name, 
        db.func.count(UserSkill.id).label('usage_count')
    ).join(UserSkill).group_by(Skill.id).order_by(db.func.count(UserSkill.id).desc()).limit(10).all()
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'banned_users': banned_users,
        'public_profiles': public_profiles,
        'total_skills': total_skills,
        'total_swaps': total_swaps,
        'pending_swaps': pending_swaps,
        'completed_swaps': completed_swaps,
        'new_users_week': new_users_week,
        'new_swaps_week': new_swaps_week,
        'top_skills': skill_usage
    }
    
    return render_template('admin_dashboard.html', stats=stats)

# User Management
@admin.route('/user_list')
@admin_required
def user_list():
    """View and moderate user profiles"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')  # all, active, banned
    
    query = User.query
    
    # Apply filters
    if search:
        query = query.filter(User.name.contains(search) | User.email.contains(search))
    
    if status_filter == 'active':
        query = query.filter_by(is_banned=False)
    elif status_filter == 'banned':
        query = query.filter_by(is_banned=True)
    
    users = query.order_by(User.id.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('user_list.html', 
                         users=users, 
                         search=search, 
                         status_filter=status_filter)

@admin.route('/ban_user/<int:user_id>')
@admin_required
def ban_user(user_id):
    """Ban a user"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot ban an admin user.', 'error')
        return redirect(url_for('admin.user_list'))
    
    user.is_banned = True
    db.session.commit()
    
    flash(f'User {user.name} has been banned.', 'success')
    return redirect(url_for('admin.user_list'))

@admin.route('/unban_user/<int:user_id>')
@admin_required
def unban_user(user_id):
    """Unban a user"""
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    
    flash(f'User {user.name} has been unbanned.', 'success')
    return redirect(url_for('admin.user_list'))

@admin.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    """Delete a user and all related data"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot delete an admin user.', 'error')
        return redirect(url_for('admin.user_list'))
    
    # Delete related data
    UserSkill.query.filter_by(user_id=user_id).delete()
    SwapRequest.query.filter((SwapRequest.from_user_id == user_id) | (SwapRequest.to_user_id == user_id)).delete()
    Feedback.query.filter_by(reviewer_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.name} has been deleted.', 'success')
    return redirect(url_for('admin.user_list'))

# Swap Moderation
@admin.route('/swap_moderation')
@admin_required
def swap_moderation():
    """View and manage all swap requests"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')  # all, pending, accepted, completed, rejected
    
    query = SwapRequest.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    swaps = query.order_by(SwapRequest.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('swap_moderation.html', 
                         swaps=swaps, 
                         status_filter=status_filter)

@admin.route('/force_complete_swap/<int:swap_id>')
@admin_required
def force_complete_swap(swap_id):
    """Force complete a swap (admin intervention)"""
    swap = SwapRequest.query.get_or_404(swap_id)
    swap.status = 'completed'
    db.session.commit()
    
    flash('Swap has been marked as completed.', 'success')
    return redirect(url_for('admin.swap_moderation'))

@admin.route('/cancel_swap_admin/<int:swap_id>')
@admin_required
def cancel_swap_admin(swap_id):
    """Cancel a swap (admin intervention)"""
    swap = SwapRequest.query.get_or_404(swap_id)
    swap.status = 'cancelled'
    db.session.commit()
    
    flash('Swap has been cancelled.', 'success')
    return redirect(url_for('admin.swap_moderation'))

# Skill Management
@admin.route('/skill_moderation')
@admin_required
def skill_moderation():
    """Moderate skills and remove inappropriate ones"""
    skills = Skill.query.order_by(Skill.name).all()
    
    # Get usage count for each skill
    skill_usage = {}
    for skill in skills:
        usage_count = UserSkill.query.filter_by(skill_id=skill.id).count()
        skill_usage[skill.id] = usage_count
    
    return render_template('skill_moderation.html', 
                         skills=skills, 
                         skill_usage=skill_usage)

@admin.route('/delete_skill/<int:skill_id>')
@admin_required
def delete_skill(skill_id):
    """Delete a skill and all user associations"""
    skill = Skill.query.get_or_404(skill_id)
    
    # Delete user skill associations
    UserSkill.query.filter_by(skill_id=skill_id).delete()
    
    # Update swap requests to remove skill references
    SwapRequest.query.filter_by(offered_skill_id=skill_id).update({'offered_skill_id': None})
    SwapRequest.query.filter_by(wanted_skill_id=skill_id).update({'wanted_skill_id': None})
    
    db.session.delete(skill)
    db.session.commit()
    
    flash(f'Skill "{skill.name}" has been deleted.', 'success')
    return redirect(url_for('admin.skill_moderation'))

# Broadcasting
@admin.route('/broadcast', methods=['GET', 'POST'])
@admin_required
def broadcast():
    """Send platform-wide messages"""
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        recipient_type = request.form.get('recipient_type')  # all, active, admins
        
        # Here you would typically integrate with an email service or notification system
        # For now, we'll just flash a success message
        
        if recipient_type == 'all':
            recipient_count = User.query.count()
        elif recipient_type == 'active':
            recipient_count = User.query.filter_by(is_banned=False).count()
        elif recipient_type == 'admins':
            recipient_count = User.query.filter_by(is_admin=True).count()
        
        # In a real implementation, you would send emails/notifications here
        flash(f'Message "{subject}" would be sent to {recipient_count} users.', 'success')
        return redirect(url_for('admin.broadcast'))
    
    # Get user counts for the form
    all_users = User.query.count()
    active_users = User.query.filter_by(is_banned=False).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    return render_template('broadcast.html', 
                         all_users=all_users,
                         active_users=active_users,
                         admin_users=admin_users)

# Reports and Analytics
@admin.route('/download_user_report')
@admin_required
def download_user_report():
    """Download user activity report"""
    users = User.query.all()
    
    # Generate CSV data
    csv_data = "ID,Name,Email,Location,Is_Public,Is_Banned,Offered_Skills,Wanted_Skills,Swaps_Sent,Swaps_Received\n"
    
    for user in users:
        offered_count = UserSkill.query.filter_by(user_id=user.id, type='offered').count()
        wanted_count = UserSkill.query.filter_by(user_id=user.id, type='wanted').count()
        swaps_sent = SwapRequest.query.filter_by(from_user_id=user.id).count()
        swaps_received = SwapRequest.query.filter_by(to_user_id=user.id).count()
        
        csv_data += f"{user.id},{user.name},{user.email},{user.location or ''},{user.is_public},{user.is_banned},{offered_count},{wanted_count},{swaps_sent},{swaps_received}\n"
    
    # In a real implementation, you would return this as a downloadable file
    flash('User report would be downloaded (CSV functionality not implemented).', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/download_swap_report')
@admin_required
def download_swap_report():
    """Download swap activity report"""
    swaps = SwapRequest.query.all()
    
    # Generate CSV data
    csv_data = "ID,From_User,To_User,Offered_Skill,Wanted_Skill,Status,Created_Date\n"
    
    for swap in swaps:
        csv_data += f"{swap.id},{swap.requester.name},{swap.receiver.name},{swap.offered_skill.name if swap.offered_skill else ''},{swap.wanted_skill.name if swap.wanted_skill else ''},{swap.status},{swap.created_at}\n"
    
    # In a real implementation, you would return this as a downloadable file
    flash('Swap report would be downloaded (CSV functionality not implemented).', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/download_feedback_report')
@admin_required
def download_feedback_report():
    """Download feedback logs"""
    feedback_list = Feedback.query.all()
    
    # Generate CSV data
    csv_data = "ID,Swap_ID,Reviewer,Rating,Comment\n"
    
    for feedback in feedback_list:
        comment = feedback.comment.replace(',', ';') if feedback.comment else ''
        csv_data += f"{feedback.id},{feedback.swap_id},{feedback.reviewer.name},{feedback.rating},{comment}\n"
    
    # In a real implementation, you would return this as a downloadable file
    flash('Feedback report would be downloaded (CSV functionality not implemented).', 'info')
    return redirect(url_for('admin.admin_dashboard'))
