from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload, Session

from .base import Base

if TYPE_CHECKING:
    from .package import Package


class Extraction(Base):
    __tablename__ = "extractions"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    source_package_id: Mapped[int] = mapped_column(
        "source_package_id", ForeignKey("packages.id"), nullable=False
    )
    source_package: Mapped[Package] = relationship(
        "Package",
        back_populates="as_source",
        foreign_keys=[source_package_id],
    )
    source_config: Mapped[JSON] = mapped_column("source_config", JSON(), nullable=True)

    target_package_id: Mapped[int] = mapped_column(
        "target_package_id", ForeignKey("packages.id"), nullable=False
    )
    target_package: Mapped[Package] = relationship(
        "Package", back_populates="as_target", foreign_keys=[target_package_id]
    )
    target_config: Mapped[JSON] = mapped_column("target_config", JSON(), nullable=True)

    state: Mapped[JSON] = mapped_column("state", JSON(), nullable=True)

    @classmethod
    def one_by_name(cls, session: Session, name: str) -> Optional["Extraction"]:
        stmt = (
            select(cls)
            .filter_by(name=name)
            .options(selectinload(Extraction.source_package))
            .options(selectinload(Extraction.target_package))
        )
        return session.scalar(stmt)

    @classmethod
    def create(
        cls,
        session: Session,
        name: str,
        source_package_id: int,
        source_config: Optional[dict],
        target_package_id: int,
        target_config: Optional[dict],
    ) -> "Extraction":
        extraction = cls(
            name=name,
            source_package_id=source_package_id,
            source_config=source_config,
            target_package_id=target_package_id,
            target_config=target_config,
        )
        session.add(extraction)
        session.flush()
        return extraction

    def delete(self, session: Session) -> "Extraction":
        session.delete(self)
        session.flush()
        return self


class ExtractionSchema(BaseModel):
    id: int
    name: str
    source_package_id: int
    source_config: str
    target_package_id: int
    target_config: str

    class Config:
        orm_mode = True
