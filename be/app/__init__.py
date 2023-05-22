from app.app import create_app
from app.log import setup_logging


setup_logging()

__all__ = ["create_app"]
