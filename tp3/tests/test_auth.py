from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from authlib.integrations.starlette_client import OAuthError
from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient

from backend.main import create_app


def auth_app(settings, writer=True):
    settings = replace(
        settings,
        auth_mode="auth0",
        session_secret="s" * 40,
        auth0_domain="example.auth0.com",
        client_id="test-id",
        client_secret="test-secret",
        write_subjects=frozenset({"auth0|operator"}) if writer else frozenset(),
    )
    app = create_app(settings)
    app.state.oauth = SimpleNamespace(
        auth0=SimpleNamespace(
            authorize_access_token=AsyncMock(
                return_value={"userinfo": {"sub": "auth0|operator", "name": "Ana"}}
            ),
            authorize_redirect=AsyncMock(
                return_value=RedirectResponse("https://example.auth0.com/authorize")
            ),
        )
    )
    return app


def test_anonymous_and_callback(settings):
    app = auth_app(settings)
    with TestClient(app, base_url=settings.base_url) as client:
        assert client.get("/health").status_code == 200
        for url in ["/chips", "/summary", "/audit", "/session", "/openapi.json"]:
            assert client.get(url).status_code == 401
        for url in ["/", "/docs"]:
            assert client.get(url, follow_redirects=False).headers["location"] == "/login"
        assert client.get("/login", follow_redirects=False).status_code == 307
        callback = client.get("/callback", follow_redirects=False)
        assert callback.status_code == 302
        session = client.get("/session").json()
        assert session["user"]["name"] == "Ana" and session["can_write"]
        cookie = callback.headers["set-cookie"]
        assert "httponly" in cookie.lower() and "samesite=lax" in cookie.lower()
        client.headers["X-CSRF-Token"] = session["csrf_token"]
        assert client.post("/chips", json={"part_number": "a", "board": "b"}).status_code == 201
        logout = client.post("/logout").json()
        assert "returnTo=http%3A%2F%2F127.0.0.1%3A8000%2Flogged-out" in logout["redirect"]
        assert client.get("/chips").status_code == 401
        assert client.get("/logged-out").status_code == 200


def test_reader_cannot_write_or_audit(settings):
    with TestClient(auth_app(settings, writer=False), base_url=settings.base_url) as client:
        client.get("/callback")
        session = client.get("/session").json()
        assert not session["can_write"]
        client.headers["X-CSRF-Token"] = session["csrf_token"]
        assert client.get("/chips").status_code == 200
        assert client.get("/audit").status_code == 403
        assert client.post("/chips", json={"part_number": "a", "board": "b"}).status_code == 403
        assert client.post("/logout").status_code == 200


def test_csrf(client):
    client.headers.pop("X-CSRF-Token")
    assert client.post("/chips", json={"part_number": "a", "board": "b"}).status_code == 403
    assert client.post("/logout").status_code == 403
    client.headers["X-CSRF-Token"] = "wrong"
    assert client.delete("/chips/1").status_code == 403
    assert client.delete("/chips/1", headers=[(b"X-CSRF-Token", b"\xff")]).status_code == 403


@pytest.mark.parametrize("invalid", [OAuthError(error="invalid_state"), ValueError("bad nonce")])
def test_callback_failure(settings, invalid):
    app = auth_app(settings)
    app.state.oauth.auth0.authorize_access_token.side_effect = invalid
    with TestClient(app, base_url=settings.base_url) as client:
        assert client.get("/callback").status_code == 400
        assert client.get("/chips").status_code == 401


def test_cookie_tamper(settings):
    with TestClient(auth_app(settings), base_url=settings.base_url) as client:
        client.cookies.set("lab_session", "forged")
        assert client.get("/chips").status_code == 401


def test_local_restrictions(settings):
    with TestClient(
        create_app(settings), base_url=settings.base_url, client=("192.0.2.1", 123)
    ) as client:
        assert client.get("/chips").status_code == 403
    with TestClient(create_app(settings), base_url="http://evil.example") as client:
        assert client.get("/chips").status_code == 400
    with pytest.raises(ValueError):
        create_app(replace(settings, environment="production"))
    with pytest.raises(ValueError):
        create_app(replace(settings, auth_mode="auth0", session_secret=""))
