#!/usr/bin/env python3
"""
Test script for RF_Lupa-Wak! API
"""

import requests
import json
import sys

def test_health_check(base_url):
    """Test health check endpoint"""
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check failed: {e}")
        return False

def test_prediction(base_url):
    """Test prediction endpoint"""
    # Sample data
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
        "total_sks_tidak_lulus": 6
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        print(f"✅ Prediction: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_invalid_data(base_url):
    """Test with invalid data"""
    invalid_data = {
        "ips_1": 3.5,
        "ips_2": 3.2,
        # Missing required fields
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(invalid_data)
        )
        print(f"✅ Invalid Data Test: {response.status_code} (expected 400)")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Invalid data test failed: {e}")
        return False

def main():
    # Default to localhost if no URL provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print(f"🧪 Testing RF_Lupa-Wak! API at: {base_url}")
    print("=" * 50)
    
    tests = [
        ("Health Check", lambda: test_health_check(base_url)),
        ("Prediction", lambda: test_prediction(base_url)),
        ("Invalid Data", lambda: test_invalid_data(base_url))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 