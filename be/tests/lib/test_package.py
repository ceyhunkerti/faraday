from app.lib import package as lib
from app import models
from unittest.mock import patch
from tests.utils import get_session
from sqlalchemy.orm import Session


@patch("app.lib.package.get_session", get_session)
def test_add(session: Session) -> None:
    packages = [
        {
            "name": "target-gsheet",
            "title": "test tap title 1",
            "config": {"x": "y"},
        },
        {
            "name": "tap-bing-ads",
            "title": "test tap title 2",
            "config": {"a": "b"},
        },
    ]

    for package in packages:
        lib.add(**package)  # type: ignore

    for pe in packages:
        pg = models.Package.one_by_name(session=session, name=pe["name"])  # type: ignore
        assert pg is not None, f"{pe['name']} not found!"
        assert pg.name == pe["name"]
        assert pg.title == pe["title"]
        assert pg.config == pe["config"]


@patch("app.lib.package.get_session", get_session)
def test_remove(session: Session) -> None:
    packages = [
        {
            "name": "target-gsheet",
            "title": "test tap title 1",
            "config": {"x": "y"},
        },
        {
            "name": "tap-bing-ads",
            "title": "test tap title 2",
            "config": {"a": "b"},
        },
    ]

    for package in packages:
        lib.add(**package)  # type: ignore

    for package in packages:
        lib.remove(name=package["name"])  # type: ignore

    for pe in packages:
        pg = models.Package.one_by_name(session=session, name=pe["name"])  # type: ignore
        assert pg is None, f"{pe['name']} not removed!"
