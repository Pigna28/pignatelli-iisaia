# Demo de la entrega v2

La demo vigente muestra **hilos de ensayo**, con preparación, medición y revisión.
Se incluyen tres chips (A0, A1 y A2), doce hilos, treinta y seis pasos y nueve
archivos CSV de evidencia. Hay cuatro hilos por estado: Aprobado, Fallido y En progreso.
Los valores son ficticios para la exposición.

## Cargar y ejecutar

Desde `pignatelli-iisaia-main_v2/tp_final`:

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_demo
.\.venv\Scripts\python.exe run.py
```

Abrir http://127.0.0.1:8000. Si estaba abierto el servidor anterior, detenerlo y
reiniciarlo desde **esta carpeta**. Recargar el navegador. La pantalla debe tener
cinco indicadores, incluido **En progreso** en amarillo, y el botón **Nuevo hilo**.

La carga agrega la campaña sin borrar lo que ya existe. Repetirla conserva los
cambios manuales y no duplica ni repone muestras eliminadas. `--append` se acepta
por compatibilidad, aunque la demo vigente siempre conserva registros anteriores.

Para una base separada con solamente A0/A1/A2:

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_demo --database data/demo-v2.db
$env:DATABASE_PATH = 'data/demo-v2.db'
.\.venv\Scripts\python.exe run.py
```

Al terminar ese servidor, quitar la selección con `Remove-Item Env:DATABASE_PATH`.
La base habitual es `data/lab.db`; todas las rutas quedan dentro de esta entrega.

## Recorrido para exponer

1. Abrir el indicador **En progreso** y ver que reúne hilos de distintas muestras.
2. Elegir **Ganancia — A0**: preparación aprobada, medición en progreso y revisión
   pendiente. Explicar que un ensayo reúne varios pasos, no solo un resultado.
3. Agregar una nota y cambiar un paso. El estado del hilo se calcula a partir de
   sus pasos: cualquier fallo lo deja Fallido; sin fallos, algún pendiente lo deja
   En progreso; todos aprobados lo dejan Aprobado.
4. Abrir **Ancho de banda — A0**, desplegar la evidencia y descargar su CSV.
   Mostrar que también se puede adjuntar un PDF, una imagen o un enlace por paso.
5. Volver al listado, filtrar por estado y exportar los hilos visibles a CSV.
6. Buscar A1 o A2 y abrir otro indicador. Recargar para comprobar el guardado.
7. Consultar la bitácora para mostrar altas, modificaciones y bajas.

## Qué se guarda y dónde

`data/lab.db` contiene muestras, hilos, pasos, notas, archivos adjuntos y bitácora.
Los archivos cargados quedan dentro de SQLite; los enlaces guardan nombre y URL.
`artifacts/` contiene capturas y salidas de comprobaciones. Los backups se hacen con:

```powershell
.\.venv\Scripts\python.exe -m scripts.backup data/backups/antes-demo.db
```

## Demo anterior y conservación

La primera demo, `fixtures/demo_lab.json`, tenía 8 muestras y 48 mediciones.
Se conserva, con el cargador `scripts/seed_measurements_legacy.py`. Las mediciones
anteriores pasan a hilos de un paso sin alterar sus valores ni agruparlas por inferencia.
Si esa demo estaba cargada, al agregar A0/A1/A2 quedan **11 muestras y 60 hilos:
42 aprobados, 14 fallidos y 4 en progreso**. Si hay datos propios, también se conservan
y los contadores los incluyen. El detalle A0/A1/A2 está en [demo-data.md](demo-data.md).
