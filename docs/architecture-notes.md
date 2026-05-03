# Architecture Notes

## Components

### Supervisor Agent
- Receives user-facing internship requests.
- Determines whether the task is internship search or pipeline management.
- Delegates execution to the Career Specialist Agent.
- Returns the final response to the user.

### Career Specialist Agent
- Receives delegated work from the Supervisor.
- Chooses `fetch_jobs` for internship search tasks.
- Chooses `sync_pipeline` for save, update, get, and list tasks.
- Returns a concise summary of tool results.

### MCP Server on Cloud Run
- Hosts MCP tools behind a JSON-RPC over SSE interface.
- Serves as the integration layer between agents and data services.

### Mock Job Dataset
- Provides deterministic internship listings for demos and grading.
- Avoids dependency on unstable third-party APIs.

### Cloud Firestore
- Stores internship pipeline entries.
- Persists job status, notes, deadlines, and timestamps.

## Tool Contracts

### `fetch_jobs`
Input fields:
- `keyword`
- `location`
- `term`

### `sync_pipeline`
Input fields:
- `action`
- `payload`

Supported actions:
- `create`
- `update`
- `get`
- `list`

## Firestore Collection
- `pipeline_entries`
