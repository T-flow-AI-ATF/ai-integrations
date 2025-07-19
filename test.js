require('dotenv').config();
const { triagePatient, flagVitals } = require('./triage');

(async () => {
  // Test the AI triage (set useAI to true)
  try {
    const aiTriage = await triagePatient('Patient is having a seizure and vomiting', true);
    console.log('AI Triage Level:', aiTriage);
  } catch (err) {
    console.error('AI Triage Error:', err);
  }

  // Test the rule-based triage (set useAI to false)
  const ruleTriage = await triagePatient('Patient is having a headache and tiredness', false);
  console.log('Rule-based Triage Level:', ruleTriage);

  // Test the vitals flagging
  const vitalsResult = flagVitals({ pulse: 55, systolicBP: 120, diastolicBP: 80 });
  console.log('Vitals Flagging:', vitalsResult);
})(); 