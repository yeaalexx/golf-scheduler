from app import create_app, db
from app.models import User, Booking, GolfCourse
from sqlalchemy import inspect

def init_database():
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")
        
        # Verify tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")

if __name__ == "__main__":
    init_database() 