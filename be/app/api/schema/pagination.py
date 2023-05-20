from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PageQueryParams(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 20


class Pagination(BaseModel, Generic[T]):
    query: str
    total: int
    page: int
    per_page: int
    items: List[T]
