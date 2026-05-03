from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "mock_jobs.json"
FALLBACK_DATA_PATH = BASE_DIR.parent / "data" / "mock_jobs.json"
DEFAULT_MOCK_PIPELINE_PATH = BASE_DIR / "app" / "mock_pipeline.json"

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "pipeline_entries")
_job_data_value = os.getenv("JOB_DATA_PATH")
JOB_DATA_PATH = Path(_job_data_value).resolve() if _job_data_value else DEFAULT_DATA_PATH
if not JOB_DATA_PATH.exists() and FALLBACK_DATA_PATH.exists():
    JOB_DATA_PATH = FALLBACK_DATA_PATH
MOCK_PIPELINE_PATH = Path(os.getenv("MOCK_PIPELINE_PATH", str(DEFAULT_MOCK_PIPELINE_PATH))).resolve()
