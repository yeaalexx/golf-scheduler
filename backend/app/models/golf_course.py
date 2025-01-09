from app import db

class GolfCourse(db.Model):
    __tablename__ = 'golf_course'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    teeitup_id = db.Column(db.String(64), unique=True)
    location = db.Column(db.String(200))
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='course', lazy=True) 