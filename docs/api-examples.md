# MCP API Examples

## Health
`GET /health`

## JSON-RPC endpoint
`POST /rpc`

### Example: fetch_jobs
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "fetch_jobs",
  "params": {
    "keyword": "software",
    "location": "Richmond",
    "term": "Spring 2026"
  }
}
```

### Example: sync_pipeline create
```json
{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "sync_pipeline",
  "params": {
    "action": "create",
    "payload": {
      "jobId": "job_001",
      "company": "Capital One",
      "title": "Software Engineering Intern",
      "location": "Richmond, VA",
      "term": "Spring 2026",
      "status": "saved",
      "notes": "Need tailored resume"
    }
  }
}
```

### Example: sync_pipeline update
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "sync_pipeline",
  "params": {
    "action": "update",
    "payload": {
      "jobId": "job_001",
      "status": "interviewing"
    }
  }
}
```

### Example: sync_pipeline get
```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "method": "sync_pipeline",
  "params": {
    "action": "get",
    "payload": {
      "jobId": "job_001"
    }
  }
}
```

### Example: sync_pipeline list
```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "method": "sync_pipeline",
  "params": {
    "action": "list",
    "payload": {}
  }
}
```

## MCP metadata
`GET /`

Example response:
```json
{
  "name": "acc-mcp-server",
  "protocol": "mcp",
  "transports": {
    "sse": "/sse",
    "rpc": "/rpc",
    "mcp": "/mcp"
  }
}
```

## MCP RPC endpoint
`POST /mcp`

### Example: initialize
```json
{
  "jsonrpc": "2.0",
  "id": "init-1",
  "method": "initialize",
  "params": {}
}
```

### Example: tools/list
```json
{
  "jsonrpc": "2.0",
  "id": "tools-1",
  "method": "tools/list",
  "params": {}
}
```

### Example: tools/call
```json
{
  "jsonrpc": "2.0",
  "id": "call-1",
  "method": "tools/call",
  "params": {
    "name": "fetch_jobs",
    "arguments": {
      "keyword": "software",
      "location": "Richmond",
      "term": "Spring 2026"
    }
  }
}
```

## SSE endpoints
- `GET /sse`
- `POST /sse`
- `POST /sse/rpc`

`/sse` is intended for MCP-style SSE discovery and streaming. `/sse/rpc` remains available for the earlier lightweight JSON-RPC-over-SSE path.
