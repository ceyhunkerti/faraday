from sqlalchemy.orm import Session
from app.lib import package as libp
from app.lib import extraction as lib
from app import models
from unittest.mock import patch
from tests.utils import get_session
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
import glob


@patch("app.lib.package.get_session", get_session)
def add_packages() -> None:
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
        libp.add(**package)  # type: ignore


@patch("app.lib.extraction.get_session", get_session)
def test_add(session: Session, pip_bin: str) -> None:
    with patch("app.lib.package.pip_bin", pip_bin):
        add_packages()

    lib.add(
        name="ext-1",
        source_package="tap-bing-ads",
        target_package="target-gsheet",
    )
    extraction = models.Extraction.one_by_name(session=session, name="ext-1")  # type: ignore
    assert extraction is not None, "Extraction %s not found" % "ext-1"
    assert extraction.source_package.name == "tap-bing-ads", (
        "source package %s not found" % "tap-bing-ads"
    )
    assert extraction.target_package.name == "target-gsheet", (
        "target package %s not found" % "target-gsheet"
    )


@patch("app.lib.extraction.get_session", get_session)
def test_remove(session: Session, pip_bin: str) -> None:
    with patch("app.lib.package.pip_bin", pip_bin):
        add_packages()

    lib.add(
        name="ext-1",
        source_package="tap-bing-ads",
        target_package="target-gsheet",
    )
    lib.remove(name="ext-1")

    extraction = models.Extraction.one_by_name(session=session, name="ext-1")  # type: ignore
    assert extraction is None, "Extraction %s is not removed" % "ext-1"


@patch("app.lib.extraction.get_session", get_session)
@patch("app.lib.package.get_session", get_session)
def test_run(venv_bin: str, pip_bin: str) -> None:
    tap = "tap-csv"
    target = "target-csv"

    with NamedTemporaryFile(mode="w", suffix=".csv") as s1, NamedTemporaryFile(
        mode="w", suffix=".csv"
    ) as s2, TemporaryDirectory() as td, patch(
        "app.lib.package.pip_bin", pip_bin
    ), patch(
        "app.lib.extraction.venv_bin", venv_bin
    ):

        def get_text(content):
            text = [content["columns"]] + content["data"]
            text = "\n".join([",".join(r) for r in text])
            return text

        def write_content(f, content):
            data = get_text(content)
            f.write(data)
            f.flush()

        leads = {
            "columns": ["a", "b"],
            "data": [
                ["1", "xyz"],
                ["2", "klm"],
            ],
        }

        opportunities = {
            "columns": ["x", "y"],
            "data": [
                ["10", "XYZ"],
                ["20", "KLM"],
            ],
        }

        tap_config = {
            "files": [
                {
                    "entity": "leads",
                    "path": s1.name,
                    "keys": leads["columns"],
                    "delimiter": ",",
                },
                {
                    "entity": "opportunities",
                    "path": s2.name,
                    "keys": opportunities["columns"],
                    "delimiter": ",",
                },
            ]
        }

        target_config = {
            "delimiter": "\t",
            "quotechar": "'",
            "output_path_prefix": td + "/",
            "disable_collection": True,
        }

        write_content(s1, leads)
        write_content(s2, opportunities)

        libp.add(
            name=tap,
            config=tap_config,
            url="git+https://github.com/MeltanoLabs/tap-csv.git",
        )
        libp.add(
            name=target,
            config=target_config,
            url="git+https://github.com/MeltanoLabs/target-csv.git",
        )
        lib.add(
            name="csv-to-csv-demo",
            source_package=tap,
            target_package=target,
        )
        lib.run("csv-to-csv-demo")

        leads_name = glob.glob(os.path.join(td, "leads*csv"))[0]
        opportunities_name = glob.glob(os.path.join(td, "opportunities*csv"))[0]
        with open(leads_name, "r") as fl, open(opportunities_name, "r") as fo:
            assert fl.read() == get_text(leads) + "\n", "leads failed"
            assert fo.read() == get_text(opportunities) + "\n", "opportunities failed"
