"""Alias package to mirror expected imports.

Provides access to infrastructure-layer modules implemented under `data_accessor.infrastructure`.
"""

from src.data_accessor.infrastructure.repositories.music_query_repository import (  # noqa: F401
    MusicQueryRepository,
    DefaultSqlSafetyChecker,
)

__all__ = ["MusicQueryRepository", "DefaultSqlSafetyChecker"]
