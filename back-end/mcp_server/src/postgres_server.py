from datetime import datetime
from punq import Container
from fastmcp import FastMCP
from fastmcp.tools import Tool
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.rate_limiting import (
    RateLimitingMiddleware,
    SlidingWindowRateLimitingMiddleware
)

from .abstract_postgres_server import AbstractPostgresServer
from data_accessor.src.domain.interfaces.abstract_music_query_service import AbstractMusicQueryService
from data_accessor.src.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.src.domain.services.music_query_service import MusicQueryService
from data_accessor.src.application.music_query_controller import MusicQueryController, AbstractMusicQueryController
from data_accessor.src.infrastructure.repositories.music_query_repository import MusicQueryRepository

# Set up the dependency injection container
container = Container()
container.register(MusicQueryRepository, instance=MusicQueryRepository(
    "analysis", "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
))
container.register(AbstractMusicQueryRepository, MusicQueryRepository)
container.register(AbstractMusicQueryService, MusicQueryService)
container.register(AbstractMusicQueryController, MusicQueryController)

# Resolve the controller via the container
controller = container.resolve(AbstractMusicQueryController)

mcp = FastMCP(
    name="Postgres MCP Server",
    instructions="""
        This server provides tools to translate natural language query to SQL queries.
        It queries the postgres server using SQL queries to fetch data.
        Call get_table_schema() to fetch the table schema related to the natural language query.
    """
)

# Add middleware in logical order
mcp.add_middleware(ErrorHandlingMiddleware(
    include_traceback=True,
    transform_errors=True
))
mcp.add_middleware(RateLimitingMiddleware(max_requests_per_second=50))
mcp.add_middleware(TimingMiddleware())
mcp.add_middleware(LoggingMiddleware())
mcp.add_middleware(SlidingWindowRateLimitingMiddleware(
    max_requests=5,
    window_minutes=1
))

class PostgresServer(AbstractPostgresServer):

    def __init__(self):
        # Inject controller into the server instance
        self.controller = controller

    @mcp.tool()
    async def get_table_schema(self, user_query: str) -> list:
        # Implementation placeholder
        return await self.controller.get_table_schema(user_query)

    @mcp.tool()
    async def execute_sql_statement(self, user_query: str) -> list:
        # Implementation placeholder
        return await self.controller.execute_sql(user_query)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy",
        "service": "mcp-server",
        "date/time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

app = mcp.http_app()
