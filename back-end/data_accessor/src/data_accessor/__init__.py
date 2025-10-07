"""Data accessor package"""
from .application.interfaces.music_query_controller import IMusicQueryController
from .application.controllers.music_query_controller import MusicQueryController
from .domain.interfaces.music_query_repository import IMusicQueryRepository
from .domain.interfaces.music_query_service import IMusicQueryService
from .domain.services.music_query_service import MusicQueryService
from .infrastructure.repositories.music_query_repository import MusicQueryRepository

__all__ = [
    "IMusicQueryController",
    "MusicQueryController",
    "IMusicQueryRepository",
    "IMusicQueryService",
    "MusicQueryService",
    "MusicQueryRepository"
]
