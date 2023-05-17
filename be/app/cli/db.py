import click
from app.lib.db import init as init_db, drop as drop_db

from app.db import engine


@click.group()
def db():
    "database commands"


@db.command()
def init() -> None:
    with engine.connect() as conn:
        init_db(conn)
        conn.commit()


@db.command()
def drop() -> None:
    with engine.connect() as conn:
        drop_db(conn)
        conn.commit()
