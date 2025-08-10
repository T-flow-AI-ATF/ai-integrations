# 🎯 Next.js Quick Start - React Hook

## Custom Hook for Easy Integration

Create `hooks/useTriage.ts`:

```typescript
// hooks/useTriage.ts
import { useState } from 'react';
import { TriageAPI } from '@/lib/triage-api';
import { TriageRequest, TriageResponse } from '@/types/triage';

interface UseTriageState {
  loading: boolean;
  result: TriageResponse | null;
  error: string | null;
}

interface UseTriageReturn extends UseTriageState {
  submitTriage: (request: TriageRequest) => Promise<void>;
  reset: () => void;
}

export function useTriage(): UseTriageReturn {
  const [state, setState] = useState<UseTriageState>({
    loading: false,
    result: null,
    error: null,
  });

  const submitTriage = async (request: TriageRequest) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const result = await TriageAPI.submitTriage(request);
      setState(prev => ({ ...prev, result, loading: false }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to process triage';
      setState(prev => ({ ...prev, error: errorMessage, loading: false }));
    }
  };

  const reset = () => {
    setState({ loading: false, result: null, error: null });
  };

  return { ...state, submitTriage, reset };
}
```

## Simple Form Component Using Hook

```tsx
// components/SimpleTriageForm.tsx
'use client';

import { useState } from 'react';
import { useTriage } from '@/hooks/useTriage';

export default function SimpleTriageForm() {
  const [symptoms, setSymptoms] = useState('');
  const [age, setAge] = useState('');
  const [pulse, setPulse] = useState('');
  const [systolic, setSystolic] = useState('');
  const [diastolic, setDiastolic] = useState('');

  const { loading, result, error, submitTriage, reset } = useTriage();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    await submitTriage({
      symptoms: symptoms.trim(),
      patient_info: age ? { age: parseInt(age) } : undefined,
      vitals: (pulse || systolic || diastolic) ? {
        pulse: pulse ? parseInt(pulse) : undefined,
        systolicBP: systolic ? parseInt(systolic) : undefined,
        diastolicBP: diastolic ? parseInt(diastolic) : undefined,
      } : undefined,
      use_ai: true
    });
  };

  if (result) {
    return (
      <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Triage Result</h2>
        
        <div className={`p-4 rounded-lg mb-4 ${
          result.triage_level === 'Critical' ? 'bg-red-100 text-red-800' :
          result.triage_level === 'Urgent' ? 'bg-orange-100 text-orange-800' :
          result.triage_level === 'Moderate' ? 'bg-yellow-100 text-yellow-800' :
          'bg-green-100 text-green-800'
        }`}>
          <div className="text-2xl font-bold">{result.triage_level}</div>
        </div>

        {result.vitals_flags && (
          <div className="mb-4">
            <h3 className="font-semibold mb-2">Vitals:</h3>
            {Object.entries(result.vitals_flags)
              .filter(([key]) => key !== 'any_flag')
              .map(([key, flagged]) => (
                <div key={key} className="flex justify-between">
                  <span className="capitalize">{key.replace('_flag', '')}:</span>
                  <span className={flagged ? 'text-red-600' : 'text-green-600'}>
                    {flagged ? '⚠️ Flagged' : '✅ Normal'}
                  </span>
                </div>
              ))}
          </div>
        )}

        <button 
          onClick={reset}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          New Assessment
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Medical Triage</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Symptoms *</label>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            className="w-full p-2 border rounded"
            rows={3}
            placeholder="Describe symptoms..."
            required
            minLength={5}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Age</label>
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="35"
            min={0}
            max={120}
          />
        </div>

        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="block text-xs mb-1">Pulse</label>
            <input
              type="number"
              value={pulse}
              onChange={(e) => setPulse(e.target.value)}
              className="w-full p-2 border rounded text-sm"
              placeholder="80"
              min={30}
              max={250}
            />
          </div>
          <div>
            <label className="block text-xs mb-1">Systolic</label>
            <input
              type="number"
              value={systolic}
              onChange={(e) => setSystolic(e.target.value)}
              className="w-full p-2 border rounded text-sm"
              placeholder="120"
              min={60}
              max={300}
            />
          </div>
          <div>
            <label className="block text-xs mb-1">Diastolic</label>
            <input
              type="number"
              value={diastolic}
              onChange={(e) => setDiastolic(e.target.value)}
              className="w-full p-2 border rounded text-sm"
              placeholder="80"
              min={30}
              max={200}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !symptoms.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Submit Assessment'}
        </button>
      </form>
    </div>
  );
}
```

## Super Simple Page

```tsx
// app/page.tsx or pages/index.tsx
import SimpleTriageForm from '@/components/SimpleTriageForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <SimpleTriageForm />
    </div>
  );
}
```

## One Command Setup

```bash
# Install everything needed
npm install axios && mkdir -p lib hooks components types && echo "Ready to copy the code above!"
```

This gives your frontend dev a **working triage form in under 10 minutes** with full symptoms + vitals integration! 🚀
