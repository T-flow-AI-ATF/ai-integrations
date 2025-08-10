# 🚀 T-Flow Triage API - Next.js Integration Guide

## 📋 **Live API Information**

**Base URL**: `https://tflow-medical-triage.onrender.com`  
**Interactive Docs**: https://tflow-medical-triage.onrender.com/docs

## 🔧 **Next.js Setup**

### 1. Install Dependencies

```bash
npm install axios
# or
yarn add axios

# For TypeScript (recommended)
npm install -D @types/node
```

### 2. TypeScript Interfaces

Create `types/triage.ts`:

```typescript
// types/triage.ts
export interface PatientInfo {
  age?: number;
  gender?: 'M' | 'F' | 'O';
  medical_history?: string;
}

export interface VitalsData {
  pulse?: number;
  systolicBP?: number;
  diastolicBP?: number;
}

export interface TriageRequest {
  symptoms: string;
  patient_info?: PatientInfo;
  vitals?: VitalsData;
  use_ai?: boolean;
}

export interface VitalsFlags {
  pulse_flag: boolean;
  systolic_flag: boolean;
  diastolic_flag: boolean;
  any_flag: boolean;
}

export interface TriageResponse {
  triage_level: 'Critical' | 'Urgent' | 'Moderate' | 'Low';
  record_id: string;
  timestamp: string;
  vitals_flags?: VitalsFlags;
  vitals_record_id?: string;
  error?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  timestamp: string;
}
```

### 3. API Client Service

Create `lib/triage-api.ts`:

```typescript
// lib/triage-api.ts
import axios from 'axios';
import { TriageRequest, TriageResponse, HealthResponse } from '@/types/triage';

const API_BASE = 'https://tflow-medical-triage.onrender.com/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 60000, // 60 seconds for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export class TriageAPI {
  /**
   * Submit combined triage assessment with symptoms and optional vitals
   */
  static async submitTriage(request: TriageRequest): Promise<TriageResponse> {
    try {
      const response = await apiClient.post<TriageResponse>('/triage', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.detail || 
          error.message || 
          'Failed to process triage request'
        );
      }
      throw error;
    }
  }

  /**
   * Check API health status
   */
  static async checkHealth(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * Get recent triage records
   */
  static async getRecentTriage(limit: number = 10) {
    const response = await apiClient.get(`/triage/recent?limit=${limit}`);
    return response.data;
  }

  /**
   * Get system statistics
   */
  static async getStats() {
    const response = await apiClient.get('/stats');
    return response.data;
  }
}

export default TriageAPI;
```

### 4. Next.js API Route (Optional Server-Side Proxy)

Create `pages/api/triage.ts` or `app/api/triage/route.ts`:

```typescript
// pages/api/triage.ts (Pages Router)
import type { NextApiRequest, NextApiResponse } from 'next';
import { TriageAPI } from '@/lib/triage-api';
import { TriageRequest } from '@/types/triage';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const triageRequest: TriageRequest = req.body;
    
    // Validate required fields
    if (!triageRequest.symptoms || triageRequest.symptoms.trim().length < 5) {
      return res.status(400).json({ error: 'Symptoms must be at least 5 characters' });
    }

    const result = await TriageAPI.submitTriage(triageRequest);
    res.status(200).json(result);
  } catch (error) {
    console.error('Triage API error:', error);
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Internal server error' 
    });
  }
}
```

```typescript
// app/api/triage/route.ts (App Router)
import { NextRequest, NextResponse } from 'next/server';
import { TriageAPI } from '@/lib/triage-api';
import { TriageRequest } from '@/types/triage';

export async function POST(request: NextRequest) {
  try {
    const triageRequest: TriageRequest = await request.json();
    
    // Validate required fields
    if (!triageRequest.symptoms || triageRequest.symptoms.trim().length < 5) {
      return NextResponse.json(
        { error: 'Symptoms must be at least 5 characters' },
        { status: 400 }
      );
    }

    const result = await TriageAPI.submitTriage(triageRequest);
    return NextResponse.json(result);
  } catch (error) {
    console.error('Triage API error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## 🎨 **React Components**

### 1. Main Triage Form Component

Create `components/TriageForm.tsx`:

```tsx
// components/TriageForm.tsx
'use client';

import { useState } from 'react';
import { TriageAPI } from '@/lib/triage-api';
import { TriageRequest, TriageResponse, PatientInfo, VitalsData } from '@/types/triage';

interface TriageFormProps {
  onResult?: (result: TriageResponse) => void;
}

