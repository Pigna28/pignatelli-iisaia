# Registro de contexto y prompts — TP3

## Antecedentes

Los prompts originales del contrato TP2 se conservan sin cambios en
[docs/history/prompts-tp2.md](docs/history/prompts-tp2.md).
El contrato original es [opeanapi.yaml](opeanapi.yaml).

## Pedido real de esta implementación

> Basate en el tp de referencia en tp3\tp-referencia
> Quiero que basado en el contexto de la implementacion en los documentos openapi.yal, readme y promps en la carpeta tp3 realices:
>
> La totalidad del tp, documentacion y demás complementos necesarios, determina que complementos tareas y añadidos pueden darse para que la implemetacion tome profesionalismo y sea capaz de implementar todos los conceptos que se buscan.
>
> A demás tienes en la carpeta IISAIA-main los documentos de la materia por si necesitas consultar material

## Contexto utilizado

1. README, prompts y contrato originales de `tp3` para preservar el dominio.
2. README, código Auth0 y dependencias de `tp-referencia` para estudiar el ejemplo.
3. Material de semanas 00, 04 y 05 para identificar producto completo, contexto,
   evidencia de proceso, planificación y verificación.
4. Documentación oficial de FastAPI y Authlib para contrastar integración y pruebas.

## Decisiones propuestas por el agente

Se adoptaron FastAPI, SQLite estándar y JavaScript nativo. Se mantuvieron las rutas
originales y se sumaron resumen, sesión y auditoría. Se eligió Auth0 en servidor,
autorización por subject, CSRF y modo local exclusivamente loopback.
Se agregaron seed explícito, CSV, backup, CI y pruebas. Estas decisiones se tomaron
bajo la autorización general del pedido; no fueron respuestas del usuario a un
cuestionario ni decisiones históricas suyas.

## Iteración observada

- Especificación y plan en disco antes de los módulos de aplicación.
- Primera suite: 37 aprobadas y 1 falla en la expectativa de reemisión de cookie.
- Corregida la prueba: 38 aprobadas.
- Primer flujo en Chrome: falla SQLite por cambio de hilo del worker.
- Corrección del ciclo de conexiones y regresión concurrente: flujo aprobado.
- Suite ampliada: 52 aprobadas y 99% de cobertura del backend.

Las pruebas se escribieron después de los primeros módulos: este trabajo no se
presenta como una ejecución TDD estricta. No se ejecutaron subagentes ni el plugin
Superpowers. Tampoco se generó un historial Git artificial.

## Prompts sugeridos para continuar (no ejecutados)

### Agregar una métrica sin alterar el contrato

“Leé AGENTS.md y docs/spec.md. Proponé un catálogo opcional de métricas y unidades,
conservando TestInput y los registros existentes. Separá sugerencias de validaciones
obligatorias y mostrámelas antes de cambiar el comportamiento.”

### Diagnosticar una regresión

“Reproducí el defecto con una prueba que falle, identificá la causa y corregí el
módulo mínimo. No cambies el contrato para hacer pasar la prueba. Ejecutá la
regresión y las verificaciones afectadas; informá evidencia real.”

### Preparar la defensa

“Usá docs/defense.md para preguntarme por una decisión a la vez. Pedime explicar
el camino de una request desde el formulario hasta SQLite y detectar qué pasa
cuando falla la auditoría. No respondas por mí antes de que lo intente.”

## Correcciones solicitadas — 13/10/2026

Pedido real del usuario, sobre `tp_final/README.md` y `tp_final/prompts.md`:

```text
Correcciones a realizar:

1. Debería añadirse la seccion de En progreso (amarillo)
2. Las secciones de muestras registradas, ensayos realizados, aprobados y fallidos deberían poder enviar a una subseccion donde se especifiquen todos los realizados
3. Los ensayos realizados para cada muestra deberían ser un hilo de pruebas, no una en particular. Dentro de este hilo se debería poder cargar documentos en cada paso, como presentaciones, links o imagenes
4. Actualiza el promps y el README cuando termines las correcciones
```

### Implementación de la corrección

