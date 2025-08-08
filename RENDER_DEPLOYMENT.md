# T-Flow Medical Triage API - Render Deployment

## ✅ Your Repository is Ready for Deployment!

### What's Been Set Up:
- ✅ FastAPI backend with proper package structure  
- ✅ Self-contained triage_core module (no import issues)
- ✅ render.yaml configuration file
- ✅ All dependencies properly specified
- ✅ Environment variable handling
- ✅ Production-ready main.py with PORT configuration

## Quick Deploy to Render

### Prerequisites
✅ Your GitHub repository: `emmanuelotoo/ai-integrations`
✅ Supabase database running  
✅ Groq API key

### Step 1: Create Web Service on Render

1. Go to [Render.com](https://render.com) and sign in with GitHub
2. Click **"New"** → **"Web Service"**  
3. Connect your GitHub repository: `emmanuelotoo/ai-integrations`
4. Click **"Connect"** next to your repository

### Step 2: Configure Service Settings

**Basic Settings:**
- **Name:** `tflow-medical-triage` (or your preferred name)
- **Runtime:** `Python 3`
- **Build Command:** `cd backend && pip install -r requirements.txt`
- **Start Command:** `cd backend && python main.py`

**Plan:**
- Select **"Free"** (750 hours/month)

### Step 3: Environment Variables

⚠️ **CRITICAL**: Add these environment variables in Render dashboard:

```
GROQ_API_KEY = your_actual_groq_api_key
SUPABASE_URL = your_actual_supabase_project_url  
SUPABASE_ANON_KEY = your_actual_supabase_anon_key
PYTHON_VERSION = 3.11.0
PORT = 10000
```

**Where to find your keys:**
- **Groq API Key**: [console.groq.com](https://console.groq.com) → API Keys
- **Supabase Keys**: Your Supabase project → Settings → API

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. ⏱️ Wait 5-10 minutes for first deployment  
4. Your API will be live at: `https://your-app-name.onrender.com`

### Step 5: Test Your Deployment

Once deployed, test with:
```bash
# Health check
curl https://your-app-name.onrender.com/api/health

# Test triage
curl -X POST https://your-app-name.onrender.com/api/triage \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "chest pain and difficulty breathing", "use_ai": true}'
```

## API Endpoints Available:

- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/triage` - AI-powered triage assessment  
- `POST /api/vitals` - Vital signs analysis
- `GET /api/stats` - System statistics
- `GET /api/triage/recent` - Recent triage records
- `GET /api/vitals/recent` - Recent vital signs

## Important Notes:

- **First deployment takes longer** (5-10 minutes)
- **Auto-deploys** on every GitHub push to main branch  
- **Free tier sleeps** after 15 minutes of inactivity
- **Wakes up automatically** when receiving requests
- **HTTPS enabled** by default
- **Interactive docs** available at `/docs` endpoint

## Frontend Integration:

Once deployed, integrate with your frontend:

```javascript
const API_BASE = 'https://your-app-name.onrender.com/api';

// Triage request
const triageData = {
  symptoms: "patient symptoms here",
  patient_info: { age: 35 },
  use_ai: true
};

const response = await fetch(`${API_BASE}/triage`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(triageData)
});

const result = await response.json();
console.log('Triage Level:', result.triage_level);
```

## Troubleshooting:

**Build Fails?**
- Check that environment variables are set
- Verify Groq and Supabase keys are valid

**API Returns 500 Errors?**  
- Check Render logs for detailed error messages
- Verify database tables exist in Supabase

**Deployment Takes Too Long?**
- First deployment is slow, subsequent ones are faster
- Check build logs for any issues

Your T-Flow AI Medical Triage System is ready for production! 🚀
