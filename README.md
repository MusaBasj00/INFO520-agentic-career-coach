# Agentic Career Coach (ACC)

Agentic Career Coach is a multi-agent internship search assistant built for VCU Business INFO 520. The system follows a supervisor-specialist architecture in Vertex AI Agent Builder, uses an MCP server on Cloud Run with JSON-RPC over SSE, and persists internship pipeline data in Cloud Firestore.

## Target Architecture

- **Supervisor Agent**: receives user requests, identifies intent, delegates work, and returns the final response.
- **Career Specialist Agent**: receives A2A handoff from the supervisor, selects MCP tools, and summarizes results.
- **MCP Server**: hosted on Cloud Run and exposes `fetch_jobs` and `sync_pipeline` through JSON-RPC, MCP-style RPC, and SSE endpoints for Vertex AI Agent Builder integration.
- **Firestore**: stores saved internships, application status, notes, deadlines, and timestamps.
- **Mock Job Dataset**: provides reliable internship listings for demo and evaluation.

## End-to-End Flow

1. User submits an internship-related request to the Supervisor Agent.
2. The Supervisor interprets the request and determines whether delegation is needed.
3. The Supervisor performs an A2A handoff to the Career Specialist Agent.
4. The Career Specialist selects the correct MCP tool.
5. The Specialist invokes the MCP server on Cloud Run using JSON-RPC over SSE.
6. The MCP tool processes the request.
7. The MCP server returns the result to the Career Specialist Agent.
8. The Career Specialist summarizes the result and sends it back to the Supervisor Agent.
9. The Supervisor returns the final combined response to the user.

## Core Demo Scenarios

1. Search internships by keyword, location, and term.
2. Save a selected internship to the pipeline.
3. Update an internship application status.
4. Retrieve the current internship pipeline.

## Agent Definitions

### Supervisor Agent
- Location: `agents/supervisor/prompt.md`
- Role: receives user requests, routes internship search or pipeline-management tasks, and delegates execution to the specialist agent.

### Career Specialist Agent
- Location: `agents/specialist/prompt.md`
- Role: executes MCP tool calls for `fetch_jobs` and `sync_pipeline`, then returns concise task results.

## MCP Server Components

### `fetch_jobs`
- Location: `mcp-server/app/tools.py`
- Purpose: searches the internship dataset by keyword, location, and term.

### `sync_pipeline`
- Location: `mcp-server/app/tools.py`
- Purpose: performs create, update, get, and list operations for internship pipeline entries.

### Supporting services
- `mcp-server/app/firestore_service.py` for Firestore persistence
- `mcp-server/app/mcp_protocol.py` for MCP-compatible tool discovery and invocation
- `mcp-server/app/main.py` for HTTP, RPC, and SSE endpoints

## Run and Deploy

### Local run
From `agentic-career-coach/mcp-server`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Local tests
```powershell
python test_rpc.py
python test_mcp.py
```

### Cloud Run deployment
From `agentic-career-coach` project root:

```powershell
gcloud config set project vocal-catalyst-430900-m9
gcloud builds submit --config mcp-server\cloudbuild.yaml
```

Detailed deployment, validation, and Vertex configuration steps are also documented in:
- `docs/deployment-guide.md`
- `docs/runbook.md`
- `docs/deploy-next-commands.md`
- `docs/vertex-agent-config.md`

## Repository Structure

```text
agentic-career-coach/
├─ README.md
├─ docs/
├─ data/
│  └─ mock_jobs.json
├─ agents/
│  ├─ supervisor/
│  │  └─ prompt.md
│  └─ specialist/
│     └─ prompt.md
└─ mcp-server/
   ├─ app/
   │  ├─ __init__.py
   │  ├─ config.py
   │  ├─ data_loader.py
   │  ├─ firestore_service.py
   │  ├─ main.py
   │  ├─ mcp_models.py
   │  ├─ mcp_protocol.py
   │  ├─ mock_store.py
   │  ├─ models.py
   │  ├─ schemas.py
   │  ├─ tools.py
   │  └─ utils.py
   ├─ Dockerfile
   ├─ cloudbuild.yaml
   ├─ requirements.txt
   ├─ test_mcp.py
   └─ test_rpc.py
```

## Submission Alignment

This repository includes the required multi-agent source code, agent definitions, MCP server implementation, and clear local run / Cloud Run deploy steps requested for the capstone submission.
