from __future__ import annotations
from typing import Protocol, Iterable
import sqlparse
from sqlparse.sql import Statement
from sqlparse import tokens as T


# ----------------------
# Rule Protocol
# ----------------------

class SqlSafetyRule(Protocol):
    """Return True if the query passes the rule; False otherwise."""
    def check(self, stmt: Statement, raw: str) -> bool: ...


# ----------------------
# Rule Implementations
# ----------------------

class SingleStatementRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        parsed = sqlparse.parse(raw)
        return len(parsed) == 1


class MustBeSelectRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return stmt.get_type() == "SELECT"


class NoWithCTERule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return all(
            not (token.ttype is T.CTE or token.match(T.Keyword.CTE, "WITH"))
            for token in stmt.flatten()
        )


class NoSemicolonRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return ";" not in raw.rstrip().rstrip(";")  # no trailing semi either


class NoCommentRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return all(t.ttype not in (T.Comment, T.Comment.Single, T.Comment.Multiline)
                   for t in stmt.flatten())


class NoForbiddenKeywordsRule:
    def __init__(self, forbidden: Iterable[str]):
        self.forbidden = {kw.lower() for kw in forbidden}

    def check(self, stmt: Statement, raw: str) -> bool:
        for token in stmt.flatten():
            if token.ttype in (T.Keyword, T.DML, T.DDL):
                if token.value.lower() in self.forbidden:
                    return False
        return True