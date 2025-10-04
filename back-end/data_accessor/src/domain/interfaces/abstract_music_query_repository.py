from abc import ABC, abstractmethod

class AbstractMusicQueryRepository(ABC):
    """
    Abstract base class for database query repository.
    This class defines the interface for querying data from a database.
    """
    @abstractmethod
    async def execute_sql_statement(self, sql_statement: str) -> list:
        """
        Execute a query and return the results.

        :param query: The SQL query to execute.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    async def get_table_schema(self, query_embeddings: list[float]) -> list:
        """
        Fetch the database schema for a given schema name based on query embeddings.

        :param query_embeddings: Prompt embeddings.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
