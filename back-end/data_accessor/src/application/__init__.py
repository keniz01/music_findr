"""Alias package to mirror expected imports.

Provides access to application-layer modules implemented under `data_accessor.application`.
"""

from src.data_accessor.application.controllers.music_query_controller import (  # noqa: F401
    MusicQueryController,
)

# Expose interfaces
from src.data_accessor.application.interfaces.music_query_controller import (  # noqa: F401
    IMusicQueryController,
)

__all__ = ["MusicQueryController", "IMusicQueryController"]
