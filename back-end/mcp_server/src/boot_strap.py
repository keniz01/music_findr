from data_accessor import (
    IMusicQueryController,
    IMusicQueryRepository,
    IMusicQueryService,
    MusicQueryController,
    MusicQueryRepository,
    MusicQueryService,
)
from punq import Container
from sqlalchemy.ext.asyncio import create_async_engine


def setup_container(connection_string: str) -> Container:
    container = Container()

    engine = create_async_engine(connection_string)

    repo = MusicQueryRepository(engine=engine)
    container.register(IMusicQueryRepository, instance=repo)

    service = MusicQueryService(repository=repo)
    container.register(IMusicQueryService, instance=service)

    controller = MusicQueryController(music_query_service=service)
    container.register(IMusicQueryController, instance=controller)

    return container
