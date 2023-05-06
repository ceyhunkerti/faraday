import click
from app.utils.db import init as init_db


# from app.db import get_async_session
from .coro import coro
from app.db.base import async_engine
import sqlalchemy as sa


@click.group()
def db():
    "database commands"


def get_table_names(conn):
    inspector = sa.inspect(conn)
    return inspector.get_table_names()


@db.command()
@coro
async def init() -> None:
    await init_db(async_engine)
