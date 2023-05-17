from sqlalchemy.pool import NullPool

from app import settings
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f"{settings.db.URL.rsplit('/app', 1)[0] + '/test'}",
    pool_pre_ping=True,
    echo=settings.db.ECHO,
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
