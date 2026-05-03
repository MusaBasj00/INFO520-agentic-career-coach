from typing import Literal

from pydantic import BaseModel, Field


class PipelineEntry(BaseModel):
    jobId: str
    company: str = ""
    title: str = ""
    location: str = ""
    url: str = ""
    term: str = ""
    status: str = "saved"
    deadline: str = ""
    notes: str = ""
    createdAt: str | None = None
    updatedAt: str | None = None


class FetchJobsResponse(BaseModel):
    results: list[dict]
    count: int


class PipelineActionResponse(BaseModel):
    mode: Literal["mock", "firestore"]
    entry: PipelineEntry | None = None
    entries: list[PipelineEntry] = Field(default_factory=list)
    message: str = ""
