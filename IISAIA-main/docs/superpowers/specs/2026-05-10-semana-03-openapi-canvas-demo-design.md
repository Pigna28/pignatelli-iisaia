# Semana 03 — Cierre con OpenAPI + ChatGPT canvas demo

**Status:** Design approved, ready for implementation plan
**Date:** 2026-05-10
**Affects:** `semanas/03/`

## Goal

Replace the closing third of semana 03 (sections §7 and §8) so the class lands on **OpenAPI as the formalization of the "contrato"** introduced in §4, climaxing with a live demo where ChatGPT canvas authors an `openapi.yaml` for the projects/tasks domain and the resulting yaml gets rendered in Swagger UI.

The current §7 ("De lo local al stack" — Python/FastAPI/SQLite/Uvicorn + CLI rationale + install homework) and §8 (Claude Code builds a FastAPI server live) are retired.

## Why

- The whole-week through-line of semana 03 is "supervisor arquitectónico también del lado del servidor — vos dictás el contrato, la IA implementa." OpenAPI is literally that contract as a versioned, machine-readable artifact, so it strengthens the through-line rather than introducing a new concept at the end.
- Semana 04's source material lists Cursor + Antigravity (not Claude Code), so the existing §7's "install Claude Code before next class" homework is already mismatched.
- The Claude Code FastAPI demo had narrative weight but didn't visibly close the contract loop — students saw code appear, not the contract itself become an artifact. Canvas + Swagger UI close that loop visibly.

## Scope

### In scope
- Rebuild §7 (8 slides → 3 slides), retitled "OpenAPI: el contrato escrito"
- Rebuild §8 (6 slides → 5 slides), retitled "Demo en vivo: canvas escribe el openapi.yaml"
- Patch 7 small touchpoints across §1–§6 where the deleted §7/§8 was set up or previewed
- Rewrite `spine.md` whole-week through-line and §7/§8 entries
- Replace `source_material/07-*.md` and `source_material/08-*.md`
- Update `source_material/index.md`

### Out of scope
- §1–§6 conceptual content (only the 7 mechanical patches listed below)
- Semana 04 setup homework wording — placeholder in §8.5 footer; finalize when semana 04 plan firms up
- Animation contracts, theme CSS, shared patterns library — reuse existing components only

## Narrative framing

OpenAPI is positioned as **the contract from §4, formalized**. Same five pieces (method, path, schema-in, schema-out, error codes), now in YAML. The §7.2 side-by-side slide makes the mapping explicit:

| §4 vocabulary  | OpenAPI keyword                |
| -------------- | ------------------------------ |
| `method`       | HTTP-method key under `paths`  |
| `path`         | `paths` keys                   |
| `schema-in`    | `requestBody`                  |
| `schema-out`   | `responses`                    |
| error codes    | response keys (`'400'`, `'404'`) |

§4's `schema-in` / `schema-out` vocabulary stays unchanged in §1–§6. The OpenAPI keywords are introduced in §7.2 as the concrete spelling, with `schema-in` / `schema-out` retained as the conceptual labels. This is pedagogically stronger than retconning §4.

## Domain

The canvas demo evolves the exact contract block from §4: `POST /projects/{id}/tasks` with `title` (required), `due_date` (optional), returning 201/400/404. The full openapi.yaml the demo will produce covers:

```
GET    /projects
POST   /projects
GET    /projects/{id}/tasks
POST   /projects/{id}/tasks         → 201 / 400 / 404
DELETE /projects/{id}/tasks/{taskId}
```

This satisfies the demo's five visible requirements: three methods, hierarchical resources, at least one error response, typed schemas, room for live iteration.

## Per-slide design

### §7 — OpenAPI: el contrato escrito (3 slides)

