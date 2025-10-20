import logging
from typing import Any, Dict, List

from ...application.interfaces.music_query_controller import IMusicQueryController
from ...domain.interfaces.music_query_service import IMusicQueryService


class MusicQueryController(IMusicQueryController):

    def __init__(self, music_query_service: IMusicQueryService) -> None:
        """
        Initialize the controller with a service (dependency injection).
        """
        self.music_query_service = music_query_service

    async def get_table_schema(self, query_embeddings: List[float]) -> Dict[str, Any]:
        try:
            schema = await self.music_query_service.get_table_schema(query_embeddings)
            logging.info("Controller: Fetched database schema.")
            return schema
        except Exception as e:
            logging.error(f"Controller: Error fetching schema: {e}")
            raise

    async def execute_sql_statement(self, sql: str) -> List[Dict[str, Any]]:
        try:
            response = await self.music_query_service.execute_sql_statement(sql)
            logging.info("Controller: SQL executed successfully.")
            return response
        except Exception as e:
            logging.error(f"Controller: Error executing SQL: {e}")
            raise
