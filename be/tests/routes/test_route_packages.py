from flask.testing import FlaskClient
from tests import data


def test_index(client: FlaskClient) -> None:
    packages = data.gen_package(10)

    response = client.get("/packages")
    assert response.status_code == 200
    assert len(response.json) == len(packages)  # type: ignore
