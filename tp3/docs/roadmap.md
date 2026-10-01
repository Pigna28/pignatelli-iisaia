# Complementos y evolución priorizada

## Ya incorporados

Interfaz adaptable, búsqueda, filtros, contadores, CSV con escape de fórmulas,
validación estricta, persistencia, índice relacional, cascada, auditoría atómica,
Auth0, permisos por subject, CSRF, cabeceras de seguridad, request IDs, modo local
delimitado, seed explícito, backup verificado, contrato comprobado, pruebas de
navegador, CI preparado y contexto/documentación para nuevas sesiones.

## P0 — Antes de compartir fuera de la computadora

| Tarea | Criterio de cierre |
|---|---|
| Configurar tenant real | Login, lector, operador, cancelación y logout probados con Auth0/Google |
| Publicar repositorio y ejecutar CI | Workflow verde visible; secretos y bases excluidos |
| Desplegar HTTPS | Cookie Secure, Auth0 con origen final, almacenamiento persistente |
| Limitar requests en proxy | Límites de body y tasa probados; errores no filtran credenciales |
| Ensayar restauración real | Backup recuperado en otra ruta y datos verificados |
| Definir retención de auditoría | Responsable y política de archivo documentados |

## P1 — Para uso habitual del laboratorio

| Mejora | Valor | Cambio requerido |
|---|---|---|
| Serial de muestra y lote | Trazabilidad física inequívoca | Campo adicional, migración e importación de existentes |
| Catálogo de métricas y unidades | Evitar variaciones tipográficas | Sugerencias UI primero; no rechazar históricos |
| Límites de aceptación versionados | Calcular passed con criterio reproducible | Especificación, unidad y versión junto a cada medición |
| Temperatura, alimentación, instrumento y calibración | Contexto metrológico | Modelo de condiciones y validación de equipos |
| Paginación en chips y tests | Evitar listas y CSV gigantes | Contrato versionado; exportación completa en servidor |
| Sesiones en servidor | Revocación individual | Almacenamiento de sesiones, vencimiento y rotación |
| Actualizar cliente HTTP | Resolver deprecaciones actuales | Ensayar migración de httpx a cliente soportado por Authlib/Starlette |

## P2 — Escala e integración

PostgreSQL y migraciones incrementales, separación por laboratorio con autorización
por recurso, importación CSV con vista previa y reporte de errores, adquisición
SCPI/PyVISA en un servicio separado, adjuntos de curvas y certificados, límites
versionados y alertas, métricas operativas y pruebas de carga.

Un MCP propio tendría sentido si se necesitan consultas recurrentes del agente
sobre datos del laboratorio. Empezar con tools de lectura (`list_chips`,
`list_measurements`) y recursos de contrato. No exponer borrados por defecto ni
entregar acceso directo a SQLite sin autorización y trazabilidad.

La adquisición automática, los umbrales eléctricos y la multiempresa requieren
información de dominio adicional. Implementarlos por suposición podría producir
resultados de ingeniería incorrectos. No forman parte del alcance actual.
