# T-Flow AI Medical Triage API - Frontend Integration Guide

## 🚀 Live API Information

**Base URL**: `https://tflow-medical-triage.onrender.com`  
**API Documentation**: https://tflow-medical-triage.onrender.com/docs  
**Health Check**: https://tflow-medical-triage.onrender.com/api/health

## 📋 Available Endpoints

### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "T-Flow AI Medical Triage API",
  "version": "1.0.0",
  "timestamp": "2025-08-08T02:33:12.547070688Z"
}
```

### 2. AI Medical Triage (Primary Endpoint)
```http
POST /api/triage
Content-Type: application/json
```

**Request Body:**
```json
{
  "symptoms": "Patient has severe chest pain and difficulty breathing",
  "patient_info": {
    "age": 45,
    "gender": "M",
    "medical_history": "hypertension"
  },
  "use_ai": true
}
```

**Response:**
```json
{
  "triage_level": "Critical",
  "record_id": "uuid-here",
  "timestamp": "2025-08-08T02:33:12.547070688Z",
  "error": null
}
```

**Triage Levels:**
- `"Critical"` - Immediate emergency intervention required
- `"Urgent"` - Medical attention needed within 2-4 hours  
- `"Moderate"` - Medical evaluation within 24-48 hours
- `"Low"` - Routine care or self-management

### 3. Vital Signs Analysis
```http
POST /api/vitals  
Content-Type: application/json
```

**Request Body:**
```json
{
  "pulse": 120,
  "systolicBP": 180,
  "diastolicBP": 95,
  "patient_info": {
    "age": 60,
    "gender": "F"
  }
}
```

**Response:**
```json
{
  "flags": {
    "pulse_flag": true,
    "systolic_flag": true,
    "diastolic_flag": false,
    "any_flag": true
  },
  "record_id": "uuid-here",
  "timestamp": "2025-08-08T02:33:12.547070688Z",
  "error": null
}
```

### 4. Recent Triage Records
```http
GET /api/triage/recent?limit=10
```

**Response:**
```json
{
  "records": [
    {
      "id": "uuid",
      "symptoms": "chest pain",
      "triage_level": "Critical",
      "created_at": "2025-08-08T02:33:12.547070688Z",
      "use_ai": true,
      "patient_info": {"age": 45}
    }
  ],
  "count": 1,
  "timestamp": "2025-08-08T02:33:12.547070688Z"
}
```

### 5. Recent Vitals Records  
```http
GET /api/vitals/recent?limit=10
```

### 6. System Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "triage_stats": {
    "total_assessments": 150,
    "levels_breakdown": {
      "Critical": 15,
      "Urgent": 45,
      "Moderate": 60,
      "Low": 30
    }
  },
  "vitals_stats": {
    "total_checks": 200,
    "flagged_cases": 75,
    "flag_percentage": 37.5
  },
  "timestamp": "2025-08-08T02:33:12.547070688Z"
}
```

## 🔧 Frontend Implementation Examples

### React/Next.js Implementation

```javascript
// api/triage.js
const API_BASE = 'https://tflow-medical-triage.onrender.com/api';

export class TriageAPI {
  static async submitTriage(symptoms, patientInfo = {}, useAI = true) {
    try {
      const response = await fetch(`${API_BASE}/triage`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms,
          patient_info: patientInfo,
          use_ai: useAI
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Triage API error:', error);
      throw error;
    }
  }

  static async submitVitals(pulse, systolicBP, diastolicBP, patientInfo = {}) {
    try {
      const response = await fetch(`${API_BASE}/vitals`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pulse,
          systolicBP,
          diastolicBP,
          patient_info: patientInfo
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Vitals API error:', error);
      throw error;
    }
  }

  static async getStats() {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Stats API error:', error);
      throw error;
    }
  }

  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}
```

### React Component Example

