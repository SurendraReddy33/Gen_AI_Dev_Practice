"""
Test script to verify the login endpoint works correctly
"""

import requests
import json

def test_login():
    url = "http://127.0.0.1:8000/user/login"
    
    # Test data
    test_data = {
        "username": "bhaskar@gmail.com",
        "password": "Bhaskar@1"
    }
    
    # Headers for form data
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        print("Testing login endpoint...")
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
        else:
            print("❌ Login failed")
            if response.status_code == 422:
                print("This suggests the form data format is incorrect")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the FastAPI server is running with:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
