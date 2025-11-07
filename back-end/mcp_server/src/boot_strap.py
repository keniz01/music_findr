import sys
from typing import Final
from punq import Container
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from loguru import logger

from data_accessor import (
    IMusicQueryController,
    IMusicQueryRepository,
    IMusicQueryService,
    MusicQueryController,
    MusicQueryRepository,
    MusicQueryService,
)


# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
logger.remove()  # Remove default sink
logger.add(
    sys.stderr,
    level="INFO",
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level: <8}</level> "
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>"
    ),
)
logger.add("logs/setup_container.log", rotation="1 week", retention="1 month", level="DEBUG")


# -----------------------------------------------------------------------------
# Container Setup
# -----------------------------------------------------------------------------
def setup_container(connection_string: str) -> Container:
    """
    Set up the dependency injection container for the Music Query system.

    Args:
        connection_string (str): The database connection string.

    Returns:
        Container: A configured punq dependency injection container.
    """
    logger.info("Starting setup of dependency injection container [MCP Server]...")
    container = Container()

    try:
        # Create database engine
        logger.debug("Creating async SQLAlchemy engine...")
        engine: Final[AsyncEngine] = create_async_engine(connection_string, echo=False, future=True)
        logger.success("Async SQLAlchemy engine created successfully.")

        # Register repository
        logger.debug("Initializing MusicQueryRepository...")
        repo = MusicQueryRepository(engine=engine)
        container.register(IMusicQueryRepository, instance=repo)
        logger.success("Registered IMusicQueryRepository -> MusicQueryRepository")

        # Register service
        logger.debug("Initializing MusicQueryService...")
        service = MusicQueryService(repository=repo)
        container.register(IMusicQueryService, instance=service)
        logger.success("Registered IMusicQueryService -> MusicQueryService")

        # Register controller
        logger.debug("Initializing MusicQueryController...")
        controller = MusicQueryController(music_query_service=service)
        container.register(IMusicQueryController, instance=controller)
        logger.success("Registered IMusicQueryController -> MusicQueryController")

        logger.info("MCP Server Container setup completed successfully.")
        return container

    except Exception as e:
        logger.exception(f"MCP Server Container setup failed due to an error: {e}")
        raise
