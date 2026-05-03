import json
from typing import Any

from .config import JOB_DATA_PATH


class JobDataLoader:
    def __init__(self, data_path=JOB_DATA_PATH):
        self.data_path = data_path

    def load_jobs(self) -> list[dict[str, Any]]:
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)
