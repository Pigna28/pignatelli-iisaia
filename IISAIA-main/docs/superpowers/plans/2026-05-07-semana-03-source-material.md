# Semana 03 Source Material Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Populate `semanas/03/source_material/` with 9 markdown files (1 index + 8 content blocks) ready to be transformed into a reveal.js deck by `/build-class`.

**Architecture:** Markdown-only. No `demo.html`-style artifact: the live demo is generated in class with Claude Code, so the only "demo" file is a guion (`08-demo-en-vivo.md`) describing what Enzo will dictate. All copy in Spanish, professor voice, mirroring semana 02's style.

**Tech Stack:** Plain markdown.

**Spec reference:** `docs/superpowers/specs/2026-05-07-semana-03-source-material-design.md`

---

## File structure

| Path | Status | Responsibility |
|------|--------|----------------|
| `semanas/03/source_material/index.md` | Replace stub | Master index — reading order + hilo conductor |
| `semanas/03/source_material/01-backend-y-el-supervisor.md` | Create | Apertura: why backend vocabulary matters under AI assistance |
| `semanas/03/source_material/02-cliente-servidor-y-http.md` | Create | Client-server, HTTP verbs, status codes |
| `semanas/03/source_material/03-rest-como-estilo.md` | Create | REST as style: resource, URL hierarchy, idempotency, statelessness |
| `semanas/03/source_material/04-rutas-controladores-y-contratos.md` | Create | Endpoint = verb + path + schemas + status codes; the contract as dictable unit |
| `semanas/03/source_material/05-datos-relaciones-vs-documentos.md` | Create | SQL vs NoSQL, minimal modeling, SQLite as entry point |
| `semanas/03/source_material/06-errores-y-observabilidad.md` | Create | 4xx vs 5xx, logs, stack traces, vocabulary to debug with AI |
| `semanas/03/source_material/07-de-lo-local-al-stack.md` | Create | Bisagra: why local + Claude Code (CLI); stack map (FastAPI + alternatives); homework |
| `semanas/03/source_material/08-demo-en-vivo.md` | Create | Guion of the live demo: planning, execution beats, pause-points |

**Word-count targets:** 600–900 words per content markdown. `index.md` ~250 words. `08-demo-en-vivo.md` may be shorter (~400–600) since it's a script, not exposition.

---

## Voice and didactic conventions

All markdown copy must follow these conventions (mirrored from semana 02):

- **Spanish, professor voice.** Direct, second-person ("vas a", "fijate en"). Not corporate.
- **Concrete over abstract.** Examples first, name the concept after.
- **Bold the vocabulary terms** on first use. Students use these markdowns as glossary.
- **No bullet-list theatre.** Prose where prose works. Lists only for genuine enumerations.
- **Connect to course thesis.** Student is **supervisor arquitectónico**. They name what they want; the LLM writes syntax.
- **No emojis** anywhere (global rule).
- **No "diplomatura", no "Vibe Coding", no "payoff", no "seamless" / "leverage" / "robust"** etc. (memory feedback rules).
- **No mention of auth/security topics** — owned by semana 07. If an example begs for it (e.g., 401), say "lo vemos en semana 07" in one phrase and move on.
- **Avoid stepping on semana 04** — when CLI/IDE-AI is mentioned, stick to the *why* (transparency, file-by-file visibility) and the *what's next* (instalar Claude Code). No `.cursorrules`, no Composer, no agentic mode.

---

## Task 1: Replace `index.md` stub with master index

**Files:**
- Modify: `semanas/03/source_material/index.md` (currently 13-line stub)

- [ ] **Step 1: Read the current stub**

Run: `cat semanas/03/source_material/index.md`
Expected: 13-line stub with "Temas" list and an empty "Archivos" placeholder.

- [ ] **Step 2: Replace contents with the master index**

Replace the entire file with:

