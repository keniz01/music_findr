from datetime import datetime

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


def register_routes(mcp: FastMCP):
    @mcp.custom_route("/api/healthz", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "MCP Server",
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )
