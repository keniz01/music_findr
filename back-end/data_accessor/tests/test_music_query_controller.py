import unittest
from unittest.mock import AsyncMock, create_autospec

from src.application.controllers.music_query_controller import MusicQueryController
from src.domain.interfaces.music_query_service import IMusicQueryService


class TestMusicQueryController(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_service = create_autospec(IMusicQueryService, instance=True)
        self.mock_service.get_table_schema = AsyncMock()
        self.mock_service.execute_sql_statement = AsyncMock()
        self.controller = MusicQueryController(self.mock_service)

    async def test_get_table_schema(self):
        mock_response = [{"table": "songs"}, {"table": "artists"}]
        embeddings = [2132131]
        self.mock_service.get_table_schema.return_value = mock_response

        result = await self.controller.get_table_schema(embeddings)

        self.mock_service.get_table_schema.assert_awaited_once_with(embeddings)
        self.assertEqual(result, mock_response)

    async def test_execute_sql_statement(self):
        sql = "SELECT * FROM songs"
        mock_response = [{"id": 1, "title": "Imagine"}]
        self.mock_service.execute_sql_statement.return_value = mock_response

        result = await self.controller.execute_sql_statement(sql)

        self.mock_service.execute_sql_statement.assert_awaited_once_with(sql)
        self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()
