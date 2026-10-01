# Semana 03 — OpenAPI + Canvas Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the closing third of `semanas/03/` so the class lands on OpenAPI as the formalization of the §4 contract, climaxing with a ChatGPT-canvas live demo that authors `openapi.yaml` for the projects/tasks domain and renders it in Swagger UI.

**Architecture:** Three concurrent edit fronts in one HTML deck plus its source material. (1) Replace `<section>` blocks for §7 and §8 in `slides/index.html` with new content. (2) Patch 7 in-place touchpoints in §1–§6. (3) Rewrite `spine.md`, source_material 07/08, and source_material index. No new files except the renamed source_material 07. No new CSS or JS — reuse existing components (`comparison-2col`, `clickable-steps`, `section-divider`, `pipe-roadmap`, `bg-secondary-card`).

**Tech Stack:** HTML, reveal.js (existing setup), markdown. Verification is visual in browser at `http://localhost:3000/semanas/03/slides/`.

**Spec reference:** `docs/superpowers/specs/2026-05-10-semana-03-openapi-canvas-demo-design.md`

---

## File structure

| Path | Status | Responsibility |
|------|--------|---------------|
| `semanas/03/spine.md` | Modify | Update whole-week through-line, §1 6-piece map, §7 entry, §8 entry |
| `semanas/03/source_material/07-de-lo-local-al-stack.md` | Delete | Replaced by 07-openapi-* |
| `semanas/03/source_material/07-openapi-el-contrato-escrito.md` | Create | OpenAPI as contract formalization (sections, mapping, why-it-matters) |
| `semanas/03/source_material/08-demo-en-vivo.md` | Replace | Canvas demo guion: prompt template, 6 beats, Swagger UI payoff |
| `semanas/03/source_material/index.md` | Modify | Update file 7 reference |
| `semanas/03/slides/index.html` | Modify | 7 in-place patches in §1–§6; full replace of §7 outer-section; full replace of §8 outer-section; update `clickable-steps` init at bottom |

---

## Voice and conventions

All Spanish copy follows existing semana 03 conventions:
- Professor voice, second-person, direct.
- No emojis (global rule).
- Bold the vocabulary terms on first use.
- Keep `schema-in` / `schema-out` as conceptual labels in §1–§6; introduce `requestBody` / `responses` only as the OpenAPI mapping inside §7.
- HTML entities in copy: `&mdash;` (—), `&ndash;` (–), `&aacute;` (á), etc., consistent with the rest of the file.

---

## Phase 1 — Spine + source_material

Foundation work. No slide changes. Each task here can be reviewed against the spec independently.

### Task 1: Update `spine.md`

**Files:**
- Modify: `semanas/03/spine.md`

- [ ] **Step 1: Update the whole-week through-line (line 3)**

Find the sentence:
> *"La clase termina cerrando el espejo en vivo: el profesor levanta una API con Claude Code mientras los alumnos leen endpoint por endpoint lo que dictaron."*

Replace with:
> *"La clase termina cerrando el espejo en vivo: el profesor escribe un openapi.yaml en ChatGPT canvas mientras los alumnos leen endpoint por endpoint el contrato del §4 hecho archivo, y ven el yaml renderizado en Swagger UI."*

- [ ] **Step 2: Update the §1 6-piece map (around line 11)**

Find the bullet:
> *"- El mapa de la clase: HTTP → REST → endpoints → datos → errores → salto al stack local."*

Replace with:
> *"- El mapa de la clase: HTTP → REST → endpoints → datos → errores → OpenAPI (el contrato escrito)."*

- [ ] **Step 3: Replace the §7 section entirely**

Find the current `## Section 7: De lo local al stack (salto)` block (from its header through the end of its `**Slide budget:**` line) and replace with:

```markdown
## Section 7: OpenAPI — el contrato escrito
**Source material:** `source_material/07-openapi-el-contrato-escrito.md`
**Through-line:** Lo que vinimos llamando "contrato" tiene un nombre y un archivo: OpenAPI. Las cinco piezas del bloque del §4 (method, path, schema-in, schema-out, errores) se mapean directamente a paths/HTTP-method-keys/requestBody/responses. La industria le puso formato a la idea, y eso desbloquea tres cosas concretas: menos ambigüedad para la IA, codegen automático (docs, clientes, mocks, tests) y durabilidad como artefacto en el repo.
**Key analogy:** El contrato hecho archivo. La derecha del §4 ↔ la izquierda del §7: misma información, dos formatos.
**What students walk away knowing:**
- OpenAPI 3.1 es el formato estándar para describir una API REST: las cinco piezas del §4 con keys oficiales (`paths`, `requestBody`, `responses`).
- Tres razones por las que es un archivo y no un prompt: ambigüedad fija, codegen real (Swagger UI, clientes), durabilidad versionada.
- El supervisor arquitectónico ahora dirige un artefacto durable, no un prompt que se pierde.
**Animations / interactive:** None new. `comparison-2col` con step-through highlights mapeando línea-a-línea bloque del §4 ↔ openapi.yaml.
**Slide budget:** 3 slides (apertura → side-by-side → por qué importa).

## Section 8: Demo en vivo — canvas escribe el openapi.yaml
**Source material:** `source_material/08-demo-en-vivo.md`
**Through-line:** Coreografía del cierre. El profesor pega un prompt que dicta el contrato del §4 (projects/tasks) y le pide a ChatGPT canvas el openapi.yaml. Lee el yaml endpoint por endpoint mapeando al §4, agrega un endpoint en vivo, edita a mano dentro del canvas, y al final pega el yaml en editor.swagger.io para mostrar el render con docs interactivas y un "Try it" funcional. La cadena: contrato → archivo → docs renderizadas, en vivo.
**What students walk away knowing:**
- El demo no agrega un concepto nuevo; cierra el espejo y deja al alumno con ganas de tomar el yaml y darlo a una IA local en semana 4.
- (Apropiación visceral) Lo que ustedes dictaron fue el contrato; ahora tiene archivo. El rol — supervisor arquitectónico — sobrevivió la mudanza al servidor.
**Animations / interactive:** None new. Reusa `clickable-steps` (mismo componente del §8 anterior) para los 6 beats. `section-divider` para apertura.
**Slide budget:** 5 slides (divider → 5 requisitos + counter → plantilla del prompt → 6 beats → cierre + bridge a semana 4).
```

- [ ] **Step 4: Verify the spine is internally consistent**

Run: `grep -n "Claude Code\|stack local\|Salto" semanas/03/spine.md`
Expected: No remaining references to "Claude Code" or "stack local" or "Salto" as section names. (The string "stack" may appear elsewhere in unrelated contexts; verify each hit.)

### Task 2: Rename and rewrite source_material 07

**Files:**
- Delete: `semanas/03/source_material/07-de-lo-local-al-stack.md`
- Create: `semanas/03/source_material/07-openapi-el-contrato-escrito.md`

- [ ] **Step 1: Delete the old file**

Run: `rm semanas/03/source_material/07-de-lo-local-al-stack.md`

- [ ] **Step 2: Create the new file**

Write `semanas/03/source_material/07-openapi-el-contrato-escrito.md` with content covering (in this order, professor voice, ~600–900 words):

