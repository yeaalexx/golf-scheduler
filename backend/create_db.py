import psycopg2
from psycopg2 import Error
import sys
from time import sleep

def execute_with_output(message, func):
    sys.stdout.write(f"Starting: {message}...\n")
    sys.stdout.flush()
    sleep(0.1)  # Small delay to ensure output is visible
    result = func()
    sys.stdout.write(f"Completed: {message}\n")
    sys.stdout.flush()
    sleep(0.1)
    return result

def main():
    try:
        execute_with_output("Connecting to PostgreSQL", lambda: None)
        connection = psycopg2.connect(
            user="postgres",
            password="Abcs8768",
            host="localhost",
            database="golf_scheduler"
        )

        cursor = connection.cursor()
        
        # Create Users table
        execute_with_output("Creating Users table", lambda: 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(64) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(128)
                );
            """)
        )

        # Create Golf Courses table
        execute_with_output("Creating Golf Courses table", lambda:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS golf_courses (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(120) NOT NULL,
                    teeitup_id VARCHAR(64) UNIQUE,
                    location VARCHAR(200)
                );
            """)
        )

        # Create Bookings table
        execute_with_output("Creating Bookings table", lambda:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    golf_course_id INTEGER REFERENCES golf_courses(id),
                    tee_time TIMESTAMP NOT NULL,
                    players INTEGER DEFAULT 1,
                    status VARCHAR(20) DEFAULT 'pending'
                );
            """)
        )

        # Commit the changes
        execute_with_output("Committing changes", lambda: connection.commit())

        # Verify tables exist
        execute_with_output("Verifying tables", lambda: 
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
        )
        
        tables = cursor.fetchall()
        sys.stdout.write(f"Created tables: {tables}\n")
        sys.stdout.flush()

    except (Exception, Error) as error:
        sys.stderr.write(f"Error: {error}\n")
        sys.stderr.flush()
        raise error

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
            execute_with_output("Closing database connection", lambda: None)

if __name__ == "__main__":
    sys.stdout.write("Starting database creation...\n")
    sys.stdout.flush()
    main()
    sys.stdout.write("Database creation completed!\n")
    sys.stdout.flush() 