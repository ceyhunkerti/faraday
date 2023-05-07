from pydantic import BaseSettings


class LogSettings(BaseSettings):
    """Logging config for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "LOG_"

    STDOUT: bool = False
    LEVEL: str = "INFO"
    FORMAT = "[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s"