1. **Apertura — el contrato tiene nombre.** Lo que vinimos llamando "contrato" durante toda la clase es una idea informal. La industria le puso nombre y formato: **OpenAPI**, en su versión actual 3.1. Es el estándar para describir APIs REST de punta a punta. Si ya escribiste el bloque del §4, ya pensaste en OpenAPI sin saberlo.

2. **Las cinco piezas, mapeadas.** El bloque del §4 tenía: `method`, `path`, `schema-in`, `schema-out` (uno por status code), errores. OpenAPI usa nombres concretos:
   - `method` → la key HTTP-method bajo `paths`
   - `path` → las keys de `paths` (con `{id}` para variables)
   - `schema-in` → `requestBody`
   - `schema-out 201` / `schema-out 400` / `schema-out 404` → entries dentro de `responses`
   Mostrá un fragmento yaml pequeño del `POST /projects/{id}/tasks` y poné lado a lado con el bloque del §4. Misma información, dos formatos.

3. **Por qué es un archivo y no un prompt.** Tres razones:
   - **Menos ambigüedad** para la IA. El yaml fija tipos, formatos (`format: date`), requeridos, nullables. Un prompt vago deja todo eso al modelo; el yaml lo decide vos.
   - **Codegen real, no abstracto.** Del mismo archivo salen: docs interactivas (Swagger UI), clientes en cualquier lenguaje, mocks para que el frontend trabaje sin esperar al backend, tests de contrato. Una sola fuente, muchos artefactos.
   - **Durabilidad.** Un prompt se pierde cuando cerrás la conversación. Un yaml vive en el repo, se versiona en git, se compara entre branches, se vuelve a dictar. El supervisor arquitectónico ahora tiene un artefacto durable que dirige.

4. **El espejo se cierra (texto corto).** En semana 02 el átomo dictable fue un componente con sus props/state. En esta clase, el átomo dictable fue el bloque de contrato. Ahora ese bloque tiene archivo, y mañana se lo damos a una IA local para que escriba la implementación.

5. **Vago vs específico (opcional, breve).** Si el alumno le pide a la IA "armame una API", la IA elige todo. Si le pide "armame el openapi.yaml para una API de proyectos y tareas con estos endpoints…", la IA fija el contrato y después la implementación es derivada. **No incluir** un bloque comparativo formal — el vago/específico ya cerró cinco secciones y suma ruido acá. Una frase basta.

No mencionar Claude Code, FastAPI, Python, ni el setup local. Esa rama queda fuera de esta clase.

- [ ] **Step 3: Verify file exists and old file is gone**

Run: `ls semanas/03/source_material/07-*.md`
Expected: Only `07-openapi-el-contrato-escrito.md`. No `07-de-lo-local-al-stack.md`.

### Task 3: Rewrite source_material 08

**Files:**
- Modify: `semanas/03/source_material/08-demo-en-vivo.md`

- [ ] **Step 1: Replace contents entirely**

Overwrite `semanas/03/source_material/08-demo-en-vivo.md` with content covering (~400–600 words, guion voice):

1. **Qué tiene que mostrar el demo.** Cinco requisitos visibles, en orden:
   - Tres methods HTTP en juego (mínimo GET, POST, DELETE).
   - Una jerarquía de recursos visible en el path (`projects → projects/{id}/tasks → projects/{id}/tasks/{taskId}`).
   - Al menos una respuesta de error documentada (400 o 404).
   - Schemas tipados con `type`, `required`, `format` cuando aplique.
   - Iteración en vivo: agregar un endpoint nuevo desde el chat y ver canvas actualizarse.

2. **Dominio: projects/tasks (fijo).** No se decide en el momento. Se reusa el dominio del §4 — `POST /projects/{id}/tasks` con `title` (requerido), `due_date` (opcional), 201/400/404. Los endpoints completos: `GET /projects`, `POST /projects`, `GET /projects/{id}/tasks`, `POST /projects/{id}/tasks`, `DELETE /projects/{id}/tasks/{taskId}`.

3. **El primer prompt (visible en pantalla mientras se tipea).**
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

4. **Los seis beats** (cada uno con la frase clave que se dice al aula):
   - **Beat 1 — Pegar el prompt.** Canvas se abre con el yaml inicial. *"Esto no lo escribimos; lo dictamos."*
   - **Beat 2 — Leer el primer endpoint.** `POST /projects/{id}/tasks`. Recorrerlo: `paths`, `post`, `parameters`, `requestBody`, `responses`. Mapear en voz alta a las cinco piezas del §4.
   - **Beat 3 — Agregar un endpoint en vivo desde el chat.** Pedirle al modelo: *"agregá DELETE /projects/{id}, con 404 si no existe."* Mostrar el canvas actualizándose en tiempo real. *"El contrato es editable; no es un prompt de un solo tiro."*
   - **Beat 4 — Editar a mano dentro del canvas.** Por ejemplo, agregar `description` opcional al schema de `Task`, o cambiar `due_date` de `string` a `string` con `format: date-time`. *"La IA y vos comparten editor."*
   - **Beat 5 — Pegar el yaml en `editor.swagger.io`.** Mostrar Swagger UI renderizado. Click en `POST /projects` → "Try it out" → "Execute". *"Del mismo archivo salieron docs interactivas. Codegen es real, no abstracción."*
   - **Beat 6 — Cierre 30 segundos.** *"Ustedes no tipearon nada. Lo que dirigieron fue el contrato. Y ahora tiene archivo."* Bridge a semana 4: *"La próxima clase tomamos este yaml y se lo damos a una IA local para que escriba la implementación."*

5. **Lo que NO se intenta hoy.** No hay implementación, ni base de datos real, ni autenticación, ni deploy. Lo único que aparece en pantalla es el contrato como archivo, leído y editable, con su render como bonus.

6. **Plan B si canvas no aparece.** Si por alguna razón canvas no se dispara con el primer prompt, pedirlo explícitamente: *"abrilo en canvas"*. Si sigue sin abrirse, copiar el yaml a un editor local cualquiera y seguir el demo desde ahí. La pieza importante es el yaml, no la herramienta.

- [ ] **Step 2: Verify file content**

Run: `head -5 semanas/03/source_material/08-demo-en-vivo.md`
Expected: Title and opening lines about the new canvas demo. No mention of Claude Code, FastAPI, or "TBD: dominio".

### Task 4: Update source_material index

**Files:**
- Modify: `semanas/03/source_material/index.md`

- [ ] **Step 1: Update the file 7 reference**

Find the row that references `07-de-lo-local-al-stack.md` and update to:

```
| 7 | [07-openapi-el-contrato-escrito.md](07-openapi-el-contrato-escrito.md) | OpenAPI como formalización del contrato del §4 | Cierre conceptual (~10 min) |
```

Find the row that references `08-demo-en-vivo.md` and update its description to reflect the new demo:

```
| 8 | [08-demo-en-vivo.md](08-demo-en-vivo.md) | Guion del demo: ChatGPT canvas escribe el openapi.yaml; render en Swagger UI | Demo (~25 min) |
```

- [ ] **Step 2: Verify index references**

Run: `grep -E "^\| [78] \|" semanas/03/source_material/index.md`
Expected: Two rows pointing to the new filenames.

### Task 5: Commit Phase 1

- [ ] **Step 1: Commit foundation work**

