from typing import Optional
from app.models import Package
from app.lib import package as libp
from faker import Faker
import random

fake = Faker()


def gen_package(
    cnt: Optional[int] = -1, skip_install: Optional[bool] = False
) -> list[Package]:
    package_count = random.randint(1, 10) if not cnt or cnt <= -1 else cnt
    names = fake.words(package_count, unique=True)

    packages = []
    for n in names:
        package = {"name": n}
        packages.append(libp.add(**package, skip_install=True))

    return packages  # type: ignore
