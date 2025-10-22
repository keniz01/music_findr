from punq import Container, Scope
from typing import Optional
from fastmcp import Client
from src.config.mcp_config import create_mcp_client
from src.models.llama_model import LlamaModel
from src.handlers.search_handler import SearchHandler
from src.services.search_services import (
    SQLExecutor,
    SQLResultSynthesizer,
    SQLGenerator,
    TableSchemaRetriever,
)
from src.config.app_config import AppConfig


class ContainerFactory:
    """Factory class for creating configured containers"""

    @staticmethod
    def create_container(config: Optional[AppConfig] = None) -> Container:
        """
        Creates and validates a fully configured container

        Args:
            config: Application configuration (optional)
        """
        container = Container()

        # Configuration
        if config:
            container.register(AppConfig).instance(config)
        else:
            container.register(AppConfig, factory=lambda _: AppConfig())

        # BASE DEPENDENCIES (External/External-like)
        container.register(LlamaModel, factory=_llama_model_factory)
        container.register(Client, factory=_mcp_client_factory)

        # SERVICES (Transient by default)
        _register_services(container)

        # HANDLERS
        container.register(SearchHandler)

        # VALIDATION
        _validate_container(container)

        return container


def _llama_model_factory(container: Container) -> LlamaModel:
    """Factory for LlamaModel with config injection"""
    config = container.resolve(AppConfig)
    return LlamaModel(config.llm_config)


def _mcp_client_factory(container: Container) -> Client:
    """Factory for MCP Client with config injection"""
    config = container.resolve(AppConfig)
    return create_mcp_client(config.mcp_config)


def _register_services(container: Container) -> None:
    """Register all search services with explicit dependencies"""
    services = [
        TableSchemaRetriever,
        SQLGenerator,
        SQLExecutor,
        SQLResultSynthesizer,
    ]

    for service in services:
        container.register(service)


def _validate_container(container: Container) -> None:
    """Validate container wiring during startup"""
    try:
        # Resolve critical components
        components = [
            LlamaModel,
            Client,
            SearchHandler,
            TableSchemaRetriever,
            SQLGenerator,
            SQLExecutor,
            SQLResultSynthesizer,
        ]

        for component in components:
            container.resolve(component)

        print("✅ Container validation: All components resolved successfully")

    except Exception as e:
        print(f"❌ DI Container validation failed: {e}")
        raise
