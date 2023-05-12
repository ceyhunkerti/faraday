import logging
from typing import Optional

from app import models
from app.db.base import get_async_session

logger = logging.getLogger(__name__)


async def add(
    name: str,
    source_package: str,
    source_config: Optional[dict],
    target_package: str,
    target_config: Optional[dict],
) -> Optional[models.Extraction]:
    async with get_async_session() as session:
        if await models.Extraction.one_by_name(session, name=name):
            logger.warning(f"{name} already exists!")
            return None

        source_package_model = await models.Package.one_by_name(
            session=session, name=source_package
        )
        if not source_package_model:
            logger.error(f"{source_package} not found in packages!")
            raise Exception("package not found!")

        target_package_model = await models.Package.one_by_name(
            session=session, name=target_package
        )
        if not target_package_model:
            logger.error(f"{target_package} not found in packages!")
            raise Exception("package not found!")

        extraction = await models.Extraction.create(
            session=session,
            name=name,
            source_package_id=source_package_model.id,
            source_config=source_config,
            target_package_id=target_package_model.id,
            target_config=target_config,
        )
        await session.commit()
        return extraction


async def remove(name: str) -> Optional[models.Extraction]:
    async with get_async_session() as session:
        if not (extraction := await models.Extraction.one_by_name(session, name=name)):
            logger.warning(f"extraction {name} not found")
            return None
        else:
            await extraction.delete(session=session)
            await session.commit()
            return extraction
