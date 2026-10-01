# Trazabilidad y defensa

## Relación con los conceptos de la materia

| Concepto | Evidencia del TP | Explicación para la defensa |
|---|---|---|
| Supervisor arquitectónico | spec, plan, contrato original y decisiones | Qué venía fijado y qué propuso la IA |
| Contexto finito y persistencia de instrucciones | AGENTS.md raíz/backend/frontend | Abrir solo el módulo y documento pertinente |
| Tokens y selección de contexto | Fuentes resumidas en spec y docs, sin copiar todo el curso | Más contexto no implica mejor supervisión |
| HTML semántico, CSS, componentes | index.html, styles.css, diálogos, labels y tablas | Separación de estructura, presentación y comportamiento |
| Estado y eventos | app.js y ui.js | Qué cambia al seleccionar chip, macro o filtro |
| Cliente/servidor y HTTP | api.js + rutas FastAPI | Request, JSON, respuesta y error de red |
| REST, recursos, path/query/body | Seis endpoints originales | Macro y chip en path; passed en query; medición en body |
| Contrato OpenAPI | openapi.yaml y test_contract.py | Cómo se evita que cada capa invente campos |
| Relaciones y persistencia | chips 1:N tests, FK y cascada | Diferencia entre chip vacío y chip inexistente |
| Errores y observabilidad | 400/401/403/404/503, request ID, auditoría | Mensajes para usuario y evidencia para diagnóstico |
| Autenticación y autorización | auth.py y tests | Identidad de Auth0 vs permiso de operador |
| Planificación previa | docs/spec.md, docs/plan.md | Criterios de aceptación antes del código de aplicación |
| Loop de herramientas y verificación | pruebas, Chrome, capturas | El fallo concurrente escapó a los tests secuenciales |
| Skills reutilizables | .agents/skills/verificar-lab/SKILL.md | Procedimiento de preentrega; no confundir con configuración de permisos |
| Permisos de herramientas | Instalación aislada en .venv y aprobación de descarga | Un AGENTS.md orienta al modelo, no implementa un sandbox |
| GitHub Flow y CI | Workflow preparado, entrega Git pendiente | No fabricar commits ni fingir PR/review ejecutados |
| Subagentes y plugins | No usados en esta implementación | Son opciones de organización; no requisitos del runtime del producto |
| MCP | Decisión de no añadir integración redundante | Las herramientas disponibles ya permitían archivos, shell y navegador |

La skill de preentrega queda como artefacto reutilizable del proyecto; su formato
fue validado. Las verificaciones de esta entrega se ejecutaron directamente.
No se afirma que la skill se haya descubierto automáticamente en una sesión nueva.

## Fuentes de la materia

- [Trabajo final, semana 04](../../IISAIA-main/semanas/04/source_material/14-trabajo-final.md):
  interfaz + backend + persistencia, apropiación y defensa de decisiones.
- [Flujo aplicado al TP, semana 05](../../IISAIA-main/semanas/05/source_material/15-bajada-al-tp-final.md):
  spec, plan, verificación y evidencia de proceso.
- [Cómo se aprueba](../../IISAIA-main/semanas/00/source_material/02-como-se-aprueba.md):
  README como informe y no fabricar historial al final.
- [Skills y comandos](../../IISAIA-main/semanas/04/source_material/11-skills-y-slash-commands.md):
  procedimiento reutilizable y carga de contexto según necesidad.
- [Permisos](../../IISAIA-main/semanas/04/source_material/10-permisos.md):
  instrucciones del modelo no equivalen a restricciones del runtime.
- [Cuándo MCP y riesgos](../../IISAIA-main/semanas/06/source_material/10-cuando-mcp-y-riesgos.md):
  evitar duplicar capacidades nativas sin una necesidad concreta.

No todos los recursos de la materia fijan una obligación de implementación.
Algunos textos administrativos discrepan (individual vs grupos, tp3 vs tp-final).
Confirmar esos puntos con la cátedra; esta matriz no inventa una rúbrica oficial.

## Guion sugerido de demostración — 8 minutos

1. **Problema (1 min):** una muestra física contiene tres macros y múltiples
   ensayos. Mostrar por qué el número de parte no identifica la muestra.
2. **Recorrido (2 min):** alta de muestra, ensayo Tx aprobado, ensayo Rx fallido,
   filtro, CSV, recarga y persistencia.
3. **Contrato (1 min):** explicar un POST con path, body y respuesta 201; provocar
   una macro inválida (400) y un chip inexistente (404).
4. **Integridad (1 min):** mostrar que un test no puede borrarse desde otra macro.
   Borrar muestra, observar cascada y snapshot en la bitácora.
5. **Identidad (1 min):** explicar modo local y Auth0, lector/operador y CSRF.
   Si no se configuró tenant, mostrar pruebas simuladas y decirlo explícitamente.
6. **Proceso (1 min):** abrir plan y pruebas; explicar fallo de SQLite en navegador,
   corrección y prueba concurrente.
7. **Límites (1 min):** SQLite, arrays sin paginación, sesiones firmadas y roadmap.

## Preguntas que el alumno debería poder responder

- ¿Por qué `chip_id` no aparece en TestInput?
- ¿Por qué no existen POST/DELETE de macros?
- ¿Qué ocurre si falla el INSERT de auditoría después de insertar el ensayo?
- ¿Por qué DELETE puede devolver 204 primero y 404 después y seguir siendo idempotente?
- ¿Qué diferencia hay entre iniciar sesión y tener permiso para borrar?
- ¿Por qué SameSite no reemplaza la comprobación CSRF del servidor?
- ¿Por qué una fecha sin zona puede alterar la interpretación de una medición?
- ¿Qué bug puede causar una respuesta tardía al cambiar rápidamente de chip?
- ¿Qué demuestra el 99% de cobertura y qué NO demuestra?
- ¿Qué habría que cambiar para conectar un instrumento o manejar diez laboratorios?

La apropiación se demuestra explicando, corrigiendo y extendiendo el código.
No presentar este guion como evidencia de una defensa ya realizada.
