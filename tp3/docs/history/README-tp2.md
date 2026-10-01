# TP2 — Especificación de Contrato OpenAPI: IC Bring-up Lab API

## 1. Descripción de la API y Dominio Elegido
**IC Bring-up Lab API** es el contrato de un backend REST diseñado para gestionar el proceso de *bring-up* y caracterización eléctrica de circuitos integrados en un laboratorio, con el objetivo de llevar registro de las mediciones/caracterizaciones identificadas por chip, en un solo lugar.

En este flujo de trabajo se reciben múltiples muestras físicas de un mismo diseño de chip (`chips`), cada una identificada por su número de parte (`part_number`) y montada en una placa o kit de evaluación (`board`). Todas las muestras comparten una arquitectura interna fija compuesta por **3 macros (`Tx`, `Rx` y `PLL`)**, sobre las cuales los ingenieros ejecutan distintos ensayos de caracterización (`tests`, tales como mediciones de ganancia, ancho de banda, SNR, etc.).

---

## 2. Decisiones Arquitectónicas

Para evitar que la IA tomara decisiones silenciosas sobre el comportamiento del servidor, se fijaron explícitamente los siguientes criterios de diseño REST y HTTP:

1. **Jerarquía estructural y subdirectorios por Macro (`/chips/{chipId}/macros/{macro}/tests`):**
   * Un ensayo de caracterización no tiene existencia autónoma fuera de la muestra física y del bloque interno sobre el cual se midió. Por ello, en lugar de una ruta plana, se anidaron los recursos.
   * Dado que las macros de la arquitectura son fijas (`Tx`, `Rx`, `PLL`), no tiene sentido exponer un `POST` o `DELETE` de macros; en su lugar, `{macro}` se modeló como un segmento de ruta restringido mediante `enum: ["Tx", "Rx", "PLL"]` dentro de `components/parameters/Macro`.
2. **Separación entre Path, Query y Body (*"Path identifica, Query ajusta, Body transporta"*):**
   * **Path:** `{chipId}`, `{macro}` y `{testId}` viajan en la URL para identificar inequívocamente el recurso.
   * **Query:** En `GET /chips/{chipId}/macros/{macro}/tests` se incorporó el parámetro opcional `?passed=true|false` para ajustar el pedido filtrando ensayos aprobados o fallidos sin alterar la jerarquía del recurso.
   * **Body (`*Input` vs Schemas de salida):** Se separaron los esquemas de creación (`ChipInput` y `TestInput`) de los esquemas de respuesta (`Chip` y `Test`). En un `POST`, el cliente nunca envía el `id` (lo asigna automáticamente el servidor para evitar colisiones) ni repite en el JSON del body los datos que ya viajaron en el path (`chip_id` y `macro`). Sin embargo, la respuesta `201 Created` sí devuelve el objeto completo con el `id` generado para que el cliente pueda utilizarlo inmediatamente sin necesidad de hacer un `GET` adicional.
3. **Semántica de Métodos HTTP, Idempotencia y Status Codes:**
   * Se emplearon `GET` (200 OK) y `DELETE` (204 No Content) como operaciones idempotentes, y `POST` (201 Created) para la creación no idempotente de chips y ensayos.
   * Se diferenciaron explícitamente los errores de cliente: `400 Bad Request` cuando el body incumple los campos requeridos (`required`) o cuando `{macro}` no pertenece al `enum` válido, y `404 Not Found` cuando el `{chipId}` o `{testId}` solicitado no existe.
4. **Tipado estricto en Schemas:**
   * Además de los tipos primitivos (`integer`, `string`, `number`, `boolean`), se especificaron formatos estándar (`format: float` para el valor medido, `format: date` para la fecha de ensamblado y `format: date-time` ISO 8601 para la marca temporal del ensayo) y listas `required` explícitas para diferenciar atributos obligatorios de opcionales (`assembled_at` y `measured_at`).

---

## 3. Qué salió mal en la primera iteración y cómo se corrigió

Al verificar la primera versión generada por la IA y validarla en **Swagger Editor (`editor.swagger.io`)**, se detectaron dos problemas que fueron corregidos mediante un segundo prompt iterativo:

1. **Advertencias de deprecación en OpenAPI 3.1.0:**
   * **Problema:** En el primer resultado, la IA utilizó el atributo `example:` en singular dentro de las propiedades de los schemas `Chip`, `ChipInput`, `Test` y `TestInput`. Si bien esto era válido en OpenAPI 3.0, en la especificación OpenAPI 3.1.0 `example` ya no se usa, y es algo que Swagger me hizo notar mediante _warnings_.
   * **Solución:** Se le indicó al modelo reemplazar todas las ocurrencias por `examples:` en formato de array.
2. **Omisión del código `400` en el borrado de ensayos e iteración del contrato:**
   * **Problema:** En el primer YAML, la IA documentó correctamente el error `'400'` (macro fuera del enum `Tx, Rx, PLL`) en el `GET` y en el `POST` de `/chips/{chipId}/macros/{macro}/tests`, pero omitió documentar ese mismo `'400'` en el endpoint `DELETE /chips/{chipId}/macros/{macro}/tests/{testId}`, el cual también recibe `{macro}` en el path.
   * **Solución:** En el segundo prompt se exigió agregar la respuesta `'400'` al `DELETE` de ensayos para mantener la consistencia del contrato, y se aprovechó la iteración para incorporar el endpoint `DELETE /chips/{chipId}` para un borrado en cascada de una muestra y sus ensayos asociados.