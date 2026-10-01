# OpenAPI: el contrato escrito

Durante toda la clase venimos hablando del **contrato**: las cinco piezas que un endpoint compromete antes de que exista una sola línea de implementación. Method, path, qué entra, qué sale, qué errores. Esa idea, hasta ahora, vivía en una pizarra o en tu cabeza. La industria le puso nombre y formato hace tiempo: se llama **OpenAPI**, y la versión vigente es la 3.1. Es el estándar para describir una API REST de punta a punta. Si ya escribiste el bloque del §4, ya pensaste en OpenAPI sin saberlo.

## Las cinco piezas tienen keys oficiales

El bloque del §4 tenía cinco casilleros: `method`, `path`, `schema-in`, `schema-out` (uno por status code) y errores. OpenAPI les puso nombres concretos y los acomodó en un yaml. El mapeo es uno a uno:

- `method` → la key HTTP (`get`, `post`, `delete`...) anidada bajo `paths`.
- `path` → las keys de `paths`, con `{id}` para variables (igual que como las dictabas en clase).
- `schema-in` → un `requestBody` con el schema del body.
- cada `schema-out` → una entry dentro de `responses`, indexada por código (`'201'`, `'400'`, `'404'`).
- los errores son responses como cualquier otro: 400 y 404 no son adornos, son contrato.

Mirá el bloque del §4 — el `POST /projects/{id}/tasks` con `title` requerido, `due_date` opcional, 201/400/404 — y mirá este fragmento:

```yaml
paths:
  /projects/{id}/tasks:
    post:
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title]
              properties:
                title:    { type: string }
                due_date: { type: string, format: date }
      responses:
        '201': { description: Tarea creada }
        '400': { description: Body inválido }
        '404': { description: Project no existe }
```

Es la misma información del §4. Misma decisión sobre qué es requerido, mismos códigos posibles, mismo recurso anidado. Lo único que cambió es el formato: pasaste de un bloque informal a un archivo que cualquier herramienta del mundo sabe leer.

## Por qué es un archivo y no un prompt

Que el contrato sea un yaml en lugar de un mensaje en un chat te compra tres cosas concretas. Vale la pena pensarlas una por una.

**Menos ambigüedad para la IA.** Un prompt vago — "armame un endpoint para crear tareas con título y fecha" — deja diez decisiones al modelo. ¿`title` admite string vacío? ¿`due_date` es ISO completa o solo fecha? ¿qué pasa si mandás `null`? Cada una de esas preguntas la responde el modelo por su cuenta, distinta cada vez. El yaml las fija de una vez: `type`, `format: date`, `required`, `nullable`. Lo que dejás escrito deja de inventarse en cada generación.

**Codegen real, no abstracto.** Del mismo archivo salen artefactos distintos sin tipear código. Lo pegás en `editor.swagger.io` y aparecen docs interactivas con un "Try it" funcional. Le decís a una IA "generame un cliente TypeScript desde este yaml" y aparece el cliente. Pedís mocks para que el frontend trabaje sin esperar al backend, aparecen los mocks. Pedís tests de contrato, aparecen los tests. Una sola fuente, muchos artefactos derivados — eso es lo que la palabra **codegen** significa cuando deja de ser marketing.

**Durabilidad.** Un prompt se evapora cuando cerrás la conversación. Un yaml vive en el repo, se versiona en git, se compara entre branches, se le hace code review en un pull request. Si mañana querés cambiar `due_date` a `date-time`, no tenés que volver a dictarle todo el contexto a la IA: editás una línea del archivo y ya. El supervisor arquitectónico ahora dirige un artefacto durable en lugar de un prompt que se pierde.

## El espejo se cierra

En semana 02 el átomo dictable era un componente con sus props y su estado. En esta clase el átomo dictable fue el bloque de contrato. Ahora ese bloque tiene archivo, y la próxima clase lo agarramos y se lo damos a una IA local para que escriba la implementación. Lo que cambió no es el rol — seguís diciendo qué querés y la IA escribe sintaxis. Lo que cambió es que ahora lo que decís queda anclado en un archivo que sobrevive a la conversación.

Cuando le pidas a la IA "armame el `openapi.yaml` para una API de proyectos y tareas con estos endpoints…", el contrato queda fijado y la implementación deriva de ahí. Esa es la diferencia entre dictarle a la IA cada vez desde cero y dictarle una vez sobre un artefacto que ya existe.
