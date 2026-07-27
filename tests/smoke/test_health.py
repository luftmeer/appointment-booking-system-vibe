import pytest
from django.test import Client


def test_liveness_reports_ok_without_database_access(client: Client) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_liveness_rejects_unsupported_methods(client: Client, method: str) -> None:
    response = getattr(client, method)("/health/live")

    assert response.status_code == 405
    assert response.headers["Allow"] == "GET"
