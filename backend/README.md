# FastAPI Backend Configuration

## Environment Variables
Copy the .env file from the parent directory or ensure these variables are set:

```bash
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
python run_server.py
```

Or directly with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /api/health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Triage Endpoints
- `POST /api/triage` - AI-powered symptom triage
- `GET /api/triage/recent?limit=10` - Get recent triage records

### Vitals Endpoints
- `POST /api/vitals` - Vital signs analysis
- `GET /api/vitals/recent?limit=10` - Get recent vitals records

### Analytics
- `GET /api/stats` - System usage statistics

## API Usage Examples

### Triage Request
```bash
curl -X POST "http://localhost:8000/api/triage" \
     -H "Content-Type: application/json" \
     -d '{
       "symptoms": "Patient has severe chest pain and difficulty breathing",
       "patient_info": {"age": 45, "gender": "M"},
       "use_ai": true
     }'
```

### Vitals Request
```bash
curl -X POST "http://localhost:8000/api/vitals" \
     -H "Content-Type: application/json" \
     -d '{
       "pulse": 120,
       "systolicBP": 180,
       "diastolicBP": 95,
       "patient_info": {"age": 60}
     }'
```

## Testing

Run the test suite:
```bash
python -m pytest test_api.py -v
```

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000 (Next.js development)
- http://localhost:3001 (Alternative port)
- https://your-frontend-domain.com (Production - update as needed)

Update the `allow_origins` list in `main.py` for your specific frontend domains.

## Deployment

The backend can be deployed to any Python hosting service:

### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

### Render
1. Create new Web Service
2. Connect GitHub repository
3. Set build/start commands:
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && python main.py`

### Docker (Optional)
A Dockerfile can be added if containerization is needed.

## Monitoring

- Health check endpoint: `/api/health`
- Usage statistics: `/api/stats`
- FastAPI automatic logging enabled
- All endpoints include error handling and validation

## Security Features

- Input validation with Pydantic models
- PII detection in symptom descriptions
- Rate limiting ready (can be added with middleware)
- CORS protection
- Error message sanitization
