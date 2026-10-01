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
