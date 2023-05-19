from app.settings import settings, Settings


def get_settings() -> Settings:
    settings.SQLALCHEMY_DATABASE_URI = (
        settings.SQLALCHEMY_DATABASE_URI.rsplit("/app", 1)[0] + "/test"
    )
    return settings  # type: ignore
