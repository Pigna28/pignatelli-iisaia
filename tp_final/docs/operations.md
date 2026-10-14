# Operación y diagnóstico

## Configuración

`.env` se carga desde la raíz de `tp_final`, sin reemplazar variables ya presentes en el
proceso. `DATABASE_PATH` relativo se resuelve contra `tp_final`, no contra el directorio
actual de la terminal. `BASE_URL` define origen, callback y host permitido.
No incluye path, credenciales ni query. En desarrollo el servidor local usa el
puerto de BASE_URL o 8000.

| Variable | Default | Efecto |
|---|---|---|
| AUTH_MODE | local | local / auth0 |
| APP_ENV | development | development / production |
| BASE_URL | http://127.0.0.1:8000 | Origen público y URLs de Auth0 |
| DATABASE_PATH | data/lab.db | Archivo SQLite |
| SESSION_SECRET | efímero solo en local | Firma de cookie; obligatorio en Auth0 |
| AUTH0_DOMAIN | vacío | Host del tenant |
| AUTH0_CLIENT_ID | vacío | Identificador de aplicación |
| AUTH0_CLIENT_SECRET | vacío | Credencial privada del servidor |
| WRITE_SUBJECTS | vacío | Lista de operadores por subject |

## Backup y restauración

Desde `tp_final`, con el Python de su entorno:

```powershell
.\.venv\Scripts\python.exe -m scripts.backup data/backups/lab-2026-09-30.db
```

El script usa la API de backup de SQLite, por lo que incluye cambios del WAL y
es consistente aunque la aplicación siga abierta. Verifica `integrity_check` y
rechaza destinos existentes. Proteger el backup igual que la base: contiene
mediciones y subjects de operadores. Copiarlo a un almacenamiento independiente
según la política del laboratorio. La aplicación no agenda ni envía backups.

Para restaurar sin sobrescribir datos:

1. Detener el servidor con Ctrl+C.
2. Elegir un backup cuyo `integrity_check` sea `ok` y copiarlo con un nombre nuevo,
   por ejemplo `data/restored-lab.db`.
3. Cambiar `DATABASE_PATH=data/restored-lab.db` en `.env`.
4. Arrancar, revisar `/health`, inventario y ensayos. Conservar la base anterior.

No copiar solamente `lab.db` mientras el servidor escribe: SQLite usa también
archivos `-wal` y `-shm`. No editar ni borrar esos archivos con el proceso activo.

## Esquema y migraciones

El esquema vigente usa `PRAGMA user_version=2`. El arranque crea el esquema inicial
si la versión es cero y migra v1→v2 para agregar hilos, pasos y archivos. Cada
medición histórica conserva sus valores en un hilo de un paso. La migración es
transaccional: ante error revierte las tablas nuevas y conserva la versión anterior.
Versiones desconocidas se rechazan. Hacer un backup antes de actualizar una base real.
Los archivos subidos son BLOB en SQLite y quedan incluidos en el backup normal.
Al eliminar una evidencia se borran sus bytes; la auditoría solo conserva metadatos.
Para futuros cambios: backup, migración transaccional versionada y prueba con copia.
Nunca introducir un `DROP TABLE` automático como mecanismo de actualización.

## Observabilidad

Con `run.py`, el logger `lab` registra ID de request, método, path, estado y duración.
La respuesta incluye `X-Request-ID`. No se registran bodies, cookies, secretos ni
query del callback. Los logs de acceso de Uvicorn se desactivan para evitar que
el código OAuth de la URL se registre por separado. `audit` registra las mutaciones
con subject, timestamp UTC y snapshot; su API solo está disponible para operadores.

`/health` es público y comprueba la tabla chips. No comprueba Auth0, backups, espacio
disponible ni todos los objetos del esquema: no reemplaza monitoreo operativo.

## Problemas frecuentes

| Síntoma | Acción |
|---|---|
| Python abre Microsoft Store | Usar `py -3` o el ejecutable instalado |
| Puerto ocupado / WinError 10013 | Revisar qué proceso usa el puerto; elegir otro BASE_URL y ajustar Auth0 |
| 400 de Auth0 al volver | Comparar esquema, hostname, puerto y `/callback` exactos |
| Usuario puede leer pero no guardar | Revisar WRITE_SUBJECTS y reiniciar; no usar el email como subject |
| 403 CSRF | Recargar para renovar `/session`; scripts deben conservar cookie y token juntos |
| 400 en una medición | Revisar booleano real, número finito, campos requeridos y zona de measured_at |
| 404 al borrar ensayo | Verificar simultáneamente chip, macro y testId |
| 503 de SQLite | Revisar permisos, disco y procesos escritores; evitar red de archivos compartida |
| No carga Swagger | `/docs` requiere CDN; consultar `/openapi.yaml` local |

## Despliegue orientativo, no ejecutado

Usar `AUTH_MODE=auth0`, `APP_ENV=production`, `BASE_URL=https://dominio`, secreto
aleatorio estable y almacenamiento persistente para SQLite. Terminar TLS en un
proxy del mismo servidor y ejecutar un worker en loopback:

```text
python -m uvicorn backend.main:create_app --factory --host 127.0.0.1 --port 8000 --no-proxy-headers --no-access-log
```

La aplicación construye URLs de Auth0 desde BASE_URL; no necesita confiar en headers
reenviados. El proxy debe preservar Host y gestionar TLS, límites de tamaño de
request, rate limiting y logs que no incluyan códigos OAuth. Configurar también
el logger `lab` del proceso si no se usa `run.py`. No publicar el modo local ni
conectar SQLite por un filesystem de red. Para carga de escritura alta, evaluar
PostgreSQL y sesiones revocables. No se provisionó un servidor externo.
