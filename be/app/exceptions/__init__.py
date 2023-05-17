class ApplicationError(Exception):
    """Base exception type for the custom exception types."""


class PackageNotFoundError(ApplicationError):
    def __init__(self, name):
        super().__init__("%s not found" % name)


class ExtractionNotFoundError(ApplicationError):
    def __init__(self, name):
        super().__init__("%s not found" % name)
