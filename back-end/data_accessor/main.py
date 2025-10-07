import os
import sys
import asyncio
from punq import Container
from sqlalchemy.ext.asyncio import create_async_engine
from data_accessor import (
    MusicQueryController,
    MusicQueryService,
    MusicQueryRepository,
    IMusicQueryController,
    IMusicQueryRepository,
    IMusicQueryService,
)

database_url = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

def configure_container() -> Container:
    container = Container()
    engine = create_async_engine(database_url)

    # Create instances directly first
    repo = MusicQueryRepository(engine=engine, default_schema=os.getenv("DEFAULT_SCHEMA", "public"))
    service = MusicQueryService(repository=repo)
    controller = MusicQueryController(music_query_service=service)

    # Register instances
    container.register(IMusicQueryRepository, instance=repo)
    container.register(IMusicQueryService, instance=service)
    container.register(IMusicQueryController, instance=controller)

    return container

def _get_sample_embeddings() -> list[float]:
    # Short sample embedding for demo purposes
    return [0.12, -0.34, 0.56, -0.78, 0.90]


if __name__ == "__main__":
    # Create and configure the DI container
    container = configure_container()
    controller = container.resolve(IMusicQueryController)

    async def main() -> None:
        result = await controller.get_table_schema(_get_sample_embeddings())
        print(result)

    asyncio.run(main())
