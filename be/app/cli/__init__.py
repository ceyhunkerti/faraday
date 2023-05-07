import click

from .db import db
from .pkg import pkg


@click.group()
def app():
    "faraday"


@app.command()
def start() -> None:
    print("hello")


app.add_command(db)
app.add_command(pkg)
