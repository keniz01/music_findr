from punq import Container
from sqlalchemy.ext.asyncio import create_async_engine

from data_accessor import (
    IMusicQueryController,
    MusicQueryController,
    IMusicQueryRepository,
    IMusicQueryService,
    MusicQueryService,
    MusicQueryRepository,
)


def setup_container() -> IMusicQueryController:
    container = Container()

    connection_string = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    engine = create_async_engine(connection_string)

    repo = MusicQueryRepository(engine=engine, default_schema="analysis")
    container.register(IMusicQueryRepository, instance=repo)

    service = MusicQueryService(repository=repo)
    container.register(IMusicQueryService, instance=service)

    controller = MusicQueryController(music_query_service=service)
    container.register(IMusicQueryController, instance=controller)

    return container
