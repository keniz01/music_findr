from __future__ import annotations
from typing import List, Protocol
from repositories.sql_validators.rules.sql_rules import (
    MustBeSelectRule,
    NoCommentRule,
    NoForbiddenKeywordsRule,
    NoFunctionsRule,
    NoJoinRule,
    NoLimitOffsetRule,
    NoOrderGroupHavingRule,
    NoSemicolonRule,
    NoSubqueryRule,
    NoUnionOrSetOpsRule,
    NoWithCTERule,
    SingleStatementRule,
    SqlSafetyRule
)
import sqlparse

# ----------------------
# Checker
# ----------------------

class SqlSafetyChecker(Protocol):
    def is_safe_select_query(self, query: str) -> bool: ...

class DefaultSqlSafetyChecker:
    """
    Validator for "safe" SELECT SQL queries using a pluggable rule system.
    """

    def __init__(self):
        self.rules: List[SqlSafetyRule] = [
            # Fundamental
            SingleStatementRule(),
            MustBeSelectRule(),
            NoSemicolonRule(),
            NoCommentRule(),
            NoWithCTERule(),
            NoForbiddenKeywordsRule(
                ["delete", "insert", "update", "drop", "create", "alter",
                 "commit", "rollback"],
            ),

            # Advanced Structural Guardrails
            NoSubqueryRule(),
            NoUnionOrSetOpsRule(),
            NoJoinRule(),
            NoOrderGroupHavingRule(),
            NoLimitOffsetRule(),
            NoFunctionsRule()
        ]

    def is_safe_select_query(self, query: str) -> bool:
        parsed = sqlparse.parse(query)
        if not parsed:
            return False

        stmt = parsed[0]
        return all(rule.check(stmt, query) for rule in self.rules)