```bash
git add semanas/03/spine.md semanas/03/source_material/
git commit -m "$(cat <<'EOF'
docs(semana-03): retool spine + source_material around OpenAPI close

Replace §7 ('De lo local al stack') with §7 ('OpenAPI: el contrato escrito')
and rewrite §8 demo guion around a ChatGPT-canvas openapi.yaml authoring
session for the projects/tasks domain.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase 2 — §1–§6 in-place patches

Seven small edits in `semanas/03/slides/index.html`. Use grep-friendly anchors, not line numbers — line numbers shift as earlier edits land.

### Task 6: Patch §1.1 title-slide speaker notes

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Replace the speaker-notes line that previews the Claude Code demo**

Find:

```
"Hoy hacemos el reflejo de lo que vimos la semana pasada. Ahí aprendimos a nombrar las piezas del frontend para dirigir a la IA. Hoy aprendemos las del backend — methods, paths, contratos, datos, errores — y al final cerramos con un demo en vivo: levantamos un servidor con Claude Code mientras lo leemos juntos."
```

Replace with:

```
"Hoy hacemos el reflejo de lo que vimos la semana pasada. Ahí aprendimos a nombrar las piezas del frontend para dirigir a la IA. Hoy aprendemos las del backend — methods, paths, contratos, datos, errores — y al final cerramos con un demo en vivo: escribimos un openapi.yaml en ChatGPT canvas, el contrato hecho archivo, y lo vemos renderizado en Swagger UI."
```

### Task 7: Patch §1.2 mirror card and speaker notes

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Replace the mirror card right-column item 6**

Find: `Salto al stack local`
Replace with: `OpenAPI: el contrato escrito`

(There is exactly one occurrence; if `grep -n "Salto al stack local" semanas/03/slides/index.html` returns more than one hit, pause and re-read the spec — the others are in §7 which we replace wholesale in Phase 3.)

- [ ] **Step 2: Replace the §1.2 speaker-notes enumeration**

Find:

```
"Esta clase hacemos lo mismo del otro lado. Seis piezas: HTTP, REST, endpoints, datos, errores y el salto al stack local. Cada una es una palabra que vas a necesitar para especificarle a la IA qué construir, y para leer lo que devuelve sin tragártelo."
```

Replace with:

```
"Esta clase hacemos lo mismo del otro lado. Seis piezas: HTTP, REST, endpoints, datos, errores y OpenAPI, el contrato escrito. Cada una es una palabra que vas a necesitar para especificarle a la IA qué construir, y para leer lo que devuelve sin tragártelo."
```

### Task 8: Patch §1.4 backend-flow speaker notes

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Replace the diagram annotation**

Find:

```
<p><u>Diagrama interactivo del ciclo cliente-servidor-cliente. 5 de las 6 piezas (HTTP, REST, Endpoints, Datos, Errores) viven dentro del servidor. Salto al stack local NO aparece — es la bisagra a la próxima clase, no parte del request lifecycle. Sigue listado en la espejo card §1.2.</u></p>
```

Replace with:

```
<p><u>Diagrama interactivo del ciclo cliente-servidor-cliente. 5 de las 6 piezas (HTTP, REST, Endpoints, Datos, Errores) viven dentro del servidor. OpenAPI NO aparece — describe el contrato, no participa del request lifecycle. Sigue listada en la espejo card §1.2.</u></p>
```

### Task 9: Patch the 5 roadmap pipe-nodes (§2.1, §3.1, §4.1, §5.1, §6.1)

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Use replace_all to update all 5 occurrences in one edit**

Five identical pipe-node blocks need updating, one in each section opener. They all contain `<div class="pipe-label">Salto</div><div class="pipe-sub">al stack</div>`.

Find (use `replace_all: true`):

```
<div class="pipe-label">Salto</div>
        <div class="pipe-sub">al stack</div>
```

Replace with:

```
<div class="pipe-label">OpenAPI</div>
        <div class="pipe-sub">contrato escrito</div>
```

Note: there is also a single-line variant `<div class="pipe-node" data-piece="6"><div class="pipe-label">Salto</div><div class="pipe-sub">al stack</div></div>` (collapsed). Run two passes if needed:

- [ ] **Step 2: Verify both variants are caught**

Run: `grep -nE "Salto|al stack" semanas/03/slides/index.html | grep -v "stack trace\|stack del demo\|stack chico\|stack que\|de lo local"`
Expected: No remaining hits in §1–§6 range (lines ~1–2200). Hits inside the §7 outer-section (lines ~2217–2634) are fine — that whole block is replaced in Phase 3.

If the collapsed single-line variant is still there, run a second `replace_all`:

Find: `<div class="pipe-node" data-piece="6"><div class="pipe-label">Salto</div><div class="pipe-sub">al stack</div></div>`
Replace with: `<div class="pipe-node" data-piece="6"><div class="pipe-label">OpenAPI</div><div class="pipe-sub">contrato escrito</div></div>`

### Task 10: Patch §5.7 SQLite speaker notes

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Drop the line that previews the Claude Code demo**

Find (note the entire `<p>...</p>` block):

```
<p><em>"SQLite te deja concentrarte en qué modelás, no en dónde corre la base. Por eso entra en una clase de noventa minutos. Y por eso, en el cierre de hoy, vamos a poder pedirle a Claude Code que nos arme la base completa sin que tengamos que pelearnos con un servicio aparte."</em></p>
```

Replace with:

```
<p><em>"SQLite te deja concentrarte en qué modelás, no en dónde corre la base. Por eso entra en una clase de noventa minutos."</em></p>
```

### Task 11: Verify §1–§6 in browser + commit

- [ ] **Step 1: Start the dev server (skip if already running)**

Run: `npm start` (in a separate terminal if needed)
Expected: Server listening on port 3000.

- [ ] **Step 2: Open the deck and walk §1–§6**

Open `http://localhost:3000/semanas/03/slides/` in a browser. Use arrow keys to walk every slide in §1–§6. For section openers (§2.1, §3.1, §4.1, §5.1, §6.1), confirm the 6th roadmap node now reads "OpenAPI / contrato escrito" with the correct active styling on its own piece.

Open speaker notes (`s` key in reveal.js) on the title slide, §1.2, §1.4, and §5.7 and confirm the patched lines are in place.

- [ ] **Step 3: Final consistency grep**

Run: `awk '/<!-- ===.*§7|<!-- §7\.1/{exit} {print}' semanas/03/slides/index.html | grep -nE "Claude Code|claude-code|Salto|al stack local|stack del demo"`
Expected: No hits. (If "stack trace" appears in §6 unrelated to setup, ignore.)

- [ ] **Step 4: Commit Phase 2**

```bash
git add semanas/03/slides/index.html
git commit -m "$(cat <<'EOF'
fix(semana-03): patch §1-§6 references to deleted §7/§8

Update title-slide preview, §1.2 mirror card, §1.4 backend-flow notes,
the 5 section-opener roadmap pipe-nodes (data-piece=6), and §5.7
SQLite notes to point at OpenAPI as the 6th piece instead of
'salto al stack local' / Claude Code demo.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase 3 — §7 rebuild

Replace the entire `<section>` block currently containing §7 (8 slides + scoped CSS) with a fresh outer-section containing only the 3 new slides. No new CSS is needed — every visual element reuses existing classes (`comparison-2col`, `bg-secondary-card`, `pipe-node`, `piece-roadmap`).

### Task 12: Replace the §7 outer-section block

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Identify the §7 outer-section bounds**

The outer block starts at the comment `<!-- ============================================================` immediately followed by `§7 — De lo local al stack` and ends at the matching `</section>` before the §8 outer-section comment.

Run: `grep -n "§7 — De lo local al stack\|§8 — Demo en vivo" semanas/03/slides/index.html`
Expected: Two pairs of comment lines bracketing §7 and §8.

- [ ] **Step 2: Replace the entire §7 block**

Use a single Edit. Find (the outer comment block + the entire `<section>` containing §7's CSS and 8 slides + the closing `</section>`):

```html
      <!-- ============================================================
           §7 — De lo local al stack
           ============================================================ -->
      <!-- ============================================================
     §7 — De lo local al stack (salto)
     ============================================================ -->
