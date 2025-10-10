"""MCP Client configuration"""

from dataclasses import dataclass

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


@dataclass
class MCPConfig:
    """MCP client configuration"""

    server_url: str = "http://localhost:8000/mcp"


def create_mcp_client() -> Client:
    """Creates a configured MCP client"""
    config = MCPConfig()
    transport = StreamableHttpTransport(url=config.server_url)
    return Client(transport=transport)
