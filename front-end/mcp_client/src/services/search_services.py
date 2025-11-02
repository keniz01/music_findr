from fastmcp import Client
from src.services.llama_service import LlamaService
from typing import Dict, List, Any
from loguru import logger
import json
class TableSchemaRetriever:
    def __init__(self, client: Client, llama_service: LlamaService):
        if client is None:
            raise RuntimeError("MCP client is not initialized — check connection or configuration.")        
        self._client = client
        self._llama_service = llama_service

    async def get_schema_info(self, query: str) -> Dict[str, Any]:
        query_embeddings = await self._llama_service.embed_query(query)

        async with self._client as client:
            result = await client.call_tool(
                "get_table_schema", {"query_embeddings": query_embeddings}
            )

        if result.is_error:
            logger.error(f"Table schema retrieval failed: {result}")
            raise RuntimeError("Failed to retrieve table schema from MCP")

        if result.content and len(result.content) > 0:
            raw_text = result.content[0].text.strip()
            try:
                parsed = json.loads(raw_text)
                schema_info = parsed.get("schema", parsed)
                return schema_info
            except json.JSONDecodeError:
                return {"raw_schema": raw_text}

        return {}

class SQLGenerator:
    def __init__(self, llama_service: LlamaService):
        self._llama_service = llama_service

    async def generate_sql(self, query: str, schema_info: Dict[str, Any]) -> str:
        return await self._llama_service.generate_sql(query, schema_info)

class SQLExecutor:
    def __init__(self, client: Client):
        if client is None:
            raise RuntimeError("MCP client is not initialized — check connection or configuration.")        
        
        self._client = client

    async def execute(self, sql: str) -> List[Dict[str, Any]]:

        async with self._client as client:
            result = await client.call_tool(
                "execute_sql_statement", {"sql": sql}
            )

        if result.is_error:
            logger.error(f"SQL execution failed: {result}")
            raise RuntimeError("Failed to execute SQL")

        # Use structured_content to extract "result" consistently
        return result.structured_content.get("result", [])

class SQLResultSynthesizer:
    def __init__(self, llama_service: LlamaService):
        self._llama_service = llama_service

    async def synthesize(self, query: str, sql_result_set: List[Dict[str, Any]]) -> Any:
        return await self._llama_service.summarise_sql_result(query, sql_result_set)
