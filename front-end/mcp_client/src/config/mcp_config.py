"""MCP Client configuration"""

import logging
from dataclasses import dataclass

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class MCPConfig:
    """MCP client configuration"""

    server_url: str = "http://mcp_server:8002/mcp"


def create_mcp_client() -> Client:
    """Creates a configured MCP client with detailed error logging"""
    config = MCPConfig()
    transport = StreamableHttpTransport(url=config.server_url)

    try:
        client = Client(transport=transport)
        logger.info("MCP client created successfully.")
        return client
    except Exception:
        logger.exception(
            "Failed to create MCP client. "
            "Please check the server URL, network connection, and server availability. "
            "Server URL: %s", config.server_url
        )
        # Optionally, re-raise the exception to let the caller handle it
        raise
