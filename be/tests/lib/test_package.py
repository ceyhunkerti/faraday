import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib import package as lib
from app import models


@pytest.mark.asyncio
async def test_add_success(session: AsyncSession) -> None:
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