#### §7.1 — Section opener
- H2: `Pieza 6 — OpenAPI` (matches `Pieza N — X` pattern from §2.1, §3.1, §4.1, §5.1, §6.1)
- Roadmap pipe-diagram with `data-piece="6"` lit up, label changed to `OpenAPI / contrato escrito`
- Tagline: *"El contrato dejó de ser una idea. Tiene un nombre y un archivo."*
- Subtitle: *"OpenAPI 3.1 — el formato estándar para describir una API REST."*
- Speaker notes: tie back to §4's `bloque de contrato`, preview the side-by-side coming next

#### §7.2 — Side-by-side: contrato §4 ↔ openapi.yaml
- H2: *"El bloque de contrato, en dos formatos"*
- `comparison-2col` layout
- Left column ("Contrato — §4"): the §4 contract block for `POST /projects/{id}/tasks`, informal text, exactly as it appears in §4.6 (lines 1521–1531 of current `slides/index.html`)
- Right column ("OpenAPI 3.1"): equivalent yaml fragment. Target ~16–18 lines so it fits at slide-natural font size; full yaml lives in source_material:
  ```yaml
  paths:
    /projects/{id}/tasks:
      post:
        parameters:
          - { name: id, in: path, required: true, schema: { type: integer } }
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required: [title]
                properties:
                  title:    { type: string }
                  due_date: { type: string, format: date, nullable: true }
        responses:
          '201': { description: Created }
          '400': { description: title is required }
          '404': { description: project not found }
  ```
- Step-through highlights map five pieces:
  - Click 1: method (left: `POST`, right: the `post:` key)
  - Click 2: path (left: `/projects/{id}/tasks`, right: under `paths:`)
  - Click 3: schema-in (left: `entrada (body)`, right: `requestBody`)
  - Click 4: schema-out 201 (left and right)
  - Click 5: errors 400/404 (left and right)
- Footer: *"Misma información, dos formatos. La derecha es la que la IA prefiere — y la que el equipo versiona mañana."*
- Speaker notes name the §4 → OpenAPI vocabulary mapping explicitly

#### §7.3 — Por qué importa
- H2: *"Por qué importa que sea un archivo"*
- Three-column card grid:
  1. **Menos ambigüedad** — tipos, formatos, requeridos, fijados. La IA no improvisa.
  2. **Codegen** — del mismo archivo: docs interactivas, clientes en cualquier lenguaje, mocks, tests.
  3. **Durabilidad** — no es un prompt que se pierde. Es un archivo en el repo. Se versiona, se compara, se vuelve a dictar.
- Footer: *"El supervisor arquitectónico ahora dirige un artefacto durable."*
- Doubles as the bridge into the demo (no separate §7.4 slide)
- Speaker notes: pragmatic walkthrough; tie reason 2 (codegen) forward to the Swagger UI payoff in §8.4 beat 5

### §8 — Demo en vivo: canvas escribe el openapi.yaml (5 slides)

#### §8.1 — Section divider
- `section-divider` class (matches existing §8.1)
- H2: *"Demo en vivo"*
- Subtitle: *"ChatGPT canvas escribe el openapi.yaml. Ustedes leen junto al profesor, endpoint por endpoint."*
- Speaker notes: transition into demo mode, mirror the structure of the current §8.1 notes

#### §8.2 — Lo que va a aparecer
- H2: *"Lo que el yaml tiene que tener"*
- 5-column grid (same visual structure as current §8.2):
  1. **Tres methods** — GET, POST, DELETE
  2. **Jerarquía de recursos** — projects → tasks, path nesting visible
  3. **Una respuesta de error** — al menos un 400 o 404 documentado
  4. **Schemas tipados** — tipos, requeridos explícitos
  5. **Iteración en vivo** — agregar un endpoint sin reescribir
- Counter-block below the grid: *"Lo que NO entra: implementación, base de datos, auth, deploy. Hoy: el contrato como archivo, leído y editable."*
- This folds the current §8.5 ("Lo que NO se intenta hoy") into a single line, since without a running server the drift risk is much smaller

