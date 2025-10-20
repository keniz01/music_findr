from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic.config import ConfigDict


class DatabaseSettings(BaseSettings):
    db_url: Optional[str] = Field(default=None, description="Database connection URL")

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )