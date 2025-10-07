"""Alias package exposing domain exceptions under `src.domain.exceptions`."""

from src.data_accessor.domain.exceptions.forbidden_sql_statement_exception import (  # noqa: F401
    ForbiddenSqlStatementException,
)
from src.data_accessor.domain.exceptions.sql_statement_execution_exception import (  # noqa: F401
    SqlStatementExecutionException,
)

__all__ = [
    "ForbiddenSqlStatementException",
    "SqlStatementExecutionException",
]
