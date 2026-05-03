# Validation Checks

## Local checks
- [ ] `pip install -r requirements.txt` completes successfully, including test dependency `httpx`
- [ ] `uvicorn app.main:app --reload` starts without error
- [ ] `/health` returns status ok
- [ ] `python test_rpc.py` completes successfully
- [ ] `python test_mcp.py` completes successfully
- [ ] `mock_pipeline.json` updates after create and update actions

## Cloud Run checks
- [ ] Cloud Build completes successfully
- [ ] Cloud Run URL responds on `/health`
- [ ] `/rpc` returns valid internship search results
- [ ] `/rpc` create action writes a pipeline entry
- [ ] `/rpc` list action returns saved entries

## Firestore checks
- [ ] `pipeline_entries` collection exists
- [ ] create action writes a new document
- [ ] update action changes `status` and `updatedAt`
- [ ] list action returns the saved document

## Vertex AI checks
- [ ] Supervisor delegates search requests to Specialist
- [ ] Supervisor delegates pipeline requests to Specialist
- [ ] Specialist invokes `fetch_jobs`
- [ ] Specialist invokes `sync_pipeline`
- [ ] Trace screenshot clearly shows delegation and tool use

## Final submission checks
- [ ] Demo follows the 4-step script
- [ ] Reflection draft is revised and finalized
- [ ] Architecture diagram includes end-to-end flow
- [ ] GitHub repo is clean and complete
