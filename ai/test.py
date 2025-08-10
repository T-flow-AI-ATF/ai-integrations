#!/usr/bin/env python3
"""
Test suite for T-Flow AI Medical Triage System
"""

import asyncio
from triage import triage_patient, flag_vitals, get_recent_triage_records, get_recent_vitals_records


async def main():
    """Run comprehensive tests of the triage system."""
    print("=== Testing AI Medical Triage System with Supabase Integration ===\n")

    # Test 1: AI Triage with database storage
    print("1. Testing AI Triage with Supabase storage...")
    try:
        result1 = await triage_patient(
            "Patient experiencing seizure and vomiting", 
            {"patient_id": "test001", "age": 35, "gender": "F"}, 
            True
        )
        print(f"AI Triage Level: {result1['triage_level']}")
        print(f"Record ID: {result1['record_id']}")
        print(f"Timestamp: {result1['timestamp']}")
        if 'error' in result1:
            print(f"Error: {result1['error']}")
    except Exception as e:
        print(f"Test 1 Error: {e}")
    
    print("---")

    # Test 2: Rule-based Triage with database storage
    print("2. Testing Rule-based Triage with Supabase storage...")
    try:
        result2 = await triage_patient(
            "Patient has headache and tiredness", 
            {"patient_id": "test002", "age": 28, "gender": "M"}, 
            False
        )
        print(f"Rule-based Triage Level: {result2['triage_level']}")
        print(f"Record ID: {result2['record_id']}")
        print(f"Timestamp: {result2['timestamp']}")
        if 'error' in result2:
            print(f"Error: {result2['error']}")
    except Exception as e:
        print(f"Test 2 Error: {e}")
    
    print("---")

    # Test 3: Vital Signs Flagging with database storage
    print("3. Testing Vital Signs Flagging with Supabase storage...")
    try:
        vitals_result = await flag_vitals(
            {"pulse": 55, "systolicBP": 120, "diastolicBP": 80}, 
            {"patient_id": "test003", "age": 40}
        )
        print(f"Vitals Flags: {vitals_result['flags']}")
        print(f"Record ID: {vitals_result['record_id']}")
        print(f"Timestamp: {vitals_result['timestamp']}")
        if 'error' in vitals_result:
            print(f"Error: {vitals_result['error']}")
    except Exception as e:
        print(f"Test 3 Error: {e}")
    
    print("---")

    # Test 4: Recent Records Retrieval
    print("4. Testing Recent Records Retrieval...")
    try:
        recent_triage = get_recent_triage_records(5)
        print(f"Recent Triage Records: {len(recent_triage)}")
        
        recent_vitals = get_recent_vitals_records(5)
        print(f"Recent Vitals Records: {len(recent_vitals)}")
        
        if recent_triage:
            print(f"Latest triage: {recent_triage[0]['triage_level']} for symptoms: {recent_triage[0]['symptoms'][:50]}...")
            
        if recent_vitals:
            print(f"Latest vitals: Pulse {recent_vitals[0]['pulse']}, Any flags: {recent_vitals[0]['any_flag']}")
            
    except Exception as e:
        print(f"Test 4 Error: {e}")
    
    print("---")

    # Test 5: Edge Cases
    print("5. Testing Edge Cases...")
    try:
        # Test empty symptoms
        result5a = await triage_patient("", {}, True)
        print(f"Empty symptoms triage: {result5a['triage_level']}")
        
        # Test extreme vitals
        result5b = await flag_vitals({"pulse": 200, "systolicBP": 250, "diastolicBP": 150})
        print(f"Extreme vitals flags: {result5b['flags']}")
        
    except Exception as e:
        print(f"Test 5 Error: {e}")
    
    print("---")
    print("=== Test Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