#### §8.3 — La plantilla — el primer prompt
- H2: *"El primer prompt — antes de invocar canvas"*
- Code block visible while the prof types it live:
  ```
  Necesito un openapi.yaml (3.1) para una API de proyectos y tareas.

  recursos:
    Project   { id, name }
    Task      { id, title, due_date?, project_id }

  endpoints:
    GET    /projects
    POST   /projects
    GET    /projects/{id}/tasks
    POST   /projects/{id}/tasks   → 201 / 400 / 404
    DELETE /projects/{id}/tasks/{taskId}

  abrilo en canvas para que podamos editarlo juntos.
  ```
- Step-through highlights: framing line, recursos, endpoints, "abrilo en canvas"
- Footer: *"Le damos el qué. Canvas se abre. Editamos en vivo."*
- Reuses the visual pattern of current §8.3

#### §8.4 — Los seis beats del demo
- H2: *"Los seis beats del demo"*
- Subtitle: *"Checklist de momentos donde paramos a leer junto con ustedes."*
- `clickable-steps` component (reuses existing `clickable-steps.js`):
  1. **Beat 1 — Pegar el prompt** → canvas se abre con el yaml inicial. Frase clave: *"esto no lo escribimos; lo dictamos."*
  2. **Beat 2 — Leer el primer endpoint** (`POST /projects/{id}/tasks`) endpoint-por-endpoint, mapeando al bloque del §4. Conexión explícita con §4.
  3. **Beat 3 — Agregar un endpoint en vivo** desde el chat (*"agregá DELETE /projects/{id}"*) → ver canvas actualizarse. *"El contrato es editable; no es un prompt de un solo tiro."*
  4. **Beat 4 — Editar a mano dentro del canvas**: cambiar un schema, agregar un campo opcional. *"Vos también podés tocar el archivo. La IA y vos comparten editor."*
  5. **Beat 5 — Pegar el yaml en editor.swagger.io** → Swagger UI renderizado → click "Try it" → request real al mock. *"Del mismo archivo salieron docs interactivas. Codegen es real, no abstracción."* Lands the §7.3 reason 2.
  6. **Beat 6 — Cierre 30 seg** — enmarcar lo que pasó, bridge a semana 4.

#### §8.5 — Cierre
- `big-question` styled progressive reveal:
  - *"Ustedes no tipearon nada."*
  - (click) *"Lo que dirigieron fue el contrato."*
  - (click) *"Y ahora tiene archivo."*
- Subtitle: *"El rol — supervisor arquitectónico — sobrevivió la mudanza al servidor."*
- Footer block (visually subdued, smaller weight): *"Próxima clase: le damos este yaml a una IA local para que escriba la implementación. Tarea breve: [PLACEHOLDER — finalize when semana 04 plan firms up. Probable contenido: signup en Cursor o Antigravity, Python ≥3.11, Node ≥18]."*
- Speaker notes: 30 segundos, voz baja, mirar al aula.

## §1–§6 patches (7 touchpoints)

All current line references are against `semanas/03/slides/index.html` as it exists at the start of implementation. Implementer should grep for the strings rather than rely on line numbers, since edits to earlier lines shift later ones.

1. **§1.1 title slide speaker notes** (around line 125)
   Replace: *"al final cerramos con un demo en vivo: levantamos un servidor con Claude Code mientras lo leemos juntos."*
   With: *"al final cerramos con un demo en vivo: escribimos un openapi.yaml en ChatGPT canvas, el contrato del §4 hecho archivo, y lo vemos rendereado en Swagger UI."*

2. **§1.2 mirror card right column, item 6** (around line 159)
   Replace: `Salto al stack local`
   With: `OpenAPI: el contrato escrito`

3. **§1.2 speaker notes** (around line 170)
   Replace the 6-piece enumeration ending in *"y el salto al stack local"* with *"y OpenAPI, el contrato escrito"*.

