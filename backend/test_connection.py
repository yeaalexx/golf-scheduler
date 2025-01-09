import psycopg2
import os
from dotenv import load_dotenv

print("Starting database connection test...")

try:
    # Load environment variables
    load_dotenv()
    print("Environment variables loaded")

    # Get database URL
    db_url = os.getenv('DATABASE_URL')
    print(f"Database URL: {db_url}")

    # Parse the URL
    # postgresql://postgres:Abcs8768@localhost/golf_scheduler
    user = "postgres"
    password = "Abcs8768"
    host = "localhost"
    database = "golf_scheduler"

    print(f"Attempting to connect to database: {database}")
    
    # Try to connect
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host
    )
    
    print("Successfully connected to database!")
    
    # Create a cursor
    cur = conn.cursor()
    
    # List all tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = cur.fetchall()
    print("Existing tables:", tables)
    
    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed successfully")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    raise e

print("Test completed!") 