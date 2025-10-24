from punq import Container, Scope
from fastmcp import Client

from src.config.mcp_config import create_mcp_client
from src.models.llama_model import LlamaModel
from src.handlers.search_handler import SearchHandler
from src.services.search_services import (
    SQLExecutor,
    SQLResultSummarizer,
    SQLGenerator,
    TableSchemaRetriever,
)

# ---------------------------
# Factories
# ---------------------------

def _create_llama_model() -> LlamaModel:
    """Factory for creating the LlamaModel singleton."""
    return LlamaModel()


def _create_mcp_client() -> Client:
    """Factory for creating the MCP client singleton."""
    return create_mcp_client()


# ---------------------------
# Registration Helpers
# ---------------------------

def _register_search_services(container: Container) -> None:
    """Register all search-related service classes."""
    for service_cls in (
        TableSchemaRetriever,
        SQLGenerator,
        SQLExecutor,
        SQLResultSummarizer,
    ):
        container.register(service_cls)  # Default: transient scope


# ---------------------------
# Validation
# ---------------------------

def _validate_container(container: Container) -> None:
    """Validate that all critical components can be resolved."""
    critical_components = (
        LlamaModel,
        Client,
        SearchHandler,
        TableSchemaRetriever,
        SQLGenerator,
        SQLExecutor,
        SQLResultSummarizer,
    )

    try:
        for component in critical_components:
            container.resolve(component)

        print("✅ Container validation successful: All components resolved.")

    except Exception as exc:
        print(f"❌ Container validation failed: {exc}")
        raise

class ContainerFactory:
    """Factory class responsible for building and validating the DI container."""

    @staticmethod
    def create_container() -> Container:
        """
        Create and validate a fully configured dependency injection container.

        Returns:
            A configured and validated punq.Container instance.
        """
        container = Container()

        # --- Base dependencies ---
        container.register(LlamaModel, factory=_create_llama_model, scope=Scope.singleton)
        container.register(Client, factory=_create_mcp_client, scope=Scope.singleton)

        # --- Services ---
        _register_search_services(container)

        # --- Handlers ---
        container.register(SearchHandler)

        # --- Validation ---
        _validate_container(container)

        return container
