# Deployment Readiness Check

## Verified ready
- Google Cloud SDK is installed.
- Active project is `vocal-catalyst-430900-m9`.
- Active authenticated account is `songzhihaokg@gmail.com`.
- Required services already enabled:
  - `run.googleapis.com`
  - `cloudbuild.googleapis.com`
  - `artifactregistry.googleapis.com`

## Blocker found
- `firestore.googleapis.com` is not enabled yet.

## Next commands
```powershell
gcloud services enable firestore.googleapis.com
gcloud firestore databases create --location=us-central1 --type=firestore-native
```

If the Firestore database already exists after API enablement propagates, skip the create step.

## After Firestore is ready
From `agentic-career-coach` project root:
```powershell
gcloud builds submit --config mcp-server\cloudbuild.yaml
```

## Post-deploy validation
```powershell
Invoke-RestMethod -Uri https://YOUR_CLOUD_RUN_URL/health
```

```powershell
$body = '{"jsonrpc":"2.0","id":"1","method":"fetch_jobs","params":{"keyword":"software","location":"Richmond","term":"Spring 2026"}}'
Invoke-RestMethod -Uri https://YOUR_CLOUD_RUN_URL/rpc -Method Post -ContentType 'application/json' -Body $body
```
