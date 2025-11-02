from punq import Container, Scope
from fastmcp import Client
from loguru import logger

from src.config.mcp_config import create_mcp_client
from src.handlers.search_handler import SearchHandler
from src.services.search_services import (
    SQLExecutor,
    SQLResultSynthesizer,
    SQLGenerator,
    TableSchemaRetriever
)

from src.services.llama_service import LlamaService, LlamaConfig
from src.utils.sql_formatter import (
    SQLFormatter,
    RemoveSpacesTransform,
    RemoveBackTicksTransform,
    RemoveSemicolonTransform,
    RemoveWildcardsTransform,
    ReplaceEqualsWithIlikeTransform
)    

# ---------------------------
# Factories
# ---------------------------
def _create_mcp_client() -> Client:
    """Lazily create MCP client — only when actually used."""
    try:
        logger.info("Initialising dependency injection container[MCP Client]...")
        return create_mcp_client()
    except Exception as e:
        # Don't crash app startup; just log a warning
        logger.warning(f"⚠️ MCP client not initialized yet: {e}")
        return None  # Will retry later when actually used

# ---------------------------
# Registration Helpers
# ---------------------------
def _register_sql_formatter(container: Container) -> None:
    """Factory for creating the SQLFormatter singleton."""
    # Register individual transforms
    container.register(RemoveSpacesTransform)
    container.register(RemoveBackTicksTransform)
    container.register(RemoveSemicolonTransform)
    container.register(RemoveWildcardsTransform)
    container.register(ReplaceEqualsWithIlikeTransform)

    # Register the SQLFormatter — inject a list of transforms manually
    container.register(
        SQLFormatter,
        instance=SQLFormatter([
            container.resolve(RemoveSpacesTransform),
            container.resolve(RemoveBackTicksTransform),
            container.resolve(RemoveSemicolonTransform),
            container.resolve(RemoveWildcardsTransform),
            container.resolve(ReplaceEqualsWithIlikeTransform),
        ])
    )

    logger.info("Register SQLFormatter [MCP Client]...")


def _register_llama_service(container: Container) -> None:
    """Factory for creating the LlamaService singleton."""
    def factory() -> LlamaService:
        return LlamaService(
            config=LlamaConfig(), 
            sql_formatter=container.resolve(SQLFormatter)
        )
    container.register(LlamaService, factory=factory)
    logger.info("Register LlamaService [MCP Client]...")


def _register_search_services(container: Container) -> None:
    """Register all search-related service classes."""
    for service_cls in (
        TableSchemaRetriever,
        SQLGenerator,
        SQLExecutor,
        SQLResultSynthesizer,
    ):
        container.register(service_cls)
        logger.info(f"Register {service_cls.__name__} [MCP Client]...")

def _register_search_handler(container: Container) -> None:
    """Register the SearchHandler with explicit dependency resolution."""
    def factory() -> SearchHandler:
        return SearchHandler(
            schema_retriever=container.resolve(TableSchemaRetriever),
            sql_generator=container.resolve(SQLGenerator),
            sql_executor=container.resolve(SQLExecutor),
            result_synthesizer=container.resolve(SQLResultSynthesizer),
        )
    container.register(SearchHandler, factory=factory)
    logger.info("Register SearchHandler [MCP Client]...")



# ---------------------------
# Validation
# ---------------------------

def _validate_container(container: Container) -> None:
    """Validate that all critical components can be resolved."""
    critical_components = (
        LlamaService,
        TableSchemaRetriever,
        SQLGenerator,
        SQLExecutor,
        SQLResultSynthesizer,
    )

    try:
        for component in critical_components:
            container.resolve(component)

        logger.info("✅ Container validation successful: All components resolved.")

    except Exception as exc:
        logger.error(f"❌ Container validation failed: {exc}")
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
        container.register(Client, factory=_create_mcp_client, scope=Scope.singleton)

        # --- Formatters ---
        _register_sql_formatter(container)

        # --- Services ---
        _register_search_services(container)
        _register_llama_service(container)

        # --- Handlers ---
        _register_search_handler(container)

        # --- Validation ---
        _validate_container(container)

        return container