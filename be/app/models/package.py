from __future__ import annotations
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON


from .base import db, Base


class Package(Base):
    __tablename__ = "packages"

    id = db.Column(
        db.Integer, autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String(length=128), nullable=True)
    config = db.Column(JSON, nullable=True)
    url = db.Column(db.String(length=512), nullable=True)

    as_source = db.relationship(
        "Extraction",
        foreign_keys="[Extraction.source_package_id]",
        back_populates="source_package",
        cascade="delete, delete-orphan",
    )
    as_target = db.relationship(
        "Extraction",
        foreign_keys="[Extraction.target_package_id]",
        back_populates="target_package",
        cascade="delete, delete-orphan",
    )

    @classmethod
    def one(cls, id: int) -> Optional["Package"]:
        return cls.query.one_or_none(id)

    @classmethod
    def one_by_name(cls, name: str) -> Optional["Package"]:
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def all(cls, name: str) -> list["Package"]:
        return cls.query.all()

    @classmethod
    def create(
        cls,
        name: str,
        title: Optional[str] = None,
        config: Optional[dict] = None,
        url: Optional[str] = None,
    ) -> "Package":
        package = cls(name=name, title=title, config=config, url=url)
        db.session.add(package)
        db.session.flush()
        return package

    def delete(
        self,
    ) -> "Package":
        db.session.delete(self)
        db.session.flush()
        return self


class PackageSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    url: Optional[str]
    config: Optional[dict]

    class Config:
        orm_mode = True
