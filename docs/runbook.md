# ACC Runbook

This runbook is the step-by-step execution guide for local validation, Cloud Run deployment, and Vertex AI integration.

## 1. Local setup
Open a terminal in `agentic-career-coach/mcp-server`.

### Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies
```powershell
pip install -r requirements.txt
```

## 2. Start the MCP server locally
```powershell
uvicorn app.main:app --reload
```

Expected local base URL:
- `http://127.0.0.1:8000`

## 3. Verify health endpoint
```powershell
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "acc-mcp-server",
  "transport": "json-rpc and sse"
}
```

## 4. Run the local demo test script
```powershell
python test_rpc.py
```

This validates:
- `fetch_jobs`
- `sync_pipeline(create)`
- `sync_pipeline(update)`
- `sync_pipeline(list)`

## 5. Manual JSON-RPC validation
### Search internships
```powershell
curl -X POST http://127.0.0.1:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"fetch_jobs","params":{"keyword":"software","location":"Richmond","term":"Spring 2026"}}'
```

### Save internship
```powershell
curl -X POST http://127.0.0.1:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"2","method":"sync_pipeline","params":{"action":"create","payload":{"jobId":"job_001","company":"Capital One","title":"Software Engineering Intern","location":"Richmond, VA","term":"Spring 2026","status":"saved","notes":"Need tailored resume"}}}'
```

### Update status
```powershell
curl -X POST http://127.0.0.1:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"3","method":"sync_pipeline","params":{"action":"update","payload":{"jobId":"job_001","status":"interviewing"}}}'
```

### List pipeline
```powershell
curl -X POST http://127.0.0.1:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"4","method":"sync_pipeline","params":{"action":"list","payload":{}}}'
```

## 6. Firestore configuration
If you want real persistence instead of local mock storage:

```powershell
$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
$env:FIRESTORE_COLLECTION="pipeline_entries"
```

Make sure your Google credentials are available locally before starting the server.

## 7. Cloud Run deployment
From `agentic-career-coach` project root:

### Set your project
```powershell
gcloud config set project YOUR_PROJECT_ID
```

### Submit Cloud Build deployment
```powershell
gcloud builds submit --config mcp-server\cloudbuild.yaml
```

## 8. Validate deployed service
After deployment, replace `YOUR_CLOUD_RUN_URL` below.

### Health check
```powershell
curl YOUR_CLOUD_RUN_URL/health
```

### JSON-RPC test
```powershell
curl -X POST YOUR_CLOUD_RUN_URL/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"fetch_jobs","params":{"keyword":"software","location":"Richmond","term":"Spring 2026"}}'
```

## 9. Vertex AI Agent Builder setup
Use `docs/vertex-agent-config.md` and `docs/vertex-demo-prompts.md`.

### Minimum setup
1. Create Supervisor Agent.
2. Create Career Specialist Agent.
3. Register the Cloud Run MCP endpoint with the Specialist.
4. Configure Supervisor delegation to Specialist.
5. Run the four demo prompts.

## 10. Demo capture checklist
- Screenshot of architecture diagram
- Screenshot of Supervisor to Specialist handoff
- Screenshot of MCP tool invocation
- Screenshot of Firestore document
- Final demo recording
