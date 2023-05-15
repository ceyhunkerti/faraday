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
@click.argument("name_or_url", required=True)
@click.argument("title", required=False, type=str)
@click.option("--default-config", required=False, type=str)
async def add(
    name_or_url: str, title: Optional[str] = None, default_config: Optional[str] = None
) -> None:
    await lib.add(name_or_url, title=title, config=util.json_config(default_config))


@package.command()
@coro
@click.argument("name_or_url", required=True)
async def remove(name_or_url: str) -> None:
    await lib.remove(name_or_url)