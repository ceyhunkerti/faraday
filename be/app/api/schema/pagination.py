from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PageQueryParams(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 20


class Pagination(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]