Se localizó el proyecto activo en `pignatelli-iisaia/tp_final`, dado que el directorio
de trabajo anterior `IISAIA` ya no contenía el TP. Se preservó la aplicación existente
y se registró el diseño en `docs/changes-2026-10-13.md` antes de extender el modelo.

- Se agregó el indicador amarillo En progreso y navegación a listados globales
  desde los cinco indicadores, con acceso al detalle de cada muestra/hilo.
- Se reemplazó la UI de ensayos individuales por hilos de pruebas con pasos
  cronológicos, notas, estado editable, medición opcional y evidencias por paso.
- Se implementaron carga/descarga de archivos y enlaces HT../pignatelli-iisaia/tp_final/HTTPS, con controles
  de sesión, permisos, CSRF, jerarquía y límites de tamaño/cantidad.
- Se agregó una migración transaccional v1→v2: cada medición previa se convierte en
  un hilo de un paso, conservando los datos. No se agrupó por supuesta campaña.
- Se actualizaron contrato OpenAPI 2.0.0, README y documentación de operación.

### Decisiones de implementación inferidas

El usuario pidió el estado y los hilos, pero no definió cómo agregar los resultados.
Se eligió: algún paso fallido → hilo fallido; sin fallos, vacío o pasos pendientes
→ en progreso; todos aprobados → aprobado. Los indicadores cuentan hilos, no pasos.

Se eligieron archivos dentro de SQLite (backup y cascada atómicos), límite de
10 MiB por archivo y 20 evidencias por paso. Se permiten documentos, presentaciones
e imágenes comunes; las descargas son forzadas y autenticadas. No se agregó un
servicio externo, nuevas dependencias ni un antivirus. Estas son decisiones del
agente dentro del alcance pedido, no requisitos textuales del usuario.

### Evidencia y ajustes

La primera ejecución de pytest encontró permisos heredados en el directorio
temporal y la caché de la instalación movida. Se usaron directorios nuevos dentro
de `artifacts/` sin alterar permisos globales. Después, el test del contrato detectó
que faltaba `in_progress` en el schema de resumen: se actualizó junto con la API.

Resultado final de backend: **79 pruebas aprobadas**, **98,62% de cobertura**;
lint aprobado. En Chrome se verificaron los cinco listados, creación y edición
de pasos, cambio de estado, cargas de PDF/imagen/presentación, enlaces, descarga,
persistencia tras recarga, CSV, confirmación de borrados y errores de red.
Las capturas desktop/móvil se revisaron visualmente. Ver `docs/verification.md`.

Las pruebas usaron bases temporales y no migraron ni borraron datos de trabajo.
El servidor debe reiniciarse para aplicar los cambios y migrar su base al esquema v2.

## Pedido del 14/10/2026: pool inicial de demostración

> Añade un pull inicial de chips y pruebas iniciales para demostrar funcionalidad
> Chips A0 A1 A2
> Hilos mixtos de ancho de banda ganancia ruido y consumo con distintos pasos en distintas etapas.

Se interpretó «pull» como un pool de datos iniciales. Se implementó una campaña
sintética de 3 chips, 12 hilos, 36 pasos y 9 archivos CSV de evidencia. Decisiones
de implementación: cuatro hilos por chip, cuatro hilos por estado global y etapas
de preparación, medición y revisión. Los pendientes se distinguen mediante notas;
el modelo existente conserva sus tres estados. Los valores no son especificaciones
eléctricas ni mediciones reales.

La carga usa el modelo de hilos directamente y un marcador en auditoría para no
duplicar ni sobrescribir la campaña. Se ejecuta solo en desarrollo local y permite
bases pobladas. Cada alta y su auditoría comparten la transacción. No se ejecuta
automáticamente al arrancar.

Verificación: 82 tests aprobados, cobertura backend 98,62%, Ruff y formato correctos.
Chrome verificó navegación, pasos, evidencias, exportación y persistencia con esta
demo en una base temporal. Se cargó además en `data/lab.db`, con backup previo en
`data/backups/antes-demo-20261014-024615-672674.db`, 60 altas auditadas e integridad
SQLite correcta. README y especificación actualizados.
