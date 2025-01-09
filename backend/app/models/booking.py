from app import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    golf_course_id = db.Column(db.Integer, db.ForeignKey('golf_course.id'), nullable=False)
    tee_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending') 