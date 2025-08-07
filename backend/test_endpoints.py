#!/usr/bin/env python3
"""
Simple test script to verify FastAPI backend endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing T-Flow AI Medical Triage API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Triage endpoint
    print("\n3. Testing Triage Endpoint (AI)...")
    try:
        payload = {
            "symptoms": "Patient has severe chest pain and difficulty breathing",
            "patient_info": {"age": 45, "gender": "M"},
            "use_ai": True
        }
        response = requests.post(f"{BASE_URL}/api/triage", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Triage passed")
            print(f"   Triage Level: {result['triage_level']}")
            print(f"   Record ID: {result.get('record_id', 'N/A')}")
            print(f"   Timestamp: {result['timestamp']}")
        else:
            print(f"❌ AI Triage failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ AI Triage error: {e}")
    
    # Test 4: Triage endpoint (rule-based)
    print("\n4. Testing Triage Endpoint (Rule-based)...")
    try:
        payload = {
            "symptoms": "Patient has mild headache and feels tired",
            "patient_info": {"age": 30},
            "use_ai": False
        }
        response = requests.post(f"{BASE_URL}/api/triage", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Rule-based Triage passed")
            print(f"   Triage Level: {result['triage_level']}")
            print(f"   Record ID: {result.get('record_id', 'N/A')}")
        else:
            print(f"❌ Rule-based Triage failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Rule-based Triage error: {e}")
    
    # Test 5: Vitals endpoint
    print("\n5. Testing Vitals Endpoint...")
    try:
        payload = {
            "pulse": 120,
            "systolicBP": 180,
            "diastolicBP": 95,
            "patient_info": {"age": 60}
        }
        response = requests.post(f"{BASE_URL}/api/vitals", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Vitals check passed")
            print(f"   Flags: {result['flags']}")
            print(f"   Any flags: {result['flags']['any_flag']}")
        else:
            print(f"❌ Vitals check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Vitals check error: {e}")
    
    # Test 6: Recent records
    print("\n6. Testing Recent Records...")
    try:
        response = requests.get(f"{BASE_URL}/api/triage/recent?limit=5")
        if response.status_code == 200:
            result = response.json()
            print("✅ Recent triage records passed")
            print(f"   Found {result['count']} records")
        else:
            print(f"❌ Recent records failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Recent records error: {e}")
    
    # Test 7: Stats endpoint
    print("\n7. Testing Stats Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            result = response.json()
            print("✅ Stats endpoint passed")
            print(f"   Total assessments: {result['triage_stats']['total_assessments']}")
            print(f"   Flagged vitals: {result['vitals_stats']['flagged_cases']}")
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("📝 View interactive docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api_endpoints()
