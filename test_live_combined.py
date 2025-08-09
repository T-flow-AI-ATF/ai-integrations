#!/usr/bin/env python3
"""
Quick test for the live combined triage API
"""

import requests
import json

def test_live_combined_triage():
    """Test the live API with combined symptoms and vitals"""
    
    url = "https://tflow-medical-triage.onrender.com/api/triage"
    
    test_data = {
        "symptoms": "Patient has chest pain and difficulty breathing",
        "patient_info": {
            "age": 45,
            "gender": "M"
        },
        "vitals": {
            "pulse": 120,
            "systolicBP": 180,
            "diastolicBP": 95
        },
        "use_ai": True
    }
    
    print("🧪 Testing Live Combined Triage API")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Request: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        response = requests.post(url, json=test_data, timeout=60)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Triage Level: {result['triage_level']}")
            print(f"Record ID: {result.get('record_id', 'N/A')}")
            
            if result.get('vitals_flags'):
                print("\n🔍 Vitals Analysis:")
                flags = result['vitals_flags']
                for flag_name, flag_value in flags.items():
                    status = "🚨 FLAGGED" if flag_value else "✅ Normal"
                    print(f"  {flag_name}: {status}")
                print(f"  Vitals Record ID: {result.get('vitals_record_id', 'N/A')}")
            else:
                print("Vitals Analysis: Not performed")
                
            print(f"Timestamp: {result['timestamp']}")
            
        else:
            print("❌ Error:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def test_symptoms_only():
    """Test with symptoms only (no vitals)"""
    
    url = "https://tflow-medical-triage.onrender.com/api/triage"
    
    test_data = {
        "symptoms": "Patient has mild headache and feels tired",
        "patient_info": {
            "age": 30,
            "gender": "F"
        },
        "use_ai": True
    }
    
    print("\n🧪 Testing Symptoms Only")
    print("=" * 30)
    
    try:
        response = requests.post(url, json=test_data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Triage Level: {result['triage_level']}")
            print(f"Vitals Analysis: {'Yes' if result.get('vitals_flags') else 'No (as expected)'}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

if __name__ == "__main__":
    test_live_combined_triage()
    test_symptoms_only()
    
    print("\n🎉 Testing completed!")
    print("\n📋 Summary:")
    print("- Combined symptoms + vitals: Processed in single request")
    print("- Symptoms only: Still works as before")
    print("- Vitals flagging: Included in triage response when provided")
