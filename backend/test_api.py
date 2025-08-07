"""
Test suite for T-Flow AI Medical Triage API
"""

import pytest
import asyncio
import sys
import os
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Create test client
client = TestClient(app)

class TestTriageAPI:
    """Test cases for triage endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "T-Flow AI Medical Triage API" in data["message"]
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "T-Flow AI" in data["service"]
    
    def test_triage_endpoint_valid_request(self):
        """Test triage endpoint with valid request"""
        payload = {
            "symptoms": "Patient has severe chest pain and difficulty breathing",
            "patient_info": {"age": 45, "gender": "M"},
            "use_ai": True
        }
        response = client.post("/api/triage", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "triage_level" in data
        assert data["triage_level"] in ["Critical", "Urgent", "Moderate", "Low"]
        assert "timestamp" in data
    
    def test_triage_endpoint_rule_based(self):
        """Test triage endpoint with rule-based classification"""
        payload = {
            "symptoms": "Patient has mild headache and feels tired",
            "patient_info": {"age": 30},
            "use_ai": False
        }
        response = client.post("/api/triage", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "triage_level" in data
        assert data["triage_level"] in ["Critical", "Urgent", "Moderate", "Low"]
    
    def test_triage_endpoint_invalid_symptoms(self):
        """Test triage endpoint with invalid symptoms"""
        payload = {
            "symptoms": "",  # Empty symptoms
            "use_ai": True
        }
        response = client.post("/api/triage", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_triage_endpoint_short_symptoms(self):
        """Test triage endpoint with too short symptoms"""
        payload = {
            "symptoms": "Hi",  # Too short
            "use_ai": True
        }
        response = client.post("/api/triage", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_vitals_endpoint_valid_request(self):
        """Test vitals endpoint with valid request"""
        payload = {
            "pulse": 85,
            "systolicBP": 120,
            "diastolicBP": 80,
            "patient_info": {"age": 35}
        }
        response = client.post("/api/vitals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "flags" in data
        assert all(key in data["flags"] for key in ["pulse_flag", "systolic_flag", "diastolic_flag", "any_flag"])
        assert "timestamp" in data
    
    def test_vitals_endpoint_abnormal_values(self):
        """Test vitals endpoint with abnormal values"""
        payload = {
            "pulse": 120,  # High pulse
            "systolicBP": 180,  # High systolic
            "diastolicBP": 110,  # High diastolic
            "patient_info": {"age": 60}
        }
        response = client.post("/api/vitals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["flags"]["any_flag"] == True
    
    def test_vitals_endpoint_invalid_bp(self):
        """Test vitals endpoint with invalid blood pressure"""
        payload = {
            "pulse": 80,
            "systolicBP": 80,  # Lower than diastolic
            "diastolicBP": 90,  # Higher than systolic
        }
        response = client.post("/api/vitals", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_vitals_endpoint_out_of_range(self):
        """Test vitals endpoint with out of range values"""
        payload = {
            "pulse": 300,  # Way too high
            "systolicBP": 120,
            "diastolicBP": 80
        }
        response = client.post("/api/vitals", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_recent_triage_endpoint(self):
        """Test recent triage records endpoint"""
        response = client.get("/api/triage/recent?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "count" in data
        assert isinstance(data["records"], list)
        assert data["count"] == len(data["records"])
    
    def test_recent_triage_invalid_limit(self):
        """Test recent triage with invalid limit"""
        response = client.get("/api/triage/recent?limit=500")  # Too high
        assert response.status_code == 400
    
    def test_recent_vitals_endpoint(self):
        """Test recent vitals records endpoint"""
        response = client.get("/api/vitals/recent?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "count" in data
        assert isinstance(data["records"], list)
    
    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "triage_stats" in data
        assert "vitals_stats" in data
        assert "timestamp" in data

@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test async functionality"""
    
    async def test_async_triage_request(self):
        """Test triage endpoint asynchronously"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            payload = {
                "symptoms": "Patient experiencing seizure and vomiting",
                "patient_info": {"age": 35, "gender": "F"},
                "use_ai": True
            }
            response = await ac.post("/api/triage", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["triage_level"] in ["Critical", "Urgent", "Moderate", "Low"]
    
    async def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            tasks = []
            for i in range(5):
                payload = {
                    "symptoms": f"Test symptoms case {i}",
                    "use_ai": False  # Use rule-based for speed
                }
                task = ac.post("/api/triage", json=payload)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert "triage_level" in data

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
