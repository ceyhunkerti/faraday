from typing import Optional
from app.lib import extraction as lib
from app import util
from flask.cli import AppGroup
import click

manager = AppGroup(help="Extraction management commands")


@manager.command()
@click.argument("name")
@click.argument("source")
@click.option("-s", "--source-config", required=False)
@click.argument("target")
@click.option("-t", "--target-config", required=False)
def add(
    name: str,
    source_package: str,
    source_config: Optional[str],
    target_package: str,
    target_config: Optional[str],
) -> None:
    lib.add(
        name=name,
        source_package=source_package,
        target_package=target_package,
        source_config=util.json_config(source_config),
        target_config=util.json_config(target_config),
    )


@manager.command()
@click.argument("name")
def remove(name: str) -> None:
    lib.remove(name=name)
