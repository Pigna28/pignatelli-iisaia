import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
LOOPBACK = {"localhost", "127.0.0.1", "::1", "testclient"}


@dataclass(frozen=True)
class Settings:
    auth_mode: str = "local"
    environment: str = "development"
    base_url: str = "http://127.0.0.1:8000"
    database: Path = ROOT / "data/lab.db"
    session_secret: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    auth0_domain: str = ""
    client_id: str = ""
    client_secret: str = ""
    write_subjects: frozenset[str] = frozenset()

    def validate(self):
        url = urlparse(self.base_url)
        if self.environment not in {"development", "production"}:
            raise ValueError("APP_ENV debe ser development o production")
        if self.auth_mode not in {"local", "auth0"}:
            raise ValueError("AUTH_MODE debe ser local o auth0")
        if url.scheme not in {"http", "https"} or not url.hostname or url.path not in {"", "/"}:
            raise ValueError("BASE_URL debe ser un origen http(s) sin path")
        if url.username or url.password or url.query or url.fragment:
            raise ValueError("BASE_URL no admite credenciales, query ni fragmentos")
        if self.auth_mode == "local" and (
            self.environment == "production" or url.hostname not in LOOPBACK - {"testclient"}
        ):
            raise ValueError("Modo local permitido solo en desarrollo y loopback")
        if self.environment == "production" and url.scheme != "https":
            raise ValueError("Producción requiere BASE_URL con HTTPS")
        if self.auth_mode == "auth0":
            if not all((self.auth0_domain, self.client_id, self.client_secret)):
                raise ValueError("Completar AUTH0_DOMAIN, AUTH0_CLIENT_ID y AUTH0_CLIENT_SECRET")
            if len(self.session_secret) < 32:
                raise ValueError("SESSION_SECRET requiere al menos 32 caracteres")
            if any(c in self.auth0_domain for c in "/:@ ?#"):
                raise ValueError("AUTH0_DOMAIN debe ser un hostname sin https://")
        return self


def load_settings():
    load_dotenv(ROOT / ".env")
    path = Path(os.getenv("DATABASE_PATH", "data/lab.db"))
    mode = os.getenv("AUTH_MODE", "local")
    return Settings(
        auth_mode=mode,
        environment=os.getenv("APP_ENV", "development"),
        base_url=os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/"),
        database=path if path.is_absolute() else ROOT / path,
        session_secret=os.getenv("SESSION_SECRET")
        or (secrets.token_urlsafe(32) if mode == "local" else ""),
        auth0_domain=os.getenv("AUTH0_DOMAIN", ""),
        client_id=os.getenv("AUTH0_CLIENT_ID", ""),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET", ""),
        write_subjects=frozenset(
            x.strip() for x in os.getenv("WRITE_SUBJECTS", "").split(",") if x.strip()
        ),
    ).validate()
