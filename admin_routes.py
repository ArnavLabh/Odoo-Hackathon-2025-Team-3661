from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from models import (
    User, Skill, UserSkill, SwapRequest, Feedback,
    SkillDescription, BanHistory, PlatformNotification, db
)
from datetime import datetime, timedelta
import json
import csv
import io

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

@admin.route('/ban_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def ban_user(user_id):
    """Enhanced ban user with history tracking - MISSING FEATURE"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot ban an admin user.', 'error')
        return redirect(url_for('admin.user_list'))
    
    if request.method == 'POST':
        reason = request.form.get('reason', 'No reason provided')
        current_user_id = session.get('user_id')
        
        # Update user status
        user.is_banned = True
        
        # Create ban history record - NEW FEATURE
        ban_record = BanHistory(
            user_id=user_id,
            banned_by=current_user_id,
            ban_reason=reason,
            is_active=True
        )
        
        db.session.add(ban_record)
        db.session.commit()
        
        flash(f'User {user.name} has been banned. Reason: {reason}', 'success')
        return redirect(url_for('admin.user_list'))
    
    # For GET request, show ban form with reason input
    return render_template('admin/ban_user_form.html', user=user)

@admin.route('/ban_user_quick/<int:user_id>/<reason>')
@admin_required
def ban_user_quick(user_id, reason):
    """Quick ban with predefined reasons"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot ban an admin user.', 'error')
        return redirect(url_for('admin.user_list'))
    
    current_user_id = session.get('user_id')
    reason_text = reason.replace('_', ' ').title()
    
    user.is_banned = True
    
    ban_record = BanHistory(
        user_id=user_id,
        banned_by=current_user_id,
        ban_reason=reason_text,
        is_active=True
    )
    
    db.session.add(ban_record)
    db.session.commit()
    
    flash(f'User {user.name} has been banned for: {reason_text}', 'success')
    return redirect(url_for('admin.user_list'))

@admin.route('/unban_user/<int:user_id>')
@admin_required
def unban_user(user_id):
    """Enhanced unban with history tracking"""
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    
    # Update ban history - ENHANCED FEATURE
    active_ban = BanHistory.query.filter_by(user_id=user_id, is_active=True).first()
    if active_ban:
        active_ban.is_active = False
        active_ban.unbanned_at = datetime.now()
    
    db.session.commit()
    
    flash(f'User {user.name} has been unbanned.', 'success')
    return redirect(url_for('admin.user_list'))

@admin.route('/user_ban_history/<int:user_id>')
@admin_required
def user_ban_history(user_id):
    """View ban history for a user - NEW FEATURE"""
    user = User.query.get_or_404(user_id)
    ban_history = BanHistory.query.filter_by(user_id=user_id).order_by(
        BanHistory.banned_at.desc()
    ).all()
    
    return render_template('admin/ban_history.html', user=user, ban_history=ban_history)

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

# NEW FEATURE: Skill Description Moderation
@admin.route('/skill_descriptions')
@admin_required
def skill_descriptions():
    """Moderate skill descriptions - CORE MISSING FEATURE"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'pending')  # pending, approved, rejected, reported
    
    query = SkillDescription.query
    
    if status_filter == 'pending':
        query = query.filter_by(moderation_status='pending')
    elif status_filter == 'approved':
        query = query.filter_by(moderation_status='approved')
    elif status_filter == 'rejected':
        query = query.filter_by(moderation_status='rejected')
    elif status_filter == 'reported':
        query = query.filter_by(is_reported=True)
    
    descriptions = query.order_by(SkillDescription.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Count statistics for dashboard
    pending_count = SkillDescription.query.filter_by(moderation_status='pending').count()
    reported_count = SkillDescription.query.filter_by(is_reported=True).count()
    
    return render_template('admin/skill_descriptions.html', 
                         descriptions=descriptions, 
                         status_filter=status_filter,
                         pending_count=pending_count,
                         reported_count=reported_count)

@admin.route('/moderate_skill_description/<int:desc_id>/<action>', methods=['POST'])
@admin_required
def moderate_skill_description(desc_id, action):
    """Approve or reject skill description - CORE MISSING FEATURE"""
    if action not in ['approve', 'reject']:
        flash('Invalid action.', 'error')
        return redirect(url_for('admin.skill_descriptions'))
    
    description = SkillDescription.query.get_or_404(desc_id)
    current_user_id = session.get('user_id')
    
    # Get moderator notes if provided
    moderator_notes = request.form.get('moderator_notes', '')
    
    description.moderation_status = 'approved' if action == 'approve' else 'rejected'
    description.is_approved = action == 'approve'
    description.moderated_by = current_user_id
    description.moderated_at = datetime.now()
    description.moderator_notes = moderator_notes
    
    db.session.commit()
    
    flash(f'Skill description {action}ed successfully.', 'success')
    return redirect(url_for('admin.skill_descriptions'))

@admin.route('/mark_skill_description_reported/<int:desc_id>')
@admin_required
def mark_skill_description_reported(desc_id):
    """Mark a skill description as reported"""
    description = SkillDescription.query.get_or_404(desc_id)
    description.is_reported = True
    db.session.commit()
    
    flash('Skill description marked as reported.', 'warning')
    return redirect(url_for('admin.skill_descriptions'))

# ENHANCED Broadcasting and Notifications System
@admin.route('/notifications')
@admin_required
def notifications():
    """Manage platform notifications - ENHANCED FEATURE"""
    page = request.args.get('page', 1, type=int)
    
    notifications = PlatformNotification.query.order_by(
        PlatformNotification.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/notifications.html', notifications=notifications)

@admin.route('/create_notification', methods=['GET', 'POST'])
@admin_required
def create_notification():
    """Create platform-wide notification - NEW FEATURE"""
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        notification_type = request.form.get('notification_type', 'general')
        target_audience = request.form.get('target_audience', 'all')
        expires_at = request.form.get('expires_at')
        current_user_id = session.get('user_id')
        
        if not title or not message:
            flash('Title and message are required.', 'error')
            return render_template('admin/create_notification.html')
        
        notification = PlatformNotification(
            title=title,
            message=message,
            notification_type=notification_type,
            target_audience=target_audience,
            created_by=current_user_id,
            expires_at=datetime.fromisoformat(expires_at) if expires_at else None
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Calculate reach
        if target_audience == 'all':
            recipient_count = User.query.count()
        elif target_audience == 'active':
            recipient_count = User.query.filter_by(is_banned=False).count()
        elif target_audience == 'admins':
            recipient_count = User.query.filter_by(is_admin=True).count()
        else:
            recipient_count = 0
        
        flash(f'Notification created successfully. Will reach {recipient_count} users.', 'success')
        return redirect(url_for('admin.notifications'))
    
    return render_template('admin/create_notification.html')

@admin.route('/toggle_notification/<int:notification_id>')
@admin_required
def toggle_notification(notification_id):
    """Toggle notification active status"""
    notification = PlatformNotification.query.get_or_404(notification_id)
    notification.is_active = not notification.is_active
    db.session.commit()
    
    status = 'activated' if notification.is_active else 'deactivated'
    flash(f'Notification {status} successfully.', 'success')
    return redirect(url_for('admin.notifications'))

@admin.route('/delete_notification/<int:notification_id>')
@admin_required
def delete_notification(notification_id):
    """Delete a notification"""
    notification = PlatformNotification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    
    flash('Notification deleted successfully.', 'success')
    return redirect(url_for('admin.notifications'))

# Legacy broadcast route for compatibility
@admin.route('/broadcast', methods=['GET', 'POST'])
@admin_required
def broadcast():
    """Legacy broadcast - redirects to new notification system"""
    if request.method == 'POST':
        # Convert old format to new notification format
        return redirect(url_for('admin.create_notification'))
    
    return redirect(url_for('admin.notifications'))

# ENHANCED Reports and Analytics with ACTUAL Downloads
@admin.route('/download_user_report')
@admin_required
def download_user_report():
    """Download comprehensive user activity report - ENHANCED FEATURE"""
    try:
        users = User.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header with more detailed columns
        writer.writerow([
            'ID', 'Name', 'Email', 'Location', 'Is_Public', 'Is_Banned', 'Is_Admin',
            'Registration_Date', 'Last_Login', 'Offered_Skills', 'Wanted_Skills',
            'Swaps_Sent', 'Swaps_Received', 'Ban_Count', 'Active_Swaps'
        ])
        
        # Write data
        for user in users:
            offered_count = UserSkill.query.filter_by(user_id=user.id, type='offered').count()
            wanted_count = UserSkill.query.filter_by(user_id=user.id, type='wanted').count()
            swaps_sent = SwapRequest.query.filter_by(from_user_id=user.id).count()
            swaps_received = SwapRequest.query.filter_by(to_user_id=user.id).count()
            ban_count = BanHistory.query.filter_by(user_id=user.id).count()
            active_swaps = SwapRequest.query.filter(
                (SwapRequest.from_user_id == user.id) | (SwapRequest.to_user_id == user.id),
                SwapRequest.status == 'pending'
            ).count()
            
            writer.writerow([
                user.id, user.name, user.email, user.location or '',
                user.is_public, user.is_banned, user.is_admin,
                user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else '',
                user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else '',
                offered_count, wanted_count, swaps_sent, swaps_received,
                ban_count, active_swaps
            ])
        
        # Create file-like object for download
        output.seek(0)
        file_data = io.BytesIO()
        file_data.write(output.getvalue().encode('utf-8'))
        file_data.seek(0)
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'user_activity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        flash(f'Error generating user report: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin.route('/download_swap_report')
@admin_required
def download_swap_report():
    """Download enhanced swap statistics report - ENHANCED FEATURE"""
    try:
        swaps = SwapRequest.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Enhanced header with success metrics
        writer.writerow([
            'ID', 'Requester_Name', 'Requester_Email', 'Receiver_Name', 'Receiver_Email',
            'Offered_Skill', 'Wanted_Skill', 'Status', 'Created_Date', 'Days_Active',
            'Feedback_Count', 'Has_Rating', 'Success_Rate_Indicator'
        ])
        
        # Write enhanced data
        for swap in swaps:
            days_active = (datetime.now() - swap.created_at).days if swap.created_at else 0
            feedback_count = len(swap.feedback) if hasattr(swap, 'feedback') else 0
            has_rating = any(f.rating for f in swap.feedback) if hasattr(swap, 'feedback') else False
            success_indicator = 'SUCCESS' if swap.status == 'completed' else 'PENDING' if swap.status == 'pending' else 'FAILED'
            
            writer.writerow([
                swap.id, swap.requester.name, swap.requester.email,
                swap.receiver.name, swap.receiver.email,
                swap.offered_skill.name if swap.offered_skill else 'N/A',
                swap.wanted_skill.name if swap.wanted_skill else 'N/A',
                swap.status, swap.created_at.strftime('%Y-%m-%d %H:%M') if swap.created_at else '',
                days_active, feedback_count, 'Yes' if has_rating else 'No', success_indicator
            ])
        
        # Create file-like object for download
        output.seek(0)
        file_data = io.BytesIO()
        file_data.write(output.getvalue().encode('utf-8'))
        file_data.seek(0)
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'swap_statistics_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        flash(f'Error generating swap report: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))

@admin.route('/download_feedback_report')
@admin_required
def download_feedback_report():
    """Download comprehensive feedback logs report - ENHANCED FEATURE"""
    try:
        feedback_list = Feedback.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Enhanced header
        writer.writerow([
            'ID', 'Swap_ID', 'Reviewer_Name', 'Reviewer_Email', 'Rating', 'Comment',
            'Created_Date', 'Swap_Requester', 'Swap_Receiver', 'Swap_Status'
        ])
        
        # Write enhanced data
        for feedback in feedback_list:
            # Clean comment for CSV
            comment = feedback.comment.replace('\n', ' ').replace('\r', ' ') if feedback.comment else ''
            
            writer.writerow([
                feedback.id, feedback.swap_id,
                feedback.reviewer.name, feedback.reviewer.email,
                feedback.rating or 'N/A', comment,
                feedback.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(feedback, 'created_at') and feedback.created_at else '',
                feedback.swap.requester.name if feedback.swap else 'N/A',
                feedback.swap.receiver.name if feedback.swap else 'N/A',
                feedback.swap.status if feedback.swap else 'N/A'
            ])
        
        # Create file-like object for download
        output.seek(0)
        file_data = io.BytesIO()
        file_data.write(output.getvalue().encode('utf-8'))
        file_data.seek(0)
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'feedback_logs_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        flash(f'Error generating feedback report: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))
