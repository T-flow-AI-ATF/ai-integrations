# T-Flow AI Medical Triage API - Quick Start for Frontend

## 🚀 **Your Live API is Ready!**

**Base URL**: https://tflow-medical-triage.onrender.com  
**Interactive Docs**: https://tflow-medical-triage.onrender.com/docs  

## 📋 **Key Endpoints**

### 1. **Primary Triage Endpoint**
```
POST /api/triage
```

**Request:**
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
  "timestamp": "2025-08-08T02:33:12Z",
  "error": null
}
```

**Triage Levels:**
- `Critical` - Emergency intervention required
- `Urgent` - Medical attention within 2-4 hours  
- `Moderate` - Evaluation within 24-48 hours
- `Low` - Routine care

### 2. **Vital Signs Analysis**
```
POST /api/vitals
```

**Request:**
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

### 3. **Health Check**
```
GET /api/health
```

### 4. **Statistics**
```
GET /api/stats
```

## ⚡ **JavaScript Example**

```javascript
const API_BASE = 'https://tflow-medical-triage.onrender.com/api';

// Submit triage request
async function submitTriage(symptoms, patientInfo = {}) {
  try {
    const response = await fetch(`${API_BASE}/triage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        symptoms,
        patient_info: patientInfo,
        use_ai: true
      })
    });

    const result = await response.json();
    
    // Handle result
    console.log('Triage Level:', result.triage_level);
    console.log('Record ID:', result.record_id);
    
    return result;
  } catch (error) {
    console.error('API Error:', error);
  }
}

// Example usage
submitTriage('chest pain and shortness of breath', { age: 45 });
```

## 🎨 **UI Color Coding**

```javascript
const getTriageColor = (level) => {
  switch (level) {
    case 'Critical': return '#dc2626'; // Red
    case 'Urgent': return '#ea580c';   // Orange  
    case 'Moderate': return '#ca8a04'; // Yellow
    case 'Low': return '#16a34a';      // Green
  }
};
```

## 🔧 **Validation Rules**

- **symptoms**: 5-2000 characters (required)
- **pulse**: 30-250 BPM
- **systolicBP**: 60-300 mmHg
- **diastolicBP**: 30-200 mmHg (must be < systolic)

## ⚠️ **Important Notes**

1. **Cold Start**: First request after 15min inactivity takes 10-30 seconds
2. **HTTPS Only**: All endpoints use secure connections
3. **No Auth Required**: Public API, no API keys needed
4. **Rate Limits**: None implemented, but use reasonable request patterns

## 🎉 **You're Ready to Build!**

Your API is live and fully functional. Check out the detailed integration guide in `FRONTEND_INTEGRATION.md` for complete examples in React, Vue, and more!

**Test it now**: https://tflow-medical-triage.onrender.com/docs
