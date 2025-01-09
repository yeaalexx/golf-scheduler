import os
import sys
from pathlib import Path

def print_header(message):
    print(f"\n{'='*20} {message} {'='*20}")

def check_file_exists(filepath, required=True):
    exists = os.path.exists(filepath)
    print(f"{'✅' if exists else '❌'} {filepath} {'(Required)' if required else '(Optional)'}")
    if required and not exists:
        return False
    return True

def check_file_content(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if len(content.strip()) > 0:
                print(f"✅ {filepath} has content")
                return True
            else:
                print(f"❌ {filepath} is empty")
                return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {str(e)}")
        return False

def main():
    print_header("Checking Project Structure")
    
    # Required directories
    directories = [
        'app',
        'app/models',
        'app/routes',
    ]
    
    # Required files
    required_files = [
        'app/__init__.py',
        'app/models/__init__.py',
        'app/models/user.py',
        'app/models/booking.py',
        'app/models/golf_course.py',
        'app/routes/__init__.py',
        'app/routes/auth.py',
        'config.py',
        'wsgi.py',
        'init_db.py',
        'test_endpoints.py',
    ]
    
    # Optional files
    optional_files = [
        '.env',
        'requirements.txt',
    ]
    
    # Check directories
    print("\nChecking Directories:")
    for directory in directories:
        if not check_file_exists(directory):
            print(f"\n❌ Critical directory missing: {directory}")
            sys.exit(1)
    
    # Check required files
    print("\nChecking Required Files:")
    for filepath in required_files:
        if check_file_exists(filepath):
            check_file_content(filepath)
    
    # Check optional files
    print("\nChecking Optional Files:")
    for filepath in optional_files:
        if check_file_exists(filepath, required=False):
            check_file_content(filepath)
    
    # Generate requirements.txt if missing
    print("\nChecking/Generating requirements.txt...")
    os.system('pip freeze > requirements.txt')
    print("✅ requirements.txt updated")
    
    print_header("Project Verification Complete")
    print("\nNext steps:")
    print("1. Run 'python init_db.py' to ensure database is initialized")
    print("2. Run 'python test_endpoints.py' to verify all endpoints work")
    print("3. Start the server with 'python -m flask run' to test manually")

if __name__ == "__main__":
    main() 