from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import settings
from contextlib import asynccontextmanager
from typing import AsyncGenerator


async_engine = create_async_engine(
    settings.db.URL,
    pool_pre_ping=True,
    echo=settings.db.ECHO,
)
async_session_maker = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
