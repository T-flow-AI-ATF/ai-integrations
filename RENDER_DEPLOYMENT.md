# T-Flow Medical Triage API - Render Deployment

## Quick Deploy to Render

### Prerequisites
✅ GitHub repository: `T-flow-AI-ATF/ai-integrations`
✅ Supabase database running
✅ Groq API key

### Step 1: Connect Repository to Render

1. Go to [Render.com](https://render.com) and sign in with GitHub
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository: `T-flow-AI-ATF/ai-integrations`
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

Add these environment variables in Render dashboard:

```
GROQ_API_KEY = your_groq_api_key
SUPABASE_URL = your_supabase_url  
SUPABASE_ANON_KEY = your_supabase_anon_key
PYTHON_VERSION = 3.11.0
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically deploy your app
3. Wait 5-10 minutes for first deployment
4. Your API will be live at: `https://your-app-name.onrender.com`

### Step 5: Test Deployment

Test your live API:
```bash
curl https://your-app-name.onrender.com/api/health
```

### API Endpoints Available:

- `GET /api/health` - Health check
- `POST /api/triage` - Submit triage assessment  
- `POST /api/vitals` - Submit vital signs
- `GET /api/stats` - Get database statistics
- `GET /api/recent-triage` - Recent triage records
- `GET /api/recent-vitals` - Recent vital signs
- `GET /api/flagged-vitals` - Flagged vital signs
- `GET /api/all-data` - All data (admin)

### Important Notes:

- **First deployment takes longer** (5-10 minutes)
- **Auto-deploys** on every GitHub push to main branch
- **Free tier sleeps** after 15 minutes of inactivity
- **Wakes up automatically** when receiving requests
- **HTTPS enabled** by default

### Next Steps for Frontend:

Once deployed, you can integrate with Next.js:

```javascript
const API_BASE = 'https://your-app-name.onrender.com/api';

// Example API call
const triageResponse = await fetch(`${API_BASE}/triage`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(triageData)
});
```

Your medical triage system is now live! 🚀
