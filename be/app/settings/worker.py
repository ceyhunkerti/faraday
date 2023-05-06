from pydantic import BaseSettings
from typing import Literal


class WorkerSettings(BaseSettings):
    """Global SAQ Job configuration."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "WORKER_"

    JOB_TIMEOUT: int = 10
    """Max time a job can run for, in seconds.

    Set to `0` for no timeout.
    """
    JOB_HEARTBEAT: int = 0
    """Max time a job can survive without emitting a heartbeat. `0` to disable.

    `job.update()` will trigger a heartbeat.
    """
    JOB_RETRIES: int = 10
    """Max attempts for any job."""
    JOB_TTL: int = 600
    """Lifetime of available job information, in seconds.

    0: indefinite
    -1: disabled (no info retained)
    """
    JOB_RETRY_DELAY: float = 1.0
    """Seconds to delay before retrying a job."""
    JOB_RETRY_BACKOFF: bool | float = 60
    """If true, use exponential backoff for retry delays.

    - The first retry will have whatever retry_delay is.
    - The second retry will have retry_delay*2. The third retry will have retry_delay*4. And so on.
    - This always includes jitter, where the final retry delay is a random number between 0 and the calculated retry delay.
    - If retry_backoff is set to a number, that number is the maximum retry delay, in seconds."
    """  # noqa
    CONCURRENCY: int = 10
    """The number of concurrent jobs allowed to execute per worker.

    Default is set to 10.
    """
    WEB_ENABLED: bool = False
    """If true, the worker admin UI is launched on worker startup.."""
    WEB_PORT: int = 8081
    """Port to use for the worker web UI."""
    INIT_METHOD: Literal["integrated", "standalone"] = "integrated"
    """Initialization method for the worker process."""
