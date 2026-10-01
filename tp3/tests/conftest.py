import pytest
from fastapi.testclient import TestClient

from backend.config import Settings
from backend.main import create_app


@pytest.fixture
def settings(tmp_path):
    return Settings(database=tmp_path / "lab.db")


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings), base_url=settings.base_url) as client:
        session = client.get("/session").json()
        client.headers["X-CSRF-Token"] = session["csrf_token"]
        yield client


@pytest.fixture
def chip(client):
    response = client.post("/chips", json={"part_number": "IC-001", "board": "EVK-A"})
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def measurement():
    return {"metric": "gain", "measured_value": 12.5, "unit": "dB", "passed": True}
