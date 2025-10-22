from punq import Container
from fastmcp import Client

from src.config.mcp_config import create_mcp_client
from src.models.llama_model import LlamaModel
from src.services.schema_service import SchemaService
from src.services.sql_generation_service import SQLGenerationService
from src.services.sql_execution_service import SQLExecutionService
from src.services.result_synthesis_service import ResultSynthesisService
from src.handlers.search_handler import SearchHandler


def create_container() -> Container:
    container = Container()

    # Base dependencies
    container.register(LlamaModel, factory=lambda c: LlamaModel())
    container.register(Client, factory=lambda c: create_mcp_client())

    # Services
    container.register(SchemaService)
    container.register(SQLGenerationService)
    container.register(SQLExecutionService)
    container.register(ResultSynthesisService)

    # Handler
    container.register(SearchHandler)

    return container