```markdown
# Semana 3 — Arquitectura Backend y Datos

Este es el material fuente de la clase de Semana 3. La presentación reveal.js se genera con `/build-class` a partir de estos archivos.

## Orden de lectura

| # | Archivo | Tema | Bloque de clase |
|---|---------|------|-----------------|
| 1 | [01-backend-y-el-supervisor.md](01-backend-y-el-supervisor.md) | Por qué hace falta vocabulario backend cuando la IA escribe el código | Apertura (~10 min) |
| 2 | [02-cliente-servidor-y-http.md](02-cliente-servidor-y-http.md) | Cliente-servidor, verbos HTTP y códigos de estado | Anatomía (~15 min) |
| 3 | [03-rest-como-estilo.md](03-rest-como-estilo.md) | REST como estilo: recurso, jerarquía, idempotencia | Anatomía (~12 min) |
| 4 | [04-rutas-controladores-y-contratos.md](04-rutas-controladores-y-contratos.md) | El endpoint como contrato dictable | Anatomía (~12 min) |
| 5 | [05-datos-relaciones-vs-documentos.md](05-datos-relaciones-vs-documentos.md) | SQL vs NoSQL: cuándo conviene cada uno | Anatomía (~15 min) |
| 6 | [06-errores-y-observabilidad.md](06-errores-y-observabilidad.md) | Leer fallas: 4xx, 5xx, logs, stack traces | Anatomía (~10 min) |
| 7 | [07-de-lo-local-al-stack.md](07-de-lo-local-al-stack.md) | Bisagra a local; FastAPI y alternativas; tarea para semana 04 | Bisagra (~12 min) |
| 8 | [08-demo-en-vivo.md](08-demo-en-vivo.md) | Guion del demo en vivo con Claude Code | Demo (~30 min) |

## Hilo conductor

Esta clase enseña vocabulario backend para que el alumno pueda **dirigir** una IA cuando el código que se genera ya no vive en una pestaña del navegador. Es el espejo simétrico de la semana 02: igual que ahí aprendiste a nombrar las piezas del frontend, acá aprendés a nombrar las piezas del backend — verbos, rutas, contratos, datos, errores — y a pedirlas con precisión.

La clase también marca la bisagra del curso: dejamos atrás los entornos web (Canvas) y nos preparamos para trabajar en local. El cierre es un demo en vivo donde el profesor levanta un servidor con Claude Code; los alumnos no escriben código en clase, pero llegan a semana 04 con la herramienta instalada.
```

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/index.md
git commit -m "feat(semana-03): replace source_material index with master reading order"
```

---

## Task 2: Write `01-backend-y-el-supervisor.md`

**Files:**
- Create: `semanas/03/source_material/01-backend-y-el-supervisor.md`

**Goal of the file:** Open the class. Re-anchor the supervisor framing on the backend side. Establish that the student leaves with vocabulary to dictate contracts, not with FastAPI fluency. Mirror of `semanas/02/source_material/01-frontend-y-el-supervisor.md` in structure (~600–800 words).

**Key vocabulary to bold on first use:** supervisor arquitectónico, contrato, vocabulario backend, dirigir.

**Opening hook (first paragraph):** Pose the parallel question to semana 02's "if AI writes the code, why learn flexbox?" — but for backend. Something like: "Si la IA puede levantarte un servidor en treinta segundos, ¿qué sentido tiene aprender qué es un POST o cómo se modela una tabla?"

**Required sections (use H2 headings, prose between them, no bullet theatre):**

1. **La pregunta en versión backend.** Same shape as semana 02's "La pregunta incómoda". Reframe: memorizing FastAPI routes is not the point; deciding what gets built is.
2. **Lo que cambia cuando el código vive en un servidor.** Three movements (mirror semana 02's three): (a) la persistencia hace que los errores ya no sean efímeros — un bug guarda datos malos, y los datos malos no se borran al recargar; (b) el dialogo cliente-servidor introduce contratos reales — la IA puede inventar un endpoint que el frontend no sabe consumir; (c) leer la respuesta del servidor (códigos, logs, JSON) se vuelve tan importante como leer el código generado.
3. **La anatomía en seis partes.** Numbered list (this is a genuine enumeration) of the six anatomy blocks the class will visit, one sentence each. The six are: HTTP, REST, contratos/rutas, datos, errores, bisagra a local. Use the same shape as semana 02's "anatomía en cinco partes".
4. **A qué prestamos atención esta clase.** Same disclaimer slot as semana 02: not teaching FastAPI/Python/SQL production-ready. Teaching to *name the pieces*. Closing line ties back to the supervisor role and previews that the class ends with a demo.

**Don't:** introduce specific HTTP verbs, status codes, or framework names yet — those live in their own files.

- [ ] **Step 1: Re-read semana 02's `01-frontend-y-el-supervisor.md`**

Run: `cat semanas/02/source_material/01-frontend-y-el-supervisor.md`
Expected: 43-line file you'll structurally mirror.

- [ ] **Step 2: Write the file following the structure above**

Apply voice conventions. Word target: 600–800. Bold vocabulary on first use. Use H2 headings as specified. Match the prose density of semana 02's file (no bullet lists outside the "anatomía en seis partes" enumeration).

- [ ] **Step 3: Verify the file**

Run: `wc -w semanas/03/source_material/01-backend-y-el-supervisor.md`
Expected: between 600 and 850.

Run: `grep -E '(diplomatura|Vibe Coding|payoff|seamless|leverage|robust)' semanas/03/source_material/01-backend-y-el-supervisor.md` (Grep tool, case-insensitive)
Expected: no matches.

- [ ] **Step 4: Commit**

```bash
git add semanas/03/source_material/01-backend-y-el-supervisor.md
git commit -m "feat(semana-03): add 01-backend-y-el-supervisor opening"
```

---

## Task 3: Write `02-cliente-servidor-y-http.md`

**Files:**
- Create: `semanas/03/source_material/02-cliente-servidor-y-http.md`

**Goal of the file:** Teach the client-server model and HTTP as a request/response protocol. Verbs as nouns of work. Status codes as failure vocabulary. ~700–900 words.

**Key vocabulary to bold on first use:** cliente, servidor, HTTP, request, response, verbo (GET, POST, PUT, PATCH, DELETE), código de estado, 2xx, 4xx, 5xx, payload, headers.

**Opening hook:** Scene from the student's daily life — when they open Twitter or refresh Gmail, what travels between their phone and the data center. Concrete, not abstract.

**Required sections:**

1. **Cliente y servidor: dos roles, una conversación.** Define both. Highlight that *cualquier cosa* can be a client (browser, mobile app, another server, `curl`). Explicit: el frontend de semana 02 ya era un cliente, no lo sabíamos.
2. **HTTP como protocolo de pedido/respuesta.** Anatomy of a request: método + URL + headers + body. Anatomy of a response: status code + headers + body. One concrete example pair, written out as text (no diagrams in the markdown — diagrams come from `/build-class`).
3. **Los verbos como sustantivos del trabajo.** GET (leer), POST (crear), PUT/PATCH (actualizar — explain the difference: PUT replaces, PATCH modifies), DELETE (borrar). Each verb gets one sentence + one example URL.
4. **Códigos de estado: el vocabulario de las fallas.** Three families: 2xx (todo bien — 200, 201, 204), 4xx (vos, cliente, te equivocaste — 400, 404; mention 401/403 exist and "lo vemos en semana 07"), 5xx (yo, servidor, me caí — 500, 503). Emphasize: when you read a code, you're reading *whose fault* it is.
5. **Por qué importa para vos como supervisor.** When you ask the AI for an endpoint, you should be able to specify the verb, predict the status code, and read the response. If you can't, you're outsourcing decisions you don't know you made.

**Closing prompt-comparison pattern (per memory rule):** end with a "vago vs específico" pair framed around determinism / iteration / auditability. Vague: "hace una API para guardar tareas". Specific: "definí un endpoint POST `/tasks` que reciba `{title: string, due_date: string}` en el body, devuelva 201 con el objeto creado o 400 si falta `title`". Frame it as: el específico es auditable; el vago no.

- [ ] **Step 1: Write the file**

Word target: 700–900. Match voice. Section structure as above. Closing comparison block included.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/02-cliente-servidor-y-http.md`
Expected: 700–950.

