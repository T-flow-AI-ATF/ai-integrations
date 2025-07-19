# AI Medical Triage System

An AI-powered medical triage system that classifies patient symptoms into urgency levels using Groq's deepseek-r1-distill-llama-70b model with rule-based fallback.

## Features

- **AI-Powered Triage**: Uses Groq AI for intelligent symptom classification
- **Rule-Based Fallback**: Ensures system reliability when AI is unavailable
- **Vital Signs Analysis**: Flags abnormal vital signs
- **Four Triage Levels**: Critical, Urgent, Moderate, Low

## Setup

1. Clone the repository( dev branch and make pr for changes)
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy `.env.example` to `.env` and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and replace `your_groq_api_key_here` with your actual Groq API key

## Usage

### Run Tests
```bash
npm test
```

### Start Application
```bash
npm start
```

### API Usage
```javascript
const { triagePatient, flagVitals } = require('./triage');

// AI-powered triage
const aiResult = await triagePatient('Patient having chest pain', true);

// Rule-based triage
const ruleResult = await triagePatient('Patient has headache', false);

// Vital signs analysis
const vitalsResult = flagVitals({ pulse: 55, systolicBP: 120, diastolicBP: 80 });
```

## Security

- Never commit your `.env` file
- Regenerate API keys if accidentally exposed
- Use `.env.example` as a template for other developers

## License

MIT
