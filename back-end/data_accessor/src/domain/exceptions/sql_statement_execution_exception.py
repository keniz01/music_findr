"""Alias module exposing SqlStatementExecutionException under src.domain.exceptions."""

from src.data_accessor.domain.exceptions.sql_statement_execution_exception import (  # noqa: F401
    SqlStatementExecutionException,
)

__all__ = ["SqlStatementExecutionException"]
