"""
Test script to verify authentication endpoints work correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("\n1. Testing SIGNUP...")
    signup_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    print(f"   Status Code: {response.status_code}")

    if response.status_code == 201:
        data = response.json()
        print(f"   Success! User created:")
        print(f"   - Email: {data['user']['email']}")
        print(f"   - User ID: {data['user']['external_id']}")
        print(f"   - Token Type: {data['token_type']}")
        print(f"   - Access Token: {data['access_token'][:50]}...")
        return data
    else:
        print(f"   Error: {response.text}")
        return None

def test_signin(email, password):
    """Test user signin"""
    print("\n2. Testing SIGNIN...")
    signin_data = {
        "email": email,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    print(f"   Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   Success! User signed in:")
        print(f"   - Email: {data['user']['email']}")
        print(f"   - User ID: {data['user']['external_id']}")
        print(f"   - Access Token: {data['access_token'][:50]}...")
        return data
    else:
        print(f"   Error: {response.text}")
        return None

def test_protected_endpoint(token, user_id):
    """Test accessing a protected endpoint with JWT token"""
    print("\n3. Testing PROTECTED ENDPOINT...")
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Test creating a task (protected endpoint)
    task_data = {
        "title": "Test Task from Auth",
        "description": "This task was created using JWT authentication",
        "user_id": user_id
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/users/{user_id}/tasks",
        json=task_data,
        headers=headers
    )

    print(f"   Status Code: {response.status_code}")

    if response.status_code in [200, 201]:
        data = response.json()
        print(f"   Success! Task created:")
        print(f"   - Task ID: {data.get('id')}")
        print(f"   - Title: {data.get('title')}")
        return True
    else:
        print(f"   Error: {response.text}")
        return False

def test_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    print("\n4. Testing INVALID TOKEN...")
    headers = {
        "Authorization": "Bearer invalid_token_here"
    }

    response = requests.get(
        f"{BASE_URL}/api/v1/users/some-user-id/tasks",
        headers=headers
    )

    print(f"   Status Code: {response.status_code}")
    if response.status_code == 401:
        print("   Success! Invalid token correctly rejected")
        return True
    else:
        print(f"   Unexpected response: {response.text}")
        return False

def main():
    """Run all authentication tests"""
    print("=" * 60)
    print("AUTHENTICATION SYSTEM TEST")
    print("=" * 60)

    # Test signup
    signup_result = test_signup()
    if not signup_result:
        print("\nSignup failed. Cannot continue tests.")
        return

    email = signup_result['user']['email']
    password = "testpassword123"
    user_id = signup_result['user']['external_id']

    # Test signin
    signin_result = test_signin(email, password)
    if not signin_result:
        print("\nSignin failed. Cannot continue tests.")
        return

    token = signin_result['access_token']

    # Test protected endpoint
    test_protected_endpoint(token, user_id)

    # Test invalid token
    test_invalid_token()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the backend server.")
        print("Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
