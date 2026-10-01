import logging
import sqlite3
import time
import uuid
from contextlib import asynccontextmanager
from urllib.parse import urlparse

import yaml
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import auth
from .config import ROOT, Settings, load_settings
from .db import connect, initialize
from .routes import router

logger = logging.getLogger("lab")


def create_app(settings: Settings | None = None):
    settings = (settings or load_settings()).validate()

    @asynccontextmanager
    async def lifespan(app):
        initialize(settings.database)
        yield

    app = FastAPI(title="IC Bring-up Lab API", version="1.1.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.oauth = auth.setup_oauth(settings)
    app.middleware("http")(auth.guard)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret,
        session_cookie="lab_session",
        same_site="lax",
        max_age=28800,
        https_only=settings.base_url.startswith("https://"),
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[urlparse(settings.base_url).hostname])

    @app.middleware("http")
    async def observe(request, call_next):
        request_id = uuid.uuid4().hex
        started = time.monotonic()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "no-store"
        if request.url.path not in {"/docs", "/redoc"}:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; "
                "base-uri 'self'; form-action 'self'"
            )
        if settings.environment == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000"
        logger.info(
            "request_id=%s method=%s path=%s status=%s elapsed_ms=%.1f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            (time.monotonic() - started) * 1000,
        )
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        errors = [
            f"{'.'.join(str(x) for x in error['loc'])}: {error['msg']}" for error in exc.errors()
        ]
        return JSONResponse({"error": "; ".join(errors)}, status_code=400)

    @app.exception_handler(HTTPException)
    async def http_error(request, exc):
        return JSONResponse(
            {"error": str(exc.detail)}, status_code=exc.status_code, headers=exc.headers
        )

    @app.exception_handler(sqlite3.OperationalError)
    async def database_error(request, exc):
        logger.error("Database unavailable: %s", type(exc).__name__)
        return JSONResponse({"error": "Base de datos temporalmente no disponible"}, status_code=503)

    @app.get("/health", include_in_schema=False)
    def health():
        with connect(settings.database) as db:
            db.execute("SELECT COUNT(*) FROM chips").fetchone()
        return {"status": "ok"}

    @app.get("/", include_in_schema=False)
    def home():
        return FileResponse(ROOT / "frontend/index.html")

    @app.get("/openapi.yaml", include_in_schema=False)
    def yaml_contract():
        return FileResponse(ROOT / "openapi.yaml", media_type="application/yaml")

    app.include_router(auth.router)
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=ROOT / "frontend"), name="assets")

    def contract():
        if app.openapi_schema is None:
            app.openapi_schema = yaml.safe_load((ROOT / "openapi.yaml").read_text("utf-8"))
        return app.openapi_schema

    app.openapi = contract
    return app
