from functools import lru_cache
import pkgutil
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Optional
import json


@lru_cache
def module_to_os_path(dotted_path: str = "app") -> Path:
    """Find Module to OS Path.

    Return path to the base directory of the project or the module
    specified by `dotted_path`.

    Ensures that pkgutil returns a valid source file loader.
    """
    src = pkgutil.get_loader(dotted_path)
    if not isinstance(src, SourceFileLoader):
        raise TypeError("Couldn't find the path for %s", dotted_path)
    return Path(str(src.path).removesuffix("/__init__.py"))


def json_config(path_or_config: Optional[str]) -> Optional[dict]:
    val = None
    if not path_or_config:
        return None
    elif Path(path_or_config).is_file():
        with open(path_or_config) as f:
            val = f.read()
    else:
        val = path_or_config

    if val:
        return json.loads(val)
    return None
