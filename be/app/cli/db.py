import click
from app.lib.db import init as init_db, drop as drop_db

from .coro import coro
from app.db.base import async_engine


@click.group()
def db():
    "database commands"


@db.command()
@coro
async def init() -> None:
    async with async_engine.connect() as conn:
        await init_db(conn)
        await conn.commit()


@db.command()
@coro
async def drop() -> None:
    async with async_engine.connect() as conn:
        await drop_db(conn)
        await conn.commit()
