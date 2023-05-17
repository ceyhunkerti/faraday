from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import settings
from contextlib import contextmanager
from typing import Generator


engine = create_engine(
    settings.db.URL,
    pool_pre_ping=True,
    echo=settings.db.ECHO,
    poolclass=NullPool,
)
session_maker = sessionmaker(
    bind=engine,
    autoflush=False,
)


@contextmanager
def get_session() -> Generator:
    with session_maker() as session:
        yield session
