import logging
import os
from typing import Any, List

import strawberry
from strawberry.fastapi import GraphQLRouter

from dependencies.dependency_container import setup_container
from services.music_query_service import IMusicQueryService

# Get the database URL from environment, raise error if not set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Dependency injection setup
_container = setup_container(DATABASE_URL)
_music_query_service = _container.resolve(IMusicQueryService)


# Strawberry input type for the query
@strawberry.input
class SqlStatementRequest:
    sql_statement: str = ""


# JSON scalar for dynamic result sets
@strawberry.scalar(description="Arbitrary JSON object")
class JSON:
    serialize = lambda v: v
    parse_value = lambda v: v


# GraphQL Query type
@strawberry.type
class Query:
    @strawberry.field(description="Health check")
    def ping(self) -> str:
        return "GraphQL Music Query API is running!"

    @strawberry.field(description="Executes a SQL SELECT statement")
    async def execute_sql_statement(self, request: SqlStatementRequest) -> List[JSON]:
        sql = request.sql_statement.strip()

        # Only allow SELECT queries
        if not sql.lower().startswith("select"):
            raise ValueError("Only SELECT statements are allowed.")

        try:
            logging.info("Executing SQL: %s", sql)
            result = await _music_query_service.execute_sql_statement(sql)
            return result  # List of dicts (JSON)
        except Exception as e:
            logging.exception("Error executing SQL")
            raise Exception(f"Error executing SQL: {str(e)}")


# Create schema and router
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

router = graphql_app  # Export router for FastAPI
