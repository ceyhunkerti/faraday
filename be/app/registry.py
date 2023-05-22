from enum import Enum
from typing import Optional


class PackageType(Enum):
    TAP = "tap"
    TARGET = "target"


class Package:
    def __init__(
        self,
        name: str,
        package_type: PackageType,
        title: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.name = name
        self.package_type = package_type
        self.title = title
        self.url = url
        self.installed = False

    def __str__(self) -> str:
        s = f"{self.name} ({self.package_type.value})"
        if self.title:
            s += "\n  " + self.title
        if self.url:
            s += "\n  " + self.url
        return s


PACKAGES: list[Package] = [
    Package(
        name="tap-csv",
        package_type=PackageType.TAP,
        url="git+https://github.com/MeltanoLabs/tap-csv.git",
    ),
    Package(name="target-csv", package_type=PackageType.TARGET),
]


__all__ = ["PACKAGES"]
