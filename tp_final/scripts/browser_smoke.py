"""Navegador real con servidor/base temporal; no usa .env ni la base del usuario."""

import os
import socket
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from playwright.sync_api import sync_playwright

from backend.config import ROOT, Settings
from backend.main import create_app
from scripts.seed_demo import seed
from scripts.thread_browser import exercise


def main():
    (ROOT / "artifacts").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "artifacts") as directory, socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        base = f"http://127.0.0.1:{sock.getsockname()[1]}"
        settings = Settings(database=Path(directory) / "smoke.db", base_url=base)
        seed(settings)
        server = uvicorn.Server(uvicorn.Config(create_app(settings), log_level="warning"))
        thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started:
                if time.monotonic() > deadline:
                    raise RuntimeError("El servidor de prueba no inició")
                time.sleep(0.05)
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    channel=os.getenv("BROWSER_CHANNEL", "chrome") or None, headless=True
                )
                try:
                    exercise(browser, base)
                finally:
                    browser.close()
        finally:
            server.should_exit = True
            thread.join(timeout=10)


if __name__ == "__main__":
    main()
