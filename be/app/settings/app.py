from pydantic import BaseSettings, SecretBytes, validator
from pathlib import Path
from typing import Final
from app import utils
import binascii
import os

DEFAULT_MODULE_NAME = "app"
BASE_DIR: Final = utils.module_to_os_path(DEFAULT_MODULE_NAME)
STATIC_DIR = Path(BASE_DIR / "domain" / "web" / "public")


class AppSettings(BaseSettings):
    """Generic application settings.

    These settings are returned as json by the healthcheck endpoint, so
    do not include any sensitive values here, or if you do ensure to
    exclude them from serialization in the `Config` object.
    """

    class Config:
        case_sensitive = True
        env_file = ".env"

    BUILD_NUMBER: str = ""
    """Identifier for CI build."""
    CHECK_DB_READY: bool = True
    """Check for database readiness on startup."""
    CHECK_REDIS_READY: bool = True
    """Check for redis readiness on startup."""
    DEBUG: bool = False
    """Run `Litestar` with `debug=True`."""
    ENVIRONMENT: str = "prod"
    """'dev', 'prod', etc."""
    TEST_ENVIRONMENT_NAME: str = "test"
    """Value of ENVIRONMENT used to determine if running tests.

    This should be the value of `ENVIRONMENT` in `tests.env`.
    """
    LOCAL_ENVIRONMENT_NAME: str = "local"
    """Value of ENVIRONMENT used to determine if running in local development
    mode.

    This should be the value of `ENVIRONMENT` in your local `.env` file.
    """
    NAME: str = "app"
    """Application name."""
    SECRET_KEY: SecretBytes
    """Number of HTTP Worker processes to be spawned by Uvicorn."""
    JWT_ENCRYPTION_ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    STATIC_URL: str = "/static/"
    CSRF_COOKIE_NAME: str = "csrftoken"
    CSRF_COOKIE_SECURE: bool = False
    """Default URL where static assets are located."""
    STATIC_DIR: Path = STATIC_DIR
    DEV_MODE: bool = False

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            `self.NAME`, all lowercase and hyphens instead of spaces.
        """
        return "-".join(s.lower() for s in self.NAME.split())

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str] | str:
        """Parse a list of origins."""
        if isinstance(value, list):
            return value
        if isinstance(value, str) and not value.startswith("["):
            return [host.strip() for host in value.split(",")]
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            return list(value)
        raise ValueError(value)

    @validator("SECRET_KEY", pre=True, always=True)
    def generate_secret_key(cls, value: SecretBytes | None) -> SecretBytes:
        """Generate a secret key."""
        if value is None:
            return SecretBytes(binascii.hexlify(os.urandom(32)))
        return value
