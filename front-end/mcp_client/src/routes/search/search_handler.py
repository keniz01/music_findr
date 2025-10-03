from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest

import asyncio

class SearchHandler:
    def __init__(self):
        # Initialize services here (e.g., db, cache, etc.)
        pass

    async def search_by_query(self, request: SearchQueryRequest) -> ApiResponse[str]:
        print(f"Received search query: {request.query}")

        if not request.query.strip():
            return ApiResponse(success=False, error="No results found")

        return ApiResponse(success=True, result=request.query.strip())
    
    async def get_tools(self):
        ...