<section>
```

… all the way through to the closing `</section>` that immediately precedes the `<!-- ============================================================` block introducing §8.

If the Edit's `old_string` is too unwieldy as one match, do it in two steps: first replace the opening comments and the `<section>` opener with the new opener (Step 2a), then delete the §7 inner content slide-by-slide (Step 2b through 2i, one slide each), then add the new slides (Step 3a–3c). Recommended approach is the single-shot replace; only fall back if the Edit fails.

Replace with:

```html
      <!-- ============================================================
           §7 — OpenAPI: el contrato escrito
           ============================================================ -->
<section>

  <!-- §7.1: Section opener — roadmap activa "OpenAPI" -->
  <section>
    <h2>Pieza 6 &mdash; OpenAPI <span style="color: var(--text-muted); font-size: 0.55em; font-weight: 400; letter-spacing: 0.04em;">(el contrato escrito)</span></h2>
    <div class="piece-roadmap active-6">
      <div class="pipe-node" data-piece="1">
        <div class="pipe-label">HTTP</div>
        <div class="pipe-sub">protocolo</div>
      </div>
      <span class="pipe-arrow">&rarr;</span>
      <div class="pipe-node" data-piece="2">
        <div class="pipe-label">REST</div>
        <div class="pipe-sub">estilo</div>
      </div>
      <span class="pipe-arrow">&rarr;</span>
      <div class="pipe-node" data-piece="3">
        <div class="pipe-label">Endpoints</div>
        <div class="pipe-sub">contract</div>
      </div>
      <span class="pipe-arrow">&rarr;</span>
      <div class="pipe-node" data-piece="4">
        <div class="pipe-label">Datos</div>
        <div class="pipe-sub">memoria</div>
      </div>
      <span class="pipe-arrow">&rarr;</span>
      <div class="pipe-node" data-piece="5">
        <div class="pipe-label">Errores</div>
        <div class="pipe-sub">leer fallas</div>
      </div>
      <span class="pipe-arrow">&rarr;</span>
      <div class="pipe-node" data-piece="6">
        <div class="pipe-label">OpenAPI</div>
        <div class="pipe-sub">contrato escrito</div>
      </div>
    </div>
    <p style="margin-top: 32px; font-size: 0.95em; text-align: center; max-width: 36em; margin-left: auto; margin-right: auto;">
      El contrato dej&oacute; de ser una idea. <span style="color: var(--accent);">Tiene un nombre y un archivo.</span>
    </p>
    <p style="margin-top: 8px; font-size: 0.78em; color: var(--text-muted); text-align: center; max-width: 36em; margin-left: auto; margin-right: auto;">
      OpenAPI 3.1 &mdash; el formato est&aacute;ndar para describir una API REST.
    </p>
    <aside class="notes">
      <p><u>Apertura de §7. Lo que vinimos llamando "contrato" durante toda la clase tiene un nombre formal y un archivo.</u></p>
      <p><em>"&Uacute;ltima pieza del mapa. Recorrimos cinco: HTTP, REST, endpoints, datos, errores. Tenemos el vocabulario backend completo. La sexta no es un concepto nuevo &mdash; es lo mismo que vinimos llamando 'contrato' en la secci&oacute;n cuatro, ahora con un nombre y un formato est&aacute;ndar."</em></p>
      <p><em>"Se llama OpenAPI. Versi&oacute;n actual 3.1. Es el est&aacute;ndar de la industria para describir una API REST de punta a punta. Si ya escribiste el bloque del §4, ya pensaste en OpenAPI sin saberlo. Lo que viene son tres slides para verlo, y despu&eacute;s el demo en vivo."</em></p>
    </aside>
  </section>

  <!-- §7.2: Side-by-side — bloque de contrato §4 ↔ openapi.yaml -->
  <section>
    <h2>El bloque de contrato, en dos formatos</h2>
    <div class="comparison-2col" style="margin-top: 12px; align-items: stretch;">
      <div class="bg-secondary-card" style="border-left: 4px solid var(--text-muted);">
        <p style="font-size: 0.6em; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Contrato &mdash; §4</p>
        <h3 style="color: var(--text-muted);">Texto informal</h3>
        <pre style="margin: 0; box-shadow: none; font-size: 0.62em;"><code class="language-text" data-trim data-line-numbers="|1|2-4|5-6|7-10"
>POST /projects/{id}/tasks
  entrada (body):
    title       string, requerido
    due_date    fecha ISO, opcional
  salida 201 (creado):
    { id, title, due_date, project_id }
  salida 400 (datos inv&aacute;lidos):
    { error: "title es requerido" }
  salida 404 (proyecto no existe):
    { error: "no se encontr&oacute; el proyecto {id}" }</code></pre>
      </div>
      <div class="bg-secondary-card" style="border-left: 4px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin: 0 0 6px;">OpenAPI 3.1</p>
        <h3 style="color: var(--accent);">YAML, machine-readable</h3>
        <pre style="margin: 0; box-shadow: none; font-size: 0.58em;"><code class="language-yaml" data-trim data-line-numbers="|2|3|4-13|14-17|18-23"
