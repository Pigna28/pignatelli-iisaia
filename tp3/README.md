# TP3 — IC Bring-up Lab

Aplicación web para registrar muestras físicas de circuitos integrados y sus ensayos
de caracterización en las macros **Tx, Rx y PLL**. Implementa el contrato del TP2
con interfaz, persistencia SQLite, autenticación Auth0 y trazabilidad de cambios.

**Verificación local:** 52 pruebas aprobadas, 99% de cobertura del backend,
flujo completo en Chrome y revisión visual en escritorio y móvil.
Ver [evidencia y límites](docs/verification.md).

## Ejecutar en Windows

Requiere Python 3.11 o superior. Probado con Python 3.13.3. Desde la raíz del repositorio:

```powershell
cd tp3
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe run.py
```

Abrir **http://127.0.0.1:8000**. No hace falta activar el entorno virtual ni cambiar
la política de ejecución de PowerShell. Si `python` abre Microsoft Store, usar
`py -3` o la ruta del intérprete instalado para crear el entorno.

En esta carpeta de trabajo ya se creó `.venv` y se instalaron las dependencias;
alcanza con el último comando para arrancar. El entorno virtual no se versiona.

En Linux/macOS, reemplazar `.\.venv\Scripts\python.exe` por `.venv/bin/python`.
El archivo lock conserva todas las versiones verificadas, incluyendo herramientas
de desarrollo; `requirements.txt` contiene solamente dependencias de ejecución.
La primera instalación necesita internet. La interfaz funciona sin CDN; `/docs`
usa el Swagger UI por CDN que proporciona FastAPI.

### Datos de demostración opcionales

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_demo
```

Carga 3 muestras y 12 ensayos **sintéticos**, solo en modo local y si no existen
muestras. No carga datos automáticamente al iniciar. La base está en `data/lab.db`.

### Autenticación

Sin configuración se usa **modo local**, identificado en pantalla, sin identidad
real y limitado a conexiones loopback. Sirve para la demostración en la computadora.
`APP_ENV=production` rechaza ese modo. No es una configuración para publicar.

Para Auth0, copiar `.env.example` a `.env` y seguir [la guía](docs/auth0.md).
El servidor valida configuración al arrancar. Todas las cuentas autenticadas
pueden leer el laboratorio; únicamente los `sub` incluidos en `WRITE_SUBJECTS`
pueden crear, borrar y consultar la auditoría. La cuenta de Auth0 no está incluida.

## Uso

1. Registrar una muestra con número de parte y placa. El servidor asigna su ID.
2. Seleccionar la muestra y la macro Tx, Rx o PLL.
3. Registrar métrica, valor, unidad y dictamen. Las fechas son opcionales.
4. Filtrar aprobados/fallidos y exportar **la vista actual** a CSV.
5. Consultar la bitácora. Eliminar un chip borra sus ensayos en cascada y conserva
   una copia en auditoría, dentro de la misma transacción.

El buscador filtra por parte o placa. Las métricas superiores resumen todo el
laboratorio, independientemente de la muestra o filtro. Las fechas de ensayos
se almacenan en UTC y se muestran en hora local. `passed` es el dictamen del operador:
el sistema no deduce si una magnitud eléctrica cumple especificación.

## Arquitectura y contrato

Un solo proceso sirve HTML/CSS/JavaScript y FastAPI. SQLite usa conexiones por
request, claves foráneas, índice por chip/macro/resultado y WAL. El frontend
consume los endpoints originales, sin agregarles `/api`.

| Método | Ruta | Éxito | Uso |
|---|---|---|---|
| GET | `/chips` | 200 | Listar muestras |
| POST | `/chips` | 201 | Registrar muestra |
| DELETE | `/chips/{chipId}` | 204 | Borrar muestra y ensayos |
| GET | `/chips/{chipId}/macros/{macro}/tests?passed=true` | 200 | Listar/filtrar |
| POST | `/chips/{chipId}/macros/{macro}/tests` | 201 | Registrar ensayo |
| DELETE | `/chips/{chipId}/macros/{macro}/tests/{testId}` | 204 | Borrar ensayo |
| GET | `/summary` | 200 | Contadores globales |
| GET | `/audit?limit=20&before=123` | 200 | Auditoría paginada, solo operadores |
| GET | `/session` | 200 | Identidad, permisos y token CSRF |
| POST | `/logout` | 200 | Cerrar sesión y obtener URL de salida |
| GET | `/health` | 200 | Comprobar acceso a la base, público |

Errores JSON: `{"error":"mensaje"}`. `400` entrada inválida, `401` sesión ausente,
`403` permiso/CSRF, `404` recurso o relación inexistente, `503` base no disponible.
Las escrituras requieren cookie y header `X-CSRF-Token` obtenido de `/session`,
incluso en modo local. Los IDs y macros viajan en el path, nunca en el body de alta.
No se admiten campos extra, strings vacíos, valores no finitos ni timestamps sin zona.
Omitir las fechas desconocidas en lugar de enviar `null`.

[openapi.yaml](openapi.yaml) es el contrato canónico 1.1.0 servido en `/openapi.json`,
`/openapi.yaml` y `/docs`. [opeanapi.yaml](opeanapi.yaml), con la grafía original,
se conserva intacto como antecedente 1.0.0. El generador
`python -m scripts.build_contract` aplica las extensiones documentadas al original.

### Ejemplo desde PowerShell

Con el servidor en modo local:

```powershell
$session = Invoke-RestMethod http://127.0.0.1:8000/session -SessionVariable lab
$headers = @{ 'X-CSRF-Token' = $session.csrf_token }
$chip = Invoke-RestMethod http://127.0.0.1:8000/chips -Method Post -WebSession $lab -Headers $headers -ContentType 'application/json' -Body '{"part_number":"CHIP001","board":"EVK-1"}'
$url = "http://127.0.0.1:8000/chips/$($chip.id)/macros/Tx/tests"
Invoke-RestMethod $url -Method Post -WebSession $lab -Headers $headers -ContentType 'application/json' -Body '{"metric":"gain","measured_value":12.5,"unit":"dB","passed":true}'
Invoke-RestMethod "${url}?passed=true" -WebSession $lab
```

## Estructura

```text
tp3/
├── backend/             configuración, auth, schemas, SQLite, rutas y aplicación
├── frontend/            interfaz y módulos api/ui/app sin build
├── tests/               contrato, API, seguridad, concurrencia y operación
├── scripts/             seed, backup, contrato y prueba de navegador
├── docs/                especificación, plan, decisiones, operación y defensa
├── AGENTS.md            contexto persistente e invariantes para futuras sesiones
├── openapi.yaml         contrato vigente
├── opeanapi.yaml         contrato original conservado
├── requirements*.txt    dependencias y versiones verificadas
├── .env.example         configuración sin secretos
└── run.py               arranque local
```

La referencia `tp-referencia/` se conserva sin modificar y no forma parte del servidor.
El workflow de GitHub Actions está en `../.github/workflows/tp3-ci.yml`.

## Verificar

```powershell
.\.venv\Scripts\python.exe -m pytest -q --cov=backend --cov-fail-under=90
.\.venv\Scripts\python.exe -m ruff check backend tests scripts run.py
.\.venv\Scripts\python.exe -m ruff format --check backend tests scripts run.py
.\.venv\Scripts\python.exe -m scripts.browser_smoke
```

La última prueba usa Chrome instalado, una base temporal y un servidor propio en un
puerto libre. No usa `.env` ni toca datos del laboratorio. Genera capturas en
`artifacts/desktop.png` y `artifacts/mobile.png`. Si no hay Chrome:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
$env:BROWSER_CHANNEL = ''
.\.venv\Scripts\python.exe -m scripts.browser_smoke
```

