// Node.js fetch polyfill for Node < 18
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

/**
 * Helper to call Groq's deepseek-r1-distill-llama-70b model for triage classification.
 * @param {string} symptomsText - The patient's symptom description.
 * @returns {Promise<string>} - The model's response as plain text.
 */
async function callGroq(symptomsText) {
  const apiKey = process.env.GROQ_API_KEY || 'YOUR_GROQ_API_KEY'; // Replace or set env var
  const url = 'https://api.groq.com/openai/v1/chat/completions';
  const payload = {
    model: 'deepseek-r1-distill-llama-70b',
    messages: [
      {
        role: 'system',
        content: `You are a highly reliable medical triage assistant for a hospital outpatient department. Your job is to classify the urgency of a patient's symptoms into one of four triage levels: Critical, Urgent, Moderate, or Low. Respond with only the triage level, and nothing else.`
      },
      {
        role: 'user',
        content: `A patient describes their symptoms: "${symptomsText}"
Based on this description, assign the most appropriate triage level:
- Critical: Life-threatening, needs immediate attention (e.g., coma, seizure, loss of consciousness)
- Urgent: Serious, needs prompt care (e.g., vomiting, blurred vision, slurred speech)
- Moderate: Needs medical attention but not urgent (e.g., headache, neck pain)
- Low: Minor symptoms, can wait (e.g., dizziness, mild pain, tiredness)

Respond with only one word: Critical, Urgent, Moderate, or Low.`
      }
    ],
    temperature: 0.2
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Groq API error: ${response.status}`);
  }
  const data = await response.json();
  const result = data.choices?.[0]?.message?.content?.trim();
  if (!result) throw new Error('No response from Groq AI');
  // Capitalize first letter, rest lowercase
  return result.charAt(0).toUpperCase() + result.slice(1).toLowerCase();
}

/**
 * Rule-based triage fallback function.
 * @param {string} symptomsText - Free-text description of symptoms.
 * @returns {string} - Triage level: "Critical", "Urgent", "Moderate", or "Low".
 */
function ruleBasedTriage(symptomsText) {
  const text = symptomsText.toLowerCase();
  const levels = [
    { level: "Critical", keywords: ["seizure", "loss of consciousness", "coma"] },
    { level: "Urgent", keywords: ["vomiting", "blurred vision", "slurred speech"] },
    { level: "Moderate", keywords: ["headache", "neck pain"] },
    { level: "Low", keywords: ["dizziness", "mild pain", "tiredness"] }
  ];
  for (const { level, keywords } of levels) {
    if (keywords.some(keyword => text.includes(keyword))) {
      return level;
    }
  }
  return "Moderate";
}

/**
 * Triage a patient using Groq AI or rule-based fallback (OFFLINE VERSION).
 * @param {string} symptomsText - Symptom description.
 * @param {Object} patientInfo - Patient information (optional).
 * @param {boolean} [useAI=true] - Whether to use Groq AI. If false or API fails, fallback to rules.
 * @returns {Promise<Object>} - Triage result with level and mock database record.
 */
async function triagePatient(symptomsText, patientInfo = {}, useAI = true) {
  let triageLevel;
  
  if (useAI) {
    try {
      triageLevel = await callGroq(symptomsText);
    } catch (e) {
      // Fallback to rule-based if API fails
      triageLevel = ruleBasedTriage(symptomsText);
    }
  } else {
    triageLevel = ruleBasedTriage(symptomsText);
  }

  // Mock database storage (for testing without Firestore)
  const triageData = {
    symptoms: symptomsText,
    triageLevel: triageLevel,
    patientInfo: patientInfo,
    timestamp: new Date(),
    useAI: useAI
  };

  // Generate a mock record ID
  const mockRecordId = 'mock_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  
  return {
    triageLevel: triageLevel,
    recordId: mockRecordId,
    timestamp: triageData.timestamp,
    data: triageData,
    note: "OFFLINE MODE - Data not stored in Firestore"
  };
}

/**
 * Flag abnormal vital signs (OFFLINE VERSION).
 * @param {Object} vitals - Patient vitals.
 * @param {number} vitals.pulse - Pulse rate (bpm).
 * @param {number} vitals.systolicBP - Systolic blood pressure (mmHg).
 * @param {number} vitals.diastolicBP - Diastolic blood pressure (mmHg).
 * @param {Object} patientInfo - Patient information (optional).
 * @returns {Promise<Object>} - Vital signs analysis with flags and mock database record.
 */
async function flagVitals(vitals, patientInfo = {}) {
  const pulseFlag = vitals.pulse < 60 || vitals.pulse > 100;
  const systolicFlag = vitals.systolicBP < 90 || vitals.systolicBP > 160;
  const diastolicFlag = vitals.diastolicBP < 60 || vitals.diastolicBP > 100;
  const anyFlag = pulseFlag || systolicFlag || diastolicFlag;

  const vitalsData = {
    vitals: vitals,
    flags: { pulseFlag, systolicFlag, diastolicFlag, anyFlag },
    patientInfo: patientInfo,
    timestamp: new Date()
  };

  // Generate a mock record ID
  const mockRecordId = 'mock_vitals_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  
  return {
    flags: { pulseFlag, systolicFlag, diastolicFlag, anyFlag },
    recordId: mockRecordId,
    timestamp: vitalsData.timestamp,
    data: vitalsData,
    note: "OFFLINE MODE - Data not stored in Firestore"
  };
}

/**
 * Mock function for retrieving recent records (OFFLINE VERSION).
 * @param {number} limit - Number of records to retrieve (default: 10).
 * @returns {Promise<Array>} - Empty array since we're in offline mode.
 */
async function getRecentTriageRecords(limitCount = 10) {
  console.log(`[OFFLINE MODE] Would retrieve ${limitCount} recent triage records from Firestore`);
  return [];
}

/**
 * Mock function for retrieving recent vitals records (OFFLINE VERSION).
 * @param {number} limit - Number of records to retrieve (default: 10).
 * @returns {Promise<Array>} - Empty array since we're in offline mode.
 */
async function getRecentVitalsRecords(limitCount = 10) {
  console.log(`[OFFLINE MODE] Would retrieve ${limitCount} recent vitals records from Firestore`);
  return [];
}

// Export functions for use in other modules
module.exports = { 
  triagePatient, 
  flagVitals, 
  callGroq, 
  getRecentTriageRecords, 
  getRecentVitalsRecords 
}; 