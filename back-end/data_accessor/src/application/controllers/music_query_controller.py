"""Alias to expose MusicQueryController under src.application.controllers."""

from src.data_accessor.application.controllers.music_query_controller import (  # noqa: F401
    MusicQueryController,
)

__all__ = ["MusicQueryController"]
