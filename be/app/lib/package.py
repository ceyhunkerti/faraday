from typing import Optional
from app import models
import subprocess
import logging
from app.settings import settings
import os

pip_bin = os.path.join(settings.VENV_HOME, "bin/pip")

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
    if models.Package.one_by_name(name):
        logger.warning(f"{name} already exists!")
        return None
    else:
        install(url if url else name)
        logger.debug("registering package ...")
        package = models.Package.create(
            name=name,
            title=title,
            config=config,
            url=url,
        )
        logger.info(f"{name} installed")
        return package


def remove(name: str) -> Optional[models.Package]:
    if not (package := models.Package.one_by_name(name)):
        logger.warning(f"{name} not installed")
        return None
    else:
        uninstall(name)
        logger.debug("un-registering package ...")
        package.delete()
        return package
