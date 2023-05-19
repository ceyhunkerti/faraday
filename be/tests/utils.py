from sqlalchemy.pool import NullPool

from app.settings import settings
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f"{settings.SQLALCHEMY_DATABASE_URI.rsplit('/app', 1)[0] + '/test'}",
    pool_pre_ping=True,
    echo=True,
    poolclass=NullPool,
)
session_maker = sessionmaker(
    bind=engine,
    autoflush=False,
    future=True,
)


@contextmanager
def get_session() -> Generator:
    with session_maker() as session:
        yield session
