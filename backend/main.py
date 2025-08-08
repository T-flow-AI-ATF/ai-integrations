#!/usr/bin/env python3
"""
T-Flow AI Medical Triage API
FastAPI backend for the medical triage system
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
import os
from datetime import datetime

# Import triage functions from local module
from triage_core import triage_patient, flag_vitals, get_recent_triage_records, get_recent_vitals_records

# Initialize FastAPI app
app = FastAPI(
    title="T-Flow AI Medical Triage API",
    description="Hospital-grade AI-powered medical triage system with Groq Llama 3.3 70B and Supabase integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3000",
        "https://your-frontend-domain.com",  # Replace with your production domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Request/Response Models
class TriageRequest(BaseModel):
    symptoms: str = Field(..., min_length=5, max_length=2000, description="Patient symptom description")
    patient_info: Optional[Dict] = Field(default_factory=dict, description="Patient information (age, gender, etc.)")
    use_ai: bool = Field(default=True, description="Whether to use AI or rule-based triage")
    
    @validator('symptoms')
    def validate_symptoms(cls, v):
        if not v.strip():
            raise ValueError("Symptoms cannot be empty")
        # Basic PII check (extend as needed)
        pii_indicators = ['ssn', 'social security', 'credit card', 'phone number']
        if any(indicator in v.lower() for indicator in pii_indicators):
            raise ValueError("Symptoms appear to contain sensitive information")
        return v.strip()

class TriageResponse(BaseModel):
    triage_level: str
    record_id: Optional[str]
    timestamp: str
    confidence: Optional[str] = None
    error: Optional[str] = None

class VitalsRequest(BaseModel):
    pulse: int = Field(..., ge=30, le=250, description="Pulse rate (BPM)")
    systolicBP: int = Field(..., ge=60, le=300, description="Systolic blood pressure (mmHg)")
    diastolicBP: int = Field(..., ge=30, le=200, description="Diastolic blood pressure (mmHg)")
    patient_info: Optional[Dict] = Field(default_factory=dict, description="Patient information")
    
    @validator('diastolicBP')
    def validate_blood_pressure(cls, v, values):
        if 'systolicBP' in values and v >= values['systolicBP']:
            raise ValueError("Diastolic BP must be lower than systolic BP")
        return v

class VitalsResponse(BaseModel):
    flags: Dict[str, bool]
    record_id: Optional[str]
    timestamp: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str

# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "T-Flow AI Medical Triage API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        service="T-Flow AI Medical Triage API",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/triage", response_model=TriageResponse)
async def create_triage(request: TriageRequest):
    """
    AI-powered medical triage endpoint
    
    Analyzes patient symptoms using Groq's Llama 3.3 70B model
    with intelligent fallback to rule-based triage.
    """
    try:
        result = await triage_patient(
            symptoms_text=request.symptoms,
            patient_info=request.patient_info,
            use_ai=request.use_ai
        )
        
        return TriageResponse(
            triage_level=result['triage_level'],
            record_id=result.get('record_id'),
            timestamp=result['timestamp'],
            error=result.get('error')
        )
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Triage error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Triage analysis failed: {str(e)}"
        )

@app.post("/api/vitals", response_model=VitalsResponse)
async def check_vitals(request: VitalsRequest):
    """
    Vital signs analysis endpoint
    
    Analyzes patient vital signs and flags abnormal values
    according to standard medical thresholds.
    """
    try:
        vitals_data = {
            'pulse': request.pulse,
            'systolicBP': request.systolicBP,
            'diastolicBP': request.diastolicBP
        }
        
        result = await flag_vitals(
            vitals=vitals_data,
            patient_info=request.patient_info
        )
        
        return VitalsResponse(
            flags=result['flags'],
            record_id=result.get('record_id'),
            timestamp=result['timestamp'],
            error=result.get('error')
        )
        
    except Exception as e:
        print(f"Vitals analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Vitals analysis failed: {str(e)}"
        )

@app.get("/api/triage/recent")
async def get_recent_triage(limit: int = 10):
    """
    Get recent triage records
    
    Retrieves the most recent triage assessments from the database
    for monitoring and analysis purposes.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400, 
                detail="Limit must be between 1 and 100"
            )
            
        records = get_recent_triage_records(limit)
        
        return {
            "records": records,
            "count": len(records),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching recent triage: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve triage records: {str(e)}"
        )

@app.get("/api/vitals/recent")
async def get_recent_vitals(limit: int = 10):
    """
    Get recent vital signs records
    
    Retrieves the most recent vital signs assessments
    for trend analysis and monitoring.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limit must be between 1 and 100"
            )
            
        records = get_recent_vitals_records(limit)
        
        return {
            "records": records,
            "count": len(records),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching recent vitals: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve vitals records: {str(e)}"
        )

@app.get("/api/stats")
async def get_triage_stats():
    """
    Get triage system statistics
    
    Provides overview statistics for monitoring system usage
    and performance.
    """
    try:
        # Get recent records for analysis
        triage_records = get_recent_triage_records(100)
        vitals_records = get_recent_vitals_records(100)
        
        # Calculate basic statistics
        triage_levels = {}
        for record in triage_records:
            level = record.get('triage_level', 'Unknown')
            triage_levels[level] = triage_levels.get(level, 0) + 1
        
        flagged_vitals = sum(1 for record in vitals_records if record.get('any_flag', False))
        
        return {
            "triage_stats": {
                "total_assessments": len(triage_records),
                "levels_breakdown": triage_levels,
            },
            "vitals_stats": {
                "total_checks": len(vitals_records),
                "flagged_cases": flagged_vitals,
                "flag_percentage": round((flagged_vitals / len(vitals_records) * 100) if vitals_records else 0, 2)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error generating stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate statistics: {str(e)}"
        )

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: {str(exc)}"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Render provides PORT environment variable (default 10000)
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        app,  # Use app directly, not string reference
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
