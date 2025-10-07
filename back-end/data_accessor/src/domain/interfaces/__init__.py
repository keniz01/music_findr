"""Alias package exposing domain interfaces under `src.domain.interfaces`.

This forwards to the actual interface definitions under `src.data_accessor.domain.interfaces`.
"""

from src.data_accessor.domain.interfaces.music_query_repository import (  # noqa: F401
    IMusicQueryRepository,
)
from src.data_accessor.domain.interfaces.music_query_service import (  # noqa: F401
    IMusicQueryService,
)

__all__ = ["IMusicQueryRepository", "IMusicQueryService"]