>paths:
  /projects/{id}/tasks:
    post:
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
        '201':
          description: Created
          content: { application/json: { schema: { $ref: '#/components/schemas/Task' } } }
        '400':
          description: title es requerido
        '404':
          description: proyecto no existe</code></pre>
      </div>
    </div>
    <p style="margin-top: 18px; font-size: 0.82em; text-align: center; max-width: 44em; margin-left: auto; margin-right: auto;">
      Misma informaci&oacute;n, dos formatos. La derecha es <span style="color: var(--accent);">la que la IA prefiere</span> &mdash; y la que el equipo versiona ma&ntilde;ana.
    </p>
    <aside class="notes">
      <p><strong>Click 1: ilumina <code>POST</code> a la izquierda y la key <code>post:</code> a la derecha (method). Click 2: ilumina <code>/projects/{id}/tasks</code> en ambos lados (path). Click 3: ilumina <code>entrada (body)</code> &harr; <code>requestBody</code> (schema-in). Click 4: ilumina <code>salida 201</code> &harr; <code>responses '201'</code>. Click 5: ilumina las salidas 400/404 &harr; <code>'400'</code> y <code>'404'</code> (errores).</strong></p>
      <p><u>Slide-clave de §7. Mapeo l&iacute;nea-a-l&iacute;nea entre el bloque del §4 y el yaml.</u></p>
      <p><em>"Ac&aacute; est&aacute; el mismo bloque de contrato que armamos en la secci&oacute;n cuatro, dos formatos. A la izquierda, el texto informal que dictamos. A la derecha, el equivalente en OpenAPI 3.1. Misma informaci&oacute;n, distinto vestido."</em></p>
      <p><em>"Voy a recorrer las cinco piezas. Method &mdash; en el §4 es la palabra <code>POST</code> al principio; en OpenAPI es la key <code>post:</code> bajo <code>paths</code>. Path &mdash; en los dos lados es lo mismo, <code>/projects/{id}/tasks</code>, con la variable entre llaves."</em></p>
      <p><em>"Schema-in &mdash; lo que en el §4 llam&aacute;bamos 'entrada (body)' en OpenAPI se llama <code>requestBody</code>. Y dentro hay una clave nueva: <code>schema</code>, con tipos expl&iacute;citos (<code>type: string</code>), formatos (<code>format: date</code>), required, nullable. El nivel de detalle ya no es opinable."</em></p>
      <p><em>"Schema-out &mdash; lo que llam&aacute;bamos 'salida 201' / 'salida 400' / 'salida 404' en OpenAPI son entries dentro de <code>responses</code>, con la key igual al status code. Cada entry describe el cuerpo de la respuesta para ese c&oacute;digo. La separaci&oacute;n por status code que pintamos en la slide del §4.6 ya estaba apuntando ac&aacute; sin nombrar el formato."</em></p>
      <p><em>"Cinco piezas, cinco mappings, una correspondencia exacta. La derecha no agrega informaci&oacute;n nueva; cierra ambig&uuml;edades. Y como es un archivo machine-readable, mucho de lo que vimos manualmente lo va a poder hacer una herramienta."</em></p>
    </aside>
  </section>

  <!-- §7.3: Por qué importa que sea un archivo (3 razones) -->
  <section>
    <h2>Por qu&eacute; importa que sea un archivo</h2>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 18px;">
      <div class="bg-secondary-card" style="border-left: 4px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Raz&oacute;n 1</p>
        <h3 style="font-size: 1em; color: var(--accent); margin: 0 0 8px;">Menos ambig&uuml;edad</h3>
        <p style="font-size: 0.78em; line-height: 1.5; margin: 0;">Tipos, formatos, requeridos, nullables: <strong>fijados</strong>. Lo que en un prompt es opinable, en el yaml est&aacute; escrito. La IA no improvisa.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 4px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Raz&oacute;n 2</p>
        <h3 style="font-size: 1em; color: var(--accent); margin: 0 0 8px;">Codegen real</h3>
        <p style="font-size: 0.78em; line-height: 1.5; margin: 0;">Del mismo archivo: <strong>docs interactivas</strong> (Swagger UI), <strong>clientes</strong> en cualquier lenguaje, <strong>mocks</strong>, <strong>tests de contrato</strong>. Una sola fuente, muchos artefactos.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 4px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Raz&oacute;n 3</p>
        <h3 style="font-size: 1em; color: var(--accent); margin: 0 0 8px;">Durabilidad</h3>
        <p style="font-size: 0.78em; line-height: 1.5; margin: 0;">No es un prompt que se pierde. Es un archivo en el repo: <strong>se versiona</strong>, se compara entre branches, se vuelve a dictar.</p>
      </div>
    </div>
    <p style="margin-top: 28px; font-size: 0.92em; text-align: center; max-width: 40em; margin-left: auto; margin-right: auto;">
      El supervisor arquitect&oacute;nico ahora dirige <span style="color: var(--accent);">un artefacto durable</span>.
    </p>
    <aside class="notes">
      <p><u>Cierre de §7. Tres razones por las que el contrato hecho archivo desbloquea cosas que un prompt no puede.</u></p>
      <p><em>"Tres razones por las que importa que el contrato sea un archivo y no un prompt. Una por una."</em></p>
      <p><em>"Primera, ambig&uuml;edad. El yaml fija tipos, formatos como <code>format: date</code>, requeridos, nullables. Cada uno de esos detalles, en un prompt vago, lo decide la IA. En el yaml lo decid&iacute;s vos. Es la misma idea de 'vago vs espec&iacute;fico' que cerr&oacute; las cinco secciones anteriores, ahora hecha archivo."</em></p>
      <p><em>"Segunda, codegen. Y esto es lo que vamos a ver renderizado en el demo. Del mismo openapi.yaml salen docs interactivas &mdash; eso es Swagger UI, lo van a ver en pantalla en cinco minutos. Salen clientes generados en cualquier lenguaje (Python, TypeScript, Go), salen mocks que el frontend puede consumir mientras el backend no existe, salen tests que verifican que la implementaci&oacute;n cumple el contrato. Una sola fuente, muchos artefactos derivados. Eso es codegen real, no abstracci&oacute;n."</em></p>
      <p><em>"Tercera, durabilidad. Un prompt vive en una conversaci&oacute;n. Cuando cerr&aacute;s la pesta&ntilde;a se pierde, o se diluye en mil mensajes despu&eacute;s. El yaml vive en el repo: se versiona en git, se compara entre branches con un diff, se vuelve a dictar a otra IA cuando cambia algo. El supervisor arquitect&oacute;nico que vinimos nombrando toda la clase, ahora tiene un artefacto durable que dirige."</em></p>
      <p><em>"Y con eso cerramos la parte conceptual de la clase. Lo que viene es el demo en vivo: pegar un prompt, ver canvas escribir el yaml, leerlo juntos, y al final renderizarlo en Swagger UI."</em></p>
    </aside>
  </section>

</section>
```

- [ ] **Step 3: Verify §7 structurally**

Run: `grep -nE "§7\.[0-9]" semanas/03/slides/index.html`
Expected: Three §7 marker comments (`§7.1`, `§7.2`, `§7.3`). No others.

Run: `grep -nE "Salto al stack|FastAPI|Uvicorn|venv|Claude Code" semanas/03/slides/index.html`
Expected: No hits inside §7 (lines after the §7 opening comment, before the §8 opening comment). The mention of "FastAPI" in §4.7 around the previous-§4 mirror notes is allowed (left intentionally per spec).

### Task 13: Verify §7 in browser + commit

- [ ] **Step 1: Visual verification**

Open `http://localhost:3000/semanas/03/slides/#/6/0` in a browser (the §7 opener). Walk all three slides.

Check:
- §7.1: roadmap shows 6 nodes, the 6th labeled "OpenAPI / contrato escrito", active-6 styling lights it up. Tagline reads "El contrato dejó de ser una idea. Tiene un nombre y un archivo."
- §7.2: side-by-side renders. Step-through (`Space`) cycles through 5 highlight stages on both columns. Both `<pre>` blocks fit without horizontal scroll on a 1280×800 slide.
- §7.3: three cards render side-by-side. Closing line reads correctly.

If §7.2's yaml is too wide and overflows the right card, reduce its `font-size` from `0.58em` to `0.55em` (existing escape hatch — same approach used in §4.6).

- [ ] **Step 2: Speaker notes verification**

Press `s` to open the speaker notes window. Walk §7.1 → §7.2 → §7.3 and confirm the notes match the spec.

- [ ] **Step 3: Commit Phase 3**

