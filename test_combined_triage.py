#!/usr/bin/env python3
"""
Test script for the updated combined triage endpoint
"""

import requests
import json
from datetime import datetime

# Local testing URL
BASE_URL = "http://localhost:8000/api"

def test_combined_triage():
    """Test triage with both symptoms and vitals"""
    
    print("🧪 Testing Combined Triage Endpoint")
    print("=" * 50)
    
    # Test data
    test_cases = [
        {
            "name": "Critical case with abnormal vitals",
            "data": {
                "symptoms": "Patient has severe chest pain, difficulty breathing, and feels dizzy",
                "patient_info": {
                    "age": 65,
                    "gender": "M",
                    "medical_history": "hypertension, diabetes"
                },
                "vitals": {
                    "pulse": 140,
                    "systolicBP": 190,
                    "diastolicBP": 110
                },
                "use_ai": True
            }
        },
        {
            "name": "Moderate case with normal vitals",
            "data": {
                "symptoms": "Patient has a persistent cough and mild fever for 3 days",
                "patient_info": {
                    "age": 35,
                    "gender": "F"
                },
                "vitals": {
                    "pulse": 80,
                    "systolicBP": 120,
                    "diastolicBP": 75
                },
                "use_ai": True
            }
        },
        {
            "name": "Symptoms only (no vitals)",
            "data": {
                "symptoms": "Patient has headache and nausea",
                "patient_info": {
                    "age": 28,
                    "gender": "F"
                },
                "use_ai": True
            }
        },
        {
            "name": "Partial vitals",
            "data": {
                "symptoms": "Patient reports feeling tired and weak",
                "patient_info": {
                    "age": 42,
                    "gender": "M"
                },
                "vitals": {
                    "pulse": 55  # Only pulse provided
                },
                "use_ai": True
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{BASE_URL}/triage",
                json=test_case["data"],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Triage Level: {result['triage_level']}")
                print(f"   Record ID: {result.get('record_id', 'N/A')}")
                
                if result.get('vitals_flags'):
                    flags = result['vitals_flags']
                    print(f"   Vitals Analysis:")
                    for flag_name, flag_value in flags.items():
                        status = "🚨 FLAGGED" if flag_value else "✅ Normal"
                        print(f"     {flag_name}: {status}")
                    print(f"   Vitals Record ID: {result.get('vitals_record_id', 'N/A')}")
                else:
                    print(f"   Vitals Analysis: Not performed")
                
                print(f"   Timestamp: {result['timestamp']}")
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - make sure the server is running on localhost:8000")
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Combined triage testing completed!")

def test_validation():
    """Test input validation for the combined endpoint"""
    
    print("\n🛡️ Testing Input Validation")
    print("=" * 50)
    
    validation_tests = [
        {
            "name": "Invalid blood pressure (diastolic >= systolic)",
            "data": {
                "symptoms": "Patient feels unwell",
                "vitals": {
                    "pulse": 80,
                    "systolicBP": 120,
                    "diastolicBP": 130  # Invalid: higher than systolic
                }
            },
            "should_fail": True
        },
        {
            "name": "Pulse out of range",
            "data": {
                "symptoms": "Patient feels unwell", 
                "vitals": {
                    "pulse": 300,  # Invalid: too high
                    "systolicBP": 120,
                    "diastolicBP": 80
                }
            },
            "should_fail": True
        },
        {
            "name": "Empty symptoms",
            "data": {
                "symptoms": "",  # Invalid: empty
                "vitals": {
                    "pulse": 80,
                    "systolicBP": 120,
                    "diastolicBP": 80
                }
            },
            "should_fail": True
        }
    ]
    
    for i, test in enumerate(validation_tests, 1):
        print(f"\n{i}. {test['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(f"{BASE_URL}/triage", json=test["data"], timeout=10)
            
            if test["should_fail"]:
                if response.status_code != 200:
                    print(f"✅ Correctly rejected: {response.status_code}")
                    error_detail = response.json().get('detail', 'No detail provided')
                    print(f"   Error: {error_detail}")
                else:
                    print("❌ Should have failed but didn't")
            else:
                if response.status_code == 200:
                    print("✅ Valid request accepted")
                else:
                    print(f"❌ Valid request rejected: {response.status_code}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed")
        except Exception as e:
            print(f"❌ Test error: {str(e)}")

if __name__ == "__main__":
    print("🚀 T-Flow Combined Triage Testing")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test the combined functionality
    test_combined_triage()
    
    # Test validation
    test_validation()
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Review the results above")
    print("2. If tests pass, deploy the updated API to Render")
    print("3. Update frontend integration documentation")
