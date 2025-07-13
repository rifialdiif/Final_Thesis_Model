#!/usr/bin/env python3
"""
Contoh penggunaan RF_Lupa-Wak! API
"""

import requests
import json
import time

# Base URL - ganti dengan URL API Anda setelah deployment
BASE_URL = "http://localhost:5000"  # Untuk testing lokal
# BASE_URL = "https://rf-lupa-wak-api-xxxxx-xx.a.run.app"  # Untuk production

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n📊 Testing Metrics...")
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Uptime: {data['uptime_seconds']} seconds")
        print(f"Total Requests: {data['total_requests']}")
        print(f"Success Rate: {data['success_rate']}%")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_docs():
    """Test documentation endpoint"""
    print("\n📚 Testing Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"API Name: {data['api_name']}")
        print(f"Version: {data['version']}")
        print(f"Description: {data['description']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction(data, expected_label=None):
    """Test prediction endpoint"""
    print(f"\n🎯 Testing Prediction...")
    print(f"Input Data: {json.dumps(data, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=data
        )
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.3f}s")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['label']}")
            print(f"Confidence: {result['confidence_score']}")
            print(f"API Response Time: {result['response_time']}s")
            
            if expected_label:
                success = result['label'] == expected_label
                print(f"✅ Expected: {expected_label}, Got: {result['label']}")
                return success
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 RF_Lupa-Wak! API Testing")
    print("=" * 50)
    
    # Test basic endpoints
    tests = [
        ("Health Check", test_health_check),
        ("Metrics", test_metrics),
        ("Documentation", test_docs)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        test_func()
    
    # Test prediction scenarios
    test_cases = [
        {
            "name": "Mahasiswa dengan IPK Tinggi",
            "data": {
                "ips_1": 3.8,
                "ips_2": 3.9,
                "ips_3": 3.7,
                "ips_4": 3.8,
                "cuti_1": "aktif",
                "cuti_2": "aktif",
                "cuti_3": "aktif",
                "cuti_4": "aktif",
                "total_sks_ditempuh": 144,
                "total_sks_tidak_lulus": 0
            },
            "expected": "Lulus Tepat Waktu"
        },
        {
            "name": "Mahasiswa dengan IPK Rendah",
            "data": {
                "ips_1": 2.0,
                "ips_2": 2.1,
                "ips_3": 2.3,
                "ips_4": 2.2,
                "cuti_1": "aktif",
                "cuti_2": "aktif",
                "cuti_3": "aktif",
                "cuti_4": "aktif",
                "total_sks_ditempuh": 120,
                "total_sks_tidak_lulus": 15
            },
            "expected": "Lulus Tidak Tepat Waktu"
        },
        {
            "name": "Mahasiswa dengan Cuti",
            "data": {
                "ips_1": 3.2,
                "ips_2": 3.1,
                "ips_3": 0.0,
                "ips_4": 3.3,
                "cuti_1": "aktif",
                "cuti_2": "aktif",
                "cuti_3": "cuti",
                "cuti_4": "aktif",
                "total_sks_ditempuh": 90,
                "total_sks_tidak_lulus": 8
            },
            "expected": "Lulus Tidak Tepat Waktu"
        },
        {
            "name": "Mahasiswa Rata-rata",
            "data": {
                "ips_1": 3.0,
                "ips_2": 3.1,
                "ips_3": 3.2,
                "ips_4": 3.0,
                "cuti_1": "aktif",
                "cuti_2": "aktif",
                "cuti_3": "aktif",
                "cuti_4": "aktif",
                "total_sks_ditempuh": 120,
                "total_sks_tidak_lulus": 6
            },
            "expected": None  # Don't check specific result
        }
    ]
    
    print("\n" + "=" * 50)
    print("🧪 Testing Prediction Scenarios")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n📋 {test_case['name']}")
        success = test_prediction(test_case['data'], test_case['expected'])
        if success:
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} prediction tests passed")
    
    # Test error cases
    print("\n" + "=" * 50)
    print("⚠️ Testing Error Cases")
    print("=" * 50)
    
    error_cases = [
        {
            "name": "Missing Field",
            "data": {
                "ips_1": 3.5,
                "ips_2": 3.2,
                # Missing other fields
            }
        },
        {
            "name": "Invalid IPS Value",
            "data": {
                "ips_1": 5.0,  # Invalid: > 4.0
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
        },
        {
            "name": "Invalid Cuti Value",
            "data": {
                "ips_1": 3.5,
                "ips_2": 3.2,
                "ips_3": 3.8,
                "ips_4": 3.6,
                "cuti_1": "invalid",  # Invalid value
                "cuti_2": "aktif",
                "cuti_3": "aktif",
                "cuti_4": "aktif",
                "total_sks_ditempuh": 120,
                "total_sks_tidak_lulus": 6
            }
        }
    ]
    
    for error_case in error_cases:
        print(f"\n❌ {error_case['name']}")
        test_prediction(error_case['data'])

if __name__ == "__main__":
    main() 