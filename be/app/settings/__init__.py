from typing import Final
from app import util
from pydantic import BaseSettings
from pathlib import Path
from functools import lru_cache
from pydantic import ValidationError

DEFAULT_MODULE_NAME = "app"
BASE_DIR: Final = util.module_to_os_path(DEFAULT_MODULE_NAME)
STATIC_DIR = Path(BASE_DIR / "domain" / "web" / "public")
VENV_HOME = ".venv"


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"

    VENV_HOME: str = VENV_HOME

    SQLALCHEMY_DATABASE_URI: str = "postgresql://app:app@localhost:15432/app"

    LOG_STDOUT: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT = (
        "[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s][%(name)s] %(message)s"
    )


@lru_cache
def load_settings() -> Settings:
    try:
        settings = Settings.parse_obj({})
    except ValidationError as e:
        print("Could not load settings. %s", e)  # noqa: T201
        raise e from e
    return settings


settings = load_settings()


__all__ = ["settings"]
