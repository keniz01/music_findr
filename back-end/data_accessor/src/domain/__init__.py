"""Alias package to mirror expected imports.

Provides access to domain-layer modules implemented under `data_accessor.domain`.
"""

# Exceptions
from src.data_accessor.domain.exceptions.forbidden_sql_statement_exception import (  # noqa: F401
    ForbiddenSqlStatementException,
)
from src.data_accessor.domain.exceptions.sql_statement_execution_exception import (  # noqa: F401
    SqlStatementExecutionException,
)

# Interfaces
from src.data_accessor.domain.interfaces.music_query_repository import (  # noqa: F401
    IMusicQueryRepository,
)
from src.data_accessor.domain.interfaces.music_query_service import (  # noqa: F401
    IMusicQueryService,
)

# Services
from src.data_accessor.domain.services.music_query_service import (  # noqa: F401
    MusicQueryService,
)

__all__ = [
    "ForbiddenSqlStatementException",
    "SqlStatementExecutionException",
    "IMusicQueryRepository",
    "IMusicQueryService",
    "MusicQueryService",
]
