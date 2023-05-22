from typing import Optional
from pydantic import BaseModel


class PackageOutSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    url: Optional[str]
    config: Optional[dict]
    installed: bool = False

    class Config:
        orm_mode = True
