# 🚀 Updated T-Flow Triage API - Combined Symptoms & Vitals

## ✨ **What Changed**

Your frontend dev was absolutely right! The triage endpoint now processes **symptoms AND vitals together** in a single request, making the workflow much more natural.

## 📋 **New Combined Triage Endpoint**

### **POST /api/triage** (Enhanced)

**Request with Both Symptoms & Vitals:**
```json
{
  "symptoms": "Patient has chest pain and difficulty breathing",
  "patient_info": {
    "age": 45,
    "gender": "M",
    "medical_history": "hypertension"
  },
  "vitals": {
    "pulse": 120,
    "systolicBP": 180,
    "diastolicBP": 95
  },
  "use_ai": true
}
```

**Enhanced Response:**
```json
{
  "triage_level": "Critical",
  "record_id": "uuid-here",
  "timestamp": "2025-08-09T21:08:50Z",
  "vitals_flags": {
    "pulse_flag": true,
    "systolic_flag": true,
    "diastolic_flag": false,
    "any_flag": true
  },
  "vitals_record_id": "uuid-here",
  "error": null
}
```

**Request with Symptoms Only (Still Works):**
```json
{
  "symptoms": "Patient has headache and feels tired",
  "patient_info": { "age": 30 },
  "use_ai": true
}
```

**Response (No Vitals):**
```json
{
  "triage_level": "Moderate", 
  "record_id": "uuid-here",
  "timestamp": "2025-08-09T21:08:50Z",
  "vitals_flags": null,
  "vitals_record_id": null,
  "error": null
}
```

## ⚡ **Updated JavaScript Example**

```javascript
const API_BASE = 'https://tflow-medical-triage.onrender.com/api';

// Combined symptoms + vitals submission
async function submitTriageWithVitals(symptoms, patientInfo, vitals) {
  try {
    const requestData = {
      symptoms,
      patient_info: patientInfo,
      use_ai: true
    };
    
    // Add vitals if provided
    if (vitals && (vitals.pulse || vitals.systolicBP || vitals.diastolicBP)) {
      requestData.vitals = vitals;
    }

    const response = await fetch(`${API_BASE}/triage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData)
    });

    const result = await response.json();
    
    return {
      // Triage results
      triageLevel: result.triage_level,
      recordId: result.record_id,
      timestamp: result.timestamp,
      
      // Vitals analysis (if vitals were provided)
      vitalsFlags: result.vitals_flags,
      vitalsRecordId: result.vitals_record_id,
      hasVitalsFlags: result.vitals_flags?.any_flag || false
    };
  } catch (error) {
    console.error('Triage API error:', error);
    throw error;
  }
}

// Example usage
const triageResult = await submitTriageWithVitals(
  "Patient has chest pain and difficulty breathing",
  { age: 45, gender: "M" },
  { pulse: 120, systolicBP: 180, diastolicBP: 95 }
);

console.log('Triage Level:', triageResult.triageLevel);
if (triageResult.hasVitalsFlags) {
  console.log('Vitals Analysis:', triageResult.vitalsFlags);
}
```

## 🎨 **React Component Example**

```jsx
import React, { useState } from 'react';

