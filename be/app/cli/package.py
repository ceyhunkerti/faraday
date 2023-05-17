from typing import Optional
import click
from app.lib import package as lib
from .coro import coro
from app import util


@click.group()
def package():
    "package commands"


@package.command()
@coro
@click.argument("name", required=True)
@click.argument("title", required=False, type=str)
@click.option("--default-config", required=False, type=str)
@click.option("--url", required=False, type=str)
async def add(
    name: str,
    title: Optional[str] = None,
    default_config: Optional[str] = None,
    url: Optional[str] = None,
) -> None:
    await lib.add(
        name,
        title=title,
        config=util.json_config(default_config),
        url=url,
    )


@package.command()
@coro
@click.argument("name", required=True)
async def remove(name: str) -> None:
    await lib.remove(name)