export default function TriageForm({ onResult }: TriageFormProps) {
  const [symptoms, setSymptoms] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [patientGender, setPatientGender] = useState<'M' | 'F' | 'O' | ''>('');
  const [medicalHistory, setMedicalHistory] = useState('');
  
  // Vitals state
  const [pulse, setPulse] = useState('');
  const [systolicBP, setSystolicBP] = useState('');
  const [diastolicBP, setDiastolicBP] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TriageResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Prepare patient info
      const patientInfo: PatientInfo = {};
      if (patientAge) patientInfo.age = parseInt(patientAge);
      if (patientGender) patientInfo.gender = patientGender;
      if (medicalHistory.trim()) patientInfo.medical_history = medicalHistory.trim();

      // Prepare vitals
      const vitals: VitalsData = {};
      if (pulse) vitals.pulse = parseInt(pulse);
      if (systolicBP) vitals.systolicBP = parseInt(systolicBP);
      if (diastolicBP) vitals.diastolicBP = parseInt(diastolicBP);

      // Prepare request
      const request: TriageRequest = {
        symptoms: symptoms.trim(),
        patient_info: Object.keys(patientInfo).length > 0 ? patientInfo : undefined,
        vitals: Object.keys(vitals).length > 0 ? vitals : undefined,
        use_ai: true
      };

      const triageResult = await TriageAPI.submitTriage(request);
      setResult(triageResult);
      onResult?.(triageResult);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to process triage request';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const getTriageColorClass = (level: string) => {
    switch (level) {
      case 'Critical': return 'bg-red-100 text-red-800 border-red-300';
      case 'Urgent': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'Moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const renderVitalFlag = (flagName: string, flagValue: boolean) => {
    const displayName = flagName.replace('_flag', '').replace(/([A-Z])/g, ' $1').trim();
    const isNormal = !flagValue;
    
    return (
      <div key={flagName} className={`flex items-center space-x-2 p-2 rounded ${isNormal ? 'bg-green-50' : 'bg-red-50'}`}>
        <span className="text-lg">{isNormal ? '✅' : '🚨'}</span>
        <span className="font-medium capitalize">{displayName}</span>
        <span className={`text-sm px-2 py-1 rounded ${isNormal ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
          {isNormal ? 'Normal' : 'Flagged'}
        </span>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">Medical Triage Assessment</h2>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Symptoms Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Patient Symptoms *</h3>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={4}
            placeholder="Describe the patient's symptoms in detail (e.g., 'Patient has severe chest pain, difficulty breathing, and feels dizzy')..."
            required
            minLength={5}
            maxLength={2000}
          />
          <p className="text-sm text-gray-600 mt-2">
            {symptoms.length}/2000 characters (minimum 5)
          </p>
        </div>

        {/* Patient Information Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Patient Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
              <input
                type="number"
                value={patientAge}
                onChange={(e) => setPatientAge(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="35"
                min={0}
                max={120}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
              <select
                value={patientGender}
                onChange={(e) => setPatientGender(e.target.value as 'M' | 'F' | 'O' | '')}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Gender</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="O">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Medical History</label>
              <input
                type="text"
                value={medicalHistory}
                onChange={(e) => setMedicalHistory(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="diabetes, hypertension..."
              />
            </div>
          </div>
        </div>

        {/* Vitals Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Vital Signs (Optional)</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Pulse (BPM)
                <span className="text-gray-500 text-xs ml-1">(30-250)</span>
              </label>
              <input
                type="number"
                value={pulse}
                onChange={(e) => setPulse(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="80"
                min={30}
                max={250}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Systolic BP (mmHg)
                <span className="text-gray-500 text-xs ml-1">(60-300)</span>
              </label>
              <input
                type="number"
                value={systolicBP}
                onChange={(e) => setSystolicBP(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="120"
                min={60}
                max={300}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Diastolic BP (mmHg)
                <span className="text-gray-500 text-xs ml-1">(30-200)</span>
              </label>
              <input
                type="number"
                value={diastolicBP}
                onChange={(e) => setDiastolicBP(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="80"
                min={30}
                max={200}
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !symptoms.trim() || symptoms.length < 5}
          className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Processing Assessment...</span>
            </div>
          ) : (
            'Submit Triage Assessment'
          )}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <div className="flex items-center space-x-2">
            <span className="text-xl">❌</span>
            <span className="font-semibold">Error:</span>
          </div>
          <p className="mt-1">{error}</p>
        </div>
      )}

      {/* Results Display */}
      {result && !error && (
        <div className="mt-8 space-y-6">
          <h3 className="text-2xl font-bold text-gray-900">Assessment Results</h3>
          
          {/* Triage Level */}
          <div className="bg-white p-6 rounded-lg border-2 shadow-sm">
            <h4 className="text-lg font-semibold mb-3">Triage Classification</h4>
            <div className={`inline-flex items-center px-6 py-3 rounded-lg border-2 font-bold text-lg ${getTriageColorClass(result.triage_level)}`}>
              <span className="text-2xl mr-3">
                {result.triage_level === 'Critical' ? '🚨' : 
                 result.triage_level === 'Urgent' ? '⚠️' : 
                 result.triage_level === 'Moderate' ? '📋' : '✅'}
              </span>
              {result.triage_level}
            </div>
          </div>

          {/* Vitals Analysis */}
          {result.vitals_flags && (
            <div className="bg-white p-6 rounded-lg border-2 shadow-sm">
              <h4 className="text-lg font-semibold mb-4">Vital Signs Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {Object.entries(result.vitals_flags)
                  .filter(([key]) => key !== 'any_flag')
                  .map(([key, value]) => renderVitalFlag(key, value))}
              </div>
              {result.vitals_flags.any_flag && (
                <div className="mt-4 p-3 bg-red-100 border border-red-300 rounded-lg">
                  <p className="text-red-800 font-medium">
                    ⚠️ One or more vital signs are outside normal ranges
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Record Information */}
          <div className="bg-gray-100 p-4 rounded-lg text-sm text-gray-600">
            <h4 className="font-semibold mb-2">Record Information</h4>
            <div className="space-y-1">
              <p><span className="font-medium">Triage Record ID:</span> {result.record_id}</p>
              {result.vitals_record_id && (
                <p><span className="font-medium">Vitals Record ID:</span> {result.vitals_record_id}</p>
              )}
              <p><span className="font-medium">Timestamp:</span> {new Date(result.timestamp).toLocaleString()}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 2. Main Page Component

Create `pages/index.tsx` or `app/page.tsx`:

```tsx
// pages/index.tsx (Pages Router) or app/page.tsx (App Router)
import { useState, useEffect } from 'react';
import TriageForm from '@/components/TriageForm';
import { TriageAPI } from '@/lib/triage-api';
import { TriageResponse } from '@/types/triage';

export default function HomePage() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    // Check API health on page load
    const checkApiHealth = async () => {
      try {
        await TriageAPI.checkHealth();
        setApiStatus('online');
      } catch (error) {
        console.error('API health check failed:', error);
        setApiStatus('offline');
      }
    };

    checkApiHealth();
  }, []);

  const handleTriageResult = (result: TriageResponse) => {
    console.log('Triage assessment completed:', result);
    // You can add additional handling here, such as:
    // - Saving to local state
    // - Sending to analytics
    // - Navigating to results page
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">T-Flow Medical Triage</h1>
              <p className="text-gray-600 mt-1">AI-Powered Emergency Assessment System</p>
            </div>
            
            {/* API Status Indicator */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                apiStatus === 'online' ? 'bg-green-500' : 
                apiStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
              }`}></div>
              <span className="text-sm text-gray-600">
                API {apiStatus === 'checking' ? 'Checking...' : 
                     apiStatus === 'online' ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {apiStatus === 'offline' && (
            <div className="mb-8 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              <div className="flex items-center space-x-2">
                <span className="text-xl">⚠️</span>
                <span className="font-semibold">API Connection Issue</span>
              </div>
              <p className="mt-1">
                The triage API is currently unavailable. This may be due to a cold start delay (10-30 seconds) or maintenance.
              </p>
            </div>
          )}
          
          <TriageForm onResult={handleTriageResult} />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>T-Flow Medical Triage System - Powered by Groq AI & Supabase</p>
            <p className="text-sm mt-2">
              API Documentation: <a 
                href="https://tflow-medical-triage.onrender.com/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                View API Docs
              </a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
```

### 3. Environment Configuration

Create `.env.local`:

```bash
# .env.local
NEXT_PUBLIC_TRIAGE_API_URL=https://tflow-medical-triage.onrender.com/api

# If you add authentication later
# TRIAGE_API_KEY=your-api-key-here
```

## 🚀 **Quick Start Commands**

```bash
# Install dependencies
npm install axios

# Run development server  
npm run dev

# Build for production
npm run build
npm start
```

## 📱 **Mobile Responsiveness**

The components above use Tailwind CSS classes that are mobile-responsive:
- `grid-cols-1 md:grid-cols-3` - Single column on mobile, three columns on desktop
- `max-w-4xl mx-auto` - Centered layout with max width
- `px-4 sm:px-6 lg:px-8` - Responsive padding

## 🔧 **Additional Features You Can Add**

1. **Loading States**: Skeleton components while API requests are processing
2. **Error Boundary**: Catch and display React errors gracefully
3. **Form Validation**: Client-side validation before API calls
4. **Results History**: Store and display previous assessments
5. **Print Functionality**: Allow printing of triage results
6. **PWA Support**: Make the app work offline with cached results

## 🎉 **Ready to Build!**

Your Next.js frontend can now:
- ✅ Submit symptoms + vitals in one request
- ✅ Display comprehensive triage results with vitals flags
- ✅ Handle API errors gracefully
- ✅ Show loading states during processing
- ✅ Work responsively on all devices

**API Base URL**: `https://tflow-medical-triage.onrender.com`  
**Test the API**: https://tflow-medical-triage.onrender.com/docs
