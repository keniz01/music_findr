from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic.config import ConfigDict
import os

class DatabaseSettings(BaseSettings):
    database_url: Optional[str] = Field(default=None, description="Database connection URL")

    # Remove env_file; we will read from Docker secrets files
    model_config = ConfigDict(
        env_file=None,  # Don't use .env
        env_file_encoding="utf-8"
    )

    @property
    def resolved_database_url(self) -> Optional[str]:
        """
        Reads the database URL from a Docker secret file if present,
        otherwise falls back to the env variable DATABASE_URL.
        """
        secret_file = os.environ.get("DATABASE_URL_FILE")
        if secret_file and os.path.exists(secret_file):
            with open(secret_file) as f:
                return f.read().strip()

        raise Exception("DATABASE_URL is not defined. Please set the DATABASE_URL_FILE environment variable to point to a valid secret file.")

# Usage
settings = DatabaseSettings()
db_url = settings.resolved_database_url
