from typing import Generator
import pytest
import app.settings as settings
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import models
from tests.utils import get_session
from sqlalchemy import create_engine
from tempfile import TemporaryDirectory
from logging import getLogger
import subprocess
import os

logger = getLogger(__name__)


@pytest.fixture(scope="session", autouse=False)
def venv() -> Generator:
    with TemporaryDirectory(suffix="venv") as tmpdir:
        venv = os.path.join(tmpdir, ".venv")
        subprocess.run(["python3.10", "-m", "venv", venv], check=True)
        yield venv


@pytest.fixture(scope="session", autouse=False)
def pip_bin(venv: str) -> Generator:
    bin = os.path.join(venv, "bin/pip")
    yield bin


@pytest.fixture(scope="session", autouse=False)
def venv_bin(venv: str) -> Generator:
    bin = os.path.join(venv, "bin")
    yield bin


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator:
    url = settings.db.URL

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


@pytest.fixture
def session() -> Generator:
    with get_session() as session:
        yield session
