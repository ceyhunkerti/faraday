from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import JSON
from sqlalchemy import Enum

from .base import db, Base

if TYPE_CHECKING:
    from .extraction import Extraction


class Package(Base):
    __tablename__ = "packages"

    id = db.Column(
        db.Integer, autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String(length=128), nullable=True)
    config = db.Column(JSON, nullable=True)
    url = db.Column(db.String(length=512), nullable=True)

    package_type = db.Column(Enum("tap", "target", name="package_type"), nullable=False)

    __as_source = db.relationship(
        "Extraction",
        foreign_keys="[Extraction.source_package_id]",
        back_populates="source_package",
        cascade="delete, delete-orphan",
    )
    __as_target = db.relationship(
        "Extraction",
        foreign_keys="[Extraction.target_package_id]",
        back_populates="target_package",
        cascade="delete, delete-orphan",
    )

    @property
    def is_tap(self) -> bool:
        return self.package_type == "tap"

    @property
    def is_target(self) -> bool:
        return self.package_type == "target"

    @property
    def used_in(self) -> list["Extraction"]:
        return self.__as_source if self.is_tap else self.__as_target

    @classmethod
    def one(cls, id: int) -> Optional["Package"]:
        return cls.query.filter_by(id=id).one_or_none()

    @classmethod
    def one_by_name(cls, name: str) -> Optional["Package"]:
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def all(cls) -> list["Package"]:
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
