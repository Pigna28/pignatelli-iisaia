# Registro de Prompts y Decisiones — TP3

Este documento registra los prompts que utilicé para que la IA programe el código del servidor web y la base de datos, basándose en el contrato OpenAPI que diseñé previamente para el laboratorio de *bring-up*.

## 1. Creación del Servidor y Base de Datos Base

**Qué buscabamos obtener:**
Queríamos levantar el servidor rápido en la terminal de Visual Studio Code para probarlo con el frontend en Vanilla JS. Por eso le pedimos a la IA que use **FastAPI** (porque lee los esquemas solos y valida los tipos de datos) y **SQLite** (porque guarda todo en un archivo local sin tener que instalar motores de bases de datos complejos).

**El prompt utilizado:**
> "Tengo este archivo `openapi.yaml` que define una API para registrar muestras de chips y sus mediciones. Necesito que programes el backend usando FastAPI y SQLite. 
> Reglas estrictas:
> - Respetá exactamente las rutas, los métodos (GET, POST, DELETE) y los esquemas JSON que están en el YAML.
> - Creá las tablas en SQLite relacionando los ensayos con los chips mediante una clave foránea (foreign key) para que un ensayo no pueda existir sin su chip.
> - Si un dato viene mal en el body, el servidor debe devolver error 400. Si piden un chip que no existe, debe devolver 404."

---

## 2. Iteración: Agregando estados y carga de evidencias

**Qué buscabamos obtener:**
Validada la primera instrucción, nos dimos cuenta de que un ensayo de laboratorio no se hace en un solo paso. Necesitabamos que los ensayos fueran "hilos" con pasos cronológicos, que tuvieran estados (Aprobado, Fallido, En progreso) y que los ingenieros pudieran adjuntar imágenes o PDFs de las mediciones del instrumental. 

**El prompt utilizado:**
> "Necesitamos iterar el diseño de la base de datos y los endpoints:
> 1. Modificá los ensayos para que ahora tengan 3 estados posibles: 'Aprobado', 'Fallido' o 'En progreso'. 
> 2. Actualizá el GET de resumen para que cuente cuántos ensayos hay en cada uno de estos 3 estados.
> 3. Agregá un endpoint nuevo que permita subir archivos (imágenes o PDFs de hasta 10 MB) para adjuntarlos como evidencia a un ensayo específico. Estos archivos deben guardarse localmente.
> Escribí el código para actualizar la base de datos de SQLite con estos cambios sin borrar los chips que ya teníamos cargados."

**Corrección posterior:**
Al probar el código que devolvió la IA, los archivos temporales se guardaban con problemas de permisos y la ruta de respuesta (`schema-out`) del resumen no mostraba el estado 'En progreso'. Para eso, solicitamos que se cree una carpeta dedicada llamada `artifacts/` para guardar los archivos, y que corrija el esquema JSON de salida para cumplir el contrato.

---

## 3. Preparación de la base de datos para la demo

**Qué buscábamos obtener:**
Necesitábamos datos de ejemplo para mostrar las funcionalidades del TP durante la exposición. La idea era poder recorrer la aplicación con casos variados, sin tener que cargar cada chip y ensayo a mano.

**El prompt utilizado:**
> "Necesito que generes un set de datos base para este TP, representativo de las funcionalidades para una exposición.
> - Cargá muestras de chips con ensayos de Tx, Rx y PLL, incluyendo resultados aprobados y fallidos.
> - Agregá reensayos, muestras con pruebas incompletas y otras sin ensayos.
> - Los datos tienen que servir para mostrar la búsqueda, los filtros, la exportación a CSV y la bitácora.
> - Usá datos ficticios y dejá un script para volver a cargar la demo.
> - Conservá los datos que ya existan y evitá que la demo se duplique si ejecuto el script más de una vez."

**Resultado obtenido:**
La primera demo contenía 8 muestras y 48 mediciones (38 aprobadas y 10 fallidas),
con origen en `fixtures/demo_lab.json`. Ese conjunto se conserva como antecedente;
su cargador es `scripts/seed_measurements_legacy.py`.

Para representar el flujo de hilos se incorporó la campaña A0/A1/A2 mediante
`scripts/seed_demo.py`: 3 muestras, 12 hilos con 36 pasos y 9 archivos CSV, con
4 hilos aprobados, 4 fallidos y 4 en progreso. El script conserva datos anteriores
y no duplica la campaña. Las mediciones de la primera demo se migran sin borrarlas.

**Corrección de la entrega:** la carpeta v2 había quedado basada en una copia
anterior sin hilos; se integró el código vigente y se ajustaron demo y presentación.

Los archivos adjuntos de la implementación vigente quedan dentro de `data/lab.db`;
`artifacts/` reúne capturas y salidas de verificación, no los adjuntos de los pasos.
