# End-to-End Flow

1. The user sends an internship-related request to the Supervisor Agent.
2. The Supervisor Agent interprets the request and identifies the intent.
3. The Supervisor delegates the task to the Career Specialist Agent through A2A handoff.
4. The Career Specialist selects the appropriate MCP tool.
5. The Specialist invokes the MCP server on Cloud Run using JSON-RPC over SSE.
6. The MCP server executes one of the following:
   - `fetch_jobs` reads matching internships from the mock dataset.
   - `sync_pipeline` performs CRUD operations in Cloud Firestore.
7. The MCP server returns the result to the Career Specialist Agent.
8. The Career Specialist summarizes the tool output and sends it back to the Supervisor Agent.
9. The Supervisor Agent returns the final response to the user.

## Example Scenario

**Request:** Find Spring 2026 software internships in Richmond and save one to my pipeline.

1. The Supervisor receives the request and classifies it as an internship search task.
2. The Supervisor hands the task to the Career Specialist.
3. The Specialist calls `fetch_jobs` and receives matching listings.
4. The Supervisor presents the returned options to the user.
5. The user chooses one internship to save.
6. The Supervisor delegates the save request to the Career Specialist.
7. The Specialist calls `sync_pipeline` with the `create` action.
8. Firestore stores the saved internship record with timestamps.
9. The Supervisor confirms that the internship has been saved.
