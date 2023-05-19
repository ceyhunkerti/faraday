from app.lib import package as lib
from app import models
from unittest.mock import patch


def test_add(pip_bin: str) -> None:
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
    with patch("app.lib.package.pip_bin", pip_bin):
        for package in packages:
            lib.add(**package)  # type: ignore

    for pe in packages:
        pg = models.Package.one_by_name(name=pe["name"])  # type: ignore
        assert pg is not None, f"{pe['name']} not found!"
        assert pg.name == pe["name"]
        assert pg.title == pe["title"]
        assert pg.config == pe["config"]


def test_remove(pip_bin: str) -> None:
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
    with patch("app.lib.package.pip_bin", pip_bin):
        for package in packages:
            lib.add(**package)  # type: ignore

        for package in packages:
            lib.remove(name=package["name"])  # type: ignore

    for pe in packages:
        pg = models.Package.one_by_name(name=pe["name"])  # type: ignore
        assert pg is None, f"{pe['name']} not removed!"
