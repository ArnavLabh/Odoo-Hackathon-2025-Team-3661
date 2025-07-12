from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    babel.init_app(app)

    # Import models after db initialization to avoid circular imports
    from models import User, Skill, UserSkill, SwapRequest, Feedback

    # Register blueprints
    from routes import main
    from swap_routes import swaps
    from admin_routes import admin
    from api_routes import api
    
    app.register_blueprint(main)
    app.register_blueprint(swaps, url_prefix='/swaps')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