Grep for forbidden phrases: `grep -iE '(diplomatura|vibe coding|payoff|seamless)' semanas/03/source_material/02-cliente-servidor-y-http.md`
Expected: no matches.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/02-cliente-servidor-y-http.md
git commit -m "feat(semana-03): add 02-cliente-servidor-y-http"
```

---

## Task 4: Write `03-rest-como-estilo.md`

**Files:**
- Create: `semanas/03/source_material/03-rest-como-estilo.md`

**Goal of the file:** Distinguish REST (architectural style) from HTTP (transport). Recurso as central abstraction, URL hierarchy, idempotency, statelessness. ~600–800 words.

**Key vocabulary to bold:** REST, recurso, jerarquía de URLs, idempotencia, statelessness (sin estado), colección, item.

**Opening hook:** Frame the gap. The student now knows HTTP verbs exist. But how do you decide that "borrar la tarea 17 del proyecto 4" is `DELETE /projects/4/tasks/17` and not `POST /borrar-tarea?id=17&proyecto=4`? Both work over HTTP. One is REST. Most APIs you'll encounter speak REST.

**Required sections:**

1. **HTTP es el cómo; REST es el qué.** HTTP is the transport. REST is a *convention* for designing what gets transported. Quick mention that REST is not the only style (GraphQL, RPC) but is dominant.
2. **Todo es un recurso.** A resource is a noun: project, task, user, message. URLs name resources, not actions. `/projects` (collection), `/projects/4` (item), `/projects/4/tasks` (sub-collection). Two or three concrete URL trees.
3. **Las cuatro reglas que importan.** Four short subsections (one paragraph each):
   - **Recursos en plural.** Convention: `/users` not `/user`. Verbs do the action; URLs name the noun.
   - **Jerarquía cuando hay relación.** `/projects/4/tasks` says "the tasks of project 4". When relationships matter, nest.
   - **Idempotencia.** GET, PUT, DELETE are idempotent: calling them twice is the same as calling them once. POST is not. Why this matters: when a request fails and you retry, idempotent verbs are safe.
   - **Sin estado entre requests.** Each request carries everything the server needs. The server doesn't remember "the user that just called me". This is what makes REST scale and what makes auth tokens (semana 07) necessary.
4. **Cómo cambia la forma de dictar a la IA.** Once you think in resources, your prompt to the AI changes. You stop saying "hacé un endpoint para borrar tareas" and start saying "expone un recurso `/projects/{id}/tasks/{id}` con DELETE para borrar y GET para consultar".

**Closing prompt-comparison:** vague "API para gestionar proyectos y sus tareas" vs specific "diseñá una API REST con dos recursos anidados: `/projects` (GET, POST) y `/projects/{id}/tasks` (GET, POST, DELETE), todas las rutas devuelven JSON, las idempotentes (GET, DELETE) deben poder llamarse dos veces sin efectos diferentes."

- [ ] **Step 1: Write the file**

Word target: 600–800. Voice + bolding rules.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/03-rest-como-estilo.md` → expect 600–850.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/03-rest-como-estilo.md
git commit -m "feat(semana-03): add 03-rest-como-estilo"
```

---

## Task 5: Write `04-rutas-controladores-y-contratos.md`

**Files:**
- Create: `semanas/03/source_material/04-rutas-controladores-y-contratos.md`

**Goal of the file:** Make the *contract* concrete and dictable. Endpoint = verb + path + input schema + output schema + possible status codes. Pseudocode only — no FastAPI yet. ~700–900 words.

**Key vocabulary to bold:** endpoint, ruta (path), controlador, schema de entrada, schema de salida, contrato, parámetros de path, parámetros de query, body.

**Opening hook:** Concrete scenario — you tell the AI "hacé un endpoint para crear una tarea". The AI guesses ten things you didn't say: which fields are required, what happens if `due_date` is invalid, what shape the response has, what code returns on success, what on conflict. A contract removes the guesses.

**Required sections:**

1. **Una ruta es una promesa.** Define the five pieces of an endpoint: verb, path, input schema, output schema, possible status codes. Each piece corresponds to a question the AI will otherwise guess.
2. **Path, query y body: dónde viajan los datos.** Three locations data can ride. Path params (`/projects/{id}`) — identify a resource. Query params (`?page=2&sort=date`) — modify a read. Body (JSON) — carry payload for create/update. One sentence each + one mini-example.
3. **El controlador: quién atiende la promesa.** The controller is the function on the server that receives the request and produces the response. The student doesn't write controllers; they *specify* what each controller must do. Pseudocode example (language-agnostic, NOT Python):
   ```
   POST /projects/{id}/tasks
     entrada: { title: string (requerido), due_date: ISO date (opcional) }
     salida 201: { id: int, title: string, due_date: ISO date | null, project_id: int }
     salida 400: { error: "title es requerido" }
     salida 404: { error: "el proyecto no existe" }
   ```
4. **Por qué este es el átomo dictable.** This block — the contract — is the smallest complete unit you can hand to an AI without ambiguity. It's the backend equivalent of "componente con props tipadas y estado bien definido" from semana 02.

**Closing prompt-comparison:** vague "hacé el endpoint de crear tarea" vs specific (the full contract block from section 3 above, dictated as a prompt).

- [ ] **Step 1: Write the file**

Word target: 700–900. Pseudocode block must be plain text fenced as ` ``` ` (no language hint), to avoid suggesting Python.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/04-rutas-controladores-y-contratos.md` → expect 700–950.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/04-rutas-controladores-y-contratos.md
git commit -m "feat(semana-03): add 04-rutas-controladores-y-contratos"
```

