# Implementation Blueprint

## Goal
Build a stable, rubric-aligned Agentic Career Coach that demonstrates supervisor-specialist delegation, MCP tool usage over JSON-RPC/SSE, and Firestore persistence.

## Delivery Priorities
1. Working MCP server with two tools.
2. Firestore-backed pipeline persistence.
3. Clear supervisor-specialist handoff.
4. Demo-ready end-to-end flow.
5. Optional OIDC hardening if time remains.

## Build Order

### Phase 1, Data and contracts
- Create `data/mock_jobs.json` with 10 to 20 internship records.
- Lock request and response schemas for `fetch_jobs` and `sync_pipeline`.
- Confirm Firestore collection name: `pipeline_entries`.

### Phase 2, MCP server
- Implement data loader for mock jobs.
- Implement Firestore service methods: create, update, get, list.
- Implement tool functions.
- Expose the tools through the MCP server over SSE.

### Phase 3, Cloud deployment
- Containerize the MCP server.
- Deploy to Cloud Run.
- Configure environment variables for Firestore project and collection.

### Phase 4, Agent layer
- Create Supervisor prompt and routing rules.
- Create Career Specialist prompt and tool selection instructions.
- Connect Agent Builder to the Cloud Run MCP endpoint.

### Phase 5, Evaluation assets
- Capture trace screenshots.
- Add architecture narrative and end-to-end flow to the report.
- Rehearse the four-step demo.

## Demo Stories
1. Search for Spring 2026 software internships in Richmond.
2. Save a selected internship to the pipeline.
3. Update the internship status to interviewing.
4. Show the current internship pipeline.

## Risks and Mitigations
- External job APIs may fail, so use mock data.
- Auth can slow delivery, so defer OIDC until the main flow works.
- Agent orchestration can be brittle, so keep tool contracts simple and explicit.
