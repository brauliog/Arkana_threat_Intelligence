from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from arkana.api.main import app


client = TestClient(app)


def test_healthz_returns_ok():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_returns_ready_when_database_is_available():
    mock_connection = MagicMock()
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__ = MagicMock(return_value=mock_connection)
    mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)

    with patch("arkana.api.routes.health.create_engine", return_value=mock_engine):
        response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readyz_returns_not_ready_when_database_is_unavailable():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = SQLAlchemyError("connection refused")

    with patch("arkana.api.routes.health.create_engine", return_value=mock_engine):
        response = client.get("/readyz")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert "connection refused" in response.json()["detail"]
