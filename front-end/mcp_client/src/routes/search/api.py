from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest
from src.routes.search.search_handler import SearchHandler


def get_search_handler() -> SearchHandler:
    """Get or create a SearchHandler instance"""
    try:
        return SearchHandler()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to initialize search handler: {str(e)}"
        )


router = APIRouter(prefix="/api")


@router.post(
    "/search",
    summary="Search By Natural Language Query",
    description="Retrieves database records matching the natural language query",
    response_model=ApiResponse[List[Dict[str, Any]]],
)
async def search_by_query(
    request: SearchQueryRequest, handler: SearchHandler = Depends(get_search_handler)
) -> ApiResponse[List[Dict[str, Any]]]:
    """Process natural language search query using MCP server"""
    return await handler.search_by_query(request)


# Export the router
search_router = router
