import logging
from app.models import db
import sqlalchemy as sa

logger = logging.getLogger(__name__)


def get_table_names():
    return sa.inspect(db.get_engine()).get_table_names()


def is_db_empty():
    return len(get_table_names()) == 0


def init():
    if is_db_empty():
        sa.orm.configure_mappers()
        db.create_all()
    else:
        logger.warn("database is not empty!")


def drop() -> None:
    db.drop_all()
