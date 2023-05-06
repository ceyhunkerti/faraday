import click

from .db import db


@click.group()
def app():
    "faraday"


@app.command()
def start() -> None:
    print("hello")


app.add_command(db)
