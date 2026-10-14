# Demo A0, A1 y A2

Pedido del 14/10/2026: un pool inicial de chips con hilos mixtos y pasos en
distintas etapas. Implementación: carga explícita local, transaccional y auditada;
conservar muestras existentes y no repetir ni sobrescribir la campaña al ejecutarla
otra vez. El marcador de campaña permanece en auditoría incluso si se eliminan muestras.

Cada chip tiene cuatro hilos con preparación, medición y revisión. Los hilos en
progreso alternan preparación, adquisición y revisión. Los valores y dictámenes
son sintéticos, no especificaciones eléctricas reales. Las mediciones completadas
incluyen un CSV de evidencia. No se insertan mediciones en la API histórica.

| Chip | Ancho de banda (Tx) | Ganancia (Tx) | Ruido (Rx) | Consumo (PLL) |
|---|---|---|---|---|
| A0 | Aprobado | En progreso (medición) | Fallido | Aprobado |
| A1 | En progreso (preparación) | Aprobado | En progreso (revisión) | Fallido |
| A2 | Fallido | Fallido | Aprobado | En progreso (medición) |

Aceptación: 3 chips, 12 hilos, 36 pasos y 9 CSV; 4 hilos por estado.
Probar carga en base vacía y poblada, repetición después de editar, rollback
si falla auditoría, API y navegación usando el nuevo conjunto. Cargar finalmente
la demo en la base local configurada y actualizar README/prompts.
