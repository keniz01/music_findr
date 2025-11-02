import re
from typing import Protocol, List


class SQLTransform(Protocol):
    """Protocol for SQL transformation steps."""
    def apply(self, sql: str) -> str:
        ...


class RemoveSpacesTransform:
    def apply(self, sql: str) -> str:
        return sql.strip()


class RemoveBackTicksTransform:
    def apply(self, sql: str) -> str:
        return sql.replace('```sql', '').replace('```', '')


class RemoveSemicolonTransform:
    def apply(self, sql: str) -> str:
        return sql.replace(';', '')


class RemoveWildcardsTransform:
    def apply(self, sql: str) -> str:
        return sql.replace('%', '')


class ReplaceEqualsWithIlikeTransform:
    def apply(self, sql: str) -> str:
        pattern = r"=\s*'([^']*)'"
        return re.sub(pattern, r" ILIKE '\1'", sql)


class SQLFormatter:
    """Formatter that applies a sequence of injected transformations."""
    def __init__(self, transforms: List[SQLTransform]):
        self.transforms = transforms

    def format(self, sql: str) -> str:
        for transform in self.transforms:
            sql = transform.apply(sql)
        return sql.strip()
