# MCP Server

## Local setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /health`
- `GET /`
- `POST /rpc`
- `POST /mcp`
- `GET /sse`
- `POST /sse`
- `POST /sse/rpc`

## Local test

```bash
python test_rpc.py
python test_mcp.py
```

The local tests cover:
1. internship search with `fetch_jobs`
2. pipeline create with `sync_pipeline`
3. pipeline status update
4. single pipeline entry retrieval
5. pipeline list retrieval
6. MCP initialize, tool listing, and MCP tool calls

If `GOOGLE_CLOUD_PROJECT` is not configured, the server automatically uses `app/mock_pipeline.json` as local persistence.
Responses include a clear `message` field and return structured pipeline entries for easier agent summarization.

## Deployment
Use `cloudbuild.yaml` for a quick Cloud Run deployment, or follow `../docs/deployment-guide.md` for the full workflow.

## Vertex MCP note
For Vertex MCP Server connections, try the base URL first. This build now also exposes a more MCP-like SSE endpoint at `/sse` and an MCP RPC endpoint at `/mcp`.
