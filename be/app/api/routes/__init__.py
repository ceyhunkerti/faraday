from .root import bp
from .packages import bp as bp_packages

bp.register_blueprint(bp_packages)

__all__ = ["bp"]
