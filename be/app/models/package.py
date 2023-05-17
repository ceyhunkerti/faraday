from __future__ import annotations
from typing import Iterator, Optional

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import select, JSON


from .base import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column("title", String(length=128), nullable=True)
    config: Mapped[JSON] = mapped_column("config", JSON())
    url: Mapped[str] = mapped_column("url", String(length=512), nullable=True)

    as_source = relationship(
        "Extraction",
        foreign_keys="[Extraction.source_package_id]",
        back_populates="source_package",
        cascade="delete, delete-orphan",
    )
    as_target = relationship(
        "Extraction",
        foreign_keys="[Extraction.target_package_id]",
        back_populates="target_package",
        cascade="delete, delete-orphan",
    )

    @classmethod
    def one(cls, session: Session, id: int) -> Optional["Package"]:
        stmt = select(cls).filter_by(id=id)
        return session.scalar(stmt)

    @classmethod
    def one_by_name(cls, session: Session, name: str) -> Optional["Package"]:
        stmt = select(cls).filter_by(name=name)
        return session.scalar(stmt)

    @classmethod
    def all(cls, session: Session, name: str) -> Iterator["Package"]:
        stmt = select(cls)
        for row in session.scalars(stmt.order_by(cls.name)):
            yield row

    @classmethod
    def create(
        cls,
        session: Session,
        name: str,
        title: Optional[str] = None,
        config: Optional[dict] = None,
        url: Optional[str] = None,
    ) -> "Package":
        package = cls(name=name, title=title, config=config, url=url)
        session.add(package)
        session.flush()
        return package

    def delete(self, session: Session) -> "Package":
        session.delete(self)
        session.flush()
        return self


class PackageSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    config: Optional[dict]

    class Config:
        orm_mode = True
