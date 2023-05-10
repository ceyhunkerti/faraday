from __future__ import annotations
from typing import Optional

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

    @classmethod
    async def one(cls, session: AsyncSession, id: int) -> Optional["Package"]:
        stmt = select(cls).filter_by(id=id)
        return await session.scalar(stmt)

    @classmethod
    async def one_by_name(cls, session: AsyncSession, name: str) -> Optional["Package"]:
        stmt = select(cls).filter_by(name=name)
        return await session.scalar(stmt)

    as_source: Mapped[list[Extraction]] = relationship(
        "Extraction",
        back_populates="source_package",
        order_by="Extraction.id",
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )
    as_target: Mapped[list[Extraction]] = relationship(
        "Extraction",
        back_populates="target_package",
        order_by="Extraction.id",
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        title: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> "Package":
        pkg = cls(name=name, title=title, config=config)
        session.add(pkg)
        await session.flush()
        return pkg

    async def delete(self, session: AsyncSession) -> "Package":
        await session.delete(self)
        await session.flush()
        return self

    # @classmethod
    # async def read_all(
    #     cls, session: AsyncSession, include_notes: bool
    # ) -> AsyncIterator[Notebook]:
    #     stmt = select(cls)
    #     if include_notes:
    #         stmt = stmt.options(selectinload(cls.notes))
    #     stream = await session.stream_scalars(stmt.order_by(cls.id))
    #     async for row in stream:
    #         yield row

    # @classmethod
    # async def read_by_id(
    #     cls, session: AsyncSession, notebook_id: int, include_notes: bool = False
    # ) -> Optional[Notebook]:
    #     stmt = select(cls).where(cls.id == notebook_id)
    #     if include_notes:
    #         stmt = stmt.options(selectinload(cls.notes))
    #     return await session.scalar(stmt.order_by(cls.id))

    # @classmethod
    # async def create(
    #     cls, session: AsyncSession, title: str, notes: list[Note]
    # ) -> Notebook:
    #     notebook = Notebook(
    #         title=title,
    #         notes=notes,
    #     )
    #     session.add(notebook)
    #     await session.flush()
    #     # To fetch notes
    #     new = await cls.read_by_id(session, notebook.id, include_notes=True)
    #     if not new:
    #         raise RuntimeError()
    #     return new

    # async def update(
    #     self, session: AsyncSession, title: str, notes: list[Note]
    # ) -> None:
    #     self.title = title
    #     self.notes = notes
    #     await session.flush()

    # @classmethod
    # async def delete(cls, session: AsyncSession, notebook: Notebook) -> None:
    #     await session.delete(notebook)
    #     await session.flush()


from .ext import Extraction  # noqa: E402


class PackageSchema(BaseModel):
    id: int
    name: str
    title: Optional[str]
    config: Optional[dict]

    class Config:
        orm_mode = True


PackageSchema.update_forward_refs()
