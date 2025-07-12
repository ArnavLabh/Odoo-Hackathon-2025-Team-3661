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
    from models import User, Skill, UserSkill, SwapRequest, Feedback

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
