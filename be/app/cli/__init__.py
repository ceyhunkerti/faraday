import click
from flask.cli import FlaskGroup, run_command, with_appcontext
from flask import current_app

from . import db, package, extraction
from app import create_app


def create():
    app = current_app or create_app()

    @app.shell_context_processor
    def shell_context():
        from app import models
        from app.settings import settings

        return {"models": models, "settings": settings}

    return app


@click.group(cls=FlaskGroup, create_app=create)
def manager():
    """Management script for App"""


manager.add_command(db.manager, "db")
manager.add_command(package.manager, "package")
manager.add_command(extraction.manager, "extraction")
manager.add_command(run_command, "runserver")


@manager.command("shell")
@with_appcontext
def shell():
    import sys  # noqa
    from ptpython import repl
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    repl.embed(globals=app.make_shell_context())
