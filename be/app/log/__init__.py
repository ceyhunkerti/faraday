import logging
import sys
from app import settings

__all__ = ["setup_logging"]


def setup_logging():
    handler = logging.StreamHandler(sys.stdout if settings.log.STDOUT else sys.stderr)
    formatter = logging.Formatter(settings.log.FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.log.LEVEL)
