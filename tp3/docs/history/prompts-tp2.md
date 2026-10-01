# Registro de Prompts — TP2 (Contrato OpenAPI)

Secuencia de prompts utilizados en una única conversación de IA para generar e iterar el contrato `openapi.yaml` de la API **IC Bring-up Lab**.

---

## Prompt 1: Especificación inicial del contrato (Recursos, Schemas y Endpoints)

En este primer prompt busqué dictarle a la IA el bloque de contrato completo de la API aplicando el vocabulario de la clase: definí los recursos en plural (`chips` y `tests`), la jerarquía anidada usando las 3 macros internas fijas (`Tx`, `Rx`, `PLL`) como subdirectorios en el path, la separación entre schemas de entrada (`ChipInput`, `TestInput`) y de salida (`Chip`, `Test`), los tipos y formatos de datos (`date`, `date-time`, `float`, `enum`), el filtro opcional por query (`?passed`) y los códigos de estado HTTP (`200`, `201`, `204`, `400`, `404`).

```text
Necesito que generes un archivo openapi.yaml (estándar OpenAPI 3.1.0) para una API REST de Bring-up de circuitos integrados en laboratorio.

El sistema registra distintas muestras físicas de un mismo chip ('chips'). Cada chip posee internamente 3 macros fijas ('Tx', 'Rx', 'PLL'), las cuales funcionan como subdirectorios en la ruta para organizar de forma separada los ensayos de caracterización ('tests', como gain, bandwidth, SNR, etc.) ejecutados sobre cada bloque.

# Recursos y Schemas:
1. 'Chip':
- 'id': integer (requerido, asignado por el servidor)
- 'part_number': string (requerido, por ejemplo "CHIP001")
- 'board': string (requerido, como "EVK-1")
- 'assembled_at': string con format: date (opcional)
2. 'ChipInput': Mismos campos que 'Chip', excluyendo 'id'.
3. Test:
- 'id': integer (requerido, asignado por el servidor)
- 'chip_id': integer (requerido, tomado del parámetro {chipId} del path)
- 'macro': string con 'enum: ["Tx", "Rx", "PLL"]' (requerido, tomado del parámetro {macro} del path)
- 'metric': string (requerido, nombre del parámetro medido)
- 'measured_value': number con 'format: float' (requerido)
- 'unit': string (requerido, como por ejemplo "dB", "MHz", "dBc/Hz")
- 'passed': boolean (requerido)
- 'measured_at': string con format: date-time (opcional)
4. 'TestInput': Incluye únicamente los datos transportados en el body: 'metric', 'measured_value', 'unit', 'passed' (requeridos) y 'measured_at' (opcional). Excluye 'id', 'chip_id' y 'macro' porque los asigna el servidor o ya viajan identificados en el path.
5. 'Error':
- 'error': string (requerido, mensaje descriptivo del problema)

# Endpoints requeridos ('paths'):
1. 'GET /chips'
- Salida '200': array de objetos 'Chip'.
2. 'POST /chips'
- Entrada (body): 'ChipInput' (JSON).
- Salida '201': objeto 'Chip' creado.
- Salida '400': 'Error' (si faltan campos requeridos).
3. 'GET /chips/{chipId}/macros/{macro}/tests'
- Parámetros de path: 'chipId' (integer, requerido) y 'macro' (string con 'enum: ["Tx", "Rx", "PLL"]', requerido).
- Parámetro de query: 'passed' (boolean, opcional, para filtrar mediciones aprobadas o fallidas dentro de esa macro).
- Salida '200': array de objetos 'Test'.
- Salida '400': 'Error' (si el valor de '{macro}' no es Tx, Rx o PLL).
- Salida '404': 'Error' (si el chip 'chipId' no existe).
4. 'POST /chips/{chipId}/macros/{macro}/tests'
- Parámetros de path: 'chipId' (integer, requerido) y 'macro' (string con 'enum: ["Tx", "Rx", "PLL"]', requerido).
- Entrada: 'TestInput' (JSON).
- Salida '201': objeto 'Test' creado.
- Salida '400': 'Error' (datos de entrada inválidos en el body o macro fuera del enum).
- Salida '404': 'Error' (si el chip 'chipId' no existe).
5. 'DELETE /chips/{chipId}/macros/{macro}/tests/{testId}'
- Parámetros de path: 'chipId' (integer, requerido), 'macro' (string con 'enum: ["Tx", "Rx", "PLL"]', requerido) y 'testId' (integer, requerido).
- Salida '204': Sin contenido (borrado exitoso).
- Salida '404': 'Error' (si el chip o el ensayo no existen en esa macro).

Devuélveme únicamente el bloque de código YAML válido en OpenAPI 3.1.0 utilizando referencias $ref hacia 'components/schemas'.
```

---

## Prompt 2: Corrección tras auditoría en Swagger Editor e iteración de endpoints

Luego de validar el primer YAML en `editor.swagger.io`, lo cuál resultó muy útil como herramienta de verificación, noté que había algunos detalles a corregir, como se explican en el `README.md`. Con este segundo prompt, busqué solucionar los warnings, agregar la respuesta `400` faltante en el `DELETE` de ensayos e iterar el contrato sumando el endpoint `DELETE /chips/{chipId}` sin reescribir el diseño desde cero.

```text
Al validar el archivo generado en Swagger Editor encontré unos detalles para corregir. Además quiero iterar el contrato sumando un endpoint nuevo:

En los schemas usaste la propiedad 'example:' en singular, lo cual arroja advertencias de deprecación en OpenAPI 3.1.0. Reemplaza todos los 'example:' por 'examples:' en formato de array (por ejemplo, 'examples: ["CHIP001"]').
En 'DELETE /chips/{chipId}/macros/{macro}/tests/{testId}', agregá la respuesta '400' referenciando a '#/components/schemas/Error' (por si el parámetro '{macro}' no pertenece al enum '["Tx", "Rx", "PLL"]'), tal como ya está en el GET y en el POST.
Nuevo endpoint para dar de baja un chip: Agregá el path /chips/{chipId} con el método delete (bajo el tag Chips, con operationId: deleteChip), que reciba el parámetro $ref: '#/components/parameters/ChipId' y permita eliminar una muestra física y todos sus ensayos asociados. Debe documentar las respuestas '204' (Chip y ensayos asociados eliminados exitosamente, sin contenido) y '404' (#/components/schemas/Error si el chip indicado no existe).
Devolveme el bloque de código openapi.yaml completo y actualizado sin omitir ninguna sección.
```