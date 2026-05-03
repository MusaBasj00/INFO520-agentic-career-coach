# Demo Script

## Goal
Demonstrate supervisor-specialist delegation, MCP tool invocation on Cloud Run, and Firestore-backed persistence in under five minutes.

## Demo Setup
- Open the Agentic Career Coach interface.
- Keep the architecture diagram visible on a separate slide.
- Have Firestore console and Cloud Run endpoint ready.
- Prepare one trace or log view showing tool invocation.

## Scenario 1, Search internships
**User prompt:** Find Spring 2026 software internships in Richmond.

### What to say
- The request first reaches the Supervisor Agent.
- The Supervisor identifies this as an internship search task.
- The Supervisor delegates the task to the Career Specialist Agent.
- The Specialist calls the `fetch_jobs` MCP tool on Cloud Run.
- The system returns matching internships from the mock dataset.

### What to show
- User prompt
- Supervisor to Specialist handoff trace
- Returned internship list

## Scenario 2, Save an internship to the pipeline
**User prompt:** Save the Capital One internship to my pipeline.

### What to say
- The Supervisor identifies this as a pipeline management task.
- The Career Specialist calls `sync_pipeline` with the `create` action.
- The MCP server writes the internship record to Firestore.

### What to show
- Tool invocation details
- New Firestore document in `pipeline_entries`
- Success confirmation to the user

## Scenario 3, Update application status
**User prompt:** Update my Capital One application to interviewing.

### What to say
- The Supervisor again delegates the task.
- The Career Specialist calls `sync_pipeline` with the `update` action.
- Firestore updates the application status and timestamp.

### What to show
- Updated Firestore record
- Final status confirmation in the app

## Scenario 4, View the current pipeline
**User prompt:** Show my internship pipeline.

### What to say
- The Supervisor delegates retrieval to the Career Specialist.
- The Specialist calls `sync_pipeline` with the `list` action.
- The MCP server returns the saved internship pipeline from Firestore.

### What to show
- Tool response
- User-facing pipeline summary

## Closing talking points
- This project uses a supervisor-specialist multi-agent pattern.
- The Specialist accesses backend capabilities through MCP on Cloud Run.
- The system uses JSON-RPC over SSE and persists internship pipeline data in Firestore.
- The design aligns with the architecture diagram and end-to-end flow.
