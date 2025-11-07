import os
from typing import Any, Dict, List, Optional, Callable, Awaitable, TypeVar
from loguru import logger
from openai import AsyncOpenAI
from utils.llm_prompts import get_sql_prompt, get_summary_prompt
from utils.sql_formatter import SQLFormatter
from functools import wraps

# ---------------------------------------------------------------------
# 🧩 Exception Handling Decorator
# ---------------------------------------------------------------------
def handle_llm_errors(service_name: str):
    """Decorator to wrap LLM service calls with consistent error handling."""
    T = TypeVar("T")
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"{service_name} failed: {e}")
                raise RuntimeError(f"Llama {service_name} unavailable.") from e
        return wrapper
    return decorator

# ---------------------------------------------------------------------
# 🎛️ Configuration
# ---------------------------------------------------------------------
class LlamaConfig:
    """Encapsulates configuration for LlamaService."""

    def __init__(
        self,
        llm_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        client: Optional[AsyncOpenAI] = None
    ):
        self.llm_model = llm_model or "phi-3.5-mini-instruct"
        self.embedding_model = embedding_model or "bge-small-en-v1.5"
        self.client = client or AsyncOpenAI(
            base_url=base_url or os.getenv("LLAMA_API_BASE", "http://localhost:7001/v1"),
            api_key=api_key or os.getenv("LLAMA_API_KEY", "test-api-key")
        )

# ---------------------------------------------------------------------
# 🦙 Main Service
# ---------------------------------------------------------------------
class LlamaService:
    """
    High-level orchestrator for all Llama operations:
      - Text embeddings
      - SQL generation
      - SQL summarization
    """

    def __init__(
        self,
        config: LlamaConfig,
        sql_formatter: Callable[[str], SQLFormatter],
    ):
        self._config = config
        self._sql_formatter = sql_formatter
        self._client = config.client

    # -----------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------
    async def close(self):
        """Cleanly close the underlying API client."""
        try:
            await self._client.aclose()
            logger.info("LlamaService closed successfully.")
        except Exception as e:
            logger.warning(f"Error closing LlamaService client: {e}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    # -----------------------------------------------------------------
    # Embedding
    # -----------------------------------------------------------------
    @handle_llm_errors("embedding")
    async def embed_query(self, query: str) -> List[float]:
        """Convert text into an embedding vector."""
        logger.info(f"Embedding query: '{query[:80]}...'")
        logger.info(f"Embedding model: '{self._config.embedding_model}'")

        response = await self._client.embeddings.create(
            model=self._config.embedding_model,
            input=query
        )

        if not response.data or not response.data[0].embedding:
            raise ValueError("No embedding data returned from model.")

        embedding = response.data[0].embedding
        logger.debug(f"Embedding generated (len={len(embedding)})")
        return embedding

    # -----------------------------------------------------------------
    # SQL Generation
    # -----------------------------------------------------------------
    @handle_llm_errors("SQL generation")
    async def generate_sql(self, query: str, schema: Dict[str, Any]) -> str:
        """Generate an SQL statement from a natural language query."""
        logger.info(f"Generating SQL for: '{query[:80]}...'")

        messages = get_sql_prompt(schema, query)
        logger.debug(f"SQL prompt created with {len(messages)} messages.")

        response = await self._client.chat.completions.create(
            model=self._config.llm_model,
            messages=messages,
        )

        raw_sql = (
            response.choices[0].message.content.strip()
            if response.choices and response.choices[0].message
            else None
        )
        if not raw_sql:
            raise ValueError("Empty SQL response from model.")

        logger.debug(f"Raw SQL received: {raw_sql}")

        formatted_sql = self._sql_formatter.format(raw_sql)

        logger.info("SQL generation complete.")
        return formatted_sql

    # -----------------------------------------------------------------
    # SQL Summarization
    # -----------------------------------------------------------------
    @handle_llm_errors("SQL summarization")
    async def summarise_sql_result(
        self, user_query: str, sql_response: List[Dict[str, Any]]
    ) -> str:
        """Summarize SQL query results into a natural language response."""
        logger.info("Summarizing SQL results.")
        logger.debug(f"Query: '{user_query[:80]}...', Rows: {len(sql_response)}")

        messages = get_summary_prompt(user_query, sql_response)
        logger.debug(f"Summary prompt created with {len(messages)} messages.")

        response = await self._client.chat.completions.create(
            model=self._config.llm_model,
            messages=messages
        )

        summary = (
            response.choices[0].message.content.strip()
            if response.choices and response.choices[0].message
            else None
        )
        if not summary:
            raise ValueError("Empty summary response from model.")

        logger.info("Summary successfully generated.")
        logger.debug(f"Summary content: {summary}")
        return summary
