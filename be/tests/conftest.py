from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator
import pytest
import app.settings as settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text, event
from sqlalchemy.exc import SQLAlchemyError
from app import models
from sqlalchemy.orm import Session, SessionTransaction
from unittest.mock import patch
from sqlalchemy import create_engine
import pytest_asyncio


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator:
    url = settings.db.URL.replace("+asyncpg", "")

    engine = create_engine(url)
    conn = engine.connect()

    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError as e:
        print(e)
    finally:
        conn.execute(text("commit"))
        conn.close()

    conn = engine.connect()
    conn.execute(text("commit"))
    conn.execute(text("create database test"))
    conn.execute(text("grant all privileges on database test to app"))
    conn.close()

    engine = create_engine(url.rsplit("/app", 1)[0] + "/test")
    models.Base.metadata.create_all(engine)

    yield

    conn = engine.connect()
    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError:
        ...
    finally:
        conn.execute(text("commit"))
        conn.close()


# @pytest.fixture
@pytest_asyncio.fixture
async def session() -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(
        f"{settings.db.URL.rsplit('/app', 1)[0] + '/test'}"
    )
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

        @asynccontextmanager
        async def test_get_session() -> AsyncGenerator:
            try:
                async with AsyncSessionLocal() as session:
                    yield session
            except SQLAlchemyError:
                pass

        with patch("app.lib.package.get_async_session", test_get_session):
            yield async_session
            await async_session.close()
            await conn.rollback()
