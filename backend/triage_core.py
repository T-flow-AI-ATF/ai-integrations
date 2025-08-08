#!/usr/bin/env python3
"""
T-Flow AI Medical Triage System - Core Module
AI-powered medical triage with Supabase integration
Optimized for backend deployment
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
from groq import Groq
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url:
    raise ValueError("SUPABASE_URL environment variable is required")
if not supabase_key:
    raise ValueError("SUPABASE_ANON_KEY environment variable is required")

supabase: Client = create_client(supabase_url, supabase_key)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is required")

groq_client = Groq(api_key=groq_api_key)


async def call_groq(symptoms_text: str) -> str:
    """
    Calls Groq's Llama-3-70B model for triage classification.

    Args:
        symptoms_text (str): The patient's symptom description.

    Returns:
        str: The model's response as plain text.
    """
    system_prompt = """You are T-Flow AI, a medical symptom triage assistant designed to classify patient symptom descriptions by urgency level. Your sole purpose is to analyze free-form symptom descriptions and determine the appropriate triage category.

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

Remember: Respond with ONLY the urgency level word - Critical, Urgent, Moderate, or Low. No additional text, explanations, or punctuation."""

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'A patient describes their symptoms: "{symptoms_text}"'}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        
        result = chat_completion.choices[0].message.content.strip()
        if not result:
            raise Exception("No response from Groq AI")
        
        # Extract the final classification from AI response (after any reasoning)
        # Look for the last line that contains a valid triage level
        lines = result.split('\n')
        valid_levels = ['critical', 'urgent', 'moderate', 'low']
        
        for line in reversed(lines):
            line_clean = line.strip().lower()
            if line_clean in valid_levels:
                return line_clean.capitalize()
        
        # If no valid level found, return the last non-empty line capitalized
        for line in reversed(lines):
            if line.strip():
                return line.strip().lower().capitalize()
        
        # Fallback
        return result.capitalize()
        
    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")


def rule_based_triage(symptoms_text: str) -> str:
    """
    Rule-based triage fallback function.
    
    Args:
        symptoms_text (str): Free-text description of symptoms.
        
    Returns:
        str: Triage level: "Critical", "Urgent", "Moderate", or "Low".
    """
    text = symptoms_text.lower()
    
    levels = [
        {"level": "Critical", "keywords": ["seizure", "loss of consciousness", "coma"]},
        {"level": "Urgent", "keywords": ["vomiting", "blurred vision", "slurred speech"]},
        {"level": "Moderate", "keywords": ["headache", "neck pain"]},
        {"level": "Low", "keywords": ["dizziness", "mild pain", "tiredness"]}
    ]
    
    for level_info in levels:
        if any(keyword in text for keyword in level_info["keywords"]):
            return level_info["level"]
    
    return "Moderate"


async def triage_patient(symptoms_text: str, patient_info: Optional[Dict] = None, use_ai: bool = True) -> Dict:
    """
    Triage a patient using Groq AI or rule-based fallback and store results in Supabase.
    
    Args:
        symptoms_text (str): Symptom description.
        patient_info (Dict, optional): Patient information.
        use_ai (bool): Whether to use Groq AI. If False or API fails, fallback to rules.
        
    Returns:
        Dict: Triage result with level and database record.
    """
    if patient_info is None:
        patient_info = {}
    
    triage_level = ""
    
    if use_ai:
        try:
            triage_level = await call_groq(symptoms_text)
        except Exception as e:
            print(f"AI failed, using rule-based fallback: {e}")
            triage_level = rule_based_triage(symptoms_text)
    else:
        triage_level = rule_based_triage(symptoms_text)
    
    # Store triage result in Supabase
    try:
        data = supabase.table('triage').insert({
            'symptoms': symptoms_text,
            'triage_level': triage_level,
            'patient_info': patient_info,
            'use_ai': use_ai
        }).execute()
        
        return {
            'triage_level': triage_level,
            'record_id': data.data[0]['id'],
            'timestamp': data.data[0]['created_at'],
            'data': data.data[0]
        }
        
    except Exception as error:
        print(f"Error storing triage data: {error}")
        return {
            'triage_level': triage_level,
            'record_id': None,
            'timestamp': datetime.now().isoformat(),
            'data': None,
            'error': "Failed to store in database"
        }


async def flag_vitals(vitals: Dict, patient_info: Optional[Dict] = None) -> Dict:
    """
    Flag abnormal vital signs and store results in Supabase.
    
    Args:
        vitals (Dict): Patient vitals with keys: pulse, systolicBP, diastolicBP.
        patient_info (Dict, optional): Patient information.
        
    Returns:
        Dict: Vital signs analysis with flags and database record.
    """
    if patient_info is None:
        patient_info = {}
    
    pulse_flag = vitals['pulse'] < 60 or vitals['pulse'] > 100
    systolic_flag = vitals['systolicBP'] < 90 or vitals['systolicBP'] > 160
    diastolic_flag = vitals['diastolicBP'] < 60 or vitals['diastolicBP'] > 100
    any_flag = pulse_flag or systolic_flag or diastolic_flag
    
    try:
        data = supabase.table('vitals').insert({
            'pulse': vitals['pulse'],
            'systolic_bp': vitals['systolicBP'],
            'diastolic_bp': vitals['diastolicBP'],
            'pulse_flag': pulse_flag,
            'systolic_flag': systolic_flag,
            'diastolic_flag': diastolic_flag,
            'any_flag': any_flag,
            'patient_info': patient_info
        }).execute()
        
        return {
            'flags': {
                'pulse_flag': pulse_flag,
                'systolic_flag': systolic_flag,
                'diastolic_flag': diastolic_flag,
                'any_flag': any_flag
            },
            'record_id': data.data[0]['id'],
            'timestamp': data.data[0]['created_at'],
            'data': data.data[0]
        }
        
    except Exception as error:
        print(f"Error storing vitals data: {error}")
        return {
            'flags': {
                'pulse_flag': pulse_flag,
                'systolic_flag': systolic_flag,
                'diastolic_flag': diastolic_flag,
                'any_flag': any_flag
            },
            'record_id': None,
            'timestamp': datetime.now().isoformat(),
            'data': None,
            'error': "Failed to store in database"
        }


def get_recent_triage_records(limit_count: int = 10) -> List[Dict]:
    """
    Get recent triage records from Supabase.
    
    Args:
        limit_count (int): Number of records to retrieve (default: 10).
        
    Returns:
        List[Dict]: Array of triage records.
    """
    try:
        data = supabase.table('triage').select('*').order('created_at', desc=True).limit(limit_count).execute()
        return data.data
    except Exception as error:
        print(f"Error fetching triage records: {error}")
        return []


def get_recent_vitals_records(limit_count: int = 10) -> List[Dict]:
    """
    Get recent vital signs records from Supabase.
    
    Args:
        limit_count (int): Number of records to retrieve (default: 10).
        
    Returns:
        List[Dict]: Array of vital signs records.
    """
    try:
        data = supabase.table('vitals').select('*').order('created_at', desc=True).limit(limit_count).execute()
        return data.data
    except Exception as error:
        print(f"Error fetching vitals records: {error}")
        return []
