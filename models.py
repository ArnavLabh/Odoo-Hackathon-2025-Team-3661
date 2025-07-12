from datetime import datetime
from app import db

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)  # Allow null for OAuth users
    location = db.Column(db.String(100))
    photo_url = db.Column(db.String(200))
    availability = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    
    # OAuth fields
    google_id = db.Column(db.String(50), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now)
    
    # Password reset fields
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    skills = db.relationship('UserSkill', backref='user', lazy=True)
    sent_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.from_user_id', backref='requester', lazy=True)
    received_requests = db.relationship('SwapRequest', foreign_keys='SwapRequest.to_user_id', backref='receiver', lazy=True)
    
    def has_password(self):
        """Check if user has a password set"""
        return bool(self.password_hash)
    
    def is_oauth_user(self):
        """Check if user registered via OAuth"""
        return bool(self.google_id)
        
    def get_offered_skills(self):
        """Get all skills offered by the user"""
        return [us.skill for us in self.skills if us.type == 'offered']
        
    def get_wanted_skills(self):
        """Get all skills wanted by the user"""
        return [us.skill for us in self.skills if us.type == 'wanted']
        
    def get_average_rating(self):
        """Calculate the user's average rating from feedback"""
        try:
            from sqlalchemy import func
            
            # Get all feedback where this user was involved in the swap
            result = db.session.query(func.avg(Feedback.rating))\
                .join(SwapRequest, ((SwapRequest.from_user_id == self.id) | (SwapRequest.to_user_id == self.id)))\
                .filter(Feedback.reviewer_id != self.id)\
                .scalar()
                
            return result or 0.0
        except Exception as e:
            print(f"Error calculating average rating: {e}")
            return 0.0
        
    def get_completed_swaps_count(self):
        """Count the number of completed swaps for this user"""
        try:
            count = db.session.query(SwapRequest)\
                .filter(((SwapRequest.from_user_id == self.id) | (SwapRequest.to_user_id == self.id)) & 
                       (SwapRequest.status == 'completed'))\
                .count()
                
            return count
        except Exception as e:
            print(f"Error counting completed swaps: {e}")
            return 0

# Skill Table
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# UserSkill Table
class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'offered' or 'wanted'
    skill = db.relationship('Skill')

# SwapRequest Table
class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offered_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    wanted_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    status = db.Column(db.String(20), default='pending')  # pending / accepted / rejected / cancelled
    created_at = db.Column(db.DateTime, default=datetime.now)

    offered_skill = db.relationship('Skill', foreign_keys=[offered_skill_id], lazy=True, backref='offered_requests')
    wanted_skill = db.relationship('Skill', foreign_keys=[wanted_skill_id], lazy=True, backref='wanted_requests')

# Feedback Table
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swap_id = db.Column(db.Integer, db.ForeignKey('swap_request.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1 to 5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    swap = db.relationship('SwapRequest', backref='feedback')
    reviewer = db.relationship('User', backref='given_feedback')

# Admin Enhancement Models

class SkillDescription(db.Model):
    """For moderating skill descriptions - Key missing feature"""
    __tablename__ = 'skill_description'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_reported = db.Column(db.Boolean, default=False)
    moderation_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.now)
    moderated_at = db.Column(db.DateTime, nullable=True)
    moderated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    moderator_notes = db.Column(db.Text, nullable=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='skill_descriptions')
    skill = db.relationship('Skill', backref='descriptions')
    moderator = db.relationship('User', foreign_keys=[moderated_by])

class BanHistory(db.Model):
    """Track ban history - Another missing feature"""
    __tablename__ = 'ban_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    banned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ban_reason = db.Column(db.Text, nullable=False)
    banned_at = db.Column(db.DateTime, default=datetime.now)
    unbanned_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='ban_history')
    admin = db.relationship('User', foreign_keys=[banned_by])

class PlatformNotification(db.Model):
    """Enhanced broadcasting system"""
    __tablename__ = 'platform_notification'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default='general')  # maintenance, security, feature, general
    target_audience = db.Column(db.String(20), default='all')  # all, active, admins
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=True)

    creator = db.relationship('User', backref='notifications_created')
