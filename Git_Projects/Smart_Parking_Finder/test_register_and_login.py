"""
Test script to register a user first, then test login
"""

import requests
import json

def test_register():
    url = "http://127.0.0.1:8000/user/register"
    
    # Test user data
    user_data = {
        "username": "bhaskar",
        "email": "bhaskar@gmail.com",
        "phone": "1234567890",
        "password": "Bhaskar@1"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing user registration...")
        print(f"URL: {url}")
        print(f"Data: {user_data}")
        
        # Send POST request
        response = requests.post(url, json=user_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ User registered successfully!")
            return True
        elif response.status_code == 409:
            print("ℹ️ User already exists, proceeding to login test")
            return True
        else:
            print("❌ Registration failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    url = "http://127.0.0.1:8000/user/login"
    
    # Test data
    test_data = {
        "username": "bhaskar@gmail.com",  # Using email as username
        "password": "Bhaskar@1"
    }
    
    # Headers for form data
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        print("\nTesting login endpoint...")
        print(f"URL: {url}")
        print(f"Data: {test_data}")
        
        # Send POST request
        response = requests.post(url, data=test_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            print(f"Access Token: {token_data.get('access_token')}")
            return True
        else:
            print("❌ Login failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # First try to register, then login
    if test_register():
        test_login()