```bash
git add semanas/03/slides/index.html
git commit -m "$(cat <<'EOF'
feat(semana-03): rebuild §7 around OpenAPI as contract formalization

Replace 8-slide 'De lo local al stack' section with 3-slide 'OpenAPI:
el contrato escrito': section opener, side-by-side mapping of §4
contract block to openapi.yaml, three-card 'por qué importa' close.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase 4 — §8 rebuild

Replace the §8 outer-section block (6 slides) with 5 new slides. Update the `clickable-steps` initialization at the bottom of the file with the new 6-beat content.

### Task 14: Replace the §8 outer-section block

**Files:**
- Modify: `semanas/03/slides/index.html`

- [ ] **Step 1: Identify §8 outer-section bounds**

The §8 outer-section starts at the `<!-- ============================================================` block introducing `§8 — Demo en vivo` and ends at the matching `</section>` before `</div>` (the slides container).

Run: `grep -n "§8 — Demo en vivo\|</div>\s*</div>\s*<script" semanas/03/slides/index.html`
Expected: The §8 opener and the closing-divs/scripts block at the bottom.

- [ ] **Step 2: Replace the entire §8 block**

Find:

```html
      <!-- ============================================================
           §8 — Demo en vivo
           ============================================================ -->
      <!-- ============================================================
     §8 — Demo en vivo
     ============================================================ -->
<section>
```

… through the closing `</section>` immediately before `    </div>` (the slides container close).

Replace with:

```html
      <!-- ============================================================
           §8 — Demo en vivo: canvas escribe el openapi.yaml
           ============================================================ -->
<section>

  <!-- §8.1: Section divider — Demo en vivo -->
  <section class="section-divider">
    <h2>Demo en vivo</h2>
    <p class="muted" style="font-size: 0.85em; max-width: 36em; margin: 16px auto 0;">
      ChatGPT canvas escribe el <code>openapi.yaml</code>. Ustedes leen junto al profesor, endpoint por endpoint.
    </p>
    <aside class="notes">
      <p><u>Transici&oacute;n al cierre. La clase deja el modo conceptual y entra al modo demo en vivo.</u></p>
      <p><em>"Cerramos el recorrido conceptual. Lo que sigue no es otra secci&oacute;n te&oacute;rica: es el demo. Vamos a abrir ChatGPT, pegar un prompt y ver canvas escribir el openapi.yaml en pantalla. Ustedes me van a leer cada endpoint conmigo, mapeando al bloque del §4. Al final lo renderizamos en Swagger UI para ver las docs interactivas que salen del mismo archivo."</em></p>
    </aside>
  </section>

  <!-- §8.2: Lo que el yaml tiene que tener — 5 requisitos -->
  <section>
    <h2>Lo que el yaml tiene que tener</h2>
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 18px;">
      <div class="bg-secondary-card" style="border-left: 3px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Requisito 1</p>
        <h3 style="font-size: 0.95em; color: var(--accent); margin: 0 0 8px;">Tres methods</h3>
        <p style="font-size: 0.7em; line-height: 1.5; margin: 0;">M&iacute;nimo: GET, POST, DELETE.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 3px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Requisito 2</p>
        <h3 style="font-size: 0.95em; color: var(--accent); margin: 0 0 8px;">Jerarqu&iacute;a de recursos</h3>
        <p style="font-size: 0.7em; line-height: 1.5; margin: 0;"><code>projects &rarr; tasks</code>. Path nesting visible.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 3px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Requisito 3</p>
        <h3 style="font-size: 0.95em; color: var(--accent); margin: 0 0 8px;">Una respuesta de error</h3>
        <p style="font-size: 0.7em; line-height: 1.5; margin: 0;">Al menos un 400 o 404 documentado.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 3px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Requisito 4</p>
        <h3 style="font-size: 0.95em; color: var(--accent); margin: 0 0 8px;">Schemas tipados</h3>
        <p style="font-size: 0.7em; line-height: 1.5; margin: 0;"><code>type</code>, <code>required</code>, <code>format</code> donde aplique.</p>
      </div>
      <div class="bg-secondary-card" style="border-left: 3px solid var(--accent);">
        <p style="font-size: 0.6em; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px;">Requisito 5</p>
        <h3 style="font-size: 0.95em; color: var(--accent); margin: 0 0 8px;">Iteraci&oacute;n en vivo</h3>
        <p style="font-size: 0.7em; line-height: 1.5; margin: 0;">Agregar un endpoint sin reescribir todo.</p>
      </div>
    </div>
    <p style="margin-top: 22px; font-size: 0.78em; color: var(--text-muted); text-align: center; max-width: 44em; margin-left: auto; margin-right: auto;">
      <strong style="color: var(--text-muted);">Lo que NO entra:</strong> implementaci&oacute;n, base de datos, auth, deploy. Hoy: el contrato como archivo, le&iacute;do y editable.
    </p>
    <aside class="notes">
      <p><u>Los cinco requisitos del demo. Sirve como contrato visible con el aula sobre qu&eacute; tiene que aparecer en el yaml.</u></p>
      <p><em>"Antes de tocar nada, dejemos a la vista qu&eacute; tiene que tener el yaml. Cinco cosas. Tres methods HTTP &mdash; m&iacute;nimo GET, POST y DELETE. Una jerarqu&iacute;a de recursos &mdash; <code>projects</code> y dentro <code>tasks</code>, anidaci&oacute;n visible en el path. Una respuesta de error documentada &mdash; al menos un 400 o un 404. Schemas con tipos, requireds, formatos. E iteraci&oacute;n en vivo &mdash; vamos a agregar un endpoint sin reescribir el archivo entero."</em></p>
      <p><em>"Y abajo, el descargo de foco. No hay implementaci&oacute;n, ni base de datos real, ni autenticaci&oacute;n, ni deploy. Hoy es el contrato como archivo, le&iacute;do y editable. Si en alg&uacute;n momento alguno de estos cinco no aparece, me lo marcan."</em></p>
    </aside>
  </section>

  <!-- §8.3: La plantilla — el primer prompt -->
  <section>
    <h2>El primer prompt &mdash; antes de invocar canvas</h2>
    <p style="font-size: 0.72em; color: var(--text-muted); text-align: center; max-width: 38em; margin: 4px auto 14px;">
      Le damos el qu&eacute;. Canvas se abre. Editamos en vivo.
    </p>
    <pre style="margin: 0 auto; max-width: 38em; font-size: 0.7em; box-shadow: none;"><code class="language-text" data-trim data-line-numbers="|1|3-5|7-12|14"
>Necesito un openapi.yaml (3.1) para una API de proyectos y tareas.

recursos:
  Project   { id, name }
  Task      { id, title, due_date?, project_id }

endpoints:
  GET    /projects
  POST   /projects
  GET    /projects/{id}/tasks
  POST   /projects/{id}/tasks   &rarr; 201 / 400 / 404
  DELETE /projects/{id}/tasks/{taskId}

