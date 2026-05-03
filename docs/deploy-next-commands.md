# Next Deployment Commands

Run these after local validation is complete.

## 1. Go to the project root
```powershell
cd C:\Users\Song\.openclaw\workspace\agentic-career-coach
```

## 2. Set the Google Cloud project
```powershell
gcloud config set project YOUR_PROJECT_ID
```

## 3. Enable required services if needed
```powershell
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com firestore.googleapis.com
```

## 4. Deploy with Cloud Build from the project root
```powershell
gcloud builds submit --config mcp-server\cloudbuild.yaml
```

If you changed Dockerfile or runtime config, redeploy with the same command so Cloud Run picks up the new image.

## 5. Validate deployed health endpoint
```powershell
Invoke-RestMethod -Uri https://YOUR_CLOUD_RUN_URL/health
```

## 6. Validate deployed RPC endpoint
```powershell
$body = '{"jsonrpc":"2.0","id":"1","method":"fetch_jobs","params":{"keyword":"software","location":"Richmond","term":"Spring 2026"}}'
Invoke-RestMethod -Uri https://YOUR_CLOUD_RUN_URL/rpc -Method Post -ContentType 'application/json' -Body $body
```

## 7. Optional Firestore-enabled local run
```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:FIRESTORE_COLLECTION="pipeline_entries"
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 8. Vertex AI handoff setup
Use these docs next:
- `docs/vertex-agent-config.md`
- `docs/vertex-demo-prompts.md`
- `docs/demo-script.md`
