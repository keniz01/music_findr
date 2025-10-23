from datetime import datetime
from functools import lru_cache
from typing import Any, Dict
from punq import Container

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.models.api_response import ApiResponse
from src.models.search_query_request import SearchQueryRequest
from src.handlers.search_handler import SearchHandler
from src.dependencies.container import ContainerFactory
    
@lru_cache()
def get_container() -> Container:
    return ContainerFactory.create_container()

def get_search_handler() -> SearchHandler:
    try:
        container = get_container()
        return container.resolve(SearchHandler)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize SearchHandler: {str(e)}"
        )

# ✅ API Router with prefix and tags
router = APIRouter(
    prefix="/api"
)

# ✅ Natural language search endpoint
@router.post(
    "/search",
    summary="Search by natural language query",
    description="Retrieves database records matching the provided natural language query.",
    response_model=ApiResponse[Any],
    tags=["Search"]
)
async def search_by_query(
    request: SearchQueryRequest,
    search_handler: SearchHandler = Depends(get_search_handler)
) -> ApiResponse[Any]:
    return await search_handler.search_by_query(request)

# ✅ Health check route
@router.get(
    "/healthz",
    summary="Health Check",
    description="Verifies that the MCP client service is up and running.",
    tags=["Health"]
)
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "MCP Client",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
    )

# ✅ Exported router for FastAPI app
search_router = router
