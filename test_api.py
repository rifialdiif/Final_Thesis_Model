import requests
import json

def test_api(url):
    """Test the prediction API"""
    
    # Test data
    test_data = {
        "ips_1": 3.5,
        "ips_2": 3.2,
        "ips_3": 3.8,
        "ips_4": 3.6,
        "cuti_1": "aktif",
        "cuti_2": "aktif",
        "cuti_3": "aktif",
        "cuti_4": "aktif",
        "total_sks_ditempuh": 144,
        "total_sks_tidak_lulus": 0
    }
    
    try:
        # Test home endpoint
        print("🏠 Testing home endpoint...")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test prediction endpoint
        print("🔮 Testing prediction endpoint...")
        response = requests.post(f"{url}/predict", json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Replace with your actual Cloud Run URL
    api_url = "https://prediksi-kelulusan-api-xxxxx-xx.a.run.app"
    print(f"🧪 Testing API at: {api_url}")
    test_api(api_url) 