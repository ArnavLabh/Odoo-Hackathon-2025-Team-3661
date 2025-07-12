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
