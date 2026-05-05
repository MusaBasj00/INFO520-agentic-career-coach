from datetime import datetime, timezone
from typing import Any

try:
    from google.cloud import firestore
except ImportError:  # pragma: no cover
    firestore = None

from .config import FIRESTORE_COLLECTION, GOOGLE_CLOUD_PROJECT
from .data_loader import JobDataLoader
from .mock_store import MockPipelineStore
from .schemas import PipelineActionResponse, PipelineEntry
from .utils import compact_job, success_message


class FirestorePipelineService:
    def __init__(self):
        self.enabled = bool(firestore and GOOGLE_CLOUD_PROJECT)
        self._client = firestore.Client(project=GOOGLE_CLOUD_PROJECT) if self.enabled else None
        self._mock_store = MockPipelineStore()
        self._job_loader = JobDataLoader()

    def _collection(self):
        if not self._client:
            raise RuntimeError("Firestore is not configured")
        return self._client.collection(FIRESTORE_COLLECTION)

    def _hydrate_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        hydrated = dict(payload)
        job_id = hydrated.get("jobId", "")
        matched_job = self._job_loader.get_job_by_id(job_id) if job_id else None
        if matched_job:
            for field, value in compact_job(matched_job).items():
                if field == "keywords":
                    continue
                if not hydrated.get(field):
                    hydrated[field] = value
        return hydrated

    def _normalize_entry(self, payload: dict[str, Any], now: str | None = None) -> dict[str, Any]:
        timestamp = now or datetime.now(timezone.utc).isoformat()
        normalized_payload = self._hydrate_payload(payload)
        return {
            "jobId": normalized_payload.get("jobId", ""),
            "company": normalized_payload.get("company", ""),
            "title": normalized_payload.get("title", ""),
            "location": normalized_payload.get("location", ""),
            "url": normalized_payload.get("url", ""),
            "term": normalized_payload.get("term", ""),
            "status": normalized_payload.get("status", "saved"),
            "deadline": normalized_payload.get("deadline", ""),
            "notes": normalized_payload.get("notes", ""),
            "createdAt": normalized_payload.get("createdAt", timestamp),
            "updatedAt": timestamp,
        }

    def create_entry(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not payload.get("jobId"):
            raise ValueError("jobId is required for create")
        entry = self._normalize_entry(payload)
        if not self.enabled:
            saved = self._mock_store.create(entry)
            response = PipelineActionResponse(
                mode="mock",
                entry=PipelineEntry(**saved),
                message=success_message("create"),
            )
            return response.model_dump()
        doc_ref = self._collection().document(entry["jobId"])
        doc_ref.set(entry)
        response = PipelineActionResponse(
            mode="firestore",
            entry=PipelineEntry(**entry),
            message=success_message("create"),
        )
        return response.model_dump()

    def update_entry(self, payload: dict[str, Any]) -> dict[str, Any]:
        job_id = payload.get("jobId")
        if not job_id:
            raise ValueError("jobId is required for update")
        update_payload = {
            **self._hydrate_payload(payload),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        if not self.enabled:
            updated = self._mock_store.update(update_payload)
            if updated is None:
                raise ValueError(f"No pipeline entry found for jobId '{job_id}'")
            response = PipelineActionResponse(
                mode="mock",
                entry=PipelineEntry(**updated),
                message=success_message("update"),
            )
            return response.model_dump()
        doc_ref = self._collection().document(job_id)
        if not doc_ref.get().exists:
            raise ValueError(f"No pipeline entry found for jobId '{job_id}'")
        doc_ref.set(update_payload, merge=True)
        snapshot = doc_ref.get()
        response = PipelineActionResponse(
            mode="firestore",
            entry=PipelineEntry(**(snapshot.to_dict() or {})),
            message=success_message("update"),
        )
        return response.model_dump()

    def get_entry(self, payload: dict[str, Any]) -> dict[str, Any]:
        job_id = payload.get("jobId")
        if not job_id:
            raise ValueError("jobId is required for get")
        if not self.enabled:
            entry = self._mock_store.get(job_id)
            response = PipelineActionResponse(
                mode="mock",
                entry=PipelineEntry(**entry) if entry else None,
                message=success_message("get"),
            )
            return response.model_dump()
        snapshot = self._collection().document(job_id).get()
        response = PipelineActionResponse(
            mode="firestore",
            entry=PipelineEntry(**snapshot.to_dict()) if snapshot.exists and snapshot.to_dict() else None,
            message=success_message("get"),
        )
        return response.model_dump()

    def list_entries(self) -> dict[str, Any]:
        if not self.enabled:
            entries = [PipelineEntry(**entry) for entry in self._mock_store.list()]
            response = PipelineActionResponse(
                mode="mock",
                entries=entries,
                message=success_message("list", len(entries)),
            )
            return response.model_dump()
        docs = self._collection().stream()
        entries = [PipelineEntry(**doc.to_dict()) for doc in docs if doc.to_dict()]
        response = PipelineActionResponse(
            mode="firestore",
            entries=entries,
            message=success_message("list", len(entries)),
        )
        return response.model_dump()
