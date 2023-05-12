from typing import Final
from app import util
from app.settings.api import APISettings
from app.settings.app import AppSettings
from app.settings.db import DatabaseSettings
from app.settings.http_client import HTTPClientSettings
from app.settings.log import LogSettings
from app.settings.openapi import OpenAPISettings
from app.settings.redis import RedisSettings
from app.settings.server import ServerSettings

from functools import lru_cache

from app.settings.worker import WorkerSettings
from pydantic import ValidationError

DEFAULT_MODULE_NAME = "app"
BASE_DIR: Final = util.module_to_os_path(DEFAULT_MODULE_NAME)


@lru_cache
def load_settings() -> (
    tuple[
        AppSettings,
        APISettings,
        RedisSettings,
        DatabaseSettings,
        OpenAPISettings,
        ServerSettings,
        LogSettings,
        HTTPClientSettings,
        WorkerSettings,
    ]
):
    """Load Settings file.

    As an example, I've commented out how you might go about injecting secrets into the environment for production.

    This fetches a `.env` configuration from a Google secret and configures the environment with those variables.

    ```python
    secret_id = os.environ.get("ENV_SECRETS", None)
    env_file_exists = os.path.isfile(f"{os.curdir}/.env")
    local_service_account_exists = os.path.isfile(f"{os.curdir}/service_account.json")
    if local_service_account_exists:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
    project_id = os.environ.get("GOOGLE_PROJECT_ID", None)
    if project_id is None:
        _, project_id = google.auth.default()
        os.environ["GOOGLE_PROJECT_ID"] = project_id
    if not env_file_exists and secret_id:
        secret = secret_manager.get_secret(project_id, secret_id)
        load_dotenv(stream=io.StringIO(secret))

    try:
        settings = ...  # existing code below
    except:
        ...
    return settings
    ```
    Returns:
        Settings: application settings
    """
    try:
        """Override Application reload dir."""
        server: ServerSettings = ServerSettings.parse_obj(
            {"HOST": "0.0.0.0", "RELOAD_DIRS": [str(BASE_DIR)]},  # noqa: S104
        )
        app = AppSettings.parse_obj({})
        api = APISettings.parse_obj({})
        redis = RedisSettings.parse_obj({})
        db = DatabaseSettings.parse_obj({})
        openapi = OpenAPISettings.parse_obj({})
        log = LogSettings.parse_obj({})
        worker = WorkerSettings.parse_obj({})
        http_client = HTTPClientSettings.parse_obj({})

    except ValidationError as e:
        print("Could not load settings. %s", e)  # noqa: T201
        raise e from e
    return (
        app,
        api,
        redis,
        db,
        openapi,
        server,
        log,
        http_client,
        worker,
    )


(
    app,
    api,
    redis,
    db,
    openapi,
    server,
    log,
    http_client,
    worker,
) = load_settings()
