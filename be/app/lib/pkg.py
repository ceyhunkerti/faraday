from typing import Optional
from app import models
from app.db.base import get_async_session
import subprocess
import logging

logger = logging.getLogger(__name__)


def install(name_or_url: str) -> None:
    try:
        logger.info(f"installing package {name_or_url} ...")
        output = subprocess.check_output(
            [".venv/bin/pip", "install", name_or_url],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    if b"ERROR" in output:
        logger.exception(output)
        logger.error(f"An error occurred while installing {name_or_url}")
        raise Exception("Package install error")
    else:
        logger.info(f"{name_or_url} was installed successfully")


def uninstall(name_or_url: str) -> None:
    try:
        logger.info(f"uninstalling package {name_or_url} ...")
        output = subprocess.check_output(
            [".venv/bin/pip", "uninstall", name_or_url],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    if b"ERROR" in output:
        logger.exception(output)
        logger.error(f"An error occurred while uninstalling {name_or_url}")
        raise Exception("Package install error")
    else:
        logger.info(f"{name_or_url} was uninstalled successfully")


async def add(
    name_or_url: str, title: Optional[str] = None
) -> Optional[models.Package]:
    async with get_async_session() as session:
        if await models.Package.one_by_name(session, name_or_url):
            logger.warning(f"{name_or_url} already exists!")
            return None
        else:
            install(name_or_url)
            logger.debug("registering package ...")
            pkg = await models.Package.create(session, name_or_url, title)
            await session.commit()
            logger.info(f"{name_or_url} installed")
            return pkg


async def remove(name_or_url: str) -> Optional[models.Package]:
    async with get_async_session() as session:
        if not (pkg := await models.Package.one_by_name(session, name_or_url)):
            logger.warning(f"{name_or_url} nor installed")
            return None
        else:
            uninstall(name_or_url)
            logger.debug("un-registering package ...")
            await pkg.delete(session=session)
            await session.commit()
            return pkg