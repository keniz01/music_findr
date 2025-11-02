from data_accessor import IMusicQueryController
from fastmcp import FastMCP
from loguru import logger
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware

from src.boot_strap import setup_container
from src.mcp_tools_factory import register_tools
from src.routes import register_routes


def create_mcp_app() -> FastMCP:
    return FastMCP(
        name="Postgres MCP Server",
        instructions="""
        This server translates natural language queries into SQL queries
        and executes them on a PostgreSQL database.

        Tools:
        - get_table_schema: Analyzes a user query and returns related table schema.
        - execute_sql_statement: Translates and executes SQL for a natural language query.

        Ideal for use in LLM-enabled applications or dashboards querying structured data.
        """,
    )


def add_middlewares(mcp: FastMCP):
    mcp.add_middleware(
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True)
    )
    mcp.add_middleware(TimingMiddleware())
    mcp.add_middleware(LoggingMiddleware())

def create_app(connection_string: str) -> FastMCP:
    try:
        logger.info(f"Initializing application with connection string: {connection_string}")
        container = setup_container(connection_string)
    except Exception as err:
        logger.critical(f"Failed to initialize application: {err}")
        raise

    controller = container.resolve(IMusicQueryController)
    mcp = create_mcp_app()
    add_middlewares(mcp)
    register_tools(mcp, controller)
    register_routes(mcp)
    return mcp.http_app()
