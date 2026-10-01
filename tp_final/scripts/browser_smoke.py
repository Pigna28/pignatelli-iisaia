"""Flujo de navegador real con servidor y base temporal propios. No usa .env."""

import json
import os
import socket
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from playwright.sync_api import expect, sync_playwright

from backend.config import ROOT, Settings
from backend.main import create_app
from scripts.seed_demo import seed


def exercise(browser, base):
    page = browser.new_page(viewport={"width": 1440, "height": 1080}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(base)
    expect(page.locator("#stat-chips")).to_have_text("3")
    page.get_by_role("button", name="+ Nueva", exact=True).click()
    page.get_by_label("Número de parte").fill("E2E-CHIP")
    page.get_by_label("Placa / kit de evaluación").fill("E2E-BOARD")
    page.get_by_role("button", name="Guardar muestra", exact=True).click()
    expect(page.locator("#chip-title")).to_have_text("E2E-CHIP")
    page.get_by_role("button", name="+ Registrar ensayo", exact=True).click()
    page.get_by_label("Métrica", exact=True).fill("Ganancia E2E")
    page.get_by_label("Valor medido").fill("12.5")
    page.get_by_label("Unidad", exact=True).fill("dB")
    page.get_by_role("button", name="Guardar ensayo", exact=True).click()
    expect(page.locator("#test-list")).to_contain_text("Ganancia E2E")
    page.locator("#filter").select_option("false")
    expect(page.locator("#test-list")).to_contain_text("No hay ensayos")
    page.locator("#filter").select_option("true")
    expect(page.locator("#test-list")).to_contain_text("Ganancia E2E")
    with page.expect_download() as download:
        page.get_by_role("button", name="Exportar CSV").click()
    text = Path(download.value.path()).read_text("utf-8-sig")
    assert '"Ganancia E2E"' in text and '"12.5"' in text
    page.reload()
    expect(page.locator("#chip-title")).to_have_text("E2E-CHIP")
    expect(page.locator("#test-list")).to_contain_text("Ganancia E2E")
    page.get_by_role("button", name="Eliminar ensayo Ganancia E2E", exact=False).click()
    page.get_by_role("button", name="Cancelar", exact=True).last.click()
    expect(page.locator("#test-list")).to_contain_text("Ganancia E2E")
    page.get_by_role("button", name="Eliminar ensayo Ganancia E2E", exact=False).click()
    page.get_by_role("button", name="Eliminar definitivamente").click()
    expect(page.locator("#test-list")).to_contain_text("No hay ensayos")
    page.get_by_role("button", name="Eliminar muestra", exact=True).click()
    page.get_by_role("button", name="Eliminar definitivamente").click()
    expect(page.locator("#stat-chips")).to_have_text("3")
    page.locator("#filter").select_option("")
    page.locator(".sample").last.click()
    expect(page.locator("#test-list")).to_contain_text("Ganancia")
    ROOT.joinpath("artifacts").mkdir(exist_ok=True)
    page.screenshot(path=str(ROOT / "artifacts/desktop.png"), full_page=True)
    page.set_viewport_size({"width": 390, "height": 844})
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.screenshot(path=str(ROOT / "artifacts/mobile.png"), full_page=True)
    # XSS se prueba con datos externos: el render usa textContent, no HTML.
    page.evaluate("""async () => { const s = await (await fetch('/session')).json();
      await fetch('/chips', {method:'POST', headers:{'Content-Type':'application/json','X-CSRF-Token':s.csrf_token},
      body:JSON.stringify({part_number:'<img src=x onerror=alert(1)>',board:'XSS test'})}); }""")
    page.locator("#refresh").click()
    expect(page.locator("#chip-list")).to_contain_text("<img src=x onerror=alert(1)>")
    assert page.locator("#chip-list img").count() == 0
    # El error de red debe ser visible, sin borrar ni recrear los datos.
    page.route("**/chips", lambda route: route.abort())
    page.locator("#refresh").click()
    expect(page.locator("#notice")).to_contain_text("No se pudo conectar")
    assert not errors, errors
    print(
        json.dumps(
            {
                "browser": browser.version,
                "flow": "passed",
                "csv": "passed",
                "mobile_overflow": False,
                "xss": "passed",
                "network_error": "passed",
                "javascript_errors": errors,
            },
            indent=2,
        )
    )
    page.close()


def main():
    with tempfile.TemporaryDirectory() as directory, socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        base = f"http://127.0.0.1:{port}"
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
