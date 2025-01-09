import requests
import json

BASE_URL = 'http://localhost:5000/auth'
session = requests.Session()

def test_register():
    print("\nTesting Registration...")
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    try:
        response = session.post(f'{BASE_URL}/register', json=data)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_login():
    print("\nTesting Login...")
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    try:
        response = session.post(f'{BASE_URL}/login', json=data)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_get_me():
    print("\nTesting Get Current User...")
    try:
        response = session.get(f'{BASE_URL}/me')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_set_teeitup_credentials():
    print("\nTesting Set TeeitUp Credentials...")
    data = {
        'username': 'teeitup_user',
        'password': 'teeitup_pass123'
    }
    try:
        response = session.post(f'{BASE_URL}/teeitup-credentials', json=data)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_verify_teeitup_credentials():
    print("\nVerifying TeeitUp Credentials Set...")
    try:
        response = session.get(f'{BASE_URL}/me')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_logout():
    print("\nTesting Logout...")
    try:
        response = session.get(f'{BASE_URL}/logout')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_update_teeitup_credentials():
    print("\nTesting Update TeeitUp Credentials...")
    data = {
        'username': 'updated_teeitup_user',
        'password': 'updated_pass123'
    }
    try:
        response = session.put(f'{BASE_URL}/teeitup-credentials', json=data)
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

def test_remove_teeitup_credentials():
    print("\nTesting Remove TeeitUp Credentials...")
    try:
        response = session.delete(f'{BASE_URL}/teeitup-credentials')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        return response.json() if response.text else None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

if __name__ == '__main__':
    # Test full flow
    test_register()
    test_login()
    test_get_me()  # Should show has_teeitup: false
    test_set_teeitup_credentials()
    test_verify_teeitup_credentials()  # Should show has_teeitup: true
    test_update_teeitup_credentials()  # Update credentials
    test_verify_teeitup_credentials()  # Should show updated username
    test_remove_teeitup_credentials()  # Remove credentials
    test_verify_teeitup_credentials()  # Should show has_teeitup: false
    test_logout()