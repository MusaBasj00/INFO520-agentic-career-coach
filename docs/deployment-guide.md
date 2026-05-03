# Deployment Guide

## Local development

### 1. Create a virtual environment
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Start the MCP server
```bash
uvicorn app.main:app --reload
```

### 3. Run the local test script
```bash
python test_rpc.py
```

## Firestore setup
1. Create or select a Google Cloud project.
2. Enable Firestore in Native mode.
3. Ensure application default credentials are available locally if you want to test against Firestore.
4. Set environment variables:
```bash
set GOOGLE_CLOUD_PROJECT=your-project-id
set FIRESTORE_COLLECTION=pipeline_entries
```

## Cloud Run deployment

### Option A, deploy with Cloud Build
From `agentic-career-coach` project root:
```bash
gcloud builds submit --config mcp-server/cloudbuild.yaml
```

### Option B, manual deploy
```bash
docker build -f mcp-server/Dockerfile -t gcr.io/YOUR_PROJECT_ID/acc-mcp-server .
docker push gcr.io/YOUR_PROJECT_ID/acc-mcp-server
gcloud run deploy acc-mcp-server \
  --image gcr.io/YOUR_PROJECT_ID/acc-mcp-server \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,FIRESTORE_COLLECTION=pipeline_entries
```

## Post-deploy checks
- Open `/health`
- Send a JSON-RPC request to `/rpc`
- Validate the SSE endpoint at `/sse/rpc`
- Confirm Firestore documents are created in `pipeline_entries`

## Vertex AI integration notes
- Register the Cloud Run MCP endpoint with the Career Specialist agent.
- Keep the Supervisor agent tool-free and delegation-focused.
- Capture screenshots showing the handoff and tool invocation trace.
