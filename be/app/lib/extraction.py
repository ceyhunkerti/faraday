import logging
from typing import Optional

from app import models
from app.db import get_async_session
from app.exceptions import PackageNotFoundError, ExtractionNotFoundError
from tempfile import NamedTemporaryFile
import json
import subprocess

logger = logging.getLogger(__name__)


async def add(
    name: str,
    source_package: str,
    target_package: str,
    source_config: Optional[dict] = None,
    target_config: Optional[dict] = None,
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
            raise PackageNotFoundError(source_package)

        target_package_model = await models.Package.one_by_name(
            session=session, name=target_package
        )
        if not target_package_model:
            logger.error(f"{target_package} not found in packages!")
            raise PackageNotFoundError(target_package)

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


async def run(
    name: str,
    source_config: Optional[dict] = None,
    target_config: Optional[dict] = None,
) -> None:
    async with get_async_session() as session:
        if not (extraction := await models.Extraction.one_by_name(session, name=name)):
            raise ExtractionNotFoundError(name)
        source_package = extraction.source_package
        target_package = extraction.target_package

        s_config = (
            source_config or extraction.source_config or source_package.config or {}  # type: ignore
        )
        t_config = (
            target_config or extraction.target_config or target_package.config or {}  # type: ignore
        )

        with NamedTemporaryFile(
            mode="w", suffix=".json"
        ) as source_config_file, NamedTemporaryFile(
            mode="w", suffix=".json"
        ) as target_config_file, NamedTemporaryFile(
            mode="w", suffix=".json"
        ) as state_file:
            source_config_file.write(json.dumps(s_config))
            target_config_file.write(json.dumps(t_config))

            source_bin = f".venv/bin/{source_package.name}"
            target_bin = f".venv/bin/{target_package.name}"

            scf = f"--config {source_config_file.name}"
            tcf = f"--config {target_config_file.name}"

            command = f"{source_bin} {scf} | {target_bin} {tcf} > {state_file.name}"

            try:
                logger.info(command)
                _ = subprocess.run(command, shell=True, check=True)
                logger.info("Command executed successfully!")
            except subprocess.CalledProcessError as e:
                logger.error("Command execution failed.")
                raise e
