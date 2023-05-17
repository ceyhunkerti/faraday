from typing import Optional
from app import models
from app.db import get_async_session
import subprocess
import logging

logger = logging.getLogger(__name__)


def install(name: str) -> None:
    try:
        logger.info(f"installing package {name} ...")
        output = subprocess.check_output(
            [".venv/bin/pip", "install", name],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    if (
        b"ERROR" in output
        and b"ERROR: pip's dependency resolver does not currently take into account all the packages that are installed."  # noqa
        not in output
    ):
        logger.exception(output)
        logger.error(f"An error occurred while installing {name}")
        raise Exception("Package install error")
    else:
        logger.info(f"{name} was installed successfully")


def uninstall(name: str) -> None:
    try:
        logger.info(f"uninstalling package {name} ...")
        output = subprocess.check_output(
            [".venv/bin/pip", "uninstall", name],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        output = e.output
    if b"ERROR" in output:
        logger.exception(output)
        logger.error(f"An error occurred while uninstalling {name}")
        raise Exception("Package install error")
    else:
        logger.info(f"{name} was uninstalled successfully")


async def add(
    name: str, title: Optional[str], config: Optional[dict], url: Optional[str] = None
) -> Optional[models.Package]:
    async with get_async_session() as session:
        if await models.Package.one_by_name(session, name):
            logger.warning(f"{name} already exists!")
            return None
        else:
            install(name)
            logger.debug("registering package ...")
            package = await models.Package.create(
                session=session,
                name=name,
                title=title,
                config=config,
                url=url,
            )
            await session.commit()
            logger.info(f"{name} installed")
            return package


async def remove(name: str) -> Optional[models.Package]:
    async with get_async_session() as session:
        if not (package := await models.Package.one_by_name(session, name)):
            logger.warning(f"{name} not installed")
            return None
        else:
            uninstall(name)
            logger.debug("un-registering package ...")
            await package.delete(session=session)
            await session.commit()
            return package
