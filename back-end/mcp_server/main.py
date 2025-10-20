from src.server_factory import create_app
from src.settings.database_settings import DatabaseSettings
from src.exceptions.unknow_connection_string_error import UnknownConnectionStringError

db_settings = DatabaseSettings()

if db_settings.db_url:
    app = create_app(db_settings.db_url)
else:
    raise UnknownConnectionStringError("Database URL is not configured.")
