# TP final — IC Bring-up Lab

Aplicación web para registrar muestras físicas de circuitos integrados y sus
**hilos de ensayo** en las macros **Tx, Rx y PLL**. Cada hilo contiene una secuencia
de pasos con notas, estado, mediciones opcionales y evidencias: documentos,
presentaciones, imágenes o enlaces. Incluye SQLite, Auth0 y auditoría de cambios.

**Verificación actual (14/10/2026):** 82 pruebas aprobadas, 98,62% de
cobertura del backend; flujo de hilos, indicadores y archivos probado en Chrome,
con revisión visual de escritorio y móvil.
Ver [evidencia y límites](docs/verification.md).

## Correcciones incorporadas

- **En progreso, en amarillo**, tanto en el indicador global como en hilos y pasos.
- **Cinco indicadores navegables:** muestras, todos los ensayos, en progreso,
  aprobados y fallidos. Cada uno abre una subsección con todos sus registros,
  independiente de la muestra seleccionada. Desde allí se abre la muestra o el hilo.
- **Ensayos como hilos:** alta de hilo, pasos ordenados, edición de notas y estados,
  medición opcional y carga de evidencias en cada paso.
- **Migración automática v1→v2:** cada medición existente se conserva como un hilo
  de un paso. No se agrupan resultados históricos sin conocer su campaña original.

Si el servidor estaba abierto, **reiniciarlo** para cargar el código nuevo y aplicar
la migración; luego recargar el navegador. Para una base con datos reales, hacer
primero un backup con `python -m scripts.backup data/backups/antes-v2.db`.
Las pruebas usan bases temporales. La campaña sintética A0/A1/A2 se cargó también
en la base local de trabajo el 14/10/2026, con backup previo y sin borrar registros.

## Ejecutar en Windows

Requiere Python 3.11 o superior. Correcciones probadas con Python 3.13.14. Desde la raíz del repositorio:

