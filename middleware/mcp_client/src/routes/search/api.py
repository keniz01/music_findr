from fastapi import APIRouter, Depends
from src.routes.search.search_handler import SearchHandler
from src.models.search_query_request import SearchQueryRequest
from src.models.api_response import ApiResponse

def get_search_handler():
    # Here you can return a singleton, or inject services if needed
    return SearchHandler()


router = APIRouter(prefix="/api")

@router.post(
    "/search",
    summary="Search By User Query.",
    description="Retrieves records matching user query.",
    response_model=ApiResponse[str]
)
async def search_by_query(
    request: SearchQueryRequest,
    handler: SearchHandler = Depends(get_search_handler)
) -> ApiResponse[str]:
    return await handler.search_by_query(request)


# Export the router
search_router = router
