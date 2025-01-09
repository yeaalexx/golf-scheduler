import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

print("Starting script...", flush=True)  # Debug line

try:
    # Load environment variables
    load_dotenv()
    print("Environment variables loaded", flush=True)

    # Create Flask app
    app = Flask(__name__)
    print("Flask app created", flush=True)

    # Print environment variables (for debugging)
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}", flush=True)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("Database configured", flush=True)

    # Initialize database
    db = SQLAlchemy(app)
    print("SQLAlchemy initialized", flush=True)

    # Define models
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

    class GolfCourse(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable=False)
        teeitup_id = db.Column(db.String(64), unique=True)
        location = db.Column(db.String(200))

    class Booking(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        golf_course_id = db.Column(db.Integer, db.ForeignKey('golf_course.id'), nullable=False)
        tee_time = db.Column(db.DateTime, nullable=False)

    print("Models defined", flush=True)

    # Create tables
    with app.app_context():
        print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}", flush=True)
        print("Creating tables...", flush=True)
        db.create_all()
        print("Tables created successfully!", flush=True)
        
        # Verify tables
        tables = db.engine.table_names()
        print(f"Created tables: {tables}", flush=True)

except Exception as e:
    print(f"An error occurred: {str(e)}", file=sys.stderr, flush=True)
    print(f"Error type: {type(e)}", file=sys.stderr, flush=True)
    raise e

print("Script completed!", flush=True) 