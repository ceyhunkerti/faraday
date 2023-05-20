from typing import Type, TypeVar
from pydantic import BaseModel
from flask_sqlalchemy.pagination import Pagination
from flask import jsonify
from pydantic import parse_obj_as
from typing import List

T = TypeVar("T", bound=BaseModel)


def page_to_json(_type: Type[T], page: Pagination):
    items = parse_obj_as(List[_type], page.items)  # type: ignore

    return jsonify(
        {
            "items": [item.dict() for item in items],  # type: ignore
            "page": page.page,
            "pages": page.pages,
            "total": page.total,
            "has_prev": page.has_prev,
            "has_next": page.has_next,
            "prev_page": page.prev_num,
            "next_page": page.next_num,
        }
    )
