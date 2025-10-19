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
from pathlib import Path
from urllib.parse import quote_plus
import tomllib


def _load_database_configuration() -> tuple[str, str]:
    """Load database connection config from secrets.toml.

    Returns a tuple of (connection_string, default_schema).

    The expected TOML file structure is:

    [database]
    host = "localhost"
    port = 5432
    database = "postgres"
    user = "postgres"
    password = "password"
    schema = "analysis"
    """

    secrets_path = (Path(__file__).resolve().parent.parent / "secrets.toml")
    if not secrets_path.exists():
        raise FileNotFoundError(
            f"Missing secrets file: {secrets_path}. "
            "Create it with a [database] section."
        )

    with secrets_path.open("rb") as fp:
        data = tomllib.load(fp)

    db = data.get("database", {})
    required_keys = ["host", "port", "database", "user", "password"]
    missing = [key for key in required_keys if key not in db]
    if missing:
        raise KeyError(
            f"Missing required database keys in secrets.toml: {', '.join(missing)}"
        )

    password_escaped = quote_plus(str(db["password"]))
    connection_string = (
        f"postgresql+asyncpg://{db['user']}:{password_escaped}"
        f"@{db['host']}:{db['port']}/{db['database']}"
    )
    default_schema = str(db.get("schema", "analysis"))
    return connection_string, default_schema


def setup_container() -> IMusicQueryController:
    container = Container()

    connection_string, default_schema = _load_database_configuration()
    engine = create_async_engine(connection_string)

    repo = MusicQueryRepository(engine=engine, default_schema=default_schema)
    container.register(IMusicQueryRepository, instance=repo)

    service = MusicQueryService(repository=repo)
    container.register(IMusicQueryService, instance=service)

    controller = MusicQueryController(music_query_service=service)
    container.register(IMusicQueryController, instance=controller)

    return container
