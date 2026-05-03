from typing import Any


def compact_job(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "jobId": job.get("jobId", ""),
        "company": job.get("company", ""),
        "title": job.get("title", ""),
        "location": job.get("location", ""),
        "term": job.get("term", ""),
        "url": job.get("url", ""),
        "keywords": job.get("keywords", []),
    }


def success_message(action: str, count: int = 0) -> str:
    messages = {
        "create": "Pipeline entry saved successfully.",
        "update": "Pipeline entry updated successfully.",
        "get": "Pipeline entry retrieved successfully.",
        "list": f"Retrieved {count} pipeline entries.",
        "search": f"Found {count} matching internships.",
    }
    return messages.get(action, "Operation completed successfully.")
