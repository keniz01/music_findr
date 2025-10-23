import re
from typing import Any, Dict, List

from fastmcp import Client
from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest
from src.models.llama_model import LlamaModel

class SQLFormatter:

    def __init__(self, sql: str):
        self.sql=sql

    def remove_spaces(self):
        self.sql=self.sql.strip()
        return self

    def remove_back_ticks(self):
        self.sql=self.sql.replace('```sql','').replace('```','')
        return self

    def remove_semi_colon(self):
        self.sql=self.sql.replace(";",'')
        return self
       
    def remove_wild_cards(self):
        self.sql=self.sql.replace("%",'')
        return self
    
    def replace_equals_with_ilike(self):
        pattern = r"=\s*'([^']*)'"
        self.sql = re.sub(pattern, r" ILIKE '\1'", self.sql)       
        return self
    
class SearchHandler:
    """Handles search operations using the MCP server"""

    def __init__(self, llama_model: LlamaModel, client: Client) -> None:
        self._client=client
        self._llama_model=llama_model

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

            sql = self._llama_model.generate_sql(request.query, schema)
            formatter = SQLFormatter(sql)
            formatted_sql = (
                formatter.remove_spaces()
                        .remove_back_ticks()
                        .remove_wild_cards()
                        .remove_semi_colon()
                        .replace_equals_with_ilike()
                        .sql
            )
            sql_response = await self._execute_sql_statement(sql=formatted_sql)

            # response = self._llama_model.synthesise_sql_result(request.query, result_set)
            return ApiResponse(success=True, result=sql_response)

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
