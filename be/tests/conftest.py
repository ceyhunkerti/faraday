from typing import AsyncGenerator, Generator
import pytest
import app.settings as settings
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import models
from tests.utils import get_async_session
from sqlalchemy import create_engine

import pytest_asyncio
from logging import getLogger

logger = getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator:
    url = settings.db.URL.replace("+asyncpg", "")

    engine = create_engine(url)
    conn = engine.connect()

    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError as e:
        logger.info(e)
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

    engine = create_engine(url)
    conn = engine.connect()
    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError as e:
        logger.error(e)
    finally:
        conn.execute(text("commit"))
        conn.close()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator:
    async with get_async_session() as session:
        yield session
