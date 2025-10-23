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

    def generate_sql(self, query: str, schema:str) -> str:
        """Generates SQL statement from a natural language query"""
        prompt=f"""<|system|>You must use the context to generate a correct Postgres SQL statement to answer the question at the end.
Strictly only use table and column names defined in the context and you must use table and column aliases.
If the question does not make sense or you dont know the answer just say "I dont know".
You must only return valid SQL - do not explain, advice or assume.<|end|>
<|user|>
Count albums distributed by record label 'Greenesleeves'<|end|>
<|assistant|>
select count(a.*) album_count 
from album a 
inner join record_label rl on rl.label_id = a.label_id 
where rl.label_name ILIKE 'Greensleeves Records';<|end|>
<|user|>
How many albums does the recording artist 'Gregory Isaacs' have?<|end|>
<|assistant|>
SELECT COUNT(al.*) 
FROM album al;<|end|>
<|user|>
Show all tracks on the album 'Soca Xplosion 2007' have?<|end|>
<|assistant|>
SELECT tr.track_id, tr.title, tr.duration, tr.position, tr.release_year, tr.genre_id, tr.label_id, tr.artist_id, tr.album_id 
FROM track tr
INNER JOIN album al on al.album_id=tr.album_id 
WHERE al.title ILIKE 'Soca Xplosion';<|end|>
<|user|>
Context: {schema}
Question: {query}
<|end|>
<|assistant|>"""
        completion_response=self._text_generator(prompt, max_tokens=2048)
        sql=completion_response["choices"][0]["text"]
        return sql.strip()

    def synthesise_sql_result(self, query: str, result_set: List[Dict[str, Any]]) -> Any:
        """Converts raw SQL results into a user-friendly format"""
        # Could format results or apply further processing
        return {
            "query": query,
            "results": result_set
        }
