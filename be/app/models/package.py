from __future__ import annotations

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[str] = mapped_column("title", String(length=128), nullable=True)

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


class PackageSchema(BaseModel):
    id: int
    title: str
    name: str

    class Config:
        orm_mode = True


PackageSchema.update_forward_refs()
