class ApplicationError(Exception):
    """Base exception type for the custom exception types."""


class PackageNotFoundError(ApplicationError):
    def __init__(self, package_name):
        super().__init__("%s not found" % package_name)
