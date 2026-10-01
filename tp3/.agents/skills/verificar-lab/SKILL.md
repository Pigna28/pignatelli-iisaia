---
name: verificar-lab
description: Verifica una entrega o modificación de IC Bring-up Lab en tp3 mediante contrato, API y navegador, y registra evidencia real. Usar para preentrega o regresiones del laboratorio.
---

# Verificar IC Bring-up Lab

Localizar la raíz del proyecto por `run.py`, `openapi.yaml` y `backend/`.
Leer `AGENTS.md` y `docs/verification.md` desde esa raíz. Usar el Python de `.venv`
si existe; no sustituir la base de usuario para hacer pruebas.

Para preentrega ejecutar desde la raíz del proyecto:

1. `python -m ruff check backend tests scripts run.py` y
   `python -m ruff format --check backend tests scripts run.py`.
2. `python -m pytest -q --cov=backend --cov-fail-under=90`.
3. `python -m scripts.browser_smoke`, que usa servidor y SQLite temporales.
   Por defecto requiere Chrome instalado; con Chromium de Playwright usar
   `BROWSER_CHANNEL` vacío. Revisar las imágenes `artifacts/desktop.png` y
   `artifacts/mobile.png` además del resultado automático.

Para un cambio acotado elegir las verificaciones afectadas. El fallo histórico
de SQLite solo apareció con requests paralelos: ante cambios de DB o dependencias
no omitir la prueba de concurrencia y el flujo real de navegador.

Si falla algo, reproducir y corregir la causa dentro del alcance autorizado.
No cambiar el contrato original `opeanapi.yaml`, deshabilitar CSRF, dar permisos
de operador a todos ni usar credenciales reales para hacer pasar una prueba.
Las capturas son datos sintéticos; no deben contener secretos o datos del tenant.

Actualizar `docs/verification.md` con comandos, resultados, entorno, fallos
corregidos y validaciones que sigan pendientes. Auth0 simulado no acredita un login
real. CI local no acredita un workflow ejecutado en GitHub. No publicar ni generar
un historial Git a partir de esta skill: eso depende del pedido del usuario.
