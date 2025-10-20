from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    result: Optional[T] = None
    error: Optional[str] = None

    class Config:
        extra = "forbid"
