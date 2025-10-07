"""Alias module exposing ForbiddenSqlStatementException under src.domain.exceptions."""

from src.data_accessor.domain.exceptions.forbidden_sql_statement_exception import (  # noqa: F401
    ForbiddenSqlStatementException,
)

__all__ = ["ForbiddenSqlStatementException"]