export const CombinedTriageForm = () => {
  const [symptoms, setSymptoms] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [patientGender, setPatientGender] = useState('');
  
  // Vitals states
  const [pulse, setPulse] = useState('');
  const [systolicBP, setSystolicBP] = useState('');
  const [diastolicBP, setDiastolicBP] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const patientInfo = {};
      if (patientAge) patientInfo.age = parseInt(patientAge);
      if (patientGender) patientInfo.gender = patientGender;
      
      const vitals = {};
      if (pulse) vitals.pulse = parseInt(pulse);
      if (systolicBP) vitals.systolicBP = parseInt(systolicBP);
      if (diastolicBP) vitals.diastolicBP = parseInt(diastolicBP);
      
      const triageResult = await submitTriageWithVitals(
        symptoms, 
        patientInfo, 
        Object.keys(vitals).length > 0 ? vitals : null
      );
      
      setResult(triageResult);
    } catch (error) {
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

  const renderVitalFlag = (flagName, flagValue) => {
    const isNormal = !flagValue;
    return (
      <div className={`flex items-center space-x-2 ${isNormal ? 'text-green-600' : 'text-red-600'}`}>
        <span>{isNormal ? '✅' : '🚨'}</span>
        <span className="capitalize">{flagName.replace('_flag', '')}</span>
        <span className="text-sm">({isNormal ? 'Normal' : 'Flagged'})</span>
      </div>
    );
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Medical Triage Assessment</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Symptoms Section */}
        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold mb-3">Symptoms</h3>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full p-3 border rounded-md"
            rows={4}
            placeholder="Describe patient symptoms..."
            required
            minLength={5}
            maxLength={2000}
          />
        </div>

        {/* Patient Info Section */}
        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold mb-3">Patient Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              value={patientAge}
              onChange={(e) => setPatientAge(e.target.value)}
              className="w-full p-3 border rounded-md"
              placeholder="Age"
              min={0}
              max={120}
            />
            <select
              value={patientGender}
              onChange={(e) => setPatientGender(e.target.value)}
              className="w-full p-3 border rounded-md"
            >
              <option value="">Select Gender</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
          </div>
        </div>

        {/* Vitals Section */}
        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold mb-3">Vital Signs (Optional)</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Pulse (BPM)</label>
              <input
                type="number"
                value={pulse}
                onChange={(e) => setPulse(e.target.value)}
                className="w-full p-3 border rounded-md"
                placeholder="80"
                min={30}
                max={250}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Systolic BP</label>
              <input
                type="number"
                value={systolicBP}
                onChange={(e) => setSystolicBP(e.target.value)}
                className="w-full p-3 border rounded-md"
                placeholder="120"
                min={60}
                max={300}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Diastolic BP</label>
              <input
                type="number"
                value={diastolicBP}
                onChange={(e) => setDiastolicBP(e.target.value)}
                className="w-full p-3 border rounded-md"
                placeholder="80"
                min={30}
                max={200}
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !symptoms.trim()}
          className="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Submit Triage Assessment'}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded-md">
          <h3 className="font-semibold mb-3">Assessment Results</h3>
          {result.error ? (
            <p className="text-red-600">{result.error}</p>
          ) : (
            <div className="space-y-3">
              {/* Triage Level */}
              <div>
                <span className="text-sm font-medium">Triage Level: </span>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getTriageColor(result.triageLevel)}`}>
                  {result.triageLevel}
                </span>
              </div>

              {/* Vitals Analysis */}
              {result.vitalsFlags && (
                <div>
                  <h4 className="font-medium mb-2">Vital Signs Analysis:</h4>
                  <div className="space-y-1">
                    {Object.entries(result.vitalsFlags)
                      .filter(([key]) => key !== 'any_flag')
                      .map(([key, value]) => (
                      <div key={key}>{renderVitalFlag(key, value)}</div>
                    ))}
                  </div>
                </div>
              )}

              {/* Record IDs */}
              <div className="text-sm text-gray-600 space-y-1">
                <p>Triage Record: {result.recordId}</p>
                {result.vitalsRecordId && (
                  <p>Vitals Record: {result.vitalsRecordId}</p>
                )}
                <p>Time: {new Date(result.timestamp).toLocaleString()}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

## ✅ **Key Benefits**

1. **Single Request**: Symptoms + vitals processed together
2. **Automatic Analysis**: Vitals automatically flagged when provided  
3. **Backward Compatible**: Symptoms-only requests still work
4. **Complete Records**: Both triage and vitals records created
5. **Unified Response**: All results in one response object

## 🔧 **Validation Rules**

**Required:**
- `symptoms`: 5-2000 characters

**Optional Vitals:**
- `pulse`: 30-250 BPM
- `systolicBP`: 60-300 mmHg
- `diastolicBP`: 30-200 mmHg (must be < systolic)

## 🎉 **Ready to Use!**

Your enhanced API is live at: https://tflow-medical-triage.onrender.com

**Test it now**: https://tflow-medical-triage.onrender.com/docs

The frontend can now capture symptoms and vitals in one form and get comprehensive triage results with vitals flagging included! 🚀
