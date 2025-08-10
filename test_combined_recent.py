#!/usr/bin/env python3
"""
Test the new combined recent assessments endpoint
"""

import requests
import json
from datetime import datetime

# API URLs
BASE_URL = "https://tflow-medical-triage.onrender.com/api"

def test_combined_recent_endpoint():
    """Test the updated recent triage endpoint with combined data"""
    
    print("🧪 Testing Combined Recent Assessments Endpoint")
    print("=" * 60)
    
    # First, create a test assessment with both symptoms and vitals
    print("1. Creating test assessment with symptoms + vitals...")
    
    triage_data = {
        "symptoms": "Patient has chest pain and difficulty breathing during testing",
        "patient_info": {
            "age": 55,
            "gender": "F"
        },
        "vitals": {
            "pulse": 110,
            "systolicBP": 160,
            "diastolicBP": 90
        },
        "use_ai": True
    }
    
    try:
        # Create the assessment
        response = requests.post(f"{BASE_URL}/triage", json=triage_data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Created assessment: {result['triage_level']}")
            print(f"   Triage Record ID: {result['record_id']}")
            print(f"   Vitals Record ID: {result.get('vitals_record_id', 'N/A')}")
        else:
            print(f"❌ Failed to create test assessment: {response.status_code}")
            print(response.text)
            return
            
    except Exception as e:
        print(f"❌ Error creating test assessment: {str(e)}")
        return
    
    print("\n" + "-" * 60)
    
    # Test the updated recent triage endpoint
    print("2. Testing updated /api/triage/recent endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/triage/recent?limit=5", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} records")
            print(f"   Has vitals data: {data.get('has_vitals_data', 'Unknown')}")
            
            if data['records']:
                latest = data['records'][0]
                print(f"\n📋 Latest Assessment:")
                print(f"   Symptoms: {latest.get('symptoms', 'N/A')[:50]}...")
                print(f"   Triage Level: {latest.get('triage_level', 'N/A')}")
                print(f"   Created: {latest.get('created_at', 'N/A')}")
                
                if latest.get('vitals_data'):
                    vitals = latest['vitals_data']
                    print(f"   🔍 Associated Vitals:")
                    print(f"      Pulse: {vitals.get('pulse', 'N/A')} BPM")
                    print(f"      BP: {vitals.get('systolicBP', 'N/A')}/{vitals.get('diastolicBP', 'N/A')} mmHg")
                    print(f"      Flags: {vitals.get('any_flag', 'N/A')}")
                else:
                    print(f"   ℹ️ No vitals data associated")
            else:
                print("   No records found")
                
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fetching recent triage: {str(e)}")
    
    print("\n" + "-" * 60)
    
    # Test the new dedicated assessments endpoint
    print("3. Testing new /api/assessments/recent endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/assessments/recent?limit=3", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data['count']} assessments")
            print(f"   Has vitals data: {data.get('has_vitals_data', 'Unknown')}")
            
            for i, assessment in enumerate(data['assessments'][:2], 1):
                print(f"\n📋 Assessment {i}:")
                print(f"   ID: {assessment.get('id', 'N/A')}")
                print(f"   Triage: {assessment.get('triage_level', 'N/A')}")
                print(f"   Time: {assessment.get('created_at', 'N/A')}")
                
                if assessment.get('vitals_data'):
                    vitals = assessment['vitals_data']
                    print(f"   💓 Vitals: Pulse {vitals.get('pulse')} | BP {vitals.get('systolicBP')}/{vitals.get('diastolicBP')}")
                    flags = [k for k, v in vitals.items() if k.endswith('_flag') and v and k != 'any_flag']
                    if flags:
                        print(f"   🚨 Flagged: {', '.join(f.replace('_flag', '') for f in flags)}")
                else:
                    print(f"   ℹ️ No vitals data")
                    
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fetching recent assessments: {str(e)}")

def compare_old_vs_new():
    """Compare the old separate endpoints with the new combined approach"""
    
    print("\n" + "=" * 60)
    print("🔍 COMPARISON: Old vs New Approach")
    print("=" * 60)
    
    print("❌ OLD WAY (Separate endpoints):")
    print("   - GET /api/triage/recent → Only triage data")
    print("   - GET /api/vitals/recent → Only vitals data") 
    print("   - Frontend needs to match records by timestamp")
    print("   - Duplicate patient IDs cause confusion")
    print("   - Multiple API calls required")
    
    print("\n✅ NEW WAY (Combined endpoint):")
    print("   - GET /api/triage/recent → Triage + associated vitals")
    print("   - GET /api/assessments/recent → Same data, cleaner name")
    print("   - Single API call gets complete assessment")
    print("   - No duplicate IDs or matching logic needed")
    print("   - Clear relationship between triage and vitals")

if __name__ == "__main__":
    print("🚀 T-Flow Combined Assessments Testing")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_combined_recent_endpoint()
    compare_old_vs_new()
    
    print("\n🎉 Testing completed!")
    print("\n📝 Frontend Dev Notes:")
    print("1. Use /api/triage/recent for backward compatibility")
    print("2. Or use /api/assessments/recent for cleaner naming")
    print("3. Both endpoints now include vitals_data when available")
    print("4. No more duplicate patient IDs!")
    print("5. Single API call gives you everything you need")
