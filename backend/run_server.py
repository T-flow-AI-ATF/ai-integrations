#!/usr/bin/env python3
"""
Development server runner for T-Flow AI Medical Triage API
"""

import uvicorn
import os
from pathlib import Path

def main():
    """Run the FastAPI development server"""
    # Load environment variables from parent directory
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print(f"⚠️  No .env file found at {env_path}")
    
    print("🚀 Starting T-Flow AI Medical Triage API...")
    print("📝 API Documentation will be available at: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/api/health")
    print("📊 API Root: http://localhost:8000")
    print("🔄 Use Ctrl+C to stop the server")
    print("-" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[".", ".."],
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
