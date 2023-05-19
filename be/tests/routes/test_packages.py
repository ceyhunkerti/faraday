from flask.testing import FlaskClient


def test_index(client: FlaskClient) -> None:
    response = client.get("/packages")
    assert response.status_code == 200
    assert response.json == {"content": "hello"}
