class ApplicationError(Exception):
    """Base exception type for the custom exception types."""


class PackageExistsException(ApplicationError):
    def __init__(self, package_name):
        super.__init__("%s already exists. Try removing package first" % package_name)
