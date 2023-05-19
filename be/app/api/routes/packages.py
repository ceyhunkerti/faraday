from typing import List
from flask import Blueprint
from flask_pydantic import validate
from app.api.schema import PageQueryParams
from app.models import Package
from app.api.schema import PackageSchema
from pydantic import parse_obj_as
from flask import jsonify

from logging import getLogger

logger = getLogger(__name__)


bp = Blueprint("packages", __name__, url_prefix="/packages")


@bp.route("", methods=["GET"])
@validate()
def index(query: PageQueryParams):
    result = parse_obj_as(List[PackageSchema], Package.all())
    return jsonify([r.dict() for r in result]), 200
