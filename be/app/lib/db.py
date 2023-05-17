import logging
from app import models
import sqlalchemy as sa

logger = logging.getLogger(__name__)


def get_table_names(conn):
    inspector = sa.inspect(conn)
    return inspector.get_table_names()


def is_db_empty(conn):
    return len(get_table_names(conn)) == 0


def init(conn: sa.Connection):
    if is_db_empty(conn):
        models.Base.metadata.create_all(conn.engine)
    else:
        logger.warn("database is not empty!")


def drop(conn: sa.Connection) -> None:
    models.Base.metadata.drop_all(conn.engine)
