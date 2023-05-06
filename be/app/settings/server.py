from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    """Server configurations."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "SERVER_"

    APP_LOC: str = "app.asgi:create_app"
    """Path to app executable, or factory."""
    APP_LOC_IS_FACTORY: bool = True
    """Indicate if APP_LOC points to an executable or factory."""
    HOST: str = "localhost"
    """Server network host."""
    KEEPALIVE: int = 65
    """Seconds to hold connections open (65 is > AWS lb idle timeout)."""
    PORT: int = 8000
    """Server port."""
    RELOAD: bool | None = None
    """Turn on hot reloading."""
    RELOAD_DIRS: list[str] = ["src/"]
    """Directories to watch for reloading."""
    HTTP_WORKERS: int | None = None
    """Number of HTTP Worker processes to be spawned by Uvicorn."""
