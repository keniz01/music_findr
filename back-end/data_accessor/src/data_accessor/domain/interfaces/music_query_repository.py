from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IMusicQueryRepository(ABC):
    @abstractmethod
    async def execute_sql_statement(self, sql_statement: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL statement and return the results"""
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    async def get_table_schema(self, embeddings: List[float]) -> Dict[str, Any]:
        """Get table schema information using vector embeddings"""
        raise NotImplementedError("This method should be overridden by subclasses.")
