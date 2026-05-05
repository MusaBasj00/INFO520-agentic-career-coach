from typing import Any

from .data_loader import JobDataLoader
from .firestore_service import FirestorePipelineService
from .models import FetchJobsRequest, SyncPipelineRequest
from .schemas import FetchJobsResponse
from .utils import compact_job, success_message

job_loader = JobDataLoader()
pipeline_service = FirestorePipelineService()


def _normalize(value: str) -> str:
    return " ".join(str(value or "").lower().replace(",", " ").split())


def _location_matches(requested_location: str, job_location: str) -> bool:
    requested = _normalize(requested_location)
    actual = _normalize(job_location)
    if not requested:
        return True
    if requested in actual:
        return True
    requested_tokens = set(requested.split())
    actual_tokens = set(actual.split())
    return requested_tokens.issubset(actual_tokens)


def _term_matches(requested_term: str, job_term: str) -> bool:
    requested = _normalize(requested_term)
    actual = _normalize(job_term)
    if not requested:
        return True
    return requested == actual or requested in actual or actual in requested


def fetch_jobs(params: dict[str, Any]) -> dict[str, Any]:
    request = FetchJobsRequest(**params)
    jobs = job_loader.load_jobs()

    def matches(job: dict[str, Any]) -> bool:
        keyword = _normalize(request.keyword)
        haystack = _normalize(" ".join([
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            " ".join(job.get("keywords", [])),
            job.get("term", ""),
        ]))
        return (
            (not keyword or keyword in haystack)
            and _location_matches(request.location, job.get("location", ""))
            and _term_matches(request.term, job.get("term", ""))
        )

    results = [compact_job(job) for job in jobs if matches(job)]
    response = FetchJobsResponse(results=results, count=len(results))
    return {
        **response.model_dump(),
        "message": success_message("search", len(results)),
    }


def sync_pipeline(params: dict[str, Any]) -> dict[str, Any]:
    request = SyncPipelineRequest(**params)
    if request.action == "create":
        return pipeline_service.create_entry(request.payload)
    if request.action == "update":
        return pipeline_service.update_entry(request.payload)
    if request.action == "get":
        return pipeline_service.get_entry(request.payload)
    if request.action == "list":
        return pipeline_service.list_entries()
    raise ValueError(f"Unsupported action: {request.action}")
