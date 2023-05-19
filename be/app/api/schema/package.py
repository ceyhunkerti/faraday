from typing import Optional
from pydantic import BaseModel


class PackageSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    url: Optional[str]
    config: Optional[dict]

    class Config:
        orm_mode = True
