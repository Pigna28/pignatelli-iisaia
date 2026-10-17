# Evidencia de verificación

## Integración de la carpeta v2 — 14/10/2026

Se preparó una copia de esta entrega con el código vigente de hilos y evidencias,
sin copiar la base de datos de la otra carpeta. Entorno: Windows, Python 3.14.6,
Chrome 155.0.8059.80.

Resultados de esta preparación:

- **91 pruebas aprobadas**, incluidas las de hilos, archivos, contrato, autenticación,
  migración y compatibilidad del conjunto anterior. Dos advertencias de deprecación
  de Authlib/Starlette; no se midió de nuevo la cobertura.
- **Ruff sin errores** para backend, tests, scripts y run.py.
- **Chrome:** cinco indicadores, creación y edición de pasos, tres estados,
  adjuntos y descargas, CSV, persistencia, borrado y error de red; sin errores
  JavaScript ni desbordamiento horizontal móvil. Capturas de escritorio y móvil
  revisadas en `artifacts/threads-v2/`.
- Sobre una copia de la base v1 de esta entrega se conservan las 8 muestras,
  48 mediciones y 56 eventos originales. Tras migrar y agregar A0/A1/A2:
  **11 muestras, 60 hilos, 84 pasos, 9 adjuntos y 116 eventos**. Resumen:
  42 aprobados, 14 fallidos y 4 en progreso. Repetir la carga no cambia los totales.
  Integridad y claves foráneas comprobadas.
- Presentación regenerada en PDF, PPTX y HTML: 10 diapositivas con notas alineadas,
  capturas de hilos y texto editable en PowerPoint; XML, relaciones y navegación
  verificados por el generador y vista general revisada visualmente.

Las pruebas se ejecutaron con bases temporales y con una copia para verificar
la migración. La base de destino se respalda antes de aplicar la integración.
No se probó Auth0 con cuentas reales, despliegue ni apertura en PowerPoint.

La primera corrida de pytest usó una carpeta temporal cuyo padre aún no existía;
se corrigió la ubicación y la suite completa aprobó. Los apartados siguientes
conservan evidencias anteriores de la aplicación de origen.


## Correcciones vigentes — 13/10/2026

Entorno: Windows, Python **3.13.14**, Chrome **155.0.8059.41**. Proyecto:
`pignatelli-iisaia/tp_final`. No se agregaron dependencias.

Comandos ejecutados desde `tp_final` (con el Python de `.venv`):

```powershell
$env:COVERAGE_FILE = 'artifacts/coverage-v2'
.\.venv\Scripts\python.exe -m pytest -q --tb=short --basetemp=artifacts/test-run-20261013-c -o cache_dir=artifacts/pytest-cache --cov=backend --cov-fail-under=90
.\.venv\Scripts\python.exe -m ruff check backend tests scripts run.py
.\.venv\Scripts\python.exe -m scripts.browser_smoke
```

Resultados reales:

```text
79 passed, 2 warnings
TOTAL: 581 statements, 8 missing; coverage 98.62%
All checks passed!

browser: 155.0.8059.41
threads_flow: passed
five_overviews: passed
attachments_download: passed
csv: passed
persistence: passed
mobile_overflow: false
javascript_errors: []
```

Las pruebas nuevas cubren migración v1→v2 repetida sin duplicados y rollback ante
fallo de migración; estados derivados; conteos globales; orden de pasos; edición;
subida, persistencia, descarga y backup de bytes; límites de archivos y cantidad;
rechazo de extensiones y links no permitidos; jerarquía entre muestras/hilos/pasos;
autenticación de descarga, permisos de lector y CSRF; rollback de upload si falla
la auditoría; JSON Schema de las nuevas respuestas y OpenAPI válido.

En navegador se recorrieron los cinco indicadores, se creó un hilo con dos pasos,
se editaron estados y se cargaron evidencias de ejemplo (PDF, PNG, PPTX y URL),
verificando transporte y descarga, no validez interna de los formatos. Se comprobó
persistencia al recargar, eliminación y cancelación, CSV y error de conexión.
Capturas revisadas a 1440 px y 390 px:

- `artifacts/threads-v2/desktop.png`
- `artifacts/threads-v2/mobile.png`

La primera ejecución de pytest no pudo usar algunos temporales/cachés heredados
de la carpeta movida. Se eligieron rutas nuevas de prueba dentro de `artifacts/`,
sin cambiar permisos globales. La suite detectó también el desfase del schema del
resumen al añadir `in_progress`; se corrigió en el generador del contrato.

Se mantienen las dos advertencias de deprecación de httpx de Authlib/Starlette.
No se probaron tenant real Auth0, despliegue ni CI remoto. No se tocó la base de
trabajo: el servidor aplica la migración al próximo inicio.

## Antecedente — verificación inicial del 30/09/2026

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

## Demo A0/A1/A2 — 14/10/2026

- Pytest: **82 aprobados**, cobertura backend **98,62%**. Incluye carga sobre base
  poblada, preservación de ediciones/borrados al repetir, rollback y reintento,
  distribución de estados y descarga de las nueve evidencias sintéticas por API.
- Ruff check y format --check: correctos, 29 archivos con formato válido.
- Chrome 155.0.8059.41: cinco listados, flujo de hilos/pasos, archivos y descarga,
  CSV y persistencia correctos; sin errores JavaScript ni desborde móvil.
- Carga local efectiva en `data/lab.db`: 3 chips, 12 hilos, 36 pasos, 9 CSV,
  60 altas auditadas; `PRAGMA integrity_check` devolvió `ok`.
- Backup previo: `data/backups/antes-demo-20261014-024615-672674.db`.

Los tests y el navegador usan bases temporales; la carga local fue una operación
separada y aditiva. Persisten avisos de deprecación de httpx en Starlette/Authlib;
no se cambiaron dependencias. No hubo cambios de interfaz ni de contrato API.
