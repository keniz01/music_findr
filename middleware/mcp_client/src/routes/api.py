from fastapi import APIRouter
from src.models.search_query_request import SearchQueryRequest
from src.models.api_response import ApiResponse

router = APIRouter()

@router.post("/api/search/", response_model=ApiResponse[str])
async def search_by_query(request: SearchQueryRequest) -> ApiResponse[str]:
    print(f"Received search query: {request.query}")

    if not request.query.strip():
        return ApiResponse(success=False, error="No results found")
    
    return ApiResponse(success=True, result=request.query.strip())
