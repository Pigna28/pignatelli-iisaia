"""python run.py: sin recarga automática para evitar workers huérfanos en Windows."""

import logging
from urllib.parse import urlparse

import uvicorn

from backend.config import load_settings
from backend.main import create_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = load_settings()
    url = urlparse(settings.base_url)
    uvicorn.run(
        create_app(settings),
        host="127.0.0.1",
        port=url.port or 8000,
        proxy_headers=False,
        access_log=False,
    )
