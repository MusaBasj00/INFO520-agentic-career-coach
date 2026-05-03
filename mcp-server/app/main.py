import json
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from .mcp_models import McpRequest, McpResponse
from .mcp_protocol import handle_mcp_message
from .models import JsonRpcRequest, JsonRpcResponse
from .tools import fetch_jobs, sync_pipeline

app = FastAPI(title="Agentic Career Coach MCP Server")

METHODS = {
    "fetch_jobs": fetch_jobs,
    "sync_pipeline": sync_pipeline,
}


def handle_rpc(request: JsonRpcRequest) -> JsonRpcResponse:
    handler = METHODS.get(request.method)
    if not handler:
        return JsonRpcResponse(
            id=request.id,
            error={"code": -32601, "message": f"Method not found: {request.method}"},
        )

    try:
        result = handler(request.params)
        return JsonRpcResponse(id=request.id, result=result)
    except ValueError as error:
        return JsonRpcResponse(
            id=request.id,
            error={"code": -32602, "message": str(error)},
        )
    except Exception as error:  # pragma: no cover
        return JsonRpcResponse(
            id=request.id,
            error={"code": -32000, "message": f"Internal server error: {error}"},
        )


def handle_mcp_rpc(request: McpRequest) -> McpResponse:
    try:
        result = handle_mcp_message(request.method, request.params)
        return McpResponse(id=request.id, result=result)
    except ValueError as error:
        return McpResponse(
            id=request.id,
            error={"code": -32602, "message": str(error)},
        )
    except Exception as error:  # pragma: no cover
        return McpResponse(
            id=request.id,
            error={"code": -32000, "message": f"Internal server error: {error}"},
        )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "acc-mcp-server",
        "transport": "json-rpc and sse",
    }


@app.get("/")
def root_metadata() -> dict:
    return {
        "name": "acc-mcp-server",
        "protocol": "mcp",
        "transports": {
            "sse": "/sse",
            "rpc": "/rpc",
            "mcp": "/mcp",
        },
    }


@app.post("/rpc")
def rpc(request: JsonRpcRequest):
    response = handle_rpc(request)
    if response.error:
        code = response.error.get("code")
        status_code = 404 if code == -32601 else 400 if code == -32602 else 500
        return JSONResponse(status_code=status_code, content=response.model_dump())
    return response.model_dump()


@app.post("/mcp")
def mcp_rpc(request: McpRequest):
    response = handle_mcp_rpc(request)
    if response.error:
        code = response.error.get("code")
        status_code = 400 if code == -32602 else 500
        return JSONResponse(status_code=status_code, content=response.model_dump())
    return response.model_dump()


@app.api_route("/sse", methods=["GET", "POST"])
async def mcp_sse(request: Request):
    session_id = request.headers.get("x-session-id") or str(uuid4())

    if request.method == "POST":
        body = await request.json()
        response = handle_mcp_rpc(McpRequest(**body))

        async def post_event_generator():
            yield {
                "event": "message",
                "data": json.dumps(response.model_dump()),
            }

        return EventSourceResponse(post_event_generator(), headers={"x-session-id": session_id})

    async def get_event_generator():
        endpoint_url = f"/mcp?session_id={session_id}"
        yield {
            "event": "endpoint",
            "data": endpoint_url,
        }

    return EventSourceResponse(get_event_generator(), headers={"x-session-id": session_id})


@app.post("/sse/rpc")
async def rpc_sse(request: JsonRpcRequest):
    response = handle_rpc(request)

    async def event_generator():
        yield {
            "event": "message",
            "data": json.dumps(response.model_dump()),
        }

    return EventSourceResponse(event_generator())
