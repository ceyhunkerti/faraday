from typing import Optional
import click
from .coro import coro


@click.group()
def ext():
    "extraction commands"


@ext.command()
@coro
@click.argument("name")
@click.argument("source")
@click.option("-s", "--source-config", required=False)
@click.argument("target")
@click.option("-t", "--target-config", required=False)
async def add(
    name: str,
    source: str,
    source_config: Optional[str],
    target: str,
    target_config: Optional[str],
) -> None:
    print(name)
    print(source)
    print(source_config)
    print(target)
    print(target_config)
