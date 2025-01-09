from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    teeitup_username = db.Column(db.String(64))
    teeitup_password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
        
    def has_teeitup_credentials(self):
        """Check if user has TeeitUp credentials set"""
        return bool(self.teeitup_username and self.teeitup_password)
        
    def set_teeitup_credentials(self, username, password):
        """Set TeeitUp credentials"""
        self.teeitup_username = username
        self.teeitup_password = password
        
    def remove_teeitup_credentials(self):
        """Remove TeeitUp credentials"""
        self.teeitup_username = None
        self.teeitup_password = None 