from sqlalchemy.ext.asyncio import AsyncConnection
import logging
from app import models
import sqlalchemy as sa

logger = logging.getLogger(__name__)


def get_table_names(conn):
    inspector = sa.inspect(conn)
    return inspector.get_table_names()


def is_db_empty(conn):
    return len(get_table_names(conn)) == 0


async def init(conn: AsyncConnection):
    if await conn.run_sync(is_db_empty):
        await conn.run_sync(models.Base.metadata.create_all)
    else:
        logger.warn("database is not empty!")


async def drop(conn: AsyncConnection) -> None:
    await conn.run_sync(models.Base.metadata.drop_all)
