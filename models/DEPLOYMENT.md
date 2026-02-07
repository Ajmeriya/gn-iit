# Model Service Deployment Guide

Complete guide for deploying the AI Model Service to Render.

## Prerequisites

- Render account (https://render.com)
- Google Gemini API key (https://makersuite.google.com/app/apikey)
- Git repository access

## Quick Deployment

1. **Connect Repository**
   - Go to Render Dashboard → New Web Service
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `ai-model-service`
   - **Root Directory**: `models`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `bash start.sh`
   - **Plan**: Free (for testing) or Starter ($7/month)

3. **Environment Variables**
   - `GEMINI_API_KEY`: Your API key (mark as Secret)
   - `GEMINI_API_KEY_2`: Optional secondary key

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build

## Service URL

After deployment, you'll get a URL like:
```
https://ai-model-service.onrender.com
```

## Update Backend

In `backend/src/main/resources/application.properties`:
```properties
ai.service.url=https://ai-model-service.onrender.com
```

## Testing

```bash
# Health check
curl https://ai-model-service.onrender.com/health

# Expected response
{"status":"healthy","services":{...}}
```

## Troubleshooting

### Build Fails
- Verify Root Directory is `models`
- Check `requirements.txt` exists
- Review build logs

### Service Crashes
- Check Start Command: `bash start.sh`
- Verify environment variables are set
- Review service logs

### Module Not Found
- Ensure Root Directory is `models`
- Start Command should use `bash start.sh`
- Check that `ai_service.py` exists in models directory

## Files Structure

```
models/
├── ai_service.py          # Main Flask app
├── requirements.txt       # Dependencies
├── Procfile              # Render config
├── render.yaml           # Infrastructure as code
├── start.sh              # Start script
└── ...                   # Other source files
```

## Support

For issues, check:
- Render logs in dashboard
- Service health endpoint
- Environment variables configuration
