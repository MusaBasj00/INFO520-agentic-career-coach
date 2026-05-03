# Reflection Outline

## Paragraph 1, Project objective
Explain that the goal was to design an agentic internship assistant that demonstrates multi-agent orchestration, MCP integration, and cloud persistence on Google Cloud.

## Paragraph 2, Architecture decisions
Describe why the team chose a supervisor-specialist pattern. Emphasize clear separation of responsibilities, easier prompt control, and stronger alignment with the assignment's A2A requirement.

## Paragraph 3, MCP implementation
Explain why the MCP server was deployed on Cloud Run and why JSON-RPC over SSE was used. Mention that `fetch_jobs` and `sync_pipeline` were intentionally scoped to cover the core required use cases without overcomplicating the design.

## Paragraph 4, Data and persistence
Discuss how the internship search uses a stable mock dataset while the pipeline state is persisted in Firestore. Explain that this tradeoff improved reliability for the demo while still proving end-to-end persistence.

## Paragraph 5, Challenges and lessons learned
Mention likely challenges such as transport configuration, tool contract design, and coordinating agent handoff. Reflect on the importance of narrowing scope to deliver a robust system instead of a feature-heavy one.

## Paragraph 6, Future improvements
Mention future upgrades such as real job APIs, stronger authentication with OIDC, richer pipeline analytics, and personalized recommendation features.
