import requests
import json

def test_health_check(base_url):
    """Test health check endpoint"""
    try:
        response = requests.get(f"{base_url}/")
        print("🔍 Health Check Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_prediction(base_url):
    """Test prediction endpoint"""
    test_data = {
        "ips_1": 2.67,
    "ips_2": 3.03,
    "ips_3": 3.11,
    "ips_4": 3.45,
    "cuti_1": "aktif",
    "cuti_2": "aktif",
    "cuti_3": "aktif",
    "cuti_4": "aktif",
    "total_sks_ditempuh": 73,
    "total_sks_tidak_lulus": 0
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        print("🎯 Prediction Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {test_data}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
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
        print("⚠️ Invalid Data Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Invalid data test failed: {e}")
        return False

if __name__ == "__main__":
    # For local testing
    base_url = "http://localhost:8080"
    
    print("🧪 Testing ML Model API")
    print("=" * 50)
    
    # Test health check
    health_ok = test_health_check(base_url)
    
    # Test prediction
    prediction_ok = test_prediction(base_url)
    
    # Test invalid data
    invalid_ok = test_invalid_data(base_url)
    
    print("📊 Test Results:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Prediction: {'✅ PASS' if prediction_ok else '❌ FAIL'}")
    print(f"Invalid Data: {'✅ PASS' if invalid_ok else '❌ FAIL'}")
    
    if health_ok and prediction_ok and invalid_ok:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed!") 