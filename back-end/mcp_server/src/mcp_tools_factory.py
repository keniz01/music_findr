from typing import Any, Dict, List
from data_accessor import IMusicQueryController
from fastmcp import FastMCP
from fastmcp.tools import Tool


def register_tools(mcp: FastMCP, controller: IMusicQueryController):
    @mcp.tool()
    async def get_table_schema(query_embeddings: List[float]) -> Dict[str, Any]:
        """Get database table schema based on embeddings vector"""
        return await controller.get_table_schema(query_embeddings)

    @mcp.tool()
    async def execute_sql_statement(sql: str) -> list:
        """Execute SQL query directly"""
        return await controller.execute_sql_statement(sql)
