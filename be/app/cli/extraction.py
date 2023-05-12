from typing import Optional
import click
from .coro import coro
from app.lib import extraction as lib
from app import util


@click.group()
def extraction():
    "extraction commands"


@extraction.command()
@coro
@click.argument("name")
@click.argument("source")
@click.option("-s", "--source-config", required=False)
@click.argument("target")
@click.option("-t", "--target-config", required=False)
async def add(
    name: str,
    source_package: str,
    source_config: Optional[str],
    target_package: str,
    target_config: Optional[str],
) -> None:
    await lib.add(
        name=name,
        source_package=source_package,
        source_config=util.json_config(source_config),
        target_package=target_package,
        target_config=util.json_config(target_config),
    )


@extraction.command()
@coro
@click.argument("name")
async def remove(name: str) -> None:
    await lib.remove(name=name)
