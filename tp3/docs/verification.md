# Evidencia de verificación

Fecha de trabajo: 30 de septiembre de 2026 (Argentina; 1 de octubre en UTC).
Entorno Windows, Python 3.13.3, Chrome 154.0.8037.59.
Versiones Python fijadas en `requirements-lock.txt`.

## Suite automatizada

Comando desde `tp3`, con el Python de `.venv`:

```text
python -m pytest -q --cov=backend --cov-report=term-missing
52 passed, 2 warnings

backend/auth.py       100%
backend/config.py      93%
backend/db.py         100%
backend/main.py       100%
backend/routes.py     100%
backend/schemas.py    100%
TOTAL                 99%
```

Cobertura de líneas, no de todas las combinaciones ni de seguridad formal.
Incluye seis operaciones originales, entradas inválidas, filtro estricto,
jerarquía chip/macro/test, cascada, rollback ante fallo de auditoría,
persistencia entre instancias, requests concurrentes, paginación de auditoría,
contrato OpenAPI 3.1 y respuestas contrastadas contra JSON Schema, configuración,
backup y seed repetible.

En autenticación se verifica 401, lector vs operador, CSRF ausente/incorrecto,
cookie alterada, callback con error/firma inválida/sin identidad, logout,
cookies y cabeceras de producción. El cliente de Auth0 está simulado.

Las dos advertencias pertenecen a Authlib/Starlette por la deprecación de su
compatibilidad con httpx. No se ocultaron. No impidieron ejecutar la suite.

Lint y formato: `ruff check` aprobó y `ruff format --check` confirmó los 20
archivos Python. `pip check`: `No broken requirements found`.
Skill de preentrega: `quick_validate.py` devolvió `Skill is valid!`.

## Navegador real

```text
python -m scripts.browser_smoke
browser: 154.0.8037.59
flow: passed
csv: passed
mobile_overflow: false
xss: passed
network_error: passed
javascript_errors: []
```

Se comprobó creación de chip y ensayo, filtros, descarga CSV, recarga conservando
datos, cancelación y confirmación de borrados, y render de datos no confiables como
texto. Se abortó una request para verificar el mensaje de error de conexión.
Se revisaron capturas en 1440 px y 390 px; no hay overflow horizontal del documento.
La tabla admite scroll horizontal propio en pantallas angostas.

Las capturas locales se regeneran en `artifacts/desktop.png` y `artifacts/mobile.png`.
La prueba utiliza servidor y base temporales propios y no deja procesos activos.

## Fallos observados y correcciones

1. Primera suite: 37 pasaron y falló una expectativa sobre Set-Cookie en cada GET.
   Se verifican sus atributos en el callback que crea la sesión. Suite: 38 pasaron.
2. Primera prueba de navegador: excepción SQLite por conexión creada en otro hilo.
   Se configuró `check_same_thread=False` con una conexión exclusiva por request,
   manteniendo transacciones; el navegador volvió a pasar.
3. Se agregó regresión de requests concurrentes y pruebas operativas; 52 pasaron.

## No verificado externamente

- Tenant real Auth0/Google, credenciales y flujo con usuarios reales.
- Publicación en GitHub, ejecución remota de CI o despliegue HTTPS.
- Ejecución en Linux/macOS y carga sostenida de múltiples operadores.
- Revocación de cookies robadas, pentest independiente o auditoría metrológica.
- Detección automática de la skill de proyecto en una sesión nueva del agente.

El workflow está preparado para Linux y Chromium. No se afirma que esté verde en
GitHub: no se publicó ni ejecutó durante esta sesión. Tampoco se crearon commits o
PRs; `git` no estaba disponible en PATH y no había un historial gestionado aquí.
