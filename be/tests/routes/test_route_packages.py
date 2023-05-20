from flask.testing import FlaskClient
from tests import data


def test_index(client: FlaskClient) -> None:
    packages = data.gen_package(10)

    response = client.get("/packages")
    assert response.status_code == 200
    assert len(response.json["items"]) == len(packages)  # type: ignore

    response = client.get("/packages?page=2&per_page=3")
    assert response.status_code == 200
    assert len(response.json["items"]) == 3  # type: ignore
    assert response.json["page"] == 2  # type: ignore
