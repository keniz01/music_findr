"""Alias to expose MusicQueryService under src.domain.services."""

from src.data_accessor.domain.services.music_query_service import (  # noqa: F401
    MusicQueryService,
)

__all__ = ["MusicQueryService"]
