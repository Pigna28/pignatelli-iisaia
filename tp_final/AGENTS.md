# Contexto de trabajo de IC Bring-up Lab

Leer primero README.md y docs/spec.md. Para contratos, openapi.yaml; para decisiones,
docs/architecture.md. El material de clase y tp-referencia son fuentes de consulta.
No editar tp-referencia ni opeanapi.yaml: es el contrato histórico del alumno.

## Invariantes

- Rutas originales /chips y /chips/{chipId}/macros/{macro}/tests, sin prefijo /api.
- Tx, Rx y PLL son fijas. Nunca añadir CRUD de macros por inferencia.
- Path identifica chip y macro; no duplicarlos en TestInput.
- Validación -> 400; recursos inexistentes o jerarquía incorrecta -> 404.
- No incluir secretos, tokens OAuth, .env ni bases reales en commits/logs.
- Una conexión SQLite por request; claves foráneas habilitadas siempre.
- Mutación y auditoría forman una sola transacción.
- Usar textContent para datos del usuario y X-CSRF-Token para escrituras.
- Modo local exclusivamente loopback/desarrollo. Auth0 en producción.
- Flujo actual: chips → threads → steps → attachments. Contadores cuentan hilos.
- Estado derivado: failed si hay fallos; in_progress si vacío/pendiente; passed si todos aprueban.
- Mantener migración v1→v2 sin perder mediciones; /tests es la API histórica deprecated.
- Evidencias: máximo 10 MiB por archivo, 20 por paso, descarga autenticada y forzada.

## Flujo

1. Aclarar alcance en spec/plan para cambios sustanciales.
2. Añadir prueba de regresión para defectos de contrato o seguridad.
3. Modificar el módulo mínimo necesario; no cargar toda la referencia en contexto.
4. Ejecutar `python -m pytest -q` y `python -m ruff check backend tests scripts run.py`.
5. Si cambia la UI, ejecutar `python -m scripts.browser_smoke` y revisar capturas.
6. Actualizar contrato y documentación si cambia comportamiento observable.
7. Informar resultados reales; no atribuir decisiones al usuario sin evidencia.

No crear commits, publicaciones ni deploys ficticios. No activar integraciones,
subagentes o plugins por el solo hecho de que aparezcan en los apuntes.
