from flask import Blueprint
from flask_pydantic import validate
from app.api.schema import PageQueryParams
from app.models import Package
from app.api.schema import PackageOutSchema
from flask_sqlalchemy.pagination import Pagination
from logging import getLogger
from .base import page_to_json
from flask import jsonify

logger = getLogger(__name__)


bp = Blueprint("packages", __name__, url_prefix="/packages")


@bp.route("", methods=["GET"])
@validate()
def index(query: PageQueryParams):
    page: Pagination = Package.query.paginate(**query.dict())
    return page_to_json(PackageOutSchema, page), 200


@bp.route("/<id>", methods=["GET"])
@validate()
def show(id: int):
    package = Package.one(id=id)
    # todo return err if none
    return jsonify(PackageOutSchema.from_orm(package).dict())
