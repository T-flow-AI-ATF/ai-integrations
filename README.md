# T-Flow AI Medical Triage System

A comprehensive AI-powered medical triage system that classifies patient symptoms into urgency levels using Groq's **llama-3.3-70b-versatile** model with intelligent fallback mechanisms and Supabase integration.

**Language:** Python 3.8+

## 🏥 Features

### **AI-Powered Classification**

- **Advanced Medical AI**: Uses Groq's **llama-3.3-70b-versatile** model (latest version)
- **Hospital-Grade Prompt**: 10/10 rated medical triage prompt with comprehensive safety protocols
- **Four Triage Levels**: Critical, Urgent, Moderate, Low with specific timeframes
- **Clean Responses**: Direct single-word classifications without reasoning artifacts

### **Comprehensive Medical Coverage**

- **Pediatric Guidelines**: Age-specific criteria for patients under 18
- **Geriatric Considerations**: Specialized protocols for patients over 65
- **Mental Health Integration**: Suicide risk assessment and crisis protocols
- **Contextual Analysis**: Pain location, duration, and associated symptoms

### **Safety & Reliability**

- **Rule-Based Fallback**: Ensures system reliability when AI is unavailable
- **Critical Safety Rules**: Mandatory escalation for high-risk symptoms
- **Quality Assurance**: Clinical pattern recognition and edge case handling
- **Bias Prevention**: Cultural sensitivity and demographic neutrality

### **Data Management**

- **Supabase Integration**: Automatic storage of all triage records
- **PostgreSQL Database**: Robust relational database with JSONB support
- **Vital Signs Monitoring**: Automated flagging of abnormal vital signs
- **Historical Records**: Query recent triage and vitals data
- **Error Handling**: Graceful degradation with comprehensive error management

### **Professional Standards**

- **Medical Liability Protection**: Clear AI limitations and disclaimers
- **Ethical Guidelines**: Patient safety prioritization and professional boundaries
- **Emergency Medicine Alignment**: Follows standard hospital triage protocols
- **Cultural Sensitivity**: Multi-cultural symptom presentation awareness

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- Supabase project with database enabled
- Groq API account and key

### Installation

1. **Clone the repository (dev branch and make PR for changes)**
   ```bash
   git clone https://github.com/T-flow-AI-ATF/ai-integrations.git
   cd ai-integrations
   git checkout dev
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your credentials:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   ```

4. **Configure Supabase**
   - Create a new project at [supabase.com](https://supabase.com)
   - Run the SQL commands from `supabase_setup.sql` in the SQL Editor
   - Copy your project URL and anon key to `.env`

## 📋 Usage

### Quick Test
```bash
python test.py
```

### API Integration

#### Basic Triage Classification
```python
import asyncio
from triage import triage_patient, flag_vitals

async def example():
    # AI-powered triage with patient info
    result = await triage_patient(
        'Patient experiencing severe chest pain with sweating and nausea',
        {'patient_id': '12345', 'age': 45, 'gender': 'M'},
        True  # Use AI
    )
    
    print(result)
    # Output: {'triage_level': 'Critical', 'record_id': 'uuid', 'timestamp': '2025-08-02T...', 'data': {...}}

asyncio.run(example())
```

#### Vital Signs Analysis
```python
# Analyze vital signs
vitals_result = await flag_vitals(
    {'pulse': 110, 'systolicBP': 180, 'diastolicBP': 95},
    {'patient_id': '12345'}
)

print(vitals_result['flags'])
# Output: {'pulse_flag': True, 'systolic_flag': True, 'diastolic_flag': False, 'any_flag': True}
```

#### Retrieve Historical Data
```python
from triage import get_recent_triage_records, get_recent_vitals_records

# Get last 10 triage records
recent_triage = get_recent_triage_records(10)

# Get last 5 vitals records
recent_vitals = get_recent_vitals_records(5)
```

### Advanced Usage

#### Rule-Based Fallback
```python
# Force rule-based classification (bypass AI)
fallback_result = await triage_patient(
    'Patient has mild headache and feels tired',
    {'patient_id': '67890'},
    False  # Don't use AI
)
```

#### Error Handling
```python
try:
    result = await triage_patient(symptoms, patient_info)
    if 'error' in result:
        print(f"Database storage failed: {result['error']}")
        # AI classification still succeeded
        print(f"Triage Level: {result['triage_level']}")
except Exception as error:
    print(f"Triage failed: {error}")
    # Handle AI and fallback failure
```

## 🔧 System Architecture

### Triage Classification Flow

1. **Input Validation**: Symptom text processing
2. **AI Classification**: Groq API call with llama-3.3-70b-versatile model
3. **Fallback Logic**: Rule-based classification if AI fails
4. **Data Storage**: Supabase PostgreSQL record creation
5. **Response Formatting**: Consistent output structure

### Safety Protocols

- **Critical Safety Rules**: Automatic escalation for high-risk symptoms
- **Age-Specific Guidelines**: Pediatric and geriatric modifications
- **Mental Health Screening**: Suicide and violence risk assessment
- **Quality Assurance**: Multiple validation layers

## 🛡️ Security & Compliance

### Data Protection

- Environment variables for sensitive credentials
- Supabase Row Level Security (RLS) implementation
- Patient data anonymization support
- HIPAA-conscious design patterns

### API Security

- Rate limiting considerations
- Input sanitization
- Error message sanitization
- Audit trail maintenance

### Best Practices

- Never commit `.env` files
- Rotate API keys regularly
- Monitor usage and costs
- Implement proper logging

## 📊 Database Schema

### Triage Records (`triage` table)

```sql
CREATE TABLE triage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symptoms TEXT NOT NULL,
    triage_level VARCHAR(20) CHECK (triage_level IN ('Critical', 'Urgent', 'Moderate', 'Low')),
    patient_info JSONB,
    use_ai BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Vitals Records (`vitals` table)

```sql
CREATE TABLE vitals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vitals JSONB NOT NULL,
    flags JSONB NOT NULL,
    patient_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🧪 Testing

### Test Coverage

- AI triage classification accuracy with llama-3.3-70b-versatile
- Rule-based fallback functionality
- Vital signs flagging algorithms
- Supabase database integration
- Error handling scenarios

### Sample Test Cases

```bash
# Run comprehensive test suite
python test.py

# Individual component testing
python -c "import asyncio; from triage import triage_patient; asyncio.run(triage_patient('chest pain'))"
```

## 📖 Medical Disclaimer

**IMPORTANT**: This system is designed as a medical triage **assistant tool** and:

- ❌ Does NOT provide medical diagnosis
- ❌ Does NOT give treatment recommendations  
- ❌ Does NOT replace professional medical judgment
- ❌ Is NOT a substitute for healthcare providers
- ✅ Should be used alongside qualified medical professionals
- ✅ Prioritizes patient safety through conservative classification
- ✅ Requires medical oversight for deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch from `dev`
3. Implement changes with tests
4. Submit pull request to `dev` branch
5. Ensure compliance with healthcare standards

## 🆘 Support

For medical AI implementation questions or technical support:

- Create GitHub issues for bugs
- Contact T-Flow AI team for deployment guidance
- Review medical validation requirements for your jurisdiction

---

**Built with ❤️ by T-Flow AI Team**  
*Advancing healthcare through responsible AI innovation*