abrilo en canvas para que podamos editarlo juntos.</code></pre>
    <p style="margin-top: 18px; font-size: 0.78em; color: var(--text-muted); text-align: center; max-width: 38em; margin-left: auto; margin-right: auto;">
      Mismo dominio que el §4. Mismas cinco piezas. Ahora hechas archivo.
    </p>
    <aside class="notes">
      <p><strong>Mostrar el bloque entero, sin highlight, mientras se tipea en vivo. Click 1 ilumina la l&iacute;nea de framing. Click 2 ilumina recursos. Click 3 ilumina endpoints. Click 4 ilumina la l&iacute;nea de canvas.</strong></p>
      <p><u>Plantilla del prompt. Misma forma que §4.6 y §3.9 (vago vs espec&iacute;fico): expl&iacute;cita, pieza por pieza, mapeable a lo que termina escrito.</u></p>
      <p><em>"Antes de invocar canvas, escribimos el prompt a mano. Esta plantilla la van a ver levantarse en vivo en mi pantalla. Vamos a recorrerla pieza por pieza, igual que recorrimos el bloque del §4."</em></p>
      <p><em>"Primera l&iacute;nea: el framing. <code>openapi.yaml (3.1) para una API de proyectos y tareas</code>. Tres elecciones expl&iacute;citas &mdash; el formato (yaml), la versi&oacute;n (3.1) y el dominio (proyectos y tareas, el mismo del §4). Cero ambig&uuml;edad."</em></p>
      <p><em>"Recursos. Dos: <code>Project</code> con id y name; <code>Task</code> con id, title, due_date opcional, y project_id. La interrogaci&oacute;n marca campos opcionales, igual que en TypeScript. Los nombres son los mismos que vinimos usando."</em></p>
      <p><em>"Endpoints. Cinco. GET y POST sobre <code>/projects</code>; despu&eacute;s GET, POST y DELETE sobre <code>/projects/{id}/tasks</code> con anidaci&oacute;n. Tres methods, jerarqu&iacute;a expl&iacute;cita, y en el POST anidado dictamos los tres status: 201 cuando se cre&oacute;, 400 cuando el body est&aacute; mal, 404 cuando el proyecto no existe. Las cinco piezas del §4."</em></p>
      <p><em>"&Uacute;ltima l&iacute;nea: <code>abrilo en canvas</code>. Eso le dice al modelo que esto va a ser un documento que vamos a editar en colaboraci&oacute;n, no una respuesta corta del chat. Si por alguna raz&oacute;n no se abre, lo pedimos expl&iacute;citamente."</em></p>
    </aside>
  </section>

  <!-- §8.4: Beats del demo — clickable-steps -->
  <section>
    <h2>Los seis beats del demo</h2>
    <p style="font-size: 0.72em; color: var(--text-muted); text-align: center; max-width: 38em; margin: 4px auto 14px;">
      Checklist de momentos donde paramos a leer junto con ustedes.
    </p>
    <div id="demo-beats"></div>
    <aside class="notes">
      <p><strong>Usar como checklist mientras corre el demo. Click en cada beat al cubrirlo para mostrar el detalle al aula y dejar marca de avance.</strong></p>
      <p><u>Slide-anclaje del demo. Las seis pausas explicitan d&oacute;nde se rompe la inercia del &laquo;sigue tipeando&raquo; para leer.</u></p>
      <p><em>"Mientras corra el demo, esta slide queda atr&aacute;s. Son seis momentos donde voy a pausar y vamos a leer juntos. No son seis &laquo;pasos a seguir&raquo;: son las seis veces que rompemos la inercia para mirar lo que apareci&oacute;. Si alguno se les pasa, me lo marcan."</em></p>
    </aside>
  </section>

  <!-- §8.5: Cierre — el contrato tiene archivo -->
  <section>
    <p class="big-question" style="font-size: 1.4em;">
      Ustedes no tipearon nada.<br>
      <span class="fragment fade-in accent">Lo que dirigieron fue el contrato.</span><br>
      <span class="fragment fade-in" style="color: var(--accent);">Y ahora tiene archivo.</span>
    </p>
    <p class="muted" style="font-size: 0.85em; max-width: 32em; margin: 28px auto 0; text-align: center;">
      El rol &mdash; supervisor arquitect&oacute;nico &mdash; sobrevivi&oacute; la mudanza al servidor.
    </p>
    <p style="margin-top: 32px; padding-top: 18px; border-top: 1px solid var(--bg-secondary); font-size: 0.7em; color: var(--text-muted); text-align: center; max-width: 38em; margin-left: auto; margin-right: auto;">
      <strong style="color: var(--text-muted);">Pr&oacute;xima clase:</strong> tomamos este yaml y se lo damos a una IA local para que escriba la implementaci&oacute;n. Tarea de instalaci&oacute;n se confirma por el canal del curso esta semana.
    </p>
    <aside class="notes">
      <p><strong>Treinta segundos. Voz baja, mirar al aula, dejar las frases respirar entre fragments.</strong></p>
      <p><u>Cierre del demo y de la clase. Cierra el espejo con semana 02 y bridge a semana 4.</u></p>
      <p><em>"Lo que acaba de pasar: ustedes no tipearon nada. Lo que dirigieron fue el contrato. Y ahora tiene archivo &mdash; un openapi.yaml que pueden bajar, versionar, dictar de nuevo, pasar a otro modelo."</em></p>
      <p><em>"Eso es exactamente lo mismo que hicimos la semana pasada con el frontend. Cambi&oacute; el terreno, no el rol. El supervisor arquitect&oacute;nico sobrevivi&oacute; la mudanza al servidor."</em></p>
      <p><em>"La pr&oacute;xima clase tomamos exactamente este yaml y se lo damos a una IA local para que escriba la implementaci&oacute;n. La tarea de instalaci&oacute;n para llegar listos la mando esta semana por el canal del curso, junto con el yaml de hoy. Nos vemos."</em></p>
    </aside>
  </section>

