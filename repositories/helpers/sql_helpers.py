from typing import Protocol
import sqlparse
from sqlparse.sql import Statement


class SqlSafetyChecker(Protocol):
    def is_safe_select_query(self, query: str) -> bool: ...


class DefaultSqlSafetyChecker:
    """
    Class responsible for verifying if an SQL query is safe (i.e., a simple SELECT).
    """

    def is_safe_select_query(self, query: str) -> bool:
        parsed: tuple[Statement, ...] = sqlparse.parse(query)
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
        forbidden = {
            "delete",
            "insert",
            "update",
            "drop",
            "create",
            "alter",
            "commit",
            "rollback",
        }
        tokens = [token for token in stmt.tokens if not token.is_whitespace]
        for token in tokens:
            if str(token).strip().lower() in forbidden:
                return False

        return True