```jsx
// components/TriageForm.jsx
import React, { useState } from 'react';
import { TriageAPI } from '../api/triage';

export const TriageForm = () => {
  const [symptoms, setSymptoms] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const patientInfo = patientAge ? { age: parseInt(patientAge) } : {};
      const triageResult = await TriageAPI.submitTriage(symptoms, patientInfo);
      setResult(triageResult);
    } catch (error) {
      console.error('Triage failed:', error);
      setResult({ error: 'Failed to process triage request' });
    } finally {
      setLoading(false);
    }
  };

  const getTriageColor = (level) => {
    switch (level) {
      case 'Critical': return 'text-red-600 bg-red-100';
      case 'Urgent': return 'text-orange-600 bg-orange-100';
      case 'Moderate': return 'text-yellow-600 bg-yellow-100';
      case 'Low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Medical Triage Assessment</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Describe symptoms:
          </label>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full p-3 border rounded-md"
            rows={4}
            placeholder="Patient has chest pain and difficulty breathing..."
            required
            minLength={5}
            maxLength={2000}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Patient Age (optional):
          </label>
          <input
            type="number"
            value={patientAge}
            onChange={(e) => setPatientAge(e.target.value)}
            className="w-full p-3 border rounded-md"
            placeholder="35"
            min={0}
            max={120}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !symptoms.trim()}
          className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Submit Triage'}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded-md">
          <h3 className="font-semibold mb-2">Triage Result:</h3>
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <div>
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getTriageColor(result.triage_level)}`}>
                {result.triage_level}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Record ID: {result.record_id}
              </p>
              <p className="text-sm text-gray-600">
                Time: {new Date(result.timestamp).toLocaleString()}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

### Vue.js Implementation

```javascript
// composables/useTriage.js
import { ref } from 'vue'

export function useTriage() {
  const API_BASE = 'https://tflow-medical-triage.onrender.com/api'
  
  const loading = ref(false)
  const result = ref(null)
  const error = ref(null)

  const submitTriage = async (symptoms, patientInfo = {}, useAI = true) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE}/triage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symptoms,
          patient_info: patientInfo,
          use_ai: useAI
        })
      })

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
      
      result.value = await response.json()
      return result.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading: readonly(loading),
    result: readonly(result),
    error: readonly(error),
    submitTriage
  }
}
```

## 🔧 Error Handling

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad Request (validation error)
- `422` - Unprocessable Entity (invalid input format)
- `500` - Internal Server Error

### Error Response Format
```json
{
  "detail": "Symptoms cannot be empty"
}
```

### Validation Rules
- **symptoms**: 5-2000 characters, required
- **pulse**: 30-250 BPM
- **systolicBP**: 60-300 mmHg  
- **diastolicBP**: 30-200 mmHg (must be < systolic)
- **limit**: 1-100 for record queries

## 🎯 Integration Checklist

### ✅ Required Implementation
- [ ] Health check on app startup
- [ ] Triage form with symptom input
- [ ] Patient info collection (age, gender, etc.)
- [ ] Triage result display with appropriate colors
- [ ] Error handling for API failures
- [ ] Loading states during API calls

### 🔧 Optional Features
- [ ] Vitals form and analysis
- [ ] Recent records display
- [ ] Statistics dashboard
- [ ] Offline capability with retry logic
- [ ] Patient history tracking

### 🔒 Security Considerations
- All API calls are over HTTPS
- No authentication required (public API)
- Input validation on both frontend and backend
- Rate limiting handled by Render infrastructure

## 📱 Mobile Considerations
- API is mobile-friendly and responsive
- Consider implementing offline queue for poor connectivity
- Use appropriate loading indicators for slower connections
- The free tier may have cold start delays (10-30 seconds if inactive)

## 🚨 Important Notes

### Cold Start Behavior
- **Free Tier**: Service sleeps after 15 minutes of inactivity
- **Wake Up Time**: 10-30 seconds for first request after sleep
- **Solution**: Implement loading states and user feedback

### Rate Limits
- No specific rate limits implemented
- Render infrastructure provides DDoS protection
- Consider implementing client-side debouncing for rapid requests

## 🎉 Your API is Live and Ready!

**API Base URL**: `https://tflow-medical-triage.onrender.com`

Your frontend developer can start integrating immediately using the examples above. The interactive API documentation at `/docs` provides additional details and allows for direct testing.

---

**Need Help?** The API includes comprehensive error messages and the `/docs` endpoint provides interactive testing capabilities.
