import os
from typing import Any, List, Dict
from llama_cpp import Llama, LLAMA_POOLING_TYPE_NONE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../../../../models'))

_text_encoder=Llama(
    model_path=os.path.join(MODEL_DIR, 'bge-small-en-v1.5-q4_k_m.gguf'),
    embedding=True,
    verbose=False
)

_text_generator=Llama(
    model_path=os.path.join(MODEL_DIR, 'Phi-3.5-mini-instruct-Q6_K_L.gguf'),
    verbose=False,
    temperature=0,
    pooling_type=LLAMA_POOLING_TYPE_NONE,
    n_ctx=2048
)

class LlamaModel:
    """LlamaModel for query processing"""
    def __init__(self):
        self._text_generator=_text_generator
        self._text_encoder=_text_encoder

    def embed_query(self, query: str) -> List[float]:
        """Converts a natural language query into an embedding vector"""
        return self._text_encoder.embed(query)

    def generate_sql(self, query: str) -> str:
        """Generates SQL statement from a natural language query"""
        # In production, you would use a fine-tuned LLM or rule-based NLP parser
        return f"SELECT * FROM album WHERE title ILIKE 'pull up'"  # Example logic

    def synthesise_sql_result(self, query: str, result_set: List[Dict[str, Any]]) -> Any:
        """Converts raw SQL results into a user-friendly format"""
        # Could format results or apply further processing
        return {
            "query": query,
            "results": result_set
        }
