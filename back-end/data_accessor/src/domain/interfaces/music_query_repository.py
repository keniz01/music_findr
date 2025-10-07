"""Alias module to expose IMusicQueryRepository under src.domain.interfaces."""

from src.data_accessor.domain.interfaces.music_query_repository import (  # noqa: F401
    IMusicQueryRepository,
)

__all__ = ["IMusicQueryRepository"]
