from typing import Any, Dict, List

from fastmcp import Client
from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest
from src.models.llama_model import LlamaModel


class SearchHandler:
    """Handles search operations using the MCP server"""

    def __init__(self, llama_model: LlamaModel, client: Client) -> None:
        self._client = client
        self._llama_model = llama_model

    async def search_by_query(
        self, request: SearchQueryRequest
    ) -> ApiResponse[Any]:
        """Search for music information using natural language query"""
        if not request.query.strip():
            return ApiResponse(success=False, error="Query cannot be empty")

        try:
            schema = await self._get_table_schema(request.query)
            if not schema:
                return ApiResponse(success=False, error="No relevant tables found")

            sql = self._llama_model.generate_sql(request.query)
            result_set = await self._execute_sql_statement(sql=sql)

            response = self._llama_model.synthesise_sql_result(request.query, result_set)
            return ApiResponse(success=True, result=response)

        except Exception as e:
            return ApiResponse(success=False, error=str(e))

    async def _get_table_schema(self, query: str) -> Dict[str, Any]:
        async with self._client as client:
            query_embeddings = self._llama_model.embed_query(query)
            result = await client.call_tool("get_table_schema", {"query_embeddings": query_embeddings})
            return result.data

    async def _execute_sql_statement(self, sql: str) -> List[Dict[str, Any]]:
        async with self._client as client:
            result = await client.call_tool("execute_sql_statement", {"sql": sql})
            return result.data
