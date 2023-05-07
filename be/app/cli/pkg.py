import click
from app.lib import pkg as lib
from .coro import coro


@click.group()
def pkg():
    "package commands"


@pkg.command()
@coro
@click.argument("name_or_url", required=True)
async def add(name_or_url: str) -> None:
    await lib.add(name_or_url)


@pkg.command()
@coro
@click.argument("name_or_url", required=True)
async def remove(name_or_url: str) -> None:
    await lib.remove(name_or_url)
