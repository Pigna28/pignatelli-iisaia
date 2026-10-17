# Plan y aceptación

1. Leer contrato, referencia y consignas. Fijar alcance en `spec.md`.
2. Implementar configuración, almacenamiento versionado, schemas y API original.
   Aceptación: flujo completo, validación 400, jerarquía 404 y cascada.
3. Integrar autenticación y autorización. Aceptación: pruebas de 401/403,
   CSRF, callback inválido y logout; configuración cerrada en producción.
4. Implementar interfaz de laboratorio. Aceptación: alta, selección, filtros,
   exportación y borrado; estados visibles y adaptación a pantalla angosta.
5. Mantener contrato canónico y añadir health, sesión, resumen y auditoría.
   Aceptación: validación OpenAPI y respuestas contrastadas contra schemas.
6. Completar pruebas, lint, guía de ejecución, defensa y operación.
   Aceptación: evidencia real en `verification.md`, límites expresos.

El plan se registra antes del código de la aplicación. No se inventarán commits,
reviews de subagentes ni ejecuciones de plugins que no hayan ocurrido.

## Ampliación: conjunto para exposición

1. Preparar un JSON reproducible de ocho muestras y 48 ensayos sintéticos.
2. Ampliar la carga explícita: validación previa, auditoría y transacción única;
   conservar el rechazo sobre bases ocupadas salvo `--append`, sin duplicar cargas.
3. Verificar escenarios por API, integridad, rollback, repetición y backup.
4. Respaldar la base local, agregar el conjunto y documentar resultados y guion.

## Entrega en la carpeta v2

Conservar el código de la copia indicada, trasladar el JSON y el cargador de demo,
ampliar la presentación con carga reproducible y backup, verificarla y concentrar
los entregables dentro de la raíz v2.

## Corrección de la entrega v2 — 14/10/2026

La entrega había quedado basada en la aplicación anterior. Se integra el código
ya existente de hilos, pasos, tres estados y evidencias desde la copia de trabajo
más reciente; se preservan la presentación y los prompts editados por el usuario.

1. Incorporar backend, frontend, migración v1→v2, contrato y pruebas existentes.
2. Usar la campaña A0/A1/A2 como demo vigente; conservar el JSON y cargador históricos.
3. Probar migración de una copia de la base existente, carga adicional y repetición.
4. Alinear documentación, capturas, presentación y notas con el flujo de hilos.
5. Respaldar archivos y base de destino antes de integrar los cambios; verificar
   que todas las mediciones previas siguen presentes, sin sobrescribirlas.
