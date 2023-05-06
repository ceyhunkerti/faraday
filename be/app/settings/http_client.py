from pydantic import BaseSettings


class HTTPClientSettings(BaseSettings):
    """HTTP Client configurations."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "HTTP_"

    BACKOFF_MAX: float = 60
    BACKOFF_MIN: float = 0
    EXPONENTIAL_BACKOFF_BASE: float = 2
    EXPONENTIAL_BACKOFF_MULTIPLIER: float = 1
