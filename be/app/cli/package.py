from typing import Optional
import click
from app.lib import package as lib
from app import util
from flask.cli import AppGroup
from app.registry import PACKAGES

manager = AppGroup(help="Package management commands")


@manager.command()
@click.argument("name", required=True)
@click.argument("title", required=False, type=str)
@click.option("--default-config", required=False, type=str)
@click.option("--url", required=False, type=str)
def add(
    name: str,
    title: Optional[str] = None,
    default_config: Optional[str] = None,
    url: Optional[str] = None,
) -> None:
    lib.add(
        name,
        title=title,
        config=util.json_config(default_config),
        url=url,
    )


@manager.command()
@click.argument("name", required=True)
def remove(name: str) -> None:
    lib.remove(name)


@manager.command(name="list")
def list_packages():
    for p in PACKAGES:
        click.echo("\n" + "- " + str(p))
