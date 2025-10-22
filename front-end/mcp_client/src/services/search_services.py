from fastmcp import Client
from src.models.llama_model import LlamaModel
from typing import Dict, List, Any

class TableSchemaRetriever:
    def __init__(self, client: Client, llama_model: LlamaModel):
        self._client = client
        self._llama_model = llama_model

    async def get_schema(self, query: str) -> Dict[str, Any]:
        query_embeddings = self._llama_model.embed_query(query)
        result = await self._client.call_tool("get_table_schema", {"query_embeddings": query_embeddings})
        return result.data

class SQLGenerator:
    def __init__(self, llama_model: LlamaModel):
        self._llama_model = llama_model

    def generate_sql(self, query: str) -> str:
        return self._llama_model.generate_sql(query)

class SQLExecutor:
    def __init__(self, client: Client):
        self._client = client

    async def execute(self, sql: str) -> List[Dict[str, Any]]:
        result = await self._client.call_tool("execute_sql_statement", {"sql": sql})
        return result.data


class SQLResultSynthesizer:
    def __init__(self, llama_model: LlamaModel):
        self._llama_model = llama_model

    def synthesize(self, query: str, sql_result_set: List[Dict[str, Any]]) -> Any:
        return self._llama_model.synthesise_prompt(query, sql_result_set)