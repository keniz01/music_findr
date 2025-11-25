from __future__ import annotations
from typing import Protocol, Iterable
import sqlparse
from sqlparse.sql import (
    Statement, Function, Parenthesis, TokenList
)
from sqlparse import tokens as T


# ============================================================
# Base Rule Protocol
# ============================================================

class SqlSafetyRule(Protocol):
    """Return True if the query passes the rule; False otherwise."""
    def check(self, stmt: Statement, raw: str) -> bool:
        ...


# ============================================================
# Utility helpers
# ============================================================

def flatten(stmt: TokenList):
    return (t for t in stmt.flatten())

def any_token(stmt: TokenList, predicate):
    return any(predicate(t) for t in flatten(stmt))


# ============================================================
# Fundamental Rules
# ============================================================

class SingleStatementRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return len(sqlparse.parse(raw)) == 1


class MustBeSelectRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return stmt.get_type() == "SELECT"


class NoSemicolonRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return ";" not in raw.rstrip().rstrip(";")


class NoCommentRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return not any_token(
            stmt, lambda t: t.ttype in (T.Comment, T.Comment.Single, T.Comment.Multiline)
        )


class NoWithCTERule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return not any_token(stmt, lambda t: t.match(T.Keyword.CTE, "WITH"))


class NoForbiddenKeywordsRule:
    def __init__(self, forbidden: Iterable[str]):
        self.forbidden = {kw.lower() for kw in forbidden}

    def check(self, stmt: Statement, raw: str) -> bool:
        return not any_token(
            stmt,
            lambda t: (t.ttype in (T.DDL, T.DML, T.Keyword))
            and t.value.lower() in self.forbidden,
        )


# ============================================================
# Structure-Level Rules (More Advanced)
# ============================================================

class NoSubqueryRule:
    """Disallow SELECT inside parentheses or nested SELECTs."""
    def check(self, stmt: Statement, raw: str) -> bool:
        return not any(
            isinstance(tok, Parenthesis) and "select" in tok.value.lower()
            for tok in stmt.tokens
        )


class NoUnionOrSetOpsRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        # UNION, INTERSECT, EXCEPT
        set_ops = {"union", "intersect", "except"}
        return not any_token(
            stmt, lambda t: t.ttype == T.Keyword and t.value.lower() in set_ops
        )


class NoJoinRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        return not any_token(stmt, lambda t: t.match(T.Keyword, "JOIN"))


class NoOrderGroupHavingRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        forbidden = {"order", "group", "having"}
        return not any_token(
            stmt,
            lambda t: t.ttype == T.Keyword and t.value.lower() in forbidden
        )


class NoLimitOffsetRule:
    def check(self, stmt: Statement, raw: str) -> bool:
        forbidden = {"limit", "offset", "fetch"}
        return not any_token(
            stmt,
            lambda t: t.ttype == T.Keyword and t.value.lower() in forbidden
        )


class NoFunctionsRule:
    """Disallow ANY function call: SUM(), NOW(), LOWER(), etc."""
    def check(self, stmt: Statement, raw: str) -> bool:
        return not any(isinstance(tok, Function) for tok in flatten(stmt))
