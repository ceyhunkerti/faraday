from pydantic import BaseSettings, AnyUrl, parse_obj_as


class RedisSettings(BaseSettings):
    """Redis settings for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "REDIS_"

    URL: AnyUrl = parse_obj_as(AnyUrl, "redis://localhost:6379/0")
    """A Redis connection URL."""
    DB: int | None = None
    """Redis DB ID (optional)"""
    PORT: int | None = None
    """Redis port (optional)"""
    SOCKET_CONNECT_TIMEOUT: int = 5
    """Length of time to wait (in seconds) for a connection to become
    active."""
    HEALTH_CHECK_INTERVAL: int = 5
    """Length of time to wait (in seconds) before testing connection health."""
    SOCKET_KEEPALIVE: int = 5
    """Length of time to wait (in seconds) between keepalive commands."""
