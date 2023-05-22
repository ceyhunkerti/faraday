from app.lib.db import init as init_db, drop as drop_db
from flask.cli import AppGroup

manager = AppGroup(help="Repository management commands")


@manager.command()
def init() -> None:
    init_db()


@manager.command()
def drop() -> None:
    drop_db()
