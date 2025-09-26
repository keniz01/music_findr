from pydantic import BaseModel

class SearchQueryRequest(BaseModel):
    query: str
