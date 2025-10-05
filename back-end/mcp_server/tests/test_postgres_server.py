import unittest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from starlette.requests import Request
from data_accessor.src.application.interfaces.music_query_controller import IMusicQueryController

# Mock FastMCP before importing
mock_tool = Mock()
mock_tool.side_effect = lambda f: f

with patch('fastmcp.FastMCP.tool', return_value=mock_tool), \
     patch('punq.Container.resolve'):
    from src.services.postgres_server import PostgresServer, health_check

class TestPostgresServer(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a mock controller
        self.mock_controller = Mock(spec=IMusicQueryController)
        # Make the async methods truly async
        self.mock_controller.get_table_schema = AsyncMock()
        self.mock_controller.execute_sql = AsyncMock()

        # Create a test instance with mocked dependencies
        with patch('src.services.postgres_server.controller', self.mock_controller):
            self.server = PostgresServer()

    async def test_get_table_schema(self):
        # Arrange
        expected_schema = [{"table": "music", "columns": ["id", "name"]}]
        self.mock_controller.get_table_schema.return_value = expected_schema
        test_query = "Show me the music table schema"

        # Act
        result = await self.server.get_table_schema(test_query)

        # Assert
        self.assertEqual(result, expected_schema)
        self.mock_controller.get_table_schema.assert_called_once_with(test_query)

    async def test_execute_sql_statement(self):
        # Arrange
        expected_result = [{"id": 1, "name": "Test Song"}]
        self.mock_controller.execute_sql.return_value = expected_result
        test_query = "SELECT * FROM music"

        # Act
        result = await self.server.execute_sql_statement(test_query)

        # Assert
        self.assertEqual(result, expected_result)
        self.mock_controller.execute_sql.assert_called_once_with(test_query)

    async def test_health_check(self):
        # Arrange
        mock_request = Mock(spec=Request)
        current_time = datetime.now()

        # Act
        with patch('src.services.postgres_server.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_time
            response = await health_check(mock_request)

        # Assert
        expected_response = {
            "status": "healthy",
            "service": "mcp-server",
            "date/time": current_time.strftime("%d/%m/%Y %H:%M:%S")
        }

        self.assertEqual(response.status_code, 200)
        # Compare the JSON content instead of string representation
        import json
        actual_response = json.loads(response.body.decode())
        self.assertEqual(actual_response, expected_response)

class TestPostgresServerErrorHandling(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_controller = Mock(spec=IMusicQueryController)
        self.mock_controller.get_table_schema = AsyncMock()
        self.mock_controller.execute_sql = AsyncMock()

        with patch('src.services.postgres_server.controller', self.mock_controller):
            self.server = PostgresServer()

    async def test_get_table_schema_handles_error(self):
        # Arrange
        self.mock_controller.get_table_schema.side_effect = Exception("Database error")
        test_query = "Show me the music table schema"

        # Act & Assert
        with self.assertRaises(Exception) as context:
            await self.server.get_table_schema(test_query)

        self.assertEqual(str(context.exception), "Database error")

    async def test_execute_sql_statement_handles_error(self):
        # Arrange
        self.mock_controller.execute_sql.side_effect = Exception("Invalid SQL")
        test_query = "INVALID SQL"

        # Act & Assert
        with self.assertRaises(Exception) as context:
            await self.server.execute_sql_statement(test_query)

        self.assertEqual(str(context.exception), "Invalid SQL")

if __name__ == '__main__':
    unittest.main()