## Decisiones y proceso

El dominio, las macros y los seis endpoints provienen del TP2 del alumno. El stack
se toma del TP de referencia. Las extensiones propuestas en esta implementación
son: permisos de escritura, CSRF, auditoría, exportación, pruebas automáticas,
backup consistente, configuración explícita y CI. Ver [decisiones y alternativas](docs/architecture.md).

La especificación y el plan se escribieron antes del código de la aplicación.
La implementación se dividió en módulos y se verificó por etapas. Los archivos
`AGENTS.md` conservan contexto para siguientes sesiones. [prompts.md](prompts.md)
distingue el pedido real de las decisiones inferidas y de prompts sugeridos.
Los informes previos están conservados en [docs/history](docs/history/README-tp2.md).

### Qué falló y qué se corrigió

- **SQLite en hilos distintos:** los tests secuenciales pasaban, pero Chrome hizo
  `/chips` y `/summary` en paralelo y expuso una conexión usada desde otro worker.
  Se habilitó el uso entre hilos manteniendo una conexión exclusiva por request,
  se agregó una prueba concurrente y se repitió el flujo real.
- **Prueba de cookie demasiado prescriptiva:** suponía que cada lectura de sesión
  reemitía `Set-Cookie`. La versión instalada solo lo necesitó al crear la sesión.
  Se verifican sus atributos en el callback donde realmente se emite.
- **Python en PATH:** apuntaba al alias de Windows Store. Se usó el intérprete
  instalado para crear `.venv`; no se cambiaron configuraciones globales.

No se fabricaron commits, PRs, decisiones del alumno ni reviews de subagentes.
El material describe un flujo con plugins; aquí se ejecutaron herramientas directas.
La defensa requiere que el alumno revise y pueda explicar las decisiones.

## Documentación de entrega

- [Especificación](docs/spec.md) y [plan](docs/plan.md).
- [Arquitectura y decisiones](docs/architecture.md).
- [Configuración Auth0](docs/auth0.md).
- [Operación, backup y diagnóstico](docs/operations.md).
- [Trazabilidad con la materia y guion de defensa](docs/defense.md).
- [Verificación y límites](docs/verification.md).
- [Mejoras priorizadas](docs/roadmap.md).

## Alcance pendiente externo

Se implementó y verificó localmente la aplicación. Falta configurar y probar el
tenant real de Auth0, publicar el repositorio y ejecutar su CI, y desplegar si se
requiere acceso remoto. La carpeta solicitada es `tp3`; algunos apuntes indican
`tp-final` y contienen criterios administrativos contradictorios entre semanas.
Confirmar formato de entrega e integrantes con la cátedra. No se afirma que haya
una rúbrica formal completa en los archivos disponibles.
