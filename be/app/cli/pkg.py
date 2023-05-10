from typing import Optional
import click
from app.lib import pkg as lib
from .coro import coro
from pathlib import Path
import json


@click.group()
def pkg():
    "package commands"


def _json_config(path_or_config: Optional[str]) -> Optional[dict]:
    val = None
    if not path_or_config:
        return None
    elif Path(path_or_config).is_file():
        with open(path_or_config) as f:
            val = f.read()
    else:
        val = path_or_config

    if val:
        return json.loads(val)
    return None


@pkg.command()
@coro
@click.argument("name_or_url", required=True)
@click.argument("title", required=False, type=str)
@click.option("--default-config", required=False, type=str)
async def add(
    name_or_url: str, title: Optional[str] = None, default_config: Optional[str] = None
) -> None:
    await lib.add(name_or_url, title=title, config=_json_config(default_config))


@pkg.command()
@coro
@click.argument("name_or_url", required=True)
async def remove(name_or_url: str) -> None:
    await lib.remove(name_or_url)
