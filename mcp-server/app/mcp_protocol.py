from typing import Any
import json

from .tools import fetch_jobs, sync_pipeline

TOOL_DEFINITIONS = [
    {
        "name": "fetch_jobs",
        "description": "Fetch internship opportunities by keyword, location, and term.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"},
                "location": {"type": "string"},
                "term": {"type": "string"},
            },
            "required": [],
        },
    },
    {
        "name": "sync_pipeline",
        "description": "Create, update, get, or list internship pipeline entries.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create", "update", "get", "list"],
                },
                "payload": {"type": "object"},
            },
            "required": ["action"],
        },
    },
]

METHODS = {
    "fetch_jobs": fetch_jobs,
    "sync_pipeline": sync_pipeline,
}


def _to_safe_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _compact_for_mcp(tool_name: str, result: dict[str, Any]) -> dict[str, Any]:
    if tool_name == "fetch_jobs":
        items = result.get("results", [])
        return {
            "message": result.get("message", ""),
            "count": result.get("count", len(items)),
            "results": items,
        }

    if tool_name == "sync_pipeline":
        compact: dict[str, Any] = {
            "message": result.get("message", ""),
            "mode": result.get("mode", ""),
        }
        if result.get("entry"):
            entry = result["entry"]
            compact["entry"] = {
                "jobId": entry.get("jobId", ""),
                "company": entry.get("company", ""),
                "title": entry.get("title", ""),
                "status": entry.get("status", ""),
            }
        if result.get("entries"):
            compact["entries"] = [
                {
                    "jobId": item.get("jobId", ""),
                    "company": item.get("company", ""),
                    "title": item.get("title", ""),
                    "status": item.get("status", ""),
                }
                for item in result["entries"]
            ]
        return compact

    return result


def handle_mcp_message(method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = params or {}

    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "acc-mcp-server",
                "version": "0.1.0",
            },
            "capabilities": {
                "tools": {"listChanged": False},
            },
        }

    if method == "notifications/initialized":
        return {}

    if method == "tools/list":
        return {"tools": TOOL_DEFINITIONS}

    if method == "tools/call":
        tool_name = payload.get("name")
        arguments = payload.get("arguments", {})
        if tool_name not in METHODS:
            raise ValueError(f"Unknown tool: {tool_name}")
        raw_result = METHODS[tool_name](arguments)
        compact_result = _compact_for_mcp(tool_name, raw_result)
        return {
            "content": [
                {
                    "type": "text",
                    "text": _to_safe_text(compact_result),
                }
            ],
            "structuredContent": compact_result,
            "isError": False,
        }

    if method in METHODS:
        return METHODS[method](payload)

    raise ValueError(f"Unsupported MCP method: {method}")
