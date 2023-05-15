from __future__ import annotations
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    as_source = relationship(
        "Extraction",
        foreign_keys="[Extraction.source_package_id]",
        back_populates="source_package",
    )
    as_target = relationship(
        "Extraction",
        foreign_keys="[Extraction.target_package_id]",
        back_populates="target_package",
    )

    @classmethod
    async def one(cls, session: AsyncSession, id: int) -> Optional["Package"]:
        stmt = select(cls).filter_by(id=id)
        return await session.scalar(stmt)

    @classmethod
    async def one_by_name(cls, session: AsyncSession, name: str) -> Optional["Package"]:
        stmt = select(cls).filter_by(name=name)
        return await session.scalar(stmt)

    @classmethod
    async def all(cls, session: AsyncSession, name: str) -> AsyncIterator["Package"]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.name))
        async for row in stream:
            yield row

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        title: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> "Package":
        package = cls(name=name, title=title, config=config)
        session.add(package)
        await session.flush()
        return package

    async def delete(self, session: AsyncSession) -> "Package":
        await session.delete(self)
        await session.flush()
        return self


class PackageSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    config: Optional[dict]

    class Config:
        orm_mode = True
