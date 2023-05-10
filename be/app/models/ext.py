from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON

from .base import Base

if TYPE_CHECKING:
    from .package import Package


class Extraction(Base):
    __tablename__ = "extractions"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    source_package: Mapped[Package] = relationship(
        "Package", back_populates="as_source"
    )
    source_config: Mapped[JSON] = mapped_column("source_config", JSON(), nullable=True)

    target_package: Mapped[Package] = relationship(
        "Package", back_populates="as_target"
    )
    target_config: Mapped[JSON] = mapped_column("target_config", JSON(), nullable=True)


class ExtractionSchema(BaseModel):
    id: int
    name: str
    source_package_id: int
    source_config: str
    target_package_id: int
    target_config: str

    class Config:
        orm_mode = True


ExtractionSchema.update_forward_refs()
