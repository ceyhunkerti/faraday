from typing import Optional
from app import models
from app.db import get_session
import subprocess
import logging
from app import settings
import os

pip_bin = os.path.join(settings.app.VENV_HOME, "bin/pip")

logger = logging.getLogger(__name__)


def install(name: str) -> None:
    try:
        logger.info(f"installing package {name} ...")
        output = subprocess.check_output(
            [pip_bin, "install", name],
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


def add(
    name: str,
    title: Optional[str] = None,
    config: Optional[dict] = None,
    url: Optional[str] = None,
) -> Optional[models.Package]:
    with get_session() as session:
        if models.Package.one_by_name(session, name):
            logger.warning(f"{name} already exists!")
            return None
        else:
            install(url if url else name)
            logger.debug("registering package ...")
            package = models.Package.create(
                session=session,
                name=name,
                title=title,
                config=config,
                url=url,
            )
            session.commit()
            logger.info(f"{name} installed")
            return package


def remove(name: str) -> Optional[models.Package]:
    with get_session() as session:
        if not (package := models.Package.one_by_name(session, name)):
            logger.warning(f"{name} not installed")
            return None
        else:
            uninstall(name)
            logger.debug("un-registering package ...")
            package.delete(session=session)
            session.commit()
            return package
