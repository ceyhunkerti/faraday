from flask import Blueprint
from flask_pydantic import validate
from app.api.schema import PageQueryParams

bp = Blueprint("packages", __name__, url_prefix="/packages")


@bp.route("", methods=["GET"])
@validate()
def index(query: PageQueryParams):
    return {"content": "hello"}, 200
