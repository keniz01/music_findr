"""Alias to expose MusicQueryRepository under src.infrastructure.repositories."""

from src.data_accessor.infrastructure.repositories.music_query_repository import (  # noqa: F401
    DefaultSqlSafetyChecker,
    MusicQueryRepository,
)

__all__ = ["MusicQueryRepository", "DefaultSqlSafetyChecker"]
