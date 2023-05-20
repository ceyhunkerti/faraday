from app.settings import settings, Settings
import copy


def get_test_settings() -> Settings:
    _settings = copy.deepcopy(settings)
    _settings.SQLALCHEMY_DATABASE_URI = (
        settings.SQLALCHEMY_DATABASE_URI.rsplit("/app", 1)[0] + "/test"
    )
    return _settings  # type: ignore
