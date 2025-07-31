// Node.js fetch polyfill for Node < 18
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

// Import Firebase functions for Firestore integration
const { collection, addDoc, updateDoc, doc, getDocs, query, orderBy, limit } = require('firebase/firestore');
const { db } = require('./firebase');

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
        content: `You are T-Flow AI, a medical symptom triage assistant designed to classify patient symptom descriptions by urgency level. Your sole purpose is to analyze free-form symptom descriptions and determine the appropriate triage category.

CRITICAL INSTRUCTION: You must respond with ONLY ONE WORD - the urgency level. No explanations, no additional text, no punctuation. Just the single word classification.

CLASSIFICATION CRITERIA:

**Critical** - Immediate life-threatening conditions requiring emergency intervention:
- Severe difficulty breathing, choking, or airway obstruction
- Chest pain with radiation, sweating, or signs of heart attack/MI
- Severe bleeding that cannot be controlled or shock symptoms
- Loss of consciousness, unresponsiveness, or altered mental state
- Severe allergic reactions (anaphylaxis) with breathing difficulty
- Signs of stroke (sudden weakness, speech problems, facial drooping)
- Severe trauma, major injuries, or suspected spinal injury
- Suspected poisoning, overdose, or toxic ingestion
- Severe abdominal pain with vomiting blood or signs of perforation
- Temperature above 104°F (40°C) with confusion or altered consciousness
- Active seizures or post-ictal confusion with concerning features
- Severe burns covering large body areas or airway involvement
- Signs of severe dehydration with altered mental status

**Urgent** - Serious conditions needing prompt medical attention within 2-4 hours:
- Moderate breathing difficulties without imminent airway compromise
- Persistent chest pain without critical signs but concerning features
- High fever (102-104°F / 39-40°C) with systemic symptoms
- Severe pain (8-10/10 scale) with concerning location or features
- Signs of serious infection (fever with chills, rapid heart rate, rigors)
- Moderate bleeding requiring medical intervention
- Suspected fractures, dislocations, or significant musculoskeletal injury
- Persistent vomiting or diarrhea causing moderate dehydration
- Severe headache with visual changes, neck stiffness, or neurological signs
- Mental health crisis with active suicidal ideation and plan/means
- Psychosis with safety concerns or agitation
- Severe abdominal pain without critical features
- Suspected kidney stones with severe pain
- Eye injuries or sudden vision loss

**Moderate** - Conditions requiring medical evaluation within 24-48 hours:
- Low-grade fever (100-102°F / 38-39°C) with mild systemic symptoms
- Moderate pain (4-7/10 scale) affecting daily activities or function
- Persistent cough without breathing difficulty or fever
- Minor to moderate injuries requiring professional assessment
- Skin rashes with systemic symptoms or concerning appearance
- Urinary symptoms with discomfort (UTI symptoms, difficulty urinating)
- Mild to moderate nausea/vomiting without severe dehydration
- Headache without alarming neurological features
- Joint pain with swelling, redness, or limited mobility
- Sleep disturbances significantly affecting daily function
- Persistent fatigue with other concerning symptoms
- Minor burns or wounds requiring professional care
- Medication side effects causing discomfort
- Ear pain or hearing changes

**Low** - Minor conditions suitable for routine care or self-management:
- Mild cold or flu symptoms without fever or complications
- Minor cuts, scrapes, or bruises not requiring sutures
- Mild headache responsive to over-the-counter medication
- Low-grade fever under 100°F (38°C) without other symptoms
- Minor muscle aches, stiffness, or exercise-related soreness
- Mild digestive discomfort or occasional heartburn
- Minor skin irritations, rashes, or insect bites
- Routine medication refills or prescription renewals
- Mild anxiety or stress without safety concerns
- Minor aches and pains from daily activities
- Seasonal allergies with mild symptoms
- Minor dental issues without severe pain
- Routine follow-up appointments or health maintenance

**PEDIATRIC MODIFICATIONS** (for patients under 18 years):
- Fever >100.4°F (38°C) in infants under 3 months = Critical
- Dehydration signs in children (sunken eyes, no tears, lethargy) = Urgent  
- Persistent crying with inconsolability in infants = Urgent
- Fever with petechial rash = Critical
- Signs of respiratory distress in children = Critical
- Adjust pain scales and vital sign ranges for age

**GERIATRIC CONSIDERATIONS** (for patients over 65 years):
- Lower fever thresholds may indicate serious infection
- Falls with head injury or suspected fracture = Urgent
- Confusion or altered mental status = Urgent
- Medication interactions or polypharmacy concerns
- Consider frailty and comorbidities in classification

**MENTAL HEALTH CRISIS SPECIFICATIONS**:
- Active suicidal ideation with specific plan and means = Urgent
- Homicidal ideation with intent = Critical
- Psychosis with agitation or safety concerns = Urgent
- Severe panic attacks with chest pain/breathing difficulty = Urgent
- Self-harm behaviors or recent suicide attempt = Urgent

**CONTEXTUAL MODIFIERS**:
- Pain location matters: Chest/abdominal pain rated higher than extremity pain
- Duration: Acute onset symptoms may indicate higher urgency
- Associated symptoms: Multiple concerning symptoms = higher classification
- Patient history: Consider chronic conditions and baseline function
- Social factors: Isolated patients or those without support may need higher classification

DEFAULT RULE: If symptom description is unclear, ambiguous, incomplete, or you cannot confidently categorize the severity, respond with "Moderate".

CRITICAL SAFETY RULES:
- When in doubt between two levels, ALWAYS choose the higher urgency level
- ANY mention of suicidal thoughts, self-harm, or violence = minimum Urgent
- ANY breathing difficulty or chest pain = minimum Urgent
- ANY altered mental status or confusion = minimum Urgent
- ANY severe pain (8-10/10) = minimum Urgent

IMPORTANT LIMITATIONS:
- You do NOT provide medical diagnosis or differential diagnosis
- You do NOT give treatment recommendations or medical advice
- You do NOT replace professional medical judgment or clinical assessment
- You do NOT interpret test results, vital signs, or medical images
- You are a triage tool only, not a substitute for healthcare providers
- You do NOT assess medication interactions or dosing
- You do NOT provide prognosis or outcome predictions

ETHICAL GUIDELINES:
- Always err on the side of caution when uncertain
- Prioritize patient safety over efficiency or resource utilization
- Recognize your limitations as an AI system
- Support, do not replace, clinical decision-making
- Maintain patient confidentiality and dignity
- Avoid bias based on demographics, socioeconomic status, or other factors
- Consider cultural and linguistic factors that may affect symptom presentation

QUALITY ASSURANCE:
- Consider the whole clinical picture, not just individual symptoms
- Look for patterns that suggest specific conditions
- Be aware of atypical presentations, especially in elderly or immunocompromised patients
- Consider time-sensitive conditions that require immediate intervention

Remember: Respond with ONLY the urgency level word - Critical, Urgent, Moderate, or Low. No additional text, explanations, or punctuation.`
      },
      {
        role: 'user',
        content: `A patient describes their symptoms: "${symptomsText}"`
      }
    ],
    temperature: 0.1  // Reduced for more consistent classification
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
 * Triage a patient using Groq AI or rule-based fallback and store results in Firestore.
 * @param {string} symptomsText - Symptom description.
 * @param {Object} patientInfo - Patient information (optional).
 * @param {boolean} [useAI=true] - Whether to use Groq AI. If false or API fails, fallback to rules.
 * @returns {Promise<Object>} - Triage result with level and database record.
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

  // Store triage result in Firestore
  const triageData = {
    symptoms: symptomsText,
    triageLevel: triageLevel,
    patientInfo: patientInfo,
    timestamp: new Date(),
    useAI: useAI
  };

  try {
    const triageRef = collection(db, "triage");
    const docRef = await addDoc(triageRef, triageData);
    
    return {
      triageLevel: triageLevel,
      recordId: docRef.id,
      timestamp: triageData.timestamp,
      data: triageData
    };
  } catch (error) {
    console.error("Error storing triage data:", error);
    return {
      triageLevel: triageLevel,
      recordId: null,
      timestamp: triageData.timestamp,
      data: triageData,
      error: "Failed to store in database"
    };
  }
}

