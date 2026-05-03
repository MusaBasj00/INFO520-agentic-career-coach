import json
from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parent))
from app.main import app  # noqa: E402

client = TestClient(app)


def post_rpc(method: str, params: dict):
    payload = {
        "jsonrpc": "2.0",
        "id": method,
        "method": method,
        "params": params,
    }
    response = client.post("/rpc", json=payload)
    return response.status_code, response.json()


if __name__ == "__main__":
    scenarios = [
        ("fetch_jobs", {"keyword": "software", "location": "Richmond", "term": "Spring 2026"}),
        ("sync_pipeline", {
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
        }),
        ("sync_pipeline", {"action": "update", "payload": {"jobId": "job_001", "status": "interviewing"}}),
        ("sync_pipeline", {"action": "get", "payload": {"jobId": "job_001"}}),
        ("sync_pipeline", {"action": "list", "payload": {}}),
    ]

    failures = []
    for method, params in scenarios:
        status, body = post_rpc(method, params)
        print(f"\\n{method} -> HTTP {status}")
        print(json.dumps(body, indent=2))
        if status >= 400:
            failures.append((method, body))

    if failures:
        print("\\nValidation failed for:")
        for method, body in failures:
            print(f"- {method}: {body}")
        raise SystemExit(1)

    print("\\nAll local RPC scenarios passed.")
