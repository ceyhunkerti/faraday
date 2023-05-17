from typing import Any, Literal

from pydantic import (
    BaseSettings,
    PostgresDsn,
    parse_obj_as,
)


class DatabaseSettings(BaseSettings):
    """Configures the database for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "DB_"

    ECHO: bool = False
    """Enable SQLAlchemy engine logs."""
    ECHO_POOL: bool | Literal["debug"] = False
    """Enable SQLAlchemy connection pool logs."""
    POOL_DISABLE: bool = False
    """Disable SQLAlchemy pooling, same as setting pool to.

    [`NullPool`][sqlalchemy.pool.NullPool].
    """
    POOL_MAX_OVERFLOW: int = 10
    """See [`max_overflow`][sqlalchemy.pool.QueuePool]."""
    POOL_SIZE: int = 5
    """See [`pool_size`][sqlalchemy.pool.QueuePool]."""
    POOL_TIMEOUT: int = 30
    """See [`timeout`][sqlalchemy.pool.QueuePool]."""
    POOL_RECYCLE: int = 300
    POOL_PRE_PING: bool = True
    CONNECT_ARGS: dict[str, Any] = {}
    URL: PostgresDsn = parse_obj_as(
        PostgresDsn,
        "postgresql://app:app@localhost:15432/app",
    )

    DB_ENGINE: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None
    # MIGRATION_CONFIG: str = f"{BASE_DIR}/lib/db/alembic.ini"
    # MIGRATION_PATH: str = f"{BASE_DIR}/lib/db/migrations"
    # MIGRATION_DDL_VERSION_TABLE: str = "ddl_version"
