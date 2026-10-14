"""Prueba end-to-end de indicadores, hilos, pasos y evidencias."""

import json
from pathlib import Path

from playwright.sync_api import expect

from backend.config import ROOT


def exercise(browser, base):
    page = browser.new_page(viewport={"width": 1440, "height": 1080}, accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(base)
    expect(page.locator("#stat-chips")).to_have_text("3")
    expect(page.locator("#stat-tests")).to_have_text("12")
    for section, count in [
        ("chips", 3),
        ("tests", 12),
        ("passed", 4),
        ("failed", 4),
        ("in_progress", 4),
    ]:
        page.locator(f'[data-overview="{section}"]').click()
        expect(page.locator(".overview-item")).to_have_count(count)
    page.locator("#close-overview").click()
    page.get_by_role("button", name="+ Nueva", exact=True).click()
    page.get_by_label("Número de parte").fill("E2E-CHIP")
    page.get_by_label("Placa / kit de evaluación").fill("EVK-E2E")
    page.get_by_role("button", name="Guardar muestra", exact=True).click()
    expect(page.locator("#chip-title")).to_have_text("E2E-CHIP")
    page.get_by_role("button", name="+ Nuevo hilo").click()
    page.get_by_label("Título del hilo").fill("Caracterización RF E2E")
    page.get_by_label("Objetivo / descripción").fill("Secuencia con evidencias de cada etapa")
    page.get_by_role("button", name="Crear hilo", exact=True).click()
    expect(page.locator("#thread-title")).to_have_text("Caracterización RF E2E")
    expect(page.locator("#stat-in_progress")).to_have_text("5")
    page.get_by_role("button", name="+ Agregar paso").click()
    page.get_by_label("Título del paso").fill("Preparar banco")
    page.get_by_label("Notas del paso").fill("Revisar fuente y calibración")
    page.get_by_role("button", name="Guardar paso", exact=True).click()
    expect(page.locator(".step-card")).to_have_count(1)
    page.get_by_role("button", name="Adjuntar evidencia", exact=True).click()
    page.get_by_label("Nombre del enlace").fill("Presentación del ensayo")
    page.get_by_label("URL del enlace").fill("https://example.org/presentacion")
    page.get_by_role("button", name="Guardar enlace", exact=True).click()
    expect(page.get_by_role("link", name="Enlace: Presentación del ensayo")).to_have_attribute(
        "href", "https://example.org/presentacion"
    )
    page.get_by_role("button", name="Adjuntar evidencia", exact=True).click()
    evidence = b"%PDF-1.7\nDemo evidence"
    page.get_by_label("Archivo del paso").set_input_files(
        {"name": "informe.pdf", "mimeType": "application/pdf", "buffer": evidence}
    )
    page.get_by_role("button", name="Subir archivo", exact=True).click()
    expect(page.get_by_role("link", name="Archivo: informe.pdf")).to_be_visible()
    with page.expect_download() as download:
        page.get_by_role("link", name="Archivo: informe.pdf").click()
    assert Path(download.value.path()).read_bytes() == evidence
    # Imagen y presentación: el navegador usa el mismo selector de archivos.
    for name, mime, content in [
        ("banco.png", "image/png", b"\x89PNG\r\n\x1a\nexample"),
        (
            "resultados.pptx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            b"PK\x03\x04example",
        ),
    ]:
        page.get_by_role("button", name="Adjuntar evidencia", exact=True).click()
        page.get_by_label("Archivo del paso").set_input_files(
            {"name": name, "mimeType": mime, "buffer": content}
        )
        page.get_by_role("button", name="Subir archivo", exact=True).click()
        expect(page.get_by_role("link", name=f"Archivo: {name}")).to_be_visible()
    page.get_by_role("button", name="Editar paso", exact=True).click()
    page.get_by_label("Estado del paso").select_option("passed")
    page.get_by_role("button", name="Guardar paso", exact=True).click()
    expect(page.locator("#thread-meta .badge")).to_have_text("Aprobado")
    page.get_by_role("button", name="+ Agregar paso").click()
    page.get_by_label("Título del paso").fill("Medir ganancia")
    page.get_by_label("Métrica", exact=True).fill("gain")
    page.get_by_label("Valor medido").fill("12.5")
    page.get_by_label("Unidad", exact=True).fill("dB")
    page.get_by_role("button", name="Guardar paso", exact=True).click()
    expect(page.locator(".step-card")).to_have_count(2)
    expect(page.locator("#thread-meta .badge")).to_have_text("En progreso")
    expect(page.locator("#stat-tests")).to_have_text("13")
    page.locator('[data-overview="in_progress"]').click()
    expect(page.locator(".overview-item")).to_have_count(5)
    page.locator(".overview-item").filter(has_text="Caracterización RF E2E").click()
    expect(page.locator(".step-card")).to_have_count(2)
    page.locator("#filter").select_option("passed")
    expect(page.locator("#test-list")).to_contain_text("No hay hilos")
    page.locator("#filter").select_option("in_progress")
    expect(page.locator("#test-list")).to_contain_text("Caracterización RF E2E")
    with page.expect_download() as csv_download:
        page.get_by_role("button", name="Exportar CSV").click()
    assert "in_progress" in Path(csv_download.value.path()).read_text("utf-8-sig")
    page.reload()
    page.get_by_role("button", name="Caracterización RF E2E", exact=True).click()
    expect(page.locator(".step-card")).to_have_count(2)
    expect(page.get_by_role("link", name="Archivo: informe.pdf")).to_be_visible()
    folder = ROOT / "artifacts/threads-v2"
    folder.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(folder / "desktop.png"), full_page=True)
    page.set_viewport_size({"width": 390, "height": 844})
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.screenshot(path=str(folder / "mobile.png"), full_page=True)
    page.get_by_role("button", name="Quitar evidencia informe.pdf").click()
    page.get_by_role("button", name="Cancelar", exact=True).last.click()
    expect(page.get_by_role("link", name="Archivo: informe.pdf")).to_be_visible()
    page.get_by_role("button", name="Quitar evidencia informe.pdf").click()
    page.get_by_role("button", name="Eliminar definitivamente").click()
    expect(page.get_by_role("link", name="Archivo: informe.pdf")).to_have_count(0)
    page.locator(".step-card").last.get_by_role("button", name="Editar paso").click()
    page.get_by_label("Estado del paso").select_option("failed")
    page.get_by_role("button", name="Guardar paso", exact=True).click()
    expect(page.locator("#thread-meta .badge")).to_have_text("Fallido")
    page.locator('[data-overview="failed"]').click()
    expect(page.locator(".overview-item")).to_have_count(5)
    page.locator("#close-overview").click()
    page.locator("#filter").select_option("")
    page.get_by_role("button", name="Eliminar hilo Caracterización RF E2E", exact=False).click()
    page.get_by_role("button", name="Eliminar definitivamente").click()
    expect(page.locator("#stat-tests")).to_have_text("12")
    page.get_by_role("button", name="Eliminar muestra", exact=True).click()
    page.get_by_role("button", name="Eliminar definitivamente").click()
    expect(page.locator("#stat-chips")).to_have_text("3")
    page.evaluate("""async () => { const s = await (await fetch('/session')).json();
      await fetch('/chips', {method:'POST', headers:{'Content-Type':'application/json','X-CSRF-Token':s.csrf_token},
      body:JSON.stringify({part_number:'<img src=x onerror=alert(1)>',board:'XSS test'})}); }""")
    page.locator("#refresh").click()
    expect(page.locator("#chip-list")).to_contain_text("<img src=x onerror=alert(1)>")
    assert page.locator("#chip-list img").count() == 0
    page.route("**/chips", lambda route: route.abort())
    page.locator("#refresh").click()
    expect(page.locator("#notice")).to_contain_text("No se pudo conectar")
    assert not errors, errors
    print(
        json.dumps(
            {
                "browser": browser.version,
                "threads_flow": "passed",
                "five_overviews": "passed",
                "attachments_download": "passed",
                "csv": "passed",
                "persistence": "passed",
                "mobile_overflow": False,
                "javascript_errors": errors,
            },
            indent=2,
        )
    )
    page.close()
