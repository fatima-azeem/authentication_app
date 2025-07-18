#!/usr/bin/env python3
"""
Test script for the resend functionality
"""

import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"
API_KEY = "PYHXCbfqwdER19IcyHJxpImJgIchKxlziNyvP59lWVk="

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def test_registration_and_resend():
    """Test complete flow: registration -> resend email verification"""
    
    # Generate unique email for testing
    timestamp = int(time.time())
    test_email = f"test_{timestamp}@example.com"
    
    print(f"Testing with email: {test_email}")
    
    # Step 1: Register user
    print("\n1. Registering user...")
    register_data = {
        "email": test_email,
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "full_name": "Test User",
        "is_term_accepted": True
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data, headers=headers)
    print(f"Registration response: {response.status_code}")
    if response.status_code == 201:
        print("✅ Registration successful")
    else:
        print(f"❌ Registration failed: {response.text}")
        return False
    
    # Step 2: Try to resend email verification
    print("\n2. Testing resend email verification...")
    resend_data = {"email": test_email}
    
    response = requests.post(f"{BASE_URL}/resend-email-verification-otp", json=resend_data, headers=headers)
    print(f"Resend email verification response: {response.status_code}")
    if response.status_code == 204:
        print("✅ Resend email verification successful")
    else:
        print(f"❌ Resend email verification failed: {response.text}")
        return False
    
    # Step 3: Test password reset request
    print("\n3. Testing password reset request...")
    password_reset_data = {"email": test_email}
    
    response = requests.post(f"{BASE_URL}/request-password-reset", json=password_reset_data, headers=headers)
    print(f"Password reset request response: {response.status_code}")
    if response.status_code == 204:
        print("✅ Password reset request successful")
    else:
        print(f"❌ Password reset request failed: {response.text}")
        return False
    
    # Step 4: Test resend password reset OTP
    print("\n4. Testing resend password reset OTP...")
    
    response = requests.post(f"{BASE_URL}/resend-password-reset-otp", json=resend_data, headers=headers)
    print(f"Resend password reset OTP response: {response.status_code}")
    if response.status_code == 204:
        print("✅ Resend password reset OTP successful")
    else:
        print(f"❌ Resend password reset OTP failed: {response.text}")
        return False
    
    print("\n🎉 All tests passed! Resend functionality is working correctly.")
    return True

if __name__ == "__main__":
    test_registration_and_resend()