---

## Task 6: Write `05-datos-relaciones-vs-documentos.md`

**Files:**
- Create: `semanas/03/source_material/05-datos-relaciones-vs-documentos.md`

**Goal of the file:** Why persist. SQL (tables, schemas, foreign keys) vs NoSQL (documents). When each fits. SQLite as honest entry point. ~700–900 words.

**Key vocabulary to bold:** persistencia, base de datos relacional (SQL), tabla, fila, columna, esquema, foreign key (clave foránea), join, base de datos documental (NoSQL), documento, colección, SQLite.

**Opening hook:** Recall semana 02 — the to-do list lived in a JS variable. Refresh the page, all gone. That's not a bug; the page never had memory. The server is what gives memory. The question of this section: *what shape* does that memory take?

**Required sections:**

1. **Por qué hace falta una base de datos.** Three reasons, prose: persistencia entre sesiones, consultas eficientes (no es lo mismo buscar entre 10 ítems que entre 10 millones), integridad (no podés tener una tarea con `project_id = 99` si no existe el proyecto 99).
2. **Relacional: el mundo de tablas.** Define table, row, column, schema, foreign key. One concrete example — two tables `projects` and `tasks` with a foreign key — drawn out as text:
   ```
   projects
     id (int, primary key)
     name (text)

   tasks
     id (int, primary key)
     title (text)
     project_id (int, foreign key → projects.id)
   ```
   Mention `JOIN` as the operation that combines them. Don't teach SQL syntax beyond the conceptual.