</section>
```

Note: The footer of §8.5 carries the placeholder for the semana-04 install homework as a soft reference ("se confirma por el canal del curso esta semana"). This avoids hardcoding install commands that may change once semana 04 firms up. The spec's open thread covers this.

- [ ] **Step 3: Verify §8 structurally**

Run: `grep -nE "§8\.[0-9]" semanas/03/slides/index.html`
Expected: Five §8 marker comments (`§8.1`–`§8.5`).

Run: `grep -n "id=\"demo-beats\"" semanas/03/slides/index.html`
Expected: Exactly one hit (in §8.4).

### Task 15: Update the `clickable-steps` initialization with new beats

**Files:**
- Modify: `semanas/03/slides/index.html`

The `<script>` near the bottom of the file initializes `demo-beats` with the old 6 Claude Code beats. Replace the steps array.

- [ ] **Step 1: Find the existing init block**

Run: `grep -n "containerId: 'demo-beats'" semanas/03/slides/index.html`
Expected: One hit, in the `<script>` block near the end of the file.

- [ ] **Step 2: Replace the steps array**

Find the entire `initClickableSteps({...})` invocation (from `initClickableSteps({` through the matching `});`).

Replace with:

```javascript
  initClickableSteps({
    containerId: 'demo-beats',
    steps: [
      {
        title: 'Beat 1',
        summary: 'Pegar el prompt &mdash; canvas se abre con el yaml inicial.',
        color: 'var(--accent-secondary)',
        borderColor: 'var(--text-muted)',
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Pegar el prompt:</div>'
          + '<div style="line-height: 1.5;">Canvas se abre con el yaml inicial. Frase clave: <em>&laquo;esto no lo escribimos; lo dictamos&raquo;</em>.</div>'
      },
      {
        title: 'Beat 2',
        summary: 'Leer el primer endpoint &mdash; mapear al bloque del §4.',
        color: 'var(--accent-secondary)',
        borderColor: 'var(--text-muted)',
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Leer <code>POST /projects/{id}/tasks</code>:</div>'
          + '<div style="line-height: 1.5;">Recorrer en voz alta: <code>paths</code>, <code>post</code>, <code>parameters</code>, <code>requestBody</code>, <code>responses</code>. Mapear a las cinco piezas del §4.</div>'
      },
      {
        title: 'Beat 3',
        summary: 'Agregar un endpoint en vivo desde el chat.',
        color: 'var(--accent-secondary)',
        borderColor: 'var(--text-muted)',
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Pedirle al modelo:</div>'
          + '<div style="line-height: 1.5;"><em>&laquo;agregame DELETE /projects/{id}, con 404 si no existe&raquo;</em>. Mostrar canvas actualizando en tiempo real. Frase: <em>&laquo;el contrato es editable; no es un prompt de un solo tiro&raquo;</em>.</div>'
      },
      {
        title: 'Beat 4',
        summary: 'Editar a mano dentro del canvas.',
        color: 'var(--accent-secondary)',
        borderColor: 'var(--text-muted)',
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Editar el yaml directamente:</div>'
          + '<div style="line-height: 1.5;">Por ejemplo, agregar un campo <code>description</code> opcional al schema de <code>Task</code>. Frase: <em>&laquo;la IA y vos comparten editor&raquo;</em>.</div>'
      },
      {
        title: 'Beat 5',
        summary: 'Pegar el yaml en <code>editor.swagger.io</code> &mdash; ver Swagger UI renderizado.',
        color: 'var(--accent-secondary)',
        borderColor: 'var(--text-muted)',
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Renderizar el yaml:</div>'
          + '<div style="line-height: 1.5;">Pegar en <code>editor.swagger.io</code>. Click en <code>POST /projects</code> &rarr; <em>&laquo;Try it out&raquo;</em> &rarr; <em>&laquo;Execute&raquo;</em>. Frase: <em>&laquo;del mismo archivo salieron docs interactivas. Codegen es real, no abstracci&oacute;n&raquo;</em>.</div>'
      },
      {
        title: 'Beat 6',
        summary: 'Cierre 30 seg &mdash; el contrato tiene archivo.',
        color: 'var(--accent)',
        borderColor: 'var(--accent)',
        borderFull: true,
        example: '<div style="color: var(--text-muted); margin-bottom: 6px;">Cierre, treinta segundos:</div>'
          + '<div style="line-height: 1.5;"><em>&laquo;ustedes no tipearon nada. Lo que dirigieron fue el contrato. Y ahora tiene archivo.&raquo;</em> Bridge a semana 4: <em>&laquo;la pr&oacute;xima clase tomamos este yaml y se lo damos a una IA local para que escriba la implementaci&oacute;n.&raquo;</em></div>'
      }
    ]
  });
```

- [ ] **Step 3: Verify the script block parses cleanly**

Run: `grep -A 1 "initClickableSteps" semanas/03/slides/index.html | head -5`
Expected: The new steps array is in place.

### Task 16: Verify §8 in browser + commit

- [ ] **Step 1: Visual verification**

Reload `http://localhost:3000/semanas/03/slides/`. Walk §8.1 through §8.5.

Check:
- §8.1: section divider renders. Subtitle reads "ChatGPT canvas escribe el openapi.yaml. Ustedes leen junto al profesor, endpoint por endpoint."
- §8.2: 5-column grid renders. Counter-block ("Lo que NO entra…") appears below.
- §8.3: prompt code-block renders. Step-through cycles through 4 highlight stages.
- §8.4: clickable-steps renders. Click each of the 6 beats and confirm the detail panel shows the expected text. Beat 5 detail mentions `editor.swagger.io`. Beat 6 detail mentions "tomamos este yaml y se lo damos a una IA local".
- §8.5: closing reveal. First click reveals "Lo que dirigieron fue el contrato." Second reveals "Y ahora tiene archivo." Footer block at the bottom reads correctly.

- [ ] **Step 2: Open speaker notes for §8.5**

Press `s`. Walk §8.1–§8.5 speaker notes. Confirm they match the spec.

- [ ] **Step 3: Commit Phase 4**

```bash
git add semanas/03/slides/index.html
git commit -m "$(cat <<'EOF'
feat(semana-03): rebuild §8 demo around ChatGPT canvas + Swagger UI

Replace 6-slide Claude-Code-builds-FastAPI demo with 5-slide canvas
demo: section divider, 5 yaml requirements, prompt template, 6 beats
(clickable-steps), closing with bridge to semana 4. Demo evolves the
§4 projects/tasks contract into openapi.yaml live, ending with a
Swagger UI render at editor.swagger.io.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Phase 5 — End-to-end verification

### Task 17: Walk the entire deck top-to-bottom

- [ ] **Step 1: Reload and walk slide-by-slide**

In the browser, press `Esc` to open the slide overview. Walk every slide using arrow keys. Verify:
- Title slide → §1.1 → §1.2 → §1.4 → §1.5 → §2.1 (roadmap with piece 1 lit) → … → §6.last → §7.1 (roadmap with piece 6 lit, labeled OpenAPI) → §7.2 → §7.3 → §8.1 → §8.5.
- No broken transitions (section divider between §7 and §8 renders cleanly).
- The 6th roadmap node always reads "OpenAPI / contrato escrito" except in §7.1 where it's the active piece.
- No "Salto al stack", no "Claude Code", no "FastAPI" / "Uvicorn" / "venv" / "SQLite + servidor" leftovers anywhere.

- [ ] **Step 2: Final consistency grep**

Run:
```bash
grep -nE "Salto al stack|al stack local|Claude Code|claude-code|@anthropic-ai/claude-code|levantar un servidor con Claude|uvicorn app" semanas/03/slides/index.html
```
Expected: No hits.

Run:
```bash
grep -nE "OpenAPI|openapi\.yaml|canvas|Swagger" semanas/03/slides/index.html | wc -l
```
Expected: At least 15 hits across §1.1, §1.2, §1.4, the 5 section openers, §7.1–§7.3, §8.1–§8.5.

- [ ] **Step 3: Confirm no orphan CSS or JS remains**

The previous §7 had scoped `.s7-*` CSS (s7-pipeline, s7-alts, s7-task-grid, s7-task-card, s7-cli-cards). It was inside the §7 outer-section that we replaced wholesale, so it should already be gone.

Run: `grep -n "s7-pipeline\|s7-alts\|s7-task-grid\|s7-task-card\|s7-cli-cards" semanas/03/slides/index.html`
Expected: No hits. If any hits remain, they are dead CSS — delete the matching `<style>` block contents.

- [ ] **Step 4: Final commit (only if Step 3 found cleanups)**

If no cleanups needed, skip this step. If cleanups landed:

```bash
git add semanas/03/slides/index.html
git commit -m "$(cat <<'EOF'
chore(semana-03): drop orphan CSS from old §7 implementation

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Task 18: Mark plan complete

- [ ] **Step 1: Confirm spec coverage**

Open `docs/superpowers/specs/2026-05-10-semana-03-openapi-canvas-demo-design.md` and check each section:
- §7 rebuild — ✓ Task 12
- §8 rebuild — ✓ Task 14 + Task 15
- 7 §1–§6 patches — ✓ Tasks 6–10
- Spine + source_material — ✓ Tasks 1–4
- Open thread (semana-04 install homework) — ✓ §8.5 footer carries soft reference per spec

If any spec requirement is uncovered, add a task before closing.

- [ ] **Step 2: Push (only if user explicitly asks)**

This plan does NOT push to remote by default. If the user asks, run:

```bash
git push origin feature/semana-03-slides
```
