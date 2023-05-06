from pydantic import BaseSettings
from litestar.data_extractors import (
    RequestExtractorField,
    ResponseExtractorField,
)  # noqa: TCH002


class LogSettings(BaseSettings):
    """Logging config for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "LOG_"

    # https://stackoverflow.com/a/1845097/6560549
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    """Regex to exclude paths from logging."""
    HTTP_EVENT: str = "HTTP"
    """Log event name for logs from Litestar handlers."""
    INCLUDE_COMPRESSED_BODY: bool = False
    """Include 'body' of compressed responses in log output."""
    LEVEL: int = 20
    """Stdlib log levels.

    Only emit logs at this level, or higher.
    """
    OBFUSCATE_COOKIES: set[str] = {"session"}
    """Request cookie keys to obfuscate."""
    OBFUSCATE_HEADERS: set[str] = {"Authorization", "X-API-KEY"}
    """Request header keys to obfuscate."""
    JOB_FIELDS: list[str] = [
        "function",
        "kwargs",
        "key",
        "scheduled",
        "attempts",
        "completed",
        "queued",
        "started",
        "result",
        "error",
    ]
    """Attributes of the SAQ.

    [`Job`](https://github.com/tobymao/saq/blob/master/saq/job.py) to be
    logged.
    """
    REQUEST_FIELDS: list[RequestExtractorField] = [
        "path",
        "method",
        "headers",
        "cookies",
        "query",
        "path_params",
        "body",
    ]
    """Attributes of the [Request][litestar.connection.request.Request] to be
    logged."""
    RESPONSE_FIELDS: list[ResponseExtractorField] = [
        "status_code",
        "cookies",
        "headers",
        "body",
    ]
    """Attributes of the [Response][litestar.response.Response] to be
    logged."""
    WORKER_EVENT: str = "Worker"
    """Log event name for logs from SAQ worker."""
    SAQ_LEVEL: int = 30
    """Level to log SAQ logs."""
    SQLALCHEMY_LEVEL: int = 30
    """Level to log SQLAlchemy logs."""
    UVICORN_ACCESS_LEVEL: int = 30
    """Level to log uvicorn access logs."""
    UVICORN_ERROR_LEVEL: int = 20
    """Level to log uvicorn error logs."""
