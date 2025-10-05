from datetime import datetime
from punq import Container
from fastmcp import FastMCP
from fastmcp.tools import Tool
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.rate_limiting import (
    RateLimitingMiddleware,
    SlidingWindowRateLimitingMiddleware
)

from src.interfaces.postgres_server import IPostgresServer
from data_accessor.src.domain.interfaces.music_query_service import IMusicQueryService
from data_accessor.src.domain.interfaces.music_query_repository import IMusicQueryRepository
from data_accessor.src.domain.services.music_query_service import MusicQueryService
from data_accessor.src.application.interfaces.music_query_controller import IMusicQueryController
from data_accessor.src.application.controllers.music_query_controller import MusicQueryController
from data_accessor.src.infrastructure.repositories.music_query_repository import MusicQueryRepository

# Set up the dependency injection container
container = Container()

# Configure database
connection_string = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
engine = create_async_engine(connection_string)

# Create and register repository
repo = MusicQueryRepository(engine=engine, default_schema="analysis")
container.register(IMusicQueryRepository, instance=repo)

# Create and register service
service = MusicQueryService(repository=repo)
container.register(IMusicQueryService, instance=service)

# Create and register controller
controller = MusicQueryController(music_query_service=service)
container.register(IMusicQueryController, instance=controller)

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

class PostgresServer(IPostgresServer):

    def __init__(self):
        self.controller = container.resolve(IMusicQueryController)

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