3. **Documental: el mundo de objetos anidados.** Define document, collection. Same example as a single document with embedded tasks:
   ```
   {
     "id": "p1",
     "name": "Tesis",
     "tasks": [
       { "id": "t1", "title": "Marco teórico" },
       { "id": "t2", "title": "Bibliografía" }
     ]
   }
   ```
   Mention MongoDB and DynamoDB as well-known examples. Highlight the trade-off: anidar es cómodo para leer "todo de un proyecto" pero malo si las tareas también viven solas.
4. **Cómo elegir.** Plain heuristic, not a religious war. Relacional cuando: hay relaciones claras y querés integridad (ej. facturación, inventario). Documental cuando: el dato es jerárquico, esquema-flexible, optimizado para escritura/lectura por documento (ej. logs, perfiles de usuario con muchos campos opcionales). Most apps you'll build start relacional and stay there.
5. **SQLite como punto de entrada.** Por qué SQLite y no Postgres en una clase introductoria: cero configuración, vive en un archivo, suficiente para todo lo que vamos a hacer en el demo. Honest framing: en producción real probablemente uses Postgres, pero las decisiones de modelado son las mismas.

**Closing prompt-comparison:** vague "guardá tareas y proyectos en una base" vs specific "modelá dos tablas relacionales en SQLite — `projects(id, name)` y `tasks(id, title, due_date, project_id)` con foreign key — generá las migraciones y un seed con dos proyectos y cinco tareas".

- [ ] **Step 1: Write the file**

Word target: 700–900. Both code blocks are plain text fenced.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/05-datos-relaciones-vs-documentos.md` → expect 700–950.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/05-datos-relaciones-vs-documentos.md
git commit -m "feat(semana-03): add 05-datos-relaciones-vs-documentos"
```

---

## Task 7: Write `06-errores-y-observabilidad.md`

**Files:**
- Create: `semanas/03/source_material/06-errores-y-observabilidad.md`

**Goal of the file:** Reading failures is half of supervising. 4xx vs 5xx, logs, stack traces. Vocabulary to converse with the AI when something breaks. ~600–800 words.

**Key vocabulary to bold:** error, 4xx, 5xx, log, stack trace, mensaje de error, traza, observabilidad.

