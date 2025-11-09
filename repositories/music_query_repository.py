import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Protocol, Tuple, Union

import sqlparse
from sqlalchemy import text
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.ext.asyncio.result import AsyncResult

from ...domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from ...domain.exceptions.sql_statement_execution_exception import SqlStatementExecutionException
from ...domain.interfaces.music_query_repository import IMusicQueryRepository
from ...infrastructure.repositories.exception_handlers import raise_sql_execution_exception


class SqlSafetyChecker(Protocol):
    def is_safe_select_query(self, query: str) -> bool: ...


class DefaultSqlSafetyChecker:
    """
    Class responsible for verifying if an SQL query is safe (i.e., a simple SELECT).
    """

    def is_safe_select_query(self, query: str) -> bool:
        parsed = sqlparse.parse(query)
        if not parsed or len(parsed) != 1:
            return False

        stmt = parsed[0]
        stmt_type = stmt.get_type()
        if stmt_type != "SELECT":
            return False

        # Disallow CTEs (WITH ...)
        if any(
            token.ttype is sqlparse.tokens.CTE and token.value.upper() == "WITH"
            for token in stmt.tokens
        ):
            return False

        # Disallow semicolons (multiple statements)
        if ";" in query:
            return False

        # Disallow comments
        if "--" in query or "/*" in query:
            return False

        # Disallow transaction control and DML/DDL keywords
        forbidden = {"delete", "insert", "update", "drop", "create", "alter", "commit", "rollback"}
        tokens = [token for token in stmt.tokens if not token.is_whitespace]
        for token in tokens:
            if str(token).strip().lower() in forbidden:
                return False

        return True


class MusicQueryRepository(IMusicQueryRepository):
    """
    Repository class for music queries.
    """

    def __init__(
        self,
        engine: AsyncEngine,
        sql_safety_checker: SqlSafetyChecker = DefaultSqlSafetyChecker()
    ) -> None:
        self._engine = engine
        self._sql_safety_checker = sql_safety_checker

    @asynccontextmanager
    async def get_conn(self, schema_name: str) -> AsyncGenerator[AsyncConnection, None]:
        try:
            conn = await self._engine.connect()
            try:
                await conn.execute(text(f"SET search_path TO {schema_name}"))
                yield conn
            finally:
                await conn.close()
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            raise_sql_execution_exception("Error connecting to database", e, include_traceback=True)

    async def execute_sql_statement(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if not self._sql_safety_checker.is_safe_select_query(sql):
            logging.warning(f"Forbidden SQL statement attempted: {sql}")
            raise ForbiddenSqlStatementException("Only simple SELECT statements are allowed.")

        async with self.get_conn("music") as conn:
            try:
                result: Union[AsyncResult, CursorResult] = await conn.execute(
                    text(sql), parameters=params if params else {}
                )
                if result.returns_rows:
                    rows = result.fetchall()
                    # Convert SQL Alchemy row proxies to dicts
                    result_dicts = [dict(zip(row._fields, row)) for row in rows]
                    logging.info(f"SQL executed successfully, returned {len(rows)} rows.")
                    return result_dicts
                return []
            except Exception as e:
                logging.error(f"Error executing SQL statement: {e}")
                raise_sql_execution_exception(
                    "Error connecting to database", e, include_traceback=True
                )

    async def get_table_schema(self, query_embeddings: list[float]) -> Dict[str, Any]:
        """
        Fetches the top 4 most similar database schema entries from the 'schema_embeddings' table,
        based on cosine similarity with the given prompt embeddings.

        Args:
            query_embeddings (str): The vector embeddings of the prompt.

        Returns:
            str: A human-readable string representation of the schema.
        """
        query = self._build_similarity_query()

        try:
            async with self.get_conn("meta") as conn:
                embedding_str = f"[{','.join(map(str, query_embeddings))}]"
                result = await conn.execute(query, {"query_embeddings": embedding_str})
                rows = result.fetchall()

                formatted = self._format_schema_rows(rows)
                return {"schema": formatted}

        except Exception as e:
            logging.error(f"Error fetching database schema: {e}", exc_info=True)
            raise SqlStatementExecutionException(
                f"""
                                                    Error fetching database schema: {type(e).__name__}
                                                    Exception: {e}
                                                    """
            ) from e

    def _build_similarity_query(self) -> text:
        return text(
            """
            SELECT raw_json
            FROM schema_embeddings
            ORDER BY (embeddings <#> CAST(:query_embeddings AS vector)) ASC
            LIMIT 4
            """
        )

    def _format_schema_rows(self, rows: list) -> str:
        """
        Formats the fetched rows into a readable schema string.

        Args:
            rows (list): List of database rows.

        Returns:
            str: Formatted schema string.
        """
        schema_lines = []

        for (raw_json,) in rows:
            schema_lines.extend(self._format_single_schema(raw_json))
            schema_lines.append("")  # Add spacing between tables

        logging.info("Fetched database schema for meta")
        return "\n".join(schema_lines)

    def _format_single_schema(self, raw_json: dict) -> list[str]:
        """
        Formats a single raw_json schema entry.

        Args:
            raw_json (dict): Parsed JSON of a schema row.

        Returns:
            list[str]: Lines of formatted schema.
        """
        lines = []
        for table_name, table_info in raw_json.items():
            lines.append(f"{table_name}:")
            if isinstance(table_info, dict):
                columns = table_info.get("columns", {})
                for column_name, column_info in columns.items():
                    description = (
                        column_info.get("column_description", "")
                        if isinstance(column_info, dict)
                        else str(column_info)
                    )
                    lines.append(f"  {column_name}: {description}")
        return lines
