from sqlalchemy.ext.asyncio import AsyncEngine

from app import models
import sqlalchemy as sa


def get_table_names(conn):
    inspector = sa.inspect(conn)
    return inspector.get_table_names()


def is_db_empty(conn):
    return len(get_table_names(conn)) == 0


async def init(engine: AsyncEngine):
    async with engine.connect() as conn:
        if await conn.run_sync(is_db_empty):
            await conn.run_sync(models.Base.metadata.create_all)
        else:
            print("DB is not empty")
