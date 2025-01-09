from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': {'username': user.username, 'email': user.email}
        }), 201
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user, remember=True)
            return jsonify({
                'message': 'Logged in successfully',
                'user': {'username': user.username, 'email': user.email}
            })
        
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    try:
        if not current_user.is_authenticated:
            return jsonify({'error': 'Not authenticated'}), 401
        
        return jsonify({
            'user': {
                'username': current_user.username,
                'email': current_user.email,
                'has_teeitup': current_user.has_teeitup_credentials(),
                'teeitup_username': current_user.teeitup_username if current_user.has_teeitup_credentials() else None
            }
        })
    except Exception as e:
        print(f"Get current user error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/teeitup-credentials', methods=['POST', 'PUT', 'DELETE'])
@login_required
def manage_teeitup_credentials():
    """Manage TeeitUp credentials for the current user"""
    try:
        if request.method in ['POST', 'PUT']:
            data = request.get_json()
            
            if not all(k in data for k in ['username', 'password']):
                return jsonify({'error': 'Missing TeeitUp credentials'}), 400
            
            # Update the user's TeeitUp credentials
            current_user.set_teeitup_credentials(data['username'], data['password'])
            db.session.commit()
            
            return jsonify({
                'message': 'TeeitUp credentials updated successfully',
                'user': {
                    'username': current_user.username,
                    'email': current_user.email,
                    'has_teeitup': current_user.has_teeitup_credentials(),
                    'teeitup_username': current_user.teeitup_username
                }
            })
            
        elif request.method == 'DELETE':
            # Remove TeeitUp credentials
            current_user.remove_teeitup_credentials()
            db.session.commit()
            
            return jsonify({
                'message': 'TeeitUp credentials removed successfully',
                'user': {
                    'username': current_user.username,
                    'email': current_user.email,
                    'has_teeitup': False,
                    'teeitup_username': None
                }
            })
            
    except Exception as e:
        print(f"Error managing TeeitUp credentials: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 