**Opening hook:** Concrete scene — the AI generated an endpoint, you hit it from the browser, it returns "500 Internal Server Error". Two possible reactions: (a) copy-paste "no funciona" into the chat and pray; (b) read the logs, find the line that broke, paste *that* into the chat. The difference is vocabulary.

**Required sections:**

1. **Errores tienen dueño.** 4xx significa "vos, cliente, te equivocaste" — pediste un recurso que no existe, mandaste un body inválido, pegaste a una ruta mal escrita. 5xx significa "yo, servidor, me caí" — el código tiene un bug, la DB no responde, la AI olvidó manejar un caso. Diagnostic move: leer el código primero te dice de qué lado mirar.
2. **Logs: lo que el servidor te susurra.** A log is a line the server writes whenever something happens. Logs viven en la terminal donde corre el servidor (en local) o en un sistema de agregación (en producción). Cuando algo falla, el log tiene la verdad — qué request entró, qué pasó adentro, qué se rompió. Concrete sample log line as plain text.
3. **El stack trace: el camino al bug.** When code crashes server-side, you get a stack trace — the chain of function calls that led to the failure. Don't try to read it linearly; the relevant line is usually the *first* one that mentions *your* code (not framework code). Concrete example as plain text — three frames, point at the meaningful one.
4. **Cómo le contás esto a la IA.** Bad: "no funciona, dame fix". Good: "Tengo un 500 en POST /tasks. El log dice `KeyError: 'title'` en `routes/tasks.py:14`. El handler es \[copia el código]. ¿Por qué?". You're handing the AI the same evidence a human would need.
5. **Observabilidad: la palabra paraguas.** Quick definition: observabilidad es el conjunto de prácticas para que un sistema te cuente qué está haciendo (logs, métricas, traces). En esta clase nos quedamos con logs porque es lo que vas a ver vos en tu terminal, pero el concepto es más amplio.

**Closing prompt-comparison:** vague "este endpoint no anda, arreglalo" vs specific "el endpoint `POST /tasks` devuelve 500. El log adjunto muestra `IntegrityError: NOT NULL constraint failed: tasks.project_id` cuando mando body `{title: 'X'}`. ¿Es un bug del schema, de la validación o falta default?".

- [ ] **Step 1: Write the file**

Word target: 600–800. Logs and stack-trace examples as plain-text fenced blocks.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/06-errores-y-observabilidad.md` → expect 600–850.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/06-errores-y-observabilidad.md
git commit -m "feat(semana-03): add 06-errores-y-observabilidad"
```

---

## Task 8: Write `07-de-lo-local-al-stack.md`

**Files:**
- Create: `semanas/03/source_material/07-de-lo-local-al-stack.md`

**Goal of the file:** The bisagra. Two beats: (a) why Canvas is no longer enough → why local + CLI AI; (b) the stack map (FastAPI plus alternatives), positioning FastAPI as one choice among many. End with the homework. ~700–900 words.

**Key vocabulary to bold:** local, terminal, CLI, Claude Code, proceso, puerto, FastAPI, Python, venv, Uvicorn, Express (Node), Django, Flask.

**Opening hook:** Recall: until now everything happened in a browser tab. Canvas, ChatGPT, the page from semana 02. That worked because the artefact was self-contained. A real backend can't live in a tab — it needs a process, a port, files, a database file on a disk. That's your computer. The class pivots here.

**Required sections:**

1. **Por qué Canvas no alcanza.** Three concrete things a real backend has that a Canvas tab can't give you: un proceso que corre indefinidamente, un puerto donde escucha, un sistema de archivos para guardar la base. Sandbox tabs are great for showing a UI; they're a bad fit for a server.
2. **Por qué CLI antes que IDE.** When you use Claude Code in the terminal, you see every file the AI creates and every command it runs — `pip install`, `uvicorn main:app --reload`, `sqlite3 app.db`. Nothing hides. Para una primera vez con IA local, esa transparencia importa más que la comodidad de un IDE gráfico. Semana 04 sube de nivel a Cursor/Antigravity; en semana 03 nos quedamos con CLI por didáctica. (Don't go deeper into IDE-AI features.)
3. **El stack del demo: Python + FastAPI + SQLite + Uvicorn.** One paragraph per piece. Python: el lenguaje. FastAPI: el framework que define rutas y schemas con muy poca ceremonia. SQLite: la DB que vive en un archivo. Uvicorn: el servidor que corre tu app. Mention `venv` as the way Python isolates dependencies.
4. **Otras stacks que vas a encontrar.** Half a paragraph each: Node + Express (JavaScript en el servidor), Django o Flask (las alternativas Python históricas), Go con Gin o Fiber (servidores compilados), Ruby on Rails (la convención sobre configuración llevada al extremo). El punto no es aprenderlas — el punto es saber que FastAPI es *una elección* y por qué la elegimos: tipos modernos, schemas integrados, doc automática, suficiente para esta clase y muchas reales.
5. **Tarea para semana 04.** Explicit list (this is a real enumeration):
   - Instalar Python 3.11+
   - Instalar Node.js (Claude Code lo necesita)
   - Instalar Claude Code: `npm install -g @anthropic-ai/claude-code`
   - Verificar: `claude --version` debe responder.
   - Si algo falla: avisar por el canal del curso antes de la clase.

**Closing prompt-comparison:** vague "armame el backend" vs specific "creá un proyecto Python con venv, FastAPI, Uvicorn y SQLite. Estructura mínima: `app/main.py` con FastAPI, `app/db.py` con conexión a SQLite, `requirements.txt`. Levantalo con `uvicorn app.main:app --reload` y mostrame la URL."

- [ ] **Step 1: Verify the Claude Code install command is current**

The install command in the homework section is `npm install -g @anthropic-ai/claude-code`. If that has changed, update it. Quick check: `npm view @anthropic-ai/claude-code version` should respond.

- [ ] **Step 2: Write the file**

Word target: 700–900.

- [ ] **Step 3: Verify**

Run: `wc -w semanas/03/source_material/07-de-lo-local-al-stack.md` → expect 700–950.

Grep for forbidden phrases (in particular ensure no Cursor/Antigravity feature names like `.cursorrules`, "Composer", "agentic"): `grep -iE '(cursorrules|composer|agentic)' semanas/03/source_material/07-de-lo-local-al-stack.md`
Expected: no matches.

- [ ] **Step 4: Commit**

```bash
git add semanas/03/source_material/07-de-lo-local-al-stack.md
git commit -m "feat(semana-03): add 07-de-lo-local-al-stack bisagra"
```

---

## Task 9: Write `08-demo-en-vivo.md`

**Files:**
- Create: `semanas/03/source_material/08-demo-en-vivo.md`

**Goal of the file:** Be the *guion* of the live demo, not a finished script. Document: the requirements the demo app must hit (already fixed), the planning template Enzo uses on stage, the execution beats, and the mandatory pause-points where each conceptual block surfaces in the generated code. The actual app domain is left as an explicit `TBD: domain` block since we agreed to defer it. ~400–600 words.

**Key vocabulary to bold:** guion, plan, prompt inicial, pause-point.

**Required sections:**

1. **Qué tiene que mostrar el demo (requisitos).** Numbered list (genuine enumeration):
   1. Al menos 3 verbos HTTP distintos en juego.
   2. Al menos una relación entre dos tablas (foreign key).
   3. Al menos un camino de error visible (algún 4xx que el alumno pueda ver intencionalmente).
   4. Frontend mínimo que consuma la API (puede ser una sola página HTML servida por la misma app).
   5. Dominio no trivial — explícitamente NO un to-do list.
2. **Dominio del demo.** Block titled "TBD: dominio". One sentence saying that the concrete domain gets decided at implementation time, with the constraints from section 1. Suggest two or three candidate ideas as anchors for that decision (without committing): un mini-CRM de contactos con notas por contacto; un tracker de aplicaciones a trabajos con estados; un catálogo de libros leídos con reseñas. (These are stand-ins; the implementer will pick.)
3. **Plan que se dicta antes de tocar Claude Code.** Show the on-stage planning template Enzo uses — a short text block where, before invoking the AI, the professor writes out: stack, modelo de datos (las tablas con foreign key), endpoints (verbos + paths), forma del frontend. This is the live demonstration of "el contrato es lo que se dicta".
4. **Beats del demo.** Numbered list of pause-points, in order:
   1. Después del primer prompt: mostrar la estructura de archivos que apareció. Señalar `main.py`, `db.py`, los archivos de schema.
   2. Cuando aparezca la primera ruta: pausar y leerla en voz alta como contrato (verbo + path + entrada + salida).
   3. Cuando se levante el servidor: mostrar la terminal con Uvicorn corriendo, abrir `localhost` en el navegador, mostrar la doc automática (`/docs`) si FastAPI la genera.
   4. Cuando pegues a un endpoint mal: mostrar el 4xx en el navegador y el log en la terminal — vincular con archivo 06.
   5. Cuando aparezca el frontend: leer la llamada `fetch` o equivalente como "cliente HTTP que habla el contrato".
   6. Cierre: 30 segundos para enmarcar lo que pasó. "Ustedes no tipearon nada. Lo que dirigieron fue el contrato."
5. **Lo que NO se intenta en este demo.** Short paragraph: no auth, no deploy, no testing, no CSS bonito. Esos son otras semanas.

- [ ] **Step 1: Write the file**

Word target: 400–600. Section 2 ("TBD: dominio") must be explicitly marked as a deferred decision so the spine generation phase can flag it back to the user.

- [ ] **Step 2: Verify**

Run: `wc -w semanas/03/source_material/08-demo-en-vivo.md` → expect 400–650.

Run: `grep -nE 'TBD' semanas/03/source_material/08-demo-en-vivo.md` (Grep tool)
Expected: at least one match (the dominio TBD), and only that one.

- [ ] **Step 3: Commit**

```bash
git add semanas/03/source_material/08-demo-en-vivo.md
git commit -m "feat(semana-03): add 08-demo-en-vivo guion (domain TBD)"
```

---

## Task 10: Update top-level README and verify the set

**Files:**
- Read-only check across `semanas/03/source_material/`

- [ ] **Step 1: List the directory**

Run: `ls semanas/03/source_material/`
Expected: 9 markdown files plus nothing else: `index.md`, `01-…`, `02-…`, `03-…`, `04-…`, `05-…`, `06-…`, `07-…`, `08-…`.

- [ ] **Step 2: Cross-check forbidden vocabulary across the whole directory**

Run: `grep -irE '(diplomatura|vibe coding|payoff|seamless|leverage|robust solution|cutting-edge|cursorrules|composer|agentic)' semanas/03/source_material/`
Expected: no matches.

If matches appear, fix them in the offending file and amend the commit (or add a small follow-up fix commit, per `Never amend an existing commit unless explicitly requested` rule from CLAUDE.md → prefer a follow-up commit).

- [ ] **Step 3: Verify all 8 content files end with a vague-vs-specific prompt comparison block**

For each of `02-…` through `07-…`, check the file ends with the closing prompt-comparison pattern. Quick heuristic:

Run: `grep -c -iE '(vago|específico|determinismo|auditor)' semanas/03/source_material/0[2-7]-*.md`
Expected: each file shows ≥ 2 hits. (`01-…` and `08-…` are exempt — opening and demo guion.)

- [ ] **Step 4: Final commit if any fixes were needed**

```bash
git add semanas/03/source_material/
git commit -m "fix(semana-03): align source_material with voice and pattern conventions"
```

If no fixes, skip.

---

## Out of scope for this plan

- Generating the reveal.js slides. That happens later via `/build-class`, which has its own pipeline (spine → plan → execution).
- Building or running the actual demo backend. The demo is run live, not pre-built. The domain is explicitly deferred.
- Updating any global course docs (`programa.md`, top-level `README.md`, `CLAUDE.md`).

## Spec self-review notes

Walked through the spec section by section against this plan:

- **Goal / context / non-goals:** covered by the file structure and Task 1 index, which restates the framing.
- **Class structure (8 blocks):** one task per block (Tasks 2–9), plus Task 1 for the index and Task 10 for verification. Time budgets carried into the index.
- **Recurring slide patterns:** voice conventions stated up front; closing prompt-comparison stipulated in tasks 3–8 and verified in Task 10.
- **Key decisions log:** every decision is reflected in scope: bisagra is its own file (Task 8), errors is its own file (Task 7), REST split from HTTP (Tasks 3 + 4), no auth (verified in Task 10 grep), no `demo.html` (no such task).
- **Demo app deferred:** explicitly marked TBD in Task 9, and Task 9 verification ensures the marker exists.

No gaps. No placeholders left in the plan body itself (the only TBD is the deliberate one in Task 9, signaled).
