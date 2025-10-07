import unittest
from datetime import datetime
from unittest.mock import patch

from starlette.testclient import TestClient

from src.server_factory import create_app
from tests.mocks.mock_controller import MockMusicQueryController


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MockMusicQueryController()
        with patch("src.boot_strap.setup_container") as mock_setup_container:
            mock_container = mock_setup_container.return_value
            mock_container.resolve.return_value = self.mock_controller
            self.app = create_app()
            self.client = TestClient(self.app)

    def test_health_check(self):
        # Arrange
        current_time = datetime(2025, 10, 5, 12, 0, 0)

        # Act
        with patch("src.routes.datetime") as mock_datetime:
            mock_datetime.now.return_value = current_time
            response = self.client.get("/health")

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "mcp-server")
        self.assertEqual(data["date/time"], current_time.strftime("%d/%m/%Y %H:%M:%S"))
