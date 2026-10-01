# Especificación de implementación — IC Bring-up Lab

## Fuentes y alcance

La petición autoriza completar `tp3` partiendo de su contrato y del ejemplo
`tp-referencia`. El dominio lo fijó el usuario en TP2: muestras físicas,
macros inmutables Tx/Rx/PLL y mediciones. Se adopta del ejemplo la arquitectura
de un proceso FastAPI, SQLite, frontend sin build y login OIDC con Auth0.
Las extensiones de esta especificación son propuestas implementadas por el agente,
no decisiones históricas atribuidas al alumno.

## Criterios de aceptación

1. Crear/listar/eliminar muestras; crear/listar/filtrar/eliminar mediciones.
2. Conservar los seis endpoints originales, sus campos, arrays y códigos HTTP.
   Usar `/chips` tal como el contrato, sin imponer el prefijo `/api` del ejemplo.
3. Validar tipos, fechas y jerarquía. Rechazar campos extra, NaN, textos vacíos,
   timestamps sin zona y booleanos o números enviados como strings en JSON.
4. Persistir en SQLite con claves foráneas, borrado en cascada y transacciones.
5. Interfaz en español, adaptable, navegable con teclado, con estados de carga,
   vacío, error, confirmación de borrado, búsqueda, métricas y exportación CSV.
6. Auth0 por servidor, sesión firmada HttpOnly, autorización de escritura por
   subject, CSRF, logout sin reingreso automático. Modo local identificado,
   restringido a loopback, rechazado en producción.
7. Auditoría transaccional de cada mutación, sin tokens ni secretos.
8. Tests aislados: contrato, integridad, seguridad, autenticación simulada,
   persistencia y flujo de navegador. Reportar qué se ejecutó realmente.
9. Documentar instalación, configuración, decisiones, defensa, operación,
   trazabilidad con la materia y trabajo futuro priorizado.

## Límites deliberados

Laboratorio compartido: lectores ven todas las muestras; operadores autorizados
pueden escribir sobre todas. No hay aislamiento multiempresa. `passed` es el
dictamen del operador; no se inventan umbrales eléctricos. Números de parte pueden
repetirse porque identifican el diseño y no necesariamente la muestra física.
No hay edición de resultados: borrar y registrar conserva evidencia de ambas acciones.
No hay adquisición desde instrumentos ni certificación metrológica.
El login real requiere un tenant y credenciales del titular.