```powershell
cd tp_final
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

Carga los chips **A0, A1 y A2**, con **12 hilos, 36 pasos y 9 evidencias CSV
sintéticas**: ancho de banda y ganancia en Tx, ruido en Rx y consumo en PLL.
Hay **4 hilos aprobados, 4 fallidos y 4 en progreso**, con etapas de preparación,
medición y revisión. Ver [distribución por chip](docs/demo-data.md).

Solo se permite en modo local de desarrollo. Se puede ejecutar con muestras
existentes: agrega la campaña sin modificarlas. Repetir el comando conserva las
ediciones y no duplica la demo; si se eliminan sus muestras, tampoco las recrea.
El marcador de carga queda en auditoría y cada alta se audita en una transacción.
No carga datos automáticamente al iniciar. Usa `DATABASE_PATH` o `data/lab.db`
por defecto. Recargar la página y abrir los indicadores para explorar los hilos.
Los valores y resultados son ejemplos, no criterios eléctricos reales.

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
3. Crear un hilo con título y objetivo; comienza **En progreso**.
4. Abrirlo y agregar pasos: título, notas, estado y, si corresponde, métrica/valor/unidad.
5. En cada paso, usar **Adjuntar evidencia** para subir un archivo o guardar un enlace.
6. Usar **Editar paso** para actualizar notas, medición o estado. La auditoría conserva
   el antes y el después. Los pasos se muestran en orden de creación.
7. Filtrar hilos por estado, exportar **la lista actual de hilos** a CSV, o entrar a
   los listados globales haciendo clic en cualquiera de los cinco indicadores.
8. Consultar la bitácora. Eliminar un chip, hilo o paso elimina en cascada sus
   descendientes. La auditoría conserva datos y metadatos, **no los archivos binarios**.

El buscador filtra por parte o placa. Los indicadores resumen todo el laboratorio;
cada hilo cuenta una vez, aunque contenga muchos pasos. **Ensayos realizados** es
el total de hilos, incluidos los que siguen en progreso.

El estado del hilo se deriva de sus pasos: **Fallido** si alguno falla; en ausencia
de fallos, **En progreso** si no tiene pasos o queda alguno en progreso; **Aprobado**
si todos están aprobados. El operador decide el estado de cada paso; la aplicación
no inventa límites eléctricos. Las fechas se guardan en UTC y se muestran en hora local.

### Archivos y enlaces

Hasta **10 MiB por archivo** y **20 evidencias por paso** (archivos y enlaces juntos).
Se admiten PDF, PPT/PPTX, DOC/DOCX, XLS/XLSX, TXT/CSV, PNG/JPG/JPEG/WEBP/GIF.
Los enlaces deben ser HTTP o HTTPS, sin credenciales embebidas; no se descargan
automáticamente. Los archivos quedan dentro de SQLite, por lo que el backup los incluye.
Se descargan autenticados, conservando su nombre, mediante descarga forzada; no hay
ejecución, previsualización de documentos ni análisis antivirus del contenido.
Los lectores pueden consultar/descargar; solo los operadores pueden cargar o eliminar.

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

### API de hilos (versión 2.0.0)

Usar `B = /chips/{chipId}/macros/{macro}/threads` para la siguiente tabla:

| Método | Ruta | Uso |
|---|---|---|
| GET | `/threads?status=in_progress` | Listado global y filtros `in_progress`, `passed`, `failed` |
| GET / POST | `B` | Listar / crear hilos de la muestra y macro |
| GET / DELETE | `B/{threadId}` | Detalle con pasos y evidencias / eliminar hilo |
| POST | `B/{threadId}/steps` | Agregar un paso |
| PUT / DELETE | `B/{threadId}/steps/{stepId}` | Reemplazar datos del paso / eliminarlo |
| POST | `B/{threadId}/steps/{stepId}/attachments/links` | Agregar nombre y URL |
| POST | `B/{threadId}/steps/{stepId}/attachments/files` | Subir binario y header `X-Filename` codificado como URL |
| GET | `B/{threadId}/steps/{stepId}/attachments/{attachmentId}/download` | Descargar archivo |
| DELETE | `B/{threadId}/steps/{stepId}/attachments/{attachmentId}` | Eliminar evidencia |

Los POST devuelven 201, las lecturas y PUT 200 y los DELETE 204.
`/summary.tests` cuenta hilos y se cumple `tests = in_progress + passed + failed`.
Los endpoints `/tests` se conservan como API histórica y están marcados deprecated:
sus altas crean un hilo de un paso, pero las mediciones originales archivadas no
se sobrescriben al editar pasos. El frontend usa exclusivamente `/threads`.

Errores JSON: `{"error":"mensaje"}`. `400` entrada inválida, `401` sesión ausente,
`403` permiso/CSRF, `404` recurso o relación inexistente, `413` archivo demasiado grande,
`503` base no disponible.
Las escrituras (POST, PUT, DELETE) requieren cookie y header `X-CSRF-Token` obtenido
de `/session`, incluso en modo local. Los IDs y macros viajan en el path.
No se admiten campos extra, strings vacíos, valores no finitos ni timestamps sin zona.
En la API histórica se omiten las fechas desconocidas. En los pasos, los campos
de medición opcionales admiten null; métrica, valor y unidad se completan juntos.
PUT reemplaza los datos editables de un paso y no modifica sus evidencias.

[openapi.yaml](openapi.yaml) es el contrato canónico 2.0.0 servido en `/openapi.json`,
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

El ejemplo anterior ilustra la API histórica del TP2; el alta genera automáticamente
un hilo de un paso. Para el flujo actual, usar la interfaz o los endpoints de hilos
documentados en `/docs`.

## Estructura

```text
tp_final/
├── backend/             auth, SQLite, migraciones, hilos, pasos, evidencias y rutas históricas
├── frontend/            interfaz y módulos api/ui/app/thread-view sin build
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
La ejecución remota de CI no se verificó en esta corrección.

## Verificar

```powershell
.\.venv\Scripts\python.exe -m pytest -q --cov=backend --cov-fail-under=90
.\.venv\Scripts\python.exe -m ruff check backend tests scripts run.py
.\.venv\Scripts\python.exe -m ruff format --check backend tests scripts run.py
.\.venv\Scripts\python.exe -m scripts.browser_smoke
```

La última prueba usa Chrome instalado, una base temporal y un servidor propio en un
puerto libre. No usa `.env` ni toca datos del laboratorio. Genera capturas en
`artifacts/threads-v2/desktop.png` y `artifacts/threads-v2/mobile.png`. Si no hay Chrome:

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
- [Diseño y aceptación de las correcciones de hilos](docs/changes-2026-10-13.md).

## Alcance pendiente externo

Se implementó y verificó localmente la aplicación. Falta configurar y probar el
tenant real de Auth0, publicar el repositorio y ejecutar su CI, y desplegar si se
requiere acceso remoto. La carpeta actual es `tp_final`; algunos apuntes indican
`tp-final` y contienen criterios administrativos contradictorios entre semanas.
Confirmar formato de entrega e integrantes con la cátedra. No se afirma que haya
una rúbrica formal completa en los archivos disponibles.
