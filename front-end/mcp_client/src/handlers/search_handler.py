from time import time
from typing import Any

from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest
from src.services.search_services import (
    SQLExecutor,
    SQLResultSynthesizer,
    SQLGenerator,
    TableSchemaRetriever,
)

def get_duration_in_seconds(start: float) -> float:
    end = time()
    duration = end - start
    return duration
    
class SearchHandler:
    """Handles search operations using the MCP server"""

    def __init__(
        self, 
        schema_retriever: TableSchemaRetriever,
        sql_generator: SQLGenerator,
        sql_executor: SQLExecutor,
        result_synthesizer: SQLResultSynthesizer,
    ):
        self._schema_retriever = schema_retriever
        self._sql_generator = sql_generator
        self._sql_executor = sql_executor
        self._result_synthesizer = result_synthesizer

    async def search_by_query(self, request: SearchQueryRequest) -> ApiResponse[Any]:
        start = time()
        if not request.query.strip():
            return ApiResponse(success=False, error="Query cannot be empty", duration_secs=get_duration_in_seconds(start))

        try:
            schema_info = await self._schema_retriever.get_schema_info(request.query)
            if not schema_info:
                return ApiResponse(success=False, error="No relevant tables found", duration_secs=get_duration_in_seconds(start))

            sql = await self._sql_generator.generate_sql(request.query, schema_info)
            sql_result = await self._sql_executor.execute(sql)
            summary = await self._result_synthesizer.synthesize(request.query, sql_result)

            return ApiResponse(success=True, result=summary, duration_secs=get_duration_in_seconds(start))
        except Exception as e:
            return ApiResponse(success=False, error=str(e), duration_secs=get_duration_in_seconds(start))
