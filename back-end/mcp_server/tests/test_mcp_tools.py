import unittest
from unittest.mock import patch
from starlette.testclient import TestClient
from fastmcp import Client

from src.server_factory import create_app
from tests.mocks.mock_controller import MockMusicQueryController


class TestMcpTools(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.controller = MockMusicQueryController()
        with patch("src.boot_strap.setup_container") as mock_setup_container:
            mock_container = mock_setup_container.return_value
            mock_container.resolve.return_value = self.controller
            from src.server_factory import (
                create_mcp_app,
                add_middlewares,
                register_tools,
            )

            # Create FastMCP server
            self.mcp = create_mcp_app()
            add_middlewares(self.mcp)
            register_tools(self.mcp, self.controller)
            # Also create HTTP app for health check tests
            self.app = self.mcp.http_app()

    async def test_get_table_schema(self):
        # Test direct method call
        result = await self.controller.get_table_schema(
            [0.1, -0.2]
        )  # Using dummy embeddings
        self.assertEqual(result["table"], "users")
        self.assertEqual(result["columns"], ["id", "name"])

        # Test using FastMCP client
        async with Client(self.mcp) as client:
            result = await client.call_tool(
                "get_table_schema", {"embeddings": [0.1, -0.2]}
            )
            self.assertEqual(result.data["table"], "users")
            self.assertEqual(result.data["columns"], ["id", "name"])

    async def test_execute_sql_statement(self):
        # Test direct method call
        result = await self.controller.execute_sql_statement("SELECT * FROM users")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["name"], "Alice")

        # Test using FastMCP client
        async with Client(self.mcp) as client:
            result = await client.call_tool(
                "execute_sql_statement", {"sql": "SELECT * FROM users"}
            )
            self.assertIsInstance(result.data, list)
            self.assertEqual(result.data[0]["name"], "Alice")
