require('dotenv').config();
const { triagePatient, flagVitals, getRecentTriageRecords, getRecentVitalsRecords } = require('./triage');

/**
 * Example usage of the AI Medical Triage System with Firestore integration
 */
async function runExample() {
  console.log('🚑 AI Medical Triage System - Firestore Integration Example\n');

  // Example 1: Complete patient triage workflow
  console.log('📋 Example 1: Complete Patient Triage Workflow');
  console.log('==============================================');
  
  const patientInfo = {
    patientId: 'P12345',
    name: 'Alice Johnson',
    age: 45,
    gender: 'Female',
    contact: '+1-555-0123'
  };

  const symptoms = 'Patient experiencing severe chest pain radiating to left arm, shortness of breath, and sweating';

  try {
    // Perform AI triage
    const triageResult = await triagePatient(symptoms, patientInfo, true);
    
    console.log(`Patient: ${patientInfo.name} (ID: ${patientInfo.patientId})`);
    console.log(`Symptoms: ${symptoms}`);
    console.log(`Triage Level: ${triageResult.triageLevel}`);
    console.log(`Record ID: ${triageResult.recordId}`);
    console.log(`Timestamp: ${triageResult.timestamp}`);
    console.log('');

    // Check vitals if triage level is high
    if (triageResult.triageLevel === 'Critical' || triageResult.triageLevel === 'Urgent') {
      console.log('⚠️  High priority case - checking vital signs...');
      
      const vitals = {
        pulse: 110,
        systolicBP: 180,
        diastolicBP: 95
      };

      const vitalsResult = await flagVitals(vitals, patientInfo);
      
      console.log(`Vital Signs:`);
      console.log(`  Pulse: ${vitals.pulse} bpm ${vitalsResult.flags.pulseFlag ? '⚠️' : '✅'}`);
      console.log(`  Blood Pressure: ${vitals.systolicBP}/${vitals.diastolicBP} mmHg ${vitalsResult.flags.systolicFlag || vitalsResult.flags.diastolicFlag ? '⚠️' : '✅'}`);
      console.log(`  Overall Status: ${vitalsResult.flags.anyFlag ? 'ABNORMAL ⚠️' : 'Normal ✅'}`);
      console.log(`  Vitals Record ID: ${vitalsResult.recordId}`);
      console.log('');
    }
  } catch (error) {
    console.error('Error in triage workflow:', error);
  }

  // Example 2: Batch processing multiple patients
  console.log('👥 Example 2: Batch Processing Multiple Patients');
  console.log('==============================================');
  
  const patients = [
    {
      info: { patientId: 'P001', name: 'Bob Smith', age: 32 },
      symptoms: 'Mild headache and fatigue'
    },
    {
      info: { patientId: 'P002', name: 'Carol Davis', age: 28 },
      symptoms: 'Vomiting and blurred vision'
    },
    {
      info: { patientId: 'P003', name: 'David Wilson', age: 55 },
      symptoms: 'Loss of consciousness and seizure'
    }
  ];

  for (const patient of patients) {
    try {
      const result = await triagePatient(patient.symptoms, patient.info, true);
      console.log(`${patient.info.name}: ${result.triageLevel} (${result.recordId})`);
    } catch (error) {
      console.error(`Error processing ${patient.info.name}:`, error.message);
    }
  }
  console.log('');

  // Example 3: Retrieve and analyze recent records
  console.log('📊 Example 3: Recent Records Analysis');
  console.log('====================================');
  
  try {
    const recentTriage = await getRecentTriageRecords(10);
    const recentVitals = await getRecentVitalsRecords(10);

    console.log(`Recent Triage Records: ${recentTriage.length}`);
    console.log(`Recent Vitals Records: ${recentVitals.length}`);

    // Analyze triage distribution
    const triageDistribution = recentTriage.reduce((acc, record) => {
      acc[record.triageLevel] = (acc[record.triageLevel] || 0) + 1;
      return acc;
    }, {});

    console.log('\nTriage Level Distribution:');
    Object.entries(triageDistribution).forEach(([level, count]) => {
      console.log(`  ${level}: ${count} patients`);
    });

    // Check for abnormal vitals
    const abnormalVitals = recentVitals.filter(record => record.flags.anyFlag);
    console.log(`\nPatients with Abnormal Vitals: ${abnormalVitals.length}`);

  } catch (error) {
    console.error('Error retrieving records:', error);
  }

  console.log('\n✅ Example complete!');
}

// Run the example
runExample().catch(console.error); 