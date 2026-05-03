from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator


class FetchJobsRequest(BaseModel):
    keyword: str = Field(default="")
    location: str = Field(default="")
    term: str = Field(default="")

    @field_validator("keyword", "location", "term", mode="before")
    @classmethod
    def normalize_text(cls, value: Any) -> str:
        return str(value or "").strip()


class SyncPipelineRequest(BaseModel):
    action: Literal["create", "update", "get", "list"]
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("payload", mode="before")
    @classmethod
    def normalize_payload(cls, value: Any) -> dict[str, Any]:
        return value or {}


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
