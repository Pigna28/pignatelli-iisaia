import secrets
from urllib.parse import urlencode

import httpx
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from joserfc.errors import JoseError

from .config import LOOPBACK

router = APIRouter()
PUBLIC = {"/health", "/login", "/callback", "/logged-out"}


def setup_oauth(settings):
    oauth = OAuth()
    if settings.auth_mode == "auth0":
        oauth.register(
            "auth0",
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            server_metadata_url=f"https://{settings.auth0_domain}/.well-known/openid-configuration",
            client_kwargs={"scope": "openid profile email"},
        )
    return oauth


def failure(message, status):
    return JSONResponse({"error": message}, status_code=status)


async def guard(request, call_next):
    settings = request.app.state.settings
    if settings.auth_mode == "local":
        if (
            not request.client
            or request.client.host not in LOOPBACK
            or request.url.hostname not in LOOPBACK
        ):
            return failure("El modo local solo admite conexiones loopback", 403)
        request.state.user = {"sub": "local-demo", "name": "Operador local"}
    else:
        request.state.user = request.session.get("user")
    if request.url.path in PUBLIC:
        return await call_next(request)
    if not request.state.user:
        if request.url.path in {"/", "/docs", "/redoc"}:
            return RedirectResponse("/login", status_code=302)
        return failure("Iniciá sesión para continuar", 401)
    request.state.can_write = (
        settings.auth_mode == "local" or request.state.user["sub"] in settings.write_subjects
    )
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        csrf = request.session.get("csrf", "")
        if not csrf or not secrets.compare_digest(
            request.headers.get("X-CSRF-Token", "").encode("utf-8"), csrf.encode("utf-8")
        ):
            return failure("Token CSRF ausente o inválido; recargá la página", 403)
        if request.url.path != "/logout" and not request.state.can_write:
            return failure("Tu cuenta tiene acceso de solo lectura", 403)
    return await call_next(request)


@router.get("/login", include_in_schema=False)
async def login(request: Request):
    if request.app.state.settings.auth_mode == "local":
        return RedirectResponse("/", status_code=302)
    return await request.app.state.oauth.auth0.authorize_redirect(
        request, request.app.state.settings.base_url + "/callback", connection="google-oauth2"
    )


@router.get("/callback", include_in_schema=False)
async def callback(request: Request):
    if request.app.state.settings.auth_mode != "auth0":
        return failure("Callback disponible solo en modo Auth0", 400)
    try:
        token = await request.app.state.oauth.auth0.authorize_access_token(request)
        user = token.get("userinfo")
        if not user or not user.get("sub"):
            raise ValueError("Sin identidad verificada")
    except (OAuthError, httpx.HTTPError, JoseError, ValueError, KeyError):
        request.session.clear()
        return failure("No se pudo validar el inicio de sesión. Volvé a /login", 400)
    request.session.clear()
    request.session["user"] = {"sub": user["sub"], "name": user.get("name", "Operador")}
    request.session["csrf"] = secrets.token_urlsafe(32)
    return RedirectResponse("/", status_code=302)


@router.get("/session", include_in_schema=False)
def session(request: Request):
    request.session.setdefault("csrf", secrets.token_urlsafe(32))
    return {
        "user": request.state.user,
        "can_write": request.state.can_write,
        "mode": request.app.state.settings.auth_mode,
        "csrf_token": request.session["csrf"],
    }


@router.post("/logout", include_in_schema=False)
def logout(request: Request):
    request.session.clear()
    settings = request.app.state.settings
    target = "/logged-out"
    if settings.auth_mode == "auth0":
        target = f"https://{settings.auth0_domain}/v2/logout?" + urlencode(
            {
                "client_id": settings.client_id,
                "returnTo": settings.base_url + "/logged-out",
            }
        )
    return {"redirect": target}


@router.get("/logged-out", include_in_schema=False)
def logged_out():
    return HTMLResponse(
        '<!doctype html><html lang="es"><meta charset="utf-8">'
        "<title>Sesión cerrada</title><h1>Sesión cerrada</h1>"
        '<p><a href="/login">Volver a ingresar</a></p></html>'
    )
