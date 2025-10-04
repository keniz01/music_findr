from data_accessor.src.domain.interfaces.abstract_music_query_service import AbstractMusicQueryService
from data_accessor.src.application.abstract_music_query_controller import AbstractMusicQueryController
import logging

class MusicQueryController(AbstractMusicQueryController):

    def __init__(self, music_query_service: AbstractMusicQueryService) -> None:
        """
        Initialize the controller with a service (dependency injection).
        """
        self.music_query_service = music_query_service

    async def fetch_database_schema(self, query_embeddings: list[float]) -> list:
        try:
            schema = await self.music_query_service.fetch_database_schema(query_embeddings)
            logging.info("Controller: Fetched database schema.")
            return schema
        except Exception as e:
            logging.error(f"Controller: Error fetching schema: {e}")
            raise

    async def execute_sql(self, sql: str) -> list:
        try:
            response = await self.music_query_service.execute_sql(sql)
            logging.info("Controller: SQL executed successfully.")
            return response
        except Exception as e:
            logging.error(f"Controller: Error executing SQL: {e}")
            raise
