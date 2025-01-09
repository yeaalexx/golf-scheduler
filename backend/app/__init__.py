from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    
    # Handle unauthorized access
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Import models
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app 