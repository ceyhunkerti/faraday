import click
from flask.cli import FlaskGroup, run_command, with_appcontext
from flask import current_app

from .db import db
from .package import package
from .extraction import extraction
from app import create_app


def create(group):
    app = current_app or create_app()
    group.app = app

    @app.shell_context_processor
    def shell_context():
        from app import models
        from app.settings import settings

        return {"models": models, "settings": settings}

    return app


@click.group(cls=FlaskGroup, create_app=create)
def app():
    """Management script for the App"""


@app.command()
def start() -> None:
    print("hello")


app.add_command(db)
app.add_command(package)
app.add_command(extraction)
app.add_command(run_command, "runserver")


@app.command("shell")
@with_appcontext
def shell():
    import sys  # noqa
    from ptpython import repl
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    repl.embed(globals=app.make_shell_context())
