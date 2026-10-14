from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient
from joserfc.errors import BadSignatureError

from backend.config import load_settings
from backend.db import connect, initialize
from scripts.backup import backup
from scripts.seed_demo import seed
from tests.test_auth import auth_app


def test_parallel_requests(client, chip):
    # Reproduce la lectura simultánea /chips + /summary que realiza el frontend.
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(client.get, ["/chips", "/summary"] * 12))
    assert all(response.status_code == 200 for response in responses)


def test_backup_and_seed(settings, tmp_path):
    seed(settings)
    seed(settings)
    destination = tmp_path / "backup.db"
    backup(settings.database, destination)
    with connect(destination) as db:
        assert db.execute("SELECT COUNT(*) FROM chips").fetchone()[0] == 3
        assert db.execute("SELECT COUNT(*) FROM threads").fetchone()[0] == 12
        assert db.execute("SELECT COUNT(*) FROM tests").fetchone()[0] == 0
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    with pytest.raises(ValueError):
        backup(settings.database, destination)
    with pytest.raises(SystemExit):
        seed(replace(settings, auth_mode="auth0"))


def test_unknown_database_version(settings):
    initialize(settings.database)
    with connect(settings.database) as db:
        db.execute("PRAGMA user_version=999")
    with pytest.raises(RuntimeError):
        initialize(settings.database)


def test_outage_and_headers(client, settings):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]
    assert len(response.headers["X-Request-ID"]) == 32
    assert client.get("/openapi.yaml").status_code == 200
    with connect(settings.database) as db:
        db.execute("DROP VIEW thread_overview")
    response = client.get("/summary")
    assert response.status_code == 503
    assert "error" in response.json() and "SELECT" not in response.text


@pytest.mark.parametrize(
    "change",
    [
        {"auth_mode": "none"},
        {"environment": "staging"},
        {"base_url": "ftp://example.org"},
        {"base_url": "http://user:pass@localhost"},
        {"base_url": "http://localhost/path"},
        {"base_url": "http://example.org"},
    ],
)
def test_bad_config(settings, change):
    with pytest.raises(ValueError):
        replace(settings, **change).validate()


def test_environment_loading(monkeypatch, tmp_path):
    for name, value in {
        "AUTH_MODE": "local",
        "APP_ENV": "development",
        "DATABASE_PATH": str(tmp_path / "env.db"),
        "BASE_URL": "http://127.0.0.1:8765",
        "SESSION_SECRET": "",
        "WRITE_SUBJECTS": " user1 ,user2 ",
    }.items():
        monkeypatch.setenv(name, value)
    settings = load_settings()
    assert settings.database == tmp_path / "env.db"
    assert len(settings.session_secret) >= 32
    assert settings.write_subjects == {"user1", "user2"}


def test_bad_signature_and_missing_identity(settings):
    app = auth_app(settings)
    with TestClient(app, base_url=settings.base_url) as client:
        app.state.oauth.auth0.authorize_access_token.return_value = {}
        assert client.get("/callback").status_code == 400
        app.state.oauth.auth0.authorize_access_token.side_effect = BadSignatureError()
        assert client.get("/callback").status_code == 400
        assert client.get("/session").status_code == 401


def test_production_cookie_and_hsts(settings):
    app = auth_app(replace(settings, base_url="https://lab.example", environment="production"))
    with TestClient(app, base_url="https://lab.example") as client:
        response = client.get("/callback", follow_redirects=False)
        assert "secure" in response.headers["set-cookie"].lower()
        assert "max-age" in response.headers["Strict-Transport-Security"]


def test_local_auth_endpoints(client):
    assert client.get("/login", follow_redirects=False).headers["location"] == "/"
    assert client.get("/callback").status_code == 400
