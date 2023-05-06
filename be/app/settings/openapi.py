from pydantic import BaseSettings


# noinspection PyUnresolvedReferences
class OpenAPISettings(BaseSettings):
    """Configures OpenAPI for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "OPENAPI_"

    CONTACT_NAME: str = "Cody"
    """Name of contact on document."""
    CONTACT_EMAIL: str = "admin"
    """Email for contact on document."""
    TITLE: str | None = "Litestar Fullstack"
    """Document title."""
    VERSION: str = "v1.0"
    """Document version."""
