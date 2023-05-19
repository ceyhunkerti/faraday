from contextlib import contextmanager
import logging
from typing import Generator, Optional

from app import models
from app.exceptions import (
    PackageNotFoundError,
    ExtractionNotFoundError,
    StateUpdateError,
)
from tempfile import NamedTemporaryFile
import json
import subprocess
from app.settings import settings
import os

venv_bin: str = os.path.join(settings.VENV_HOME, "bin")
logger = logging.getLogger(__name__)


def add(
    name: str,
    source_package: str,
    target_package: str,
    source_config: Optional[dict] = None,
    target_config: Optional[dict] = None,
) -> Optional[models.Extraction]:
    if extraction := models.Extraction.one_by_name(name=name):
        logger.warning(f"{name} already exists!")
        return None

    source_package_model = models.Package.one_by_name(name=source_package)
    if not source_package_model:
        logger.error(f"{source_package} not found in packages!")
        raise PackageNotFoundError(source_package)

    target_package_model = models.Package.one_by_name(name=target_package)
    if not target_package_model:
        logger.error(f"{target_package} not found in packages!")
        raise PackageNotFoundError(target_package)

    extraction = models.Extraction.create(
        name=name,
        source_package_id=source_package_model.id,
        source_config=source_config,
        target_package_id=target_package_model.id,
        target_config=target_config,
    )
    return extraction


def remove(name: str) -> Optional[models.Extraction]:
    if not (extraction := models.Extraction.one_by_name(name=name)):
        logger.warning(f"extraction {name} not found")
        return None
    else:
        extraction.delete()
        return extraction


@contextmanager
def _tmp_files(
    extraction: models.Extraction,
    source_config: Optional[dict] = None,
    target_config: Optional[dict] = None,
) -> Generator:
    source_package = extraction.source_package
    target_package = extraction.target_package

    sc = (
        source_config or extraction.source_config or source_package.config or {}  # type: ignore
    )
    tc = (
        target_config or extraction.target_config or target_package.config or {}  # type: ignore
    )
    with NamedTemporaryFile(mode="w", suffix=".json") as scf, NamedTemporaryFile(
        mode="w", suffix=".json"
    ) as tcf, NamedTemporaryFile(mode="w", suffix=".json") as sf:

        def w_config(f, c, tag="source"):
            config_text = json.dumps(c)
            logger.debug("%s config: %s", tag, config_text)
            f.write(config_text)
            f.flush()

        w_config(scf, sc)
        w_config(tcf, tc, "target")

        yield scf, tcf, sf


def run(
    name: str,
    source_config: Optional[dict] = None,
    target_config: Optional[dict] = None,
) -> None:
    if not (extraction := models.Extraction.one_by_name(name=name)):
        raise ExtractionNotFoundError(name)
    source_package = extraction.source_package
    target_package = extraction.target_package

    s_config = (
        source_config or extraction.source_config or source_package.config or {}  # type: ignore
    )
    t_config = (
        target_config or extraction.target_config or target_package.config or {}  # type: ignore
    )

    with _tmp_files(extraction, s_config, t_config) as (
        source_config_file,
        target_config_file,
        state_file,
    ):
        source_bin = os.path.join(venv_bin, source_package.name)
        target_bin = os.path.join(venv_bin, target_package.name)

        scf = f"--config {source_config_file.name}"
        tcf = f"--config {target_config_file.name}"

        command = f"{source_bin} {scf} | {target_bin} {tcf} > {state_file.name}"
        logger.info(command)

        try:
            _ = subprocess.run(command, shell=True, check=True)
            logger.info("Command executed successfully!")
        except subprocess.CalledProcessError as e:
            logger.error("Command execution failed.")
            raise e

        try:
            with open(state_file.name, "r") as sf:
                state = json.loads(sf.read())
                extraction.update_state(state=state)
        except Exception as e:
            logger.error(e)
            raise StateUpdateError(name)