4. **§1.4 backend-flow speaker notes** (around line 403)
   Replace the annotation that mentions *"Salto al stack local NO aparece — es la bisagra a la próxima clase"* with *"OpenAPI NO aparece en el diagrama — describe el contrato, no participa del request lifecycle. Sigue listado en la espejo card §1.2."*

5. **Roadmap pipe-nodes — 5 occurrences** (around lines 624, 958, 1344, 1673, 2029)
   In every section opener (§2.1 / §3.1 / §4.1 / §5.1 / §6.1), the 6th node is:
   ```html
   <div class="pipe-node" data-piece="6"><div class="pipe-label">Salto</div><div class="pipe-sub">al stack</div></div>
   ```
   Replace with:
   ```html
   <div class="pipe-node" data-piece="6"><div class="pipe-label">OpenAPI</div><div class="pipe-sub">el contrato escrito</div></div>
   ```
   Same edit in 5 places. The active highlighting in §7.1 will use `data-piece="6"`.

6. **§5.7 SQLite speaker notes** (around line 1847)
   Drop the line: *"Y por eso, en el cierre de hoy, vamos a poder pedirle a Claude Code que nos arme la base completa sin que tengamos que pelearnos con un servicio aparte."*
   The preceding line *"SQLite te deja concentrarte en qué modelás, no en dónde corre la base"* already lands the point on its own; no replacement needed.

7. **§4.7 mirror notes — optional polish** (around line 1586)
   Current: *"…le decís 'implementá este endpoint en FastAPI'…"*
   Acceptable as-is (the contract still describes what the AI implements); leave unless a coherence sweep flags it.

## Spine + source_material updates

### `semanas/03/spine.md`
- **Whole-week through-line**: replace *"el profesor levanta una API con Claude Code mientras los alumnos leen endpoint por endpoint"* with the canvas/openapi version. Keep the rest of the through-line intact.
- **§1 (Backend y el supervisor arquitectónico)**: update the 6-piece map to end in `OpenAPI` instead of `salto al stack local`.
- **§7**: rewrite entirely. New name: "OpenAPI: el contrato escrito". Through-line: OpenAPI is the formalization of the §4 contract block; same five pieces, now machine-readable. New slide budget: 3.
- **§8**: rewrite entirely. New name: "Demo en vivo — canvas escribe el openapi.yaml". Domain: projects/tasks from §4. Climax: Swagger UI rendering of the dictated yaml. New slide budget: 5.

### `semanas/03/source_material/`
- Rename `07-de-lo-local-al-stack.md` → `07-openapi-el-contrato-escrito.md`. Rewrite content around: what OpenAPI is, why it formalizes the §4 contract, the §4-to-yaml mapping, three reasons it matters (ambiguity, codegen, durability).
- Rewrite `08-demo-en-vivo.md` around: canvas demo using the projects/tasks domain, the prompt template, the six beats, the editor.swagger.io payoff. Drop "TBD: dominio" section (domain is fixed). Drop "no autenticación, no deploy, no testing automatizado, no CSS bonito" (different mode of demo; new disclaimer is shorter).
- Update `source_material/index.md` to reference the renamed file.

## Final slide count

| Section | Before | After |
| ------- | ------ | ----- |
| §1–§6   | 43     | 43 (7 in-place edits) |
| §7      | 8      | 3     |
| §8      | 6      | 5     |
| **Total** | **57** | **51** |

The closing third of the class becomes noticeably tighter and lands on a single visual climax: Swagger UI rendering the openapi.yaml the students just dictated.

## Open threads

- **Semana 04 install homework**: §8.5 footer is a placeholder. Finalize wording (Cursor signup? Antigravity install? Python/Node version checks?) once semana 04 plan firms up. Spec should not block on this; ship with the placeholder note clearly marked in source_material.
- **§4.7 FastAPI mention**: optional polish during a coherence sweep; not required for this spec.
