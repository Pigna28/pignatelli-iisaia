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
