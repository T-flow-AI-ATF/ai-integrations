#!/usr/bin/env python3
"""
Main entry point for T-Flow AI Medical Triage System
"""

import asyncio
import argparse
from triage import triage_patient, flag_vitals, get_recent_triage_records, get_recent_vitals_records


async def interactive_triage():
    """Interactive triage session."""
    print("=== T-Flow AI Medical Triage System ===")
    print("Enter patient symptoms (or 'quit' to exit):")
    
    while True:
        symptoms = input("\nSymptoms: ").strip()
        
        if symptoms.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if not symptoms:
            print("Please enter symptoms.")
            continue
            
        try:
            # Get optional patient info
            age_input = input("Patient age (optional): ").strip()
            age = int(age_input) if age_input.isdigit() else None
            
            patient_info = {}
            if age:
                patient_info['age'] = age
                
            # Perform triage
            result = await triage_patient(symptoms, patient_info, True)
            
            print(f"\n🏥 Triage Result: {result['triage_level']}")
            if result['record_id']:
                print(f"📝 Stored in database with ID: {result['record_id']}")
            else:
                print("⚠️  Database storage failed, but triage completed")
                
        except Exception as e:
            print(f"❌ Error: {e}")


async def batch_triage(symptoms_list):
    """Batch process multiple symptoms."""
    results = []
    
    for i, symptoms in enumerate(symptoms_list, 1):
        print(f"Processing {i}/{len(symptoms_list)}: {symptoms[:50]}...")
        
        try:
            result = await triage_patient(symptoms, {'batch_id': i}, True)
            results.append(result)
            print(f"✅ {result['triage_level']}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    return results


def show_recent_records(limit=10):
    """Display recent triage and vitals records."""
    print(f"\n=== Recent {limit} Triage Records ===")
    
    triage_records = get_recent_triage_records(limit)
    for i, record in enumerate(triage_records, 1):
        print(f"{i}. {record['triage_level']} - {record['symptoms'][:60]}...")
        print(f"   {record['created_at']} (AI: {record['use_ai']})")
    
    print(f"\n=== Recent {limit} Vitals Records ===")
    
    vitals_records = get_recent_vitals_records(limit)
    for i, record in enumerate(vitals_records, 1):
        flags = "🚨" if record['any_flag'] else "✅"
        print(f"{i}. {flags} Pulse: {record['pulse']}, BP: {record['systolic_bp']}/{record['diastolic_bp']}")
        print(f"   {record['created_at']}")


async def test_vitals():
    """Interactive vitals testing."""
    print("\n=== Vitals Testing ===")
    
    try:
        pulse = int(input("Enter pulse (bpm): "))
        systolic = int(input("Enter systolic BP (mmHg): "))
        diastolic = int(input("Enter diastolic BP (mmHg): "))
        
        vitals = {
            'pulse': pulse,
            'systolicBP': systolic,
            'diastolicBP': diastolic
        }
        
        result = await flag_vitals(vitals)
        
        print(f"\n🔍 Vitals Analysis:")
        print(f"Pulse Flag: {'🚨' if result['flags']['pulse_flag'] else '✅'}")
        print(f"Systolic Flag: {'🚨' if result['flags']['systolic_flag'] else '✅'}")
        print(f"Diastolic Flag: {'🚨' if result['flags']['diastolic_flag'] else '✅'}")
        print(f"Any Abnormal: {'🚨 YES' if result['flags']['any_flag'] else '✅ NO'}")
        
        if result['record_id']:
            print(f"📝 Stored with ID: {result['record_id']}")
            
    except ValueError:
        print("❌ Please enter valid numbers")
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description='T-Flow AI Medical Triage System')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive triage mode')
    parser.add_argument('--vitals', '-v', action='store_true', help='Test vitals analysis')
    parser.add_argument('--records', '-r', type=int, default=0, help='Show recent records (specify limit)')
    parser.add_argument('--symptoms', '-s', type=str, help='Single symptom to triage')
    parser.add_argument('--batch', '-b', type=str, help='File with symptoms to batch process')
    
    args = parser.parse_args()
    
    if args.interactive:
        await interactive_triage()
    elif args.vitals:
        await test_vitals()
    elif args.records:
        show_recent_records(args.records)
    elif args.symptoms:
        result = await triage_patient(args.symptoms, {}, True)
        print(f"Triage Result: {result['triage_level']}")
    elif args.batch:
        try:
            with open(args.batch, 'r') as f:
                symptoms_list = [line.strip() for line in f if line.strip()]
            results = await batch_triage(symptoms_list)
            print(f"\nProcessed {len(results)} cases")
        except FileNotFoundError:
            print(f"❌ File not found: {args.batch}")
    else:
        # Default: run test
        print("Running test suite...")
        from test import main as test_main
        await test_main()


if __name__ == "__main__":
    asyncio.run(main())
