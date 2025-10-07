"""Alias module to expose IMusicQueryService under src.domain.interfaces.

This forwards to the actual definition in `src.data_accessor.domain.interfaces`.
"""

from src.data_accessor.domain.interfaces.music_query_service import (  # noqa: F401
    IMusicQueryService,
)

__all__ = ["IMusicQueryService"]
