from abc import ABC, abstractmethod


class AbstractPostgresServer(ABC):

    @abstractmethod
    async def get_table_schema(self, user_query: str) -> list:
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    async def execute_sql_statement(self, user_query: str) -> list:
        raise NotImplementedError("This method should be overridden by subclasses.")
