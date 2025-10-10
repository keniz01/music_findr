import unittest
from unittest.mock import AsyncMock, MagicMock

from src.domain.interfaces.music_query_repository import IMusicQueryRepository
from src.domain.services.music_query_service import MusicQueryService


class TestMusicQueryService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=IMusicQueryRepository)
        self.mock_repository.execute_sql_statement = AsyncMock()
        self.mock_repository.get_table_schema = AsyncMock()
        self.service = MusicQueryService(repository=self.mock_repository)

    async def test_execute_sql_statement_calls_repository(self):
        # Arrange
        sql_query = "SELECT * FROM songs WHERE artist = :artist"
        params = {"artist": "Queen"}
        expected_result = [{"id": 1, "title": "Bohemian Rhapsody"}]
        self.mock_repository.execute_sql_statement.return_value = expected_result

        # Act
        result = await self.service.execute_sql_statement(sql_query, params)

        # Assert
        self.mock_repository.execute_sql_statement.assert_awaited_once_with(sql_query, params)
        self.assertEqual(result, expected_result)

    async def test_get_table_schema_calls_repository(self):
        # Arrange
        embeddings = [1223333]
        expected_schema = [
            {"table": "songs", "columns": ["id", "title", "artist"]},
            {"table": "albums", "columns": ["id", "name"]},
        ]
        self.mock_repository.get_table_schema.return_value = expected_schema

        # Act
        result = await self.service.get_table_schema(embeddings)

        # Assert
        self.mock_repository.get_table_schema.assert_awaited_once_with(embeddings)
        self.assertEqual(result, expected_schema)

    async def test_execute_sql_statement_with_no_params(self):
        # Arrange
        sql_query = "SELECT * FROM songs"
        expected_result = [{"id": 1, "title": "Imagine"}]
        self.mock_repository.execute_sql_statement.return_value = expected_result

        # Act
        result = await self.service.execute_sql_statement(sql_query)

        # Assert
        self.mock_repository.execute_sql_statement.assert_awaited_once_with(sql_query, None)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
