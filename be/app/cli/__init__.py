import click

from .db import db
from .package import package
from .extraction import extraction


@click.group()
def app():
    "faraday"


@app.command()
def start() -> None:
    print("hello")


app.add_command(db)
app.add_command(package)
app.add_command(extraction)
