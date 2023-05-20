from typing import Generator
import pytest
from app.settings import settings
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.models import db
from tests.utils import get_session
from sqlalchemy import create_engine
from tempfile import TemporaryDirectory
from logging import getLogger
import subprocess
import os
from app import create_app
from tests.base import get_test_settings
from flask import Flask


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


@pytest.fixture(autouse=True)
def setup_db() -> Generator:
    url = settings.SQLALCHEMY_DATABASE_URI

    engine = create_engine(url)
    conn = engine.connect()

    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError as e:
        logger.debug(e, exc_info=True)
    finally:
        conn.execute(text("commit"))
        conn.close()

    conn = engine.connect()
    conn.execute(text("commit"))
    conn.execute(text("create database test"))
    conn.execute(text("grant all privileges on database test to app"))
    conn.close()

    test_settings = get_test_settings()
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = test_settings.SQLALCHEMY_DATABASE_URI
    app_ctx = app.app_context()
    app_ctx.push()
    db.session.close()
    db.drop_all()
    db.create_all()

    yield

    db.session.remove()
    engine = create_engine(url)
    conn = engine.connect()
    try:
        conn.execute(text("commit"))
        conn.execute(text("drop database test with (force)"))
    except SQLAlchemyError as e:
        logger.debug(e, exc_info=True)
    finally:
        conn.execute(text("commit"))
        conn.close()


@pytest.fixture(autouse=False)
def app() -> Flask:
    from flask import current_app

    with current_app.app_context():
        yield current_app


@pytest.fixture(autouse=False)
def client(app: Flask) -> Generator:
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=False)
def session() -> Generator:
    with get_session() as session:
        yield session
