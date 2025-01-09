import requests

BASE_URL = 'http://localhost:5000/auth'

def test_registration():
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print('Registration response:', response.json())
    return response.json()

def test_login():
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = requests.post(f'{BASE_URL}/login', json=data)
    print('Login response:', response.json())
    return response.json()

if __name__ == '__main__':
    print('Testing registration...')
    test_registration()
    print('\nTesting login...')
    test_login() 