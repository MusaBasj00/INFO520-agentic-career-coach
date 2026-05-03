from typing import Any

from pydantic import BaseModel, Field


class McpRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int | None = None
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class McpResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str | int | None = None
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
