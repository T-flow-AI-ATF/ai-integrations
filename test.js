require('dotenv').config();
const { triagePatient, flagVitals, getRecentTriageRecords, getRecentVitalsRecords } = require('./triage');

(async () => {
  console.log('=== Testing AI Medical Triage System with Firestore Integration ===\n');

  // Test the AI triage with Firestore storage
  try {
    console.log('1. Testing AI Triage with Firestore storage...');
    const aiTriage = await triagePatient('Patient is having a seizure and vomiting', { patientId: 'P001', name: 'John Doe' }, true);
    console.log('AI Triage Level:', aiTriage.triageLevel);
    console.log('Record ID:', aiTriage.recordId);
    console.log('Timestamp:', aiTriage.timestamp);
    console.log('---');
  } catch (err) {
    console.error('AI Triage Error:', err);
  }

  // Test the rule-based triage with Firestore storage
  try {
    console.log('2. Testing Rule-based Triage with Firestore storage...');
    const ruleTriage = await triagePatient('Patient is having a headache and tiredness', { patientId: 'P002', name: 'Jane Smith' }, false);
    console.log('Rule-based Triage Level:', ruleTriage.triageLevel);
    console.log('Record ID:', ruleTriage.recordId);
    console.log('Timestamp:', ruleTriage.timestamp);
    console.log('---');
  } catch (err) {
    console.error('Rule-based Triage Error:', err);
  }

  // Test the vitals flagging with Firestore storage
  try {
    console.log('3. Testing Vital Signs Flagging with Firestore storage...');
    const vitalsResult = await flagVitals(
      { pulse: 55, systolicBP: 120, diastolicBP: 80 }, 
      { patientId: 'P003', name: 'Bob Johnson' }
    );
    console.log('Vitals Flags:', vitalsResult.flags);
    console.log('Record ID:', vitalsResult.recordId);
    console.log('Timestamp:', vitalsResult.timestamp);
    console.log('---');
  } catch (err) {
    console.error('Vitals Flagging Error:', err);
  }

  // Test retrieving recent records
  try {
    console.log('4. Testing Recent Records Retrieval...');
    const recentTriage = await getRecentTriageRecords(5);
    console.log('Recent Triage Records:', recentTriage.length);
    
    const recentVitals = await getRecentVitalsRecords(5);
    console.log('Recent Vitals Records:', recentVitals.length);
    console.log('---');
  } catch (err) {
    console.error('Records Retrieval Error:', err);
  }

  console.log('=== Test Complete ===');
})(); 