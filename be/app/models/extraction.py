from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import JSON, ForeignKey
from .base import Base, db


class Extraction(Base):
    __tablename__ = "extractions"

    id = db.Column(
        db.Integer, autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String, nullable=False, unique=True)

    source_package_id = db.Column(db.Integer, ForeignKey("packages.id"), nullable=False)
    source_package = db.relationship(
        "Package",
        back_populates="__as_source",
        foreign_keys=[source_package_id],
    )
    source_config = db.Column(JSON, nullable=True)

    target_package_id = db.Column(db.Integer, ForeignKey("packages.id"), nullable=False)
    target_package = db.relationship(
        "Package", back_populates="__as_target", foreign_keys=[target_package_id]
    )
    target_config = db.Column(JSON, nullable=True)

    state = db.Column(JSON, nullable=True)

    @classmethod
    def one_by_name(cls, name: str) -> Optional["Extraction"]:
        return (
            cls.query.filter_by(name=name)
            .options(db.selectinload(cls.source_package))
            .options(db.selectinload(cls.target_package))
            .one_or_none()
        )

    @classmethod
    def create(
        cls,
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
        db.session.add(extraction)
        db.session.flush()
        return extraction

    def delete(self) -> "Extraction":
        db.session.delete(self)
        db.session.flush()
        return self

    def update_state(self, state: Optional[dict] = None) -> "Extraction":
        self.state = state or {}
        db.session.commit()
        db.session.flush()
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
