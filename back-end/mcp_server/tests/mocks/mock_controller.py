"""Mock implementation of IMusicQueryController for testing."""

from typing import Any, Dict, List, Optional

from data_accessor import IMusicQueryController


class MockMusicQueryController(IMusicQueryController):
    def __init__(self):
        """Initialize the mock controller."""
        self.execute_sql_statement_calls: List[Dict[str, Any]] = []
        self.get_table_schema_calls: List[Dict[str, Any]] = []
        self.mock_sql_results: List[Dict[str, Any]] = [{"id": 1, "name": "Alice"}]
        self.mock_schema_result: Dict[str, Any] = {
            "table": "users",
            "columns": ["id", "name"],
        }

    async def execute_sql_statement(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Mock implementation of execute_sql_statement."""
        self.execute_sql_statement_calls.append({"sql": sql, "params": params})
        return self.mock_sql_results

    async def get_table_schema(self, embeddings: List[float]) -> Dict[str, Any]:
        """Mock implementation of get_table_schema."""
        self.get_table_schema_calls.append({"embeddings": embeddings})
        return self.mock_schema_result

    def reset(self) -> None:
        """Reset all mock data."""
        self.execute_sql_statement_calls.clear()
        self.get_table_schema_calls.clear()
        self.mock_sql_results.clear()
        self.mock_schema_result.clear()
