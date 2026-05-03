from typing import Any

from .data_loader import JobDataLoader
from .firestore_service import FirestorePipelineService
from .models import FetchJobsRequest, SyncPipelineRequest
from .schemas import FetchJobsResponse
from .utils import compact_job, success_message

job_loader = JobDataLoader()
pipeline_service = FirestorePipelineService()


def fetch_jobs(params: dict[str, Any]) -> dict[str, Any]:
    request = FetchJobsRequest(**params)
    jobs = job_loader.load_jobs()

    def matches(job: dict[str, Any]) -> bool:
        keyword = request.keyword.lower()
        location = request.location.lower()
        term = request.term.lower()
        haystack = " ".join([
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            " ".join(job.get("keywords", [])),
            job.get("term", ""),
        ]).lower()
        return (
            (not keyword or keyword in haystack)
            and (not location or location in job.get("location", "").lower())
            and (not term or term == job.get("term", "").lower())
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
