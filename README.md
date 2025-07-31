# T-Flow AI Medical Triage System

A comprehensive AI-powered medical triage system that classifies patient symptoms into urgency levels using Groq's deepseek-r1-distill-llama-70b model with intelligent fallback mechanisms and Firestore integration.

## 🏥 Features

### **AI-Powered Classification**
- **Advanced Medical AI**: Uses Groq's deepseek-r1-distill-llama-70b model
- **Hospital-Grade Prompt**: 10/10 rated medical triage prompt with comprehensive safety protocols
- **Four Triage Levels**: Critical, Urgent, Moderate, Low with specific timeframes
- **Single-Word Output**: Clean API integration with consistent responses

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
- **Firestore Integration**: Automatic storage of all triage records
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
- Node.js (v14 or higher)
- Firebase project with Firestore enabled
- Groq API account and key

### Installation

1. **Clone the repository (dev branch and make PR for changes)**
   ```bash
   git clone https://github.com/T-flow-AI-ATF/ai-integrations.git
   cd ai-integrations
   git checkout dev
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Configure Firebase**
   - Update `firebase.js` with your Firebase configuration
   - Ensure Firestore is enabled in your Firebase project

## 📋 Usage

### Quick Test
```bash
npm test
```

### API Integration

#### Basic Triage Classification
```javascript
const { triagePatient, flagVitals } = require('./triage');

// AI-powered triage with patient info
const result = await triagePatient(
  'Patient experiencing severe chest pain with sweating and nausea',
  { patientId: '12345', age: 45, gender: 'M' },
  true // Use AI
);

console.log(result);
// Output: { triageLevel: 'Critical', recordId: 'abc123', timestamp: Date, data: {...} }
```

#### Vital Signs Analysis
```javascript
// Analyze vital signs
const vitalsResult = await flagVitals(
  { pulse: 110, systolicBP: 180, diastolicBP: 95 },
  { patientId: '12345' }
);

console.log(vitalsResult.flags);
// Output: { pulseFlag: true, systolicFlag: true, diastolicFlag: false, anyFlag: true }
```

#### Retrieve Historical Data
```javascript
const { getRecentTriageRecords, getRecentVitalsRecords } = require('./triage');

// Get last 10 triage records
const recentTriage = await getRecentTriageRecords(10);

// Get last 5 vitals records
const recentVitals = await getRecentVitalsRecords(5);
```

### Advanced Usage

#### Rule-Based Fallback
```javascript
// Force rule-based classification (bypass AI)
const fallbackResult = await triagePatient(
  'Patient has mild headache and feels tired',
  { patientId: '67890' },
  false // Don't use AI
);
```

#### Error Handling
```javascript
try {
  const result = await triagePatient(symptoms, patientInfo);
  if (result.error) {
    console.warn('Database storage failed:', result.error);
    // AI classification still succeeded
    console.log('Triage Level:', result.triageLevel);
  }
} catch (error) {
  console.error('Triage failed:', error);
  // Handle AI and fallback failure
}
```

## 🔧 System Architecture

### Triage Classification Flow
1. **Input Validation**: Symptom text processing
2. **AI Classification**: Groq API call with hospital-grade prompt
3. **Fallback Logic**: Rule-based classification if AI fails
4. **Data Storage**: Firestore record creation
5. **Response Formatting**: Consistent output structure

### Safety Protocols
- **Critical Safety Rules**: Automatic escalation for high-risk symptoms
- **Age-Specific Guidelines**: Pediatric and geriatric modifications
- **Mental Health Screening**: Suicide and violence risk assessment
- **Quality Assurance**: Multiple validation layers

## 🛡️ Security & Compliance

### Data Protection
- Environment variables for sensitive credentials
- Firebase security rules implementation
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

### Triage Records (`triage` collection)
```javascript
{
  symptoms: "Patient symptom description",
  triageLevel: "Critical|Urgent|Moderate|Low",
  patientInfo: { patientId, age, gender, ... },
  timestamp: Firestore.Timestamp,
  useAI: boolean,
  recordId: "document_id"
}
```

### Vitals Records (`vitals` collection)
```javascript
{
  vitals: { pulse, systolicBP, diastolicBP },
  flags: { pulseFlag, systolicFlag, diastolicFlag, anyFlag },
  patientInfo: { patientId, age, gender, ... },
  timestamp: Firestore.Timestamp,
  recordId: "document_id"
}
```

## 🧪 Testing

### Test Coverage
- AI triage classification accuracy
- Rule-based fallback functionality
- Vital signs flagging algorithms
- Database integration
- Error handling scenarios

### Sample Test Cases
```bash
# Run comprehensive test suite
npm test

# Individual component testing
node -e "require('./triage').triagePatient('chest pain').then(console.log)"
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
