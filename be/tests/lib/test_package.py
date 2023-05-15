import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib import package as lib
from app import models
from unittest.mock import patch
from tests.utils import get_async_session


@pytest.mark.asyncio
@patch("app.lib.package.get_async_session", get_async_session)
async def test_add(session: AsyncSession) -> None:
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
        await lib.add(**package)  # type: ignore

    for pe in packages:
        pg = await models.Package.one_by_name(session=session, name=pe["name_or_url"])  # type: ignore
        assert pg is not None, f"{pe['name_or_url']} not found!"
        assert pg.name == pe["name_or_url"]
        assert pg.title == pe["title"]
        assert pg.config == pe["config"]


@pytest.mark.asyncio
@patch("app.lib.package.get_async_session", get_async_session)
async def test_remove(session: AsyncSession) -> None:
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
        await lib.add(**package)  # type: ignore

    for package in packages:
        await lib.remove(name_or_url=package["name_or_url"])  # type: ignore

    for pe in packages:
        pg = await models.Package.one_by_name(session=session, name=pe["name_or_url"])  # type: ignore
        assert pg is None, f"{pe['name_or_url']} not removed!"
