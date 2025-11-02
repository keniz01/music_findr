from src.server_factory import create_app
from src.settings.database_settings import DatabaseSettings
from src.exceptions.unknow_connection_string_error import UnknownConnectionStringError

db_settings = DatabaseSettings()
database_url = db_settings.resolved_database_url  # ✅ use the resolved property

if database_url:
    app = create_app(database_url)
else:
    raise UnknownConnectionStringError("Database URL is not configured.")
