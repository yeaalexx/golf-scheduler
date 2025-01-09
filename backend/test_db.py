from app import create_app, db
from app.models.user import User
from app.models.golf_course import GolfCourse
from app.models.booking import Booking

def test_database():
    app = create_app()
    with app.app_context():
        try:
            # Create tables
            db.create_all()
            print("✅ Tables created successfully!")

            # Test creating a golf course
            test_course = GolfCourse(
                name="Test Golf Course",
                teeitup_id="TEST123",
                location="Test Location"
            )
            db.session.add(test_course)
            db.session.commit()
            print("✅ Added test golf course successfully!")

            # Query the golf course
            course = GolfCourse.query.filter_by(name="Test Golf Course").first()
            print(f"✅ Retrieved golf course: {course.name}")

            # Clean up test data
            db.session.delete(course)
            db.session.commit()
            print("✅ Cleaned up test data successfully!")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

        return True

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n🎉 Database test completed successfully!")
    else:
        print("\n❌ Database test failed!") 