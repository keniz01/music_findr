from __future__ import annotations
from typing import List
from repositories.sql_validators.rules.sql_rules import (
    MustBeSelectRule, 
    NoCommentRule, 
    NoForbiddenKeywordsRule, 
    NoSemicolonRule, 
    NoWithCTERule, 
    SingleStatementRule, 
    SqlSafetyRule
)
import sqlparse

# ----------------------
# Checker
# ----------------------

class DefaultSqlSafetyChecker:
    """
    Validator for "safe" SELECT SQL queries using a pluggable rule system.
    """

    def __init__(self):
        self.rules: List[SqlSafetyRule] = [
            SingleStatementRule(),
            MustBeSelectRule(),
            NoWithCTERule(),
            NoSemicolonRule(),
            NoCommentRule(),
            NoForbiddenKeywordsRule(
                forbidden=[
                    "delete", "insert", "update", "drop",
                    "create", "alter", "commit", "rollback",
                ]
            ),
        ]

    def is_safe_select_query(self, query: str) -> bool:
        parsed = sqlparse.parse(query)
        if not parsed:
            return False

        stmt = parsed[0]

        return all(rule.check(stmt, query) for rule in self.rules)