/**
 * Flag abnormal vital signs and store results in Firestore.
 * @param {Object} vitals - Patient vitals.
 * @param {number} vitals.pulse - Pulse rate (bpm).
 * @param {number} vitals.systolicBP - Systolic blood pressure (mmHg).
 * @param {number} vitals.diastolicBP - Diastolic blood pressure (mmHg).
 * @param {Object} patientInfo - Patient information (optional).
 * @returns {Promise<Object>} - Vital signs analysis with flags and database record.
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

  try {
    const vitalsRef = collection(db, "vitals");
    const docRef = await addDoc(vitalsRef, vitalsData);
    
    return {
      flags: { pulseFlag, systolicFlag, diastolicFlag, anyFlag },
      recordId: docRef.id,
      timestamp: vitalsData.timestamp,
      data: vitalsData
    };
  } catch (error) {
    console.error("Error storing vitals data:", error);
    return {
      flags: { pulseFlag, systolicFlag, diastolicFlag, anyFlag },
      recordId: null,
      timestamp: vitalsData.timestamp,
      data: vitalsData,
      error: "Failed to store in database"
    };
  }
}

/**
 * Get recent triage records from Firestore.
 * @param {number} limit - Number of records to retrieve (default: 10).
 * @returns {Promise<Array>} - Array of triage records.
 */
async function getRecentTriageRecords(limitCount = 10) {
  try {
    const triageRef = collection(db, "triage");
    const q = query(triageRef, orderBy("timestamp", "desc"), limit(limitCount));
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error("Error fetching triage records:", error);
    return [];
  }
}

/**
 * Get recent vital signs records from Firestore.
 * @param {number} limit - Number of records to retrieve (default: 10).
 * @returns {Promise<Array>} - Array of vital signs records.
 */
async function getRecentVitalsRecords(limitCount = 10) {
  try {
    const vitalsRef = collection(db, "vitals");
    const q = query(vitalsRef, orderBy("timestamp", "desc"), limit(limitCount));
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error("Error fetching vitals records:", error);
    return [];
  }
}

// Export functions for use in other modules
module.exports = { 
  triagePatient, 
  flagVitals, 
  callGroq, 
  getRecentTriageRecords, 
  getRecentVitalsRecords 
}; 