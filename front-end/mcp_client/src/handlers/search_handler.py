import json
import re
from loguru import logger
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

            summary = self._llama_model.summarise_sql_result(request.query, sql_response, formatted_sql)
            return ApiResponse(success=True, result=summary)

        except Exception as e:
            return ApiResponse(success=False, error=str(e))

    async def _get_table_schema(self, query: str) -> Dict[str, Any]:
        async with self._client as client:
            query_embeddings = self._llama_model.embed_query(query)
            result = await client.call_tool("get_table_schema", {"query_embeddings": query_embeddings})
            
            if result.is_error:
                logger.error(f"Query embeddings failed: {result}")
                raise RuntimeError("Query embeddings failed")

            if result.content and len(result.content) > 0:
                raw_text = result.content[0].text.strip()
                try:
                    parsed = json.loads(raw_text)
                    # Sometimes schema info is nested under "schema" key
                    schema_info = parsed.get("schema", parsed)
                    logger.debug("Parsed schema from JSON text successfully.")
                    return schema_info
                except json.JSONDecodeError:
                    logger.warning("Schema response not valid JSON; returning raw text.")
                    return {"raw_schema": raw_text}

    async def _execute_sql_statement(self, sql: str) -> List[dict[str, Any]]:
        async with self._client as client:
            result = await client.call_tool("execute_sql_statement", {"sql": sql})
            
            if result.is_error:
                logger.error(f"SQL execution failed: {result}")
                raise RuntimeError("SQL execution failed")

            logger.debug(f"SQL Execution Result: {result.structured_content}")
            return result.structured_content.get("result", [])

