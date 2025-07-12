from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Import models after db initialization to avoid circular imports
    from models import (
        User, Skill, UserSkill, SwapRequest, Feedback,
        SkillDescription, BanHistory, PlatformNotification
    )

    # Register blueprints
    from routes import main
    from swap_routes import swaps
    from admin_routes import admin
    from api_routes import api
    from google_auth import auth, init_oauth
    
    app.register_blueprint(main)
    app.register_blueprint(swaps, url_prefix='/swaps')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api)
    app.register_blueprint(auth)
    
    # Initialize OAuth
    init_oauth(app)

    # Add template helpers to avoid routing errors
    @app.context_processor
    def inject_helpers():
        from routing_helpers import safe_url_for, route_exists
        return {
            'safe_url_for': safe_url_for,
            'route_exists': route_exists
        }

    # Add health check route
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Skill Swap Platform is running!'}, 200

    # Error handlers to avoid werkzeug errors in templates
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Handle routing build errors
    @app.errorhandler(Exception)
    def handle_routing_error(error):
        from flask import render_template, request
        # Check if it's a werkzeug routing build error
        error_str = str(type(error))
        if 'BuildError' in error_str or 'werkzeug' in error_str.lower():
            app.logger.error(f"Routing error suppressed: {error}")
            # Return a safe page instead of crashing
            try:
                return render_template('404.html'), 404
            except:
                return '<h1>Page Not Found</h1><p>The requested page could not be found.</p>', 404
        # Re-raise other exceptions
        raise error

    # Only create tables if not in production or if DATABASE_URL is SQLite
    with app.app_context():
        try:
            # Check if we're using SQLite (local development)
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI'].lower():
                db.create_all()

                # --- DEMO USERS AND SKILLS ---
                from models import User, Skill, UserSkill
                if User.query.count() < 5:  # Only add if not already present
                    # Add default admin user
                    admin_email = "admin@skillswap.com"
                    admin_user = User.query.filter_by(email=admin_email).first()
                    if not admin_user:
                        from auth_helpers import hash_password
                        admin_password = "admin123"
                        try:
                            admin_hash = hash_password(admin_password)
                            admin_user = User(name="Admin", email=admin_email, password_hash=admin_hash, is_admin=True, is_public=False)
                            db.session.add(admin_user)
                            db.session.commit()
                            print(f"✅ Admin user created: {admin_email} / {admin_password}")
                        except Exception as e:
                            print(f"❌ Error creating admin user: {e}")
                    else:
                        # Check if admin user has proper bcrypt hash
                        if admin_user.password_hash and not admin_user.password_hash.startswith('$2b$'):
                            from auth_helpers import hash_password
                            admin_password = "admin123"
                            admin_user.password_hash = hash_password(admin_password)
                            db.session.commit()
                            print(f"🔧 Admin password hash updated to bcrypt format")

                    demo_users = [
                        {"name": "Alice Smith", "email": "alice@example.com", "skills": ["Python", "Flask", "Public Speaking"]},
                        {"name": "Bob Johnson", "email": "bob@example.com", "skills": ["JavaScript", "React", "Cooking"]},
                        {"name": "Charlie Lee", "email": "charlie@example.com", "skills": ["Java", "Spring Boot", "Photography"]},
                        {"name": "Diana Patel", "email": "diana@example.com", "skills": ["C++", "Algorithms", "Creative Writing"]},
                        {"name": "Ethan Brown", "email": "ethan@example.com", "skills": ["HTML", "CSS", "Project Management"]},
                        {"name": "Fiona Green", "email": "fiona@example.com", "skills": ["Python", "Machine Learning", "Pandas"]},
                        {"name": "George White", "email": "george@example.com", "skills": ["Go", "Docker", "Kubernetes"]},
                        {"name": "Hannah Black", "email": "hannah@example.com", "skills": ["Ruby", "Rails", "PostgreSQL"]},
                        {"name": "Ivan Grey", "email": "ivan@example.com", "skills": ["PHP", "Laravel", "MySQL"]},
                        {"name": "Julia Blue", "email": "julia@example.com", "skills": ["Swift", "iOS", "Xcode"]},
                        {"name": "Kevin Red", "email": "kevin@example.com", "skills": ["C#", ".NET", "Azure"]},
                        {"name": "Lily Violet", "email": "lily@example.com", "skills": ["JavaScript", "Vue.js", "Firebase"]},
                        {"name": "Mike Orange", "email": "mike@example.com", "skills": ["Python", "Django", "REST API"]},
                        {"name": "Nina Yellow", "email": "nina@example.com", "skills": ["R", "Statistics", "Data Science"]},
                        {"name": "Oscar Pink", "email": "oscar@example.com", "skills": ["Scala", "Akka", "Spark"]},
                        {"name": "Priya Sharma", "email": "priya@example.com", "skills": ["Yoga", "Mindfulness", "HTML"]},
                        {"name": "Rahul Mehta", "email": "rahul@example.com", "skills": ["Public Speaking", "Python", "Leadership"]},
                        {"name": "Sara Lee", "email": "sara@example.com", "skills": ["Painting", "JavaScript", "React"]},
                        {"name": "Tom Brown", "email": "tom@example.com", "skills": ["Gardening", "C++", "Algorithms"]},
                        {"name": "Uma Kapoor", "email": "uma@example.com", "skills": ["Cooking", "Project Management", "CSS"]},
                    ]
                    # Create all unique skills
                    all_skills = set(skill for user in demo_users for skill in user["skills"])
                    skill_objs = {}
                    for skill_name in all_skills:
                        skill = Skill.query.filter_by(name=skill_name).first()
                        if not skill:
                            skill = Skill(name=skill_name)
                            db.session.add(skill)
                        skill_objs[skill_name] = skill
                    db.session.commit()
                    # Create users and assign skills
                    for user in demo_users:
                        u = User(name=user["name"], email=user["email"], password_hash=None)
                        db.session.add(u)
                        db.session.commit()  # Commit to get user.id
                        for skill_name in user["skills"]:
                            us = UserSkill(user_id=u.id, skill_id=skill_objs[skill_name].id, type="offered")
                            db.session.add(us)
                    db.session.commit()
                # --- END DEMO USERS ---
            else:
                # For production databases, we assume tables exist
                # You should run migrations separately
                pass
        except Exception as e:
            # Log the error but don't crash the app
            app.logger.error(f"Database initialization error: {e}")

    return app

# Create the app instance for Vercel
app = create_app()

# For local development
if __name__ == "__main__":
    app.run(debug=True)
