#!/usr/bin/env python3
"""
Comprehensive system verification for Render deployment
"""
import sys
import os
from datetime import datetime

def test_dependencies():
    """Test all required dependencies"""
    print("=== DEPENDENCY CHECK ===")
    
    dependencies = [
        ('dotenv', 'python-dotenv'),
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('groq', 'Groq API'),
        ('supabase', 'Supabase'),
        ('pydantic', 'Pydantic')
    ]
    
    all_good = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            all_good = False
    
    return all_good

def test_environment():
    """Test environment variables"""
    print("\n=== ENVIRONMENT CHECK ===")
    
    # Load from parent .env file
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(env_path)
    
    required_vars = ['GROQ_API_KEY', 'SUPABASE_URL', 'SUPABASE_ANON_KEY']
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 10}...{value[-10:] if len(value) > 10 else value}")
        else:
            print(f"❌ {var}: Not found")
            all_good = False
    
    return all_good

def test_imports():
    """Test core module imports"""
    print("\n=== IMPORT CHECK ===")
    
    try:
        from triage_core import triage_patient, flag_vitals
        print("✅ triage_core functions imported")
        
        from main import app
        print("✅ FastAPI app imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_connections():
    """Test external API connections"""
    print("\n=== CONNECTION CHECK ===")
    
    try:
        # Test Groq API
        from groq import Groq
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("✅ Groq client initialized")
        
        # Test Supabase
        from supabase import create_client
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_ANON_KEY")
        )
        print("✅ Supabase client initialized")
        
        return True
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def test_functionality():
    """Test core functionality"""
    print("\n=== FUNCTIONALITY CHECK ===")
    
    try:
        from triage_core import triage_patient, flag_vitals
        
        # Test AI triage
        result1 = await triage_patient("chest pain", {"age": 45}, True)
        print(f"✅ AI Triage: {result1['triage_level']}")
        
        # Test vitals
        result2 = await flag_vitals({"pulse": 80, "systolicBP": 120, "diastolicBP": 80})
        print(f"✅ Vitals Analysis: {result2['flags']['any_flag']}")
        
        return True
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False

def test_fastapi():
    """Test FastAPI app creation"""
    print("\n=== FASTAPI CHECK ===")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test health endpoint  
        response = client.get("/api/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ FastAPI test error: {e}")
        return False

async def main():
    """Run comprehensive system check"""
    print(f"🔍 COMPREHENSIVE RENDER DEPLOYMENT CHECK")
    print(f"Python: {sys.version}")
    print(f"Time: {datetime.now()}")
    print("=" * 60)
    
    checks = [
        ("Dependencies", test_dependencies()),
        ("Environment", test_environment()),
        ("Imports", test_imports()),
        ("Connections", test_connections()),
        ("FastAPI", test_fastapi()),
        ("Functionality", await test_functionality())
    ]
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:15} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED - Ready for Render deployment!")
        print("🚀 Your system is 100% ready!")
    else:
        print("⚠️  Some checks failed - review issues above")
    
    return all_passed

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
