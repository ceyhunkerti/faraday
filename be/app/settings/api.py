from pydantic import BaseSettings


class APISettings(BaseSettings):
    """API specific configuration."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "API_"

    CACHE_EXPIRATION: int = 60
    """Default cache key expiration in seconds."""
    DB_SESSION_DEPENDENCY_KEY: str = "db_session"
    """Parameter name for SQLAlchemy session dependency injection."""
    DEFAULT_PAGINATION_LIMIT: int = 100
    """Max records received for collection routes."""
    DTO_INFO_KEY: str = "dto"
    """Key used for DTO field config in SQLAlchemy info dict."""
    HEALTH_PATH: str = "/health"
    """Route that the health check is served under."""
