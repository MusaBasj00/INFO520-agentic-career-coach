import json
from functools import lru_cache
from typing import Any

from .config import JOB_DATA_PATH


class JobDataLoader:
    def __init__(self, data_path=JOB_DATA_PATH):
        self.data_path = data_path

    @lru_cache(maxsize=1)
    def load_jobs(self) -> list[dict[str, Any]]:
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_job_by_id(self, job_id: str) -> dict[str, Any] | None:
        normalized_job_id = str(job_id or "").strip().lower()
        return next(
            (
                job
                for job in self.load_jobs()
                if str(job.get("jobId", "")).strip().lower() == normalized_job_id
            ),
            None,
        )
