import json
from pathlib import Path
from typing import Any

from .config import MOCK_PIPELINE_PATH


class MockPipelineStore:
    def __init__(self, path: Path = MOCK_PIPELINE_PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]\n", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, entries: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")

    def create(self, entry: dict[str, Any]) -> dict[str, Any]:
        entries = self._read()
        entries = [item for item in entries if item.get("jobId") != entry.get("jobId")]
        entries.append(entry)
        self._write(entries)
        return entry

    def update(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        entries = self._read()
        updated = None
        for index, item in enumerate(entries):
            if item.get("jobId") == payload.get("jobId"):
                entries[index] = {**item, **payload}
                updated = entries[index]
                break
        if updated is None:
            return None
        self._write(entries)
        return updated

    def get(self, job_id: str) -> dict[str, Any] | None:
        entries = self._read()
        return next((item for item in entries if item.get("jobId") == job_id), None)

    def list(self) -> list[dict[str, Any]]:
        return self._read()
