-- Supabase Database Setup for T-Flow AI Medical Triage System
-- Run these commands in the Supabase SQL Editor

-- Create triage table
CREATE TABLE IF NOT EXISTS triage (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  symptoms TEXT NOT NULL,
  triage_level TEXT NOT NULL CHECK (triage_level IN ('Critical', 'Urgent', 'Moderate', 'Low')),
  patient_info JSONB DEFAULT '{}',
  use_ai BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create vitals table
CREATE TABLE IF NOT EXISTS vitals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  pulse INTEGER,
  systolic_bp INTEGER,
  diastolic_bp INTEGER,
  pulse_flag BOOLEAN DEFAULT false,
  systolic_flag BOOLEAN DEFAULT false,
  diastolic_flag BOOLEAN DEFAULT false,
  any_flag BOOLEAN DEFAULT false,
  patient_info JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_triage_created_at ON triage(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_triage_level ON triage(triage_level);
CREATE INDEX IF NOT EXISTS idx_vitals_created_at ON vitals(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_vitals_any_flag ON vitals(any_flag) WHERE any_flag = true;

-- Add updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_triage_updated_at 
    BEFORE UPDATE ON triage 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vitals_updated_at 
    BEFORE UPDATE ON vitals 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE triage ENABLE ROW LEVEL SECURITY;
ALTER TABLE vitals ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for your security requirements)
CREATE POLICY "Enable all operations for authenticated users" ON triage
    FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');

CREATE POLICY "Enable all operations for authenticated users" ON vitals
    FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');

-- Add comments for documentation
COMMENT ON TABLE triage IS 'Medical triage records with AI and rule-based classifications';
COMMENT ON TABLE vitals IS 'Patient vital signs with automated flagging for abnormal values';

COMMENT ON COLUMN triage.symptoms IS 'Free-text description of patient symptoms';
COMMENT ON COLUMN triage.triage_level IS 'AI or rule-based classification: Critical, Urgent, Moderate, Low';
COMMENT ON COLUMN triage.patient_info IS 'JSON object containing patient metadata (age, gender, etc.)';
COMMENT ON COLUMN triage.use_ai IS 'Whether AI was used for classification (true) or rule-based fallback (false)';

COMMENT ON COLUMN vitals.pulse IS 'Pulse rate in beats per minute (bpm)';
COMMENT ON COLUMN vitals.systolic_bp IS 'Systolic blood pressure in mmHg';
COMMENT ON COLUMN vitals.diastolic_bp IS 'Diastolic blood pressure in mmHg';
COMMENT ON COLUMN vitals.any_flag IS 'True if any vital sign is flagged as abnormal';
