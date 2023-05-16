import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib import package as libp
from app.lib import extraction as lib
from app import models
from unittest.mock import patch
from tests.utils import get_async_session


@patch("app.lib.package.get_async_session", get_async_session)
async def add_packages() -> None:
    packages = [
        {
            "name_or_url": "target-csv",
            "title": "test tap title 1",
            "config": {"x": "y"},
        },
        {
            "name_or_url": "tap-bing-ads",
            "title": "test tap title 2",
            "config": {"a": "b"},
        },
    ]

    for package in packages:
        await libp.add(**package)  # type: ignore


@pytest.mark.asyncio
@patch("app.lib.extraction.get_async_session", get_async_session)
async def test_add(session: AsyncSession) -> None:
    await add_packages()

    await lib.add(
        name="ext-1",
        source_package="tap-bing-ads",
        target_package="target-csv",
    )
    extraction = await models.Extraction.one_by_name(session=session, name="ext-1")  # type: ignore
    assert extraction is not None, "Extraction %s not found" % "ext-1"
    assert extraction.source_package.name == "tap-bing-ads", (
        "source package %s not found" % "tap-bing-ads"
    )
    assert extraction.target_package.name == "target-csv", (
        "target package %s not found" % "target-csv"
    )


@pytest.mark.asyncio
@patch("app.lib.extraction.get_async_session", get_async_session)
async def test_remove(session: AsyncSession) -> None:
    await add_packages()

    await lib.add(
        name="ext-1",
        source_package="tap-bing-ads",
        target_package="target-csv",
    )
    await lib.remove(name="ext-1")

    extraction = await models.Extraction.one_by_name(session=session, name="ext-1")  # type: ignore
    assert extraction is None, "Extraction %s is not removed" % "ext-1"
