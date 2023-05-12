from typing import AsyncGenerator, Generator
import pytest
from app import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text, event
from sqlalchemy.exc import SQLAlchemyError
from app import models
from sqlalchemy.orm import Session, SessionTransaction
from app.db import get_async_session
from app.main import app
from unittest.mock import patch


@pytest.fixture(scope="session", autouse=True)
async def setup_db() -> AsyncGenerator:
    engine = create_async_engine(settings.db.URL)
    async_session_maker = async_sessionmaker(bind=engine)

    async with async_session_maker() as session:
        try:
            await session.execute(text("drop database test"))
        except SQLAlchemyError:
            ...
        finally:
            await session.commit()

        await session.execute(text("create database test"))
        await session.run_sync(models.Base.metadata.create_all)

    yield

    async with async_session_maker() as session:
        try:
            await session.execute(text("drop database test"))
        except SQLAlchemyError:
            ...
        finally:
            await session.commit()


@pytest.fixture
async def session() -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(f"{settings.db.URL}/test")
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_async_session] = test_get_session

        with patch("app.db.base.get_async_session", test_get_session):
            yield async_session
            await async_session.close()
            await conn.rollback()
