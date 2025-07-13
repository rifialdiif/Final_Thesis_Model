#!/usr/bin/env python3
"""
Test script for the Prediction API
Run this script to test the API endpoints
"""

import requests
import json

def test_health_check(base_url):
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction(base_url):
    """Test the prediction endpoint"""
    print("\n🔍 Testing prediction endpoint...")
    
    # Sample data for testing
    test_data = {
        "ips_1": 3.5,
        "ips_2": 3.2,
        "ips_3": 3.8,
        "ips_4": 3.6,
        "cuti_1": "aktif",
        "cuti_2": "aktif",
        "cuti_3": "aktif",
        "cuti_4": "aktif",
        "total_sks_ditempuh": 120,
        "total_sks_tidak_lulus": 0
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function to run all tests"""
    print("🧪 Starting API tests...")
    
    # Replace with your actual API URL after deployment
    base_url = input("Enter your API URL (e.g., https://prediction-api-xxx-xx.a.run.app): ").strip()
    
    if not base_url:
        print("❌ No URL provided. Exiting.")
        return
    
    # Remove trailing slash if present
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    print(f"🌐 Testing API at: {base_url}")
    
    # Run tests
    health_success = test_health_check(base_url)
    prediction_success = test_prediction(base_url)
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"Health Check: {'✅ PASS' if health_success else '❌ FAIL'}")
    print(f"Prediction: {'✅ PASS' if prediction_success else '❌ FAIL'}")
    
    if health_success and prediction_success:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check your deployment.")

if __name__ == "__main__":
    main() 