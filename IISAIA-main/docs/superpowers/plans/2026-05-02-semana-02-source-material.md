# Semana 02 Source Material Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Populate `semanas/02/source_material/` with 8 markdown content files and a "Frontend Showroom" `demo.html` artifact, ready to be transformed into a reveal.js deck by `/build-class`.

**Architecture:** Markdown files written first (lower-risk, content-only). Then the `demo.html` artifact built section-by-section in a single file with inline `<style>` and `<script>` (no external assets, no CDN). Each section of the demo maps 1:1 to a stop in the in-class anatomy walkthrough. All copy in Spanish.

**Tech Stack:** Plain markdown for source material. Vanilla HTML + CSS (variables, flex, grid) + ES2022 JavaScript for `demo.html`. No build tools, no frameworks, no dependencies.

**Spec reference:** `docs/superpowers/specs/2026-05-02-semana-02-source-material-design.md`

---

## File structure

| Path | Status | Responsibility |
|------|--------|----------------|
| `semanas/02/source_material/index.md` | Replace stub | Master index — reading order + 1-paragraph summary per file |
| `semanas/02/source_material/01-frontend-y-el-supervisor.md` | Create | Lead-in framing: why frontend literacy matters under AI assistance + 5-part anatomy preview |
| `semanas/02/source_material/02-estructura-html.md` | Create | Semantic HTML, document outline, the ~12 tags that matter |
| `semanas/02/source_material/03-estilo-css.md` | Create | Box model, flex/grid, type/color, CSS variables |
| `semanas/02/source_material/04-estado-y-comportamiento.md` | Create | State → DOM → events triangle |
| `semanas/02/source_material/05-single-file-platform.md` | Create | Why one HTML file wins for web LLMs; when the paradigm breaks |
| `semanas/02/source_material/06-patrones-de-prompt-ui.md` | Create | 4 reusable prompt templates + live demo script |
| `semanas/02/source_material/07-actividad-grupal.md` | Create | Activity spec: cycle, examples, constraints, submission |
| `semanas/02/source_material/demo.html` | Create | The "Frontend Showroom" teaching artifact |

**Naming note:** spec listed `00-index.md` but semana 01's pattern uses `index.md` without numeric prefix. Following semana 01's pattern for consistency. The existing `semanas/02/source_material/index.md` is a 12-line stub and gets fully replaced.

**Word-count targets:** 600–900 words per content markdown unless noted. `index.md` is short (~250 words).

---

## Voice and didactic conventions

All markdown copy must follow these conventions (referenced from `tools/skills/slide-generation/voice-and-didactics.md` for the slide step that comes after this plan, but the source markdowns should already be aligned):

- **Spanish, professor voice.** Direct, second-person plural ("ustedes" implicit / use of "vamos a", "fijate en"). Not corporate, not stiff.
- **Concrete over abstract.** Lead with examples, then name the concept. Avoid "this empowers you to..." phrasing.
- **Bold the vocabulary terms** — students use these markdowns as a glossary. When a key term is introduced, bold it on first use.
- **No bullet-list theatre.** Don't render conceptual content as flat lists when prose would work. Lists are for genuine enumerations (e.g., "los 4 patrones son: ...").
- **Connect to the course thesis.** Recurring callback: the student is supervisor arquitectónico. They name what they want; the LLM writes syntax.
- **No emojis** anywhere (per global frontend rules).

Each markdown task below includes an opening line and key vocabulary so voice stays consistent across files.

---

## Task 1: Replace `index.md` stub with master index

**Files:**
- Modify: `semanas/02/source_material/index.md` (currently 12-line stub)

- [ ] **Step 1: Read the current stub**

Run: `cat semanas/02/source_material/index.md`
Expected: ~12 lines including a "Temas" section and an "Archivos" placeholder.

- [ ] **Step 2: Replace contents with the master index**

Replace the entire file with:

```markdown
# Semana 2 — Arquitectura Frontend y Vibe Coding

Este es el material fuente de la clase de Semana 2. La presentación reveal.js se genera con `/build-class` a partir de estos archivos.

## Orden de lectura

| # | Archivo | Tema | Bloque de clase |
|---|---------|------|-----------------|
| 1 | [01-frontend-y-el-supervisor.md](01-frontend-y-el-supervisor.md) | Por qué la alfabetización frontend importa cuando la IA escribe el código | Apertura (~7 min) |
| 2 | [02-estructura-html.md](02-estructura-html.md) | HTML semántico: la estructura como sustantivos | Anatomía (~5 min) |
| 3 | [03-estilo-css.md](03-estilo-css.md) | CSS: caja, layout, tipografía, color, variables | Anatomía (~7 min) |
| 4 | [04-estado-y-comportamiento.md](04-estado-y-comportamiento.md) | Estado, DOM y eventos: el triángulo dinámico | Anatomía (~8 min) |
| 5 | [05-single-file-platform.md](05-single-file-platform.md) | El paradigma de un solo archivo: por qué gana con IAs web | Anatomía (~5 min) |
| 6 | [06-patrones-de-prompt-ui.md](06-patrones-de-prompt-ui.md) | Cuatro patrones de prompt para construir UI con IA | Patrones (~20 min) |
| 7 | [07-actividad-grupal.md](07-actividad-grupal.md) | Actividad grupal: ciclo Architect → Prompter → Reviewer → Tester | Briefing (~8 min) |
| - | [demo.html](demo.html) | Artefacto de enseñanza ("Frontend Showroom") usado en la anatomía | Anatomía (apoyo visual) |

## Hilo conductor

Esta clase enseña vocabulario frontend para que el alumno pueda **dirigir** una IA, no para reemplazar la sintaxis con la mano. El artefacto `demo.html` es a la vez la página que se diserta en clase y la referencia que el alumno se lleva a su casa: la página se enseña a sí misma.

La actividad de cierre (60 minutos en sala separada) lleva al grupo a aplicar el ciclo de desarrollo asistido por IA con la consigna abierta de construir un artefacto de una sola página en ChatGPT Canvas.
```

- [ ] **Step 3: Verify the file renders correctly as markdown**

Run: `cat semanas/02/source_material/index.md`
Expected: Valid markdown, all 7 file links point to filenames that will exist after Tasks 2-8, demo.html link exists.

- [ ] **Step 4: Commit**

```bash
git add semanas/02/source_material/index.md
git commit -m "docs(semana-02): replace source_material index stub with full master index"
```

---

## Task 2: Write `01-frontend-y-el-supervisor.md`

**Files:**
- Create: `semanas/02/source_material/01-frontend-y-el-supervisor.md`

**Word target:** ~700 words.

**Purpose:** This is the lead-in. It frames why a non-frontend-dev cohort is spending 90 minutes on frontend vocabulary in a course about AI-assisted development. Sets up the supervisor framing that the rest of the file series leans on.

**Required heading structure:**

```
# Frontend y el supervisor arquitectónico

## La pregunta incómoda

## Lo que cambia cuando la IA escribe el código

## La anatomía en cinco partes

## A qué prestamos atención esta clase
```

**Required vocabulary (bold on first use):** **supervisor arquitectónico**, **vocabulario técnico**, **HTML**, **CSS**, **JavaScript**, **estado**, **single-file platform**.

**Opening line (use as-is or near-as-is):**

> Si una IA puede escribir el código, ¿por qué seguimos aprendiendo qué es un `flexbox` o qué hace un `<section>`? La respuesta corta: porque el cuello de botella ya no es la sintaxis, es la decisión.

**Section content notes:**

- **§ La pregunta incómoda** (~150 palabras): plantea la pregunta del opening, contesta que el alumno ahora trabaja como supervisor arquitectónico — su trabajo es decidir qué se construye, no tipear cada llave. Conecta con el rol que ya viene del programa de la materia.
- **§ Lo que cambia cuando la IA escribe el código** (~200 palabras): tres cosas cambian cuando delegás sintaxis. (1) la velocidad de iteración explota; (2) el costo de equivocarse al especificar es altísimo (la IA hace exactamente lo que pediste, no lo que querías); (3) leer código se vuelve más importante que escribirlo. Cierra con: "para hacer las tres cosas bien, necesitás vocabulario."
- **§ La anatomía en cinco partes** (~250 palabras): introducción a las cinco capas que vas a ver en `demo.html`. Una frase por capa, suficiente para anclar las próximas lecturas:
  1. **Estructura** (HTML) — los sustantivos de la página.
  2. **Estilo** (CSS) — cómo se ve cada sustantivo.
  3. **Comportamiento** (JS) — qué pasa cuando el usuario interactúa.
  4. **Estado** — el dato que vive detrás de la pantalla.
  5. **Empaque** (single-file) — cómo distribuís todo eso.
  Cierra mencionando que el resto de los archivos cubren cada capa por separado.
- **§ A qué prestamos atención esta clase** (~100 palabras): expectativas explícitas. No se está enseñando a escribir HTML/CSS/JS de producción. Se está enseñando a *nombrar las cosas* para poder pedirlas. Que el lector entienda que cada concepto que ve se incluye porque tiene un payoff directo en cómo dialogan con un LLM.

**Closing thought (last paragraph):** Reafirmá el supervisor framing y haceles saber que en cinco minutos van a estar mirando una página real (referencia explícita a `demo.html`).

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write the file at `semanas/02/source_material/01-frontend-y-el-supervisor.md` following the heading structure, opening line, vocabulary, and section notes above. Write all four sections in full Spanish prose. Aim for ~700 words total.

- [ ] **Step 2: Self-check against requirements**

Read your draft. Verify: opening line preserved, all 7 vocabulary terms appear in bold on first use, all 4 sections present, closing reference to `demo.html` included, ~600–900 words total. Adjust if needed.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/01-frontend-y-el-supervisor.md
git commit -m "docs(semana-02): add 01-frontend-y-el-supervisor.md (lead-in framing)"
```

---

## Task 3: Write `02-estructura-html.md`

**Files:**
- Create: `semanas/02/source_material/02-estructura-html.md`

**Word target:** ~750 words.

**Purpose:** Teach semantic HTML as the noun-layer of a page. Not "all of HTML" — only the ~12 tags that matter when describing a UI to an LLM, and the principle of using the right one.

**Required heading structure:**

```
# La estructura: HTML como sustantivos

## Por qué los nombres importan

## Los doce sustantivos que importan

### Contenedores estructurales
### Contenido
### Interacción

## El mal hábito: la sopa de divs

## Cómo le pedís estructura a un LLM
```

**Required vocabulary (bold on first use):** **HTML semántico**, **etiqueta** (tag), **elemento**, **outline del documento**, **header**, **main**, **section**, **article**, **nav**, **footer**, **aside**, **div**.

**Opening line:**

> El HTML no se trata de hacer que algo "se vea bien" — eso es trabajo del CSS. Se trata de nombrar las partes de tu página con la palabra correcta.

**Section content notes:**

- **§ Por qué los nombres importan** (~150 palabras): el navegador, los lectores de pantalla, los buscadores, las IAs y los desarrolladores leen el HTML para entender de qué *trata* una página. Si nombrás todo `<div>`, no entendieron nada. Ejemplo concreto: comparar `<header>` vs `<div class="header">` — visualmente idénticos, semánticamente distintos.
- **§ Los doce sustantivos que importan** (~300 palabras): tabla o lista enriquecida con las ~12 etiquetas core, agrupadas en tres subsecciones. Para cada una: nombre, una frase de qué representa, un ejemplo de uso de una sola línea.
  - Contenedores estructurales: `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`, `<footer>`, `<aside>`
  - Contenido: `<h1>`–`<h6>`, `<p>`, `<ul>`/`<ol>`/`<li>`, `<a>`, `<img>`
  - Interacción: `<button>`, `<input>`, `<form>`, `<label>`
- **§ El mal hábito: la sopa de divs** (~120 palabras): explicar qué es la *div soup* (todo es `<div>`) y por qué pasa (es el camino fácil). Un párrafo. Conexión directa con la sección §Estructura del `demo.html` que tiene un toggle entre versión semántica y div soup.
- **§ Cómo le pedís estructura a un LLM** (~150 palabras): ejemplo concreto de un prompt que pide estructura semántica vs uno que sale a "armar la página":

  Prompt vago: *"Hacé una página de contacto."*

  Prompt con vocabulario: *"Hacé una página de contacto. Estructura: `<header>` con `<nav>` (Inicio, Sobre mí, Contacto); `<main>` con un `<section>` introductorio (h1 + p) y un `<form>` con `<label>` + `<input>` para nombre y email, más un `<textarea>` para el mensaje; `<footer>` con copyright."*

  Punto: el segundo prompt no es más largo, es más *preciso*. La precisión nace del vocabulario.

**Closing thought:** El HTML es el esqueleto. Si está mal nombrado, ningún CSS lo arregla. Próximo archivo: vestimos el esqueleto.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/02-estructura-html.md` following the heading structure, opening line, required vocabulary, and section notes above.

- [ ] **Step 2: Self-check**

Verify all 12+ vocabulary terms are bolded on first use, the three contenedor groups all appear, the div-soup section explicitly references `demo.html`'s §Estructura toggle, the closing leads into 03-estilo-css.md.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/02-estructura-html.md
git commit -m "docs(semana-02): add 02-estructura-html.md (semantic HTML)"
```

---

## Task 4: Write `03-estilo-css.md`

**Files:**
- Create: `semanas/02/source_material/03-estilo-css.md`

**Word target:** ~850 words (largest of the markdowns — CSS has the most surface area).

**Purpose:** Teach the CSS vocabulary that lets a student describe a layout to an LLM with precision. NOT a CSS tutorial — a *naming guide* for the four primitives that matter: box model, layout (flex + grid), type/color, variables.

**Required heading structure:**

```
# El estilo: cómo se ve cada sustantivo

## Cuatro primitivas suficientes

## Primitiva 1 — El modelo de caja

## Primitiva 2 — Layout: flexbox y grid

### Flexbox: una dimensión
### Grid: dos dimensiones

## Primitiva 3 — Tipografía y color

## Primitiva 4 — Variables CSS: la perilla del LLM

## Cómo le pedís estilo a un LLM
```

**Required vocabulary (bold on first use):** **CSS**, **modelo de caja** (box model), **margin**, **border**, **padding**, **content**, **layout**, **flexbox**, **grid**, **flex container**, **flex item**, **grid container**, **gap**, **justify-content**, **align-items**, **tipografía**, **font-family**, **paleta**, **variables CSS** (custom properties).

**Opening line:**

> Si el HTML son los sustantivos, el CSS responde a la pregunta "¿cómo se ven?". No vamos a aprender CSS entero. Vamos a aprender las cuatro perillas que importa nombrar cuando hablás con una IA.

**Section content notes:**

- **§ Cuatro primitivas suficientes** (~80 palabras): introduce las cuatro: caja, layout, tipo/color, variables. Promesa: con estas cuatro alcanza para describir el 90% de las decisiones visuales a una IA.
- **§ Primitiva 1 — El modelo de caja** (~150 palabras): cada elemento es una caja con cuatro capas (content → padding → border → margin). Diagrama mental: una cebolla. Por qué importa: porque la diferencia entre "está apretado" y "respira" es padding/margin, y querés poder pedirlo por nombre. Ejemplo concreto de prompt: *"Agregá 16px de padding interno al `<button>`."*
- **§ Primitiva 2 — Layout** (~220 palabras): la pregunta principal del CSS es *cómo se acomodan las cajas entre sí*. Hay dos respuestas dominantes en 2026:
  - **§§ Flexbox: una dimensión** (~100 palabras): para acomodar cosas en fila o columna. Vocabulario: `display: flex`, `flex-direction`, `justify-content`, `align-items`, `gap`. Caso típico: una nav-bar, una toolbar, un grupo de botones.
  - **§§ Grid: dos dimensiones** (~100 palabras): para layouts de tablero (galerías, dashboards, tarjetas en cuadrícula). Vocabulario: `display: grid`, `grid-template-columns`, `gap`. Caso típico: una galería de tarjetas, un dashboard.
  - Punto clave: cuando le pedís layout a un LLM, nombrar *flex* o *grid* hace que el código salga bien al primer intento; describir "quiero que estén una al lado de la otra" lleva a iteraciones largas.
- **§ Primitiva 3 — Tipografía y color** (~120 palabras): dos perillas que dominan la sensación de un sitio. Para tipografía: una pareja de fuentes (heading + body) o una sola sans. Para color: una paleta minimalista (fondo, texto, acento, opcional contraste). Por qué importa: si pedís "que se vea moderno", el LLM inventa; si pedís "tipografía sans, fondo `#0f172a`, acento `#6366f1`", obtenés exactamente eso.
- **§ Primitiva 4 — Variables CSS: la perilla del LLM** (~150 palabras): qué son (`--color-primary: #6366f1` definidas en `:root`), por qué importan en este curso: una variable es un punto de entrada que el LLM puede modificar después sin tener que reescribir todo el CSS. Cuando pedís *"cambiá el acento a verde"*, si el código usa variables, el cambio es una línea; si no, son veinte. Demo en clase: la sección §Estilo de `demo.html` cambia tema cambiando una variable.
- **§ Cómo le pedís estilo a un LLM** (~120 palabras): contraste entre prompt vago vs prompt vocabulario-rich. Vago: *"Hacelo más lindo."* Específico: *"Cambiá el `<main>` a un grid de 3 columnas con gap de 24px. El `<button>` primario: fondo `var(--color-primary)`, padding 12px 20px, border-radius 8px."*

**Closing thought:** Estilo es donde más se nota la diferencia entre dirigir y dejar improvisar. El próximo archivo trae la tercera capa: el comportamiento.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/03-estilo-css.md` following the structure, opening line, vocabulary, and notes above.

- [ ] **Step 2: Self-check**

Verify all four primitives have their own section, flex/grid both appear, variables CSS section explicitly references `demo.html`'s §Estilo theme switcher, vocabulary list complete in bold.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/03-estilo-css.md
git commit -m "docs(semana-02): add 03-estilo-css.md (CSS primitives)"
```

---

## Task 5: Write `04-estado-y-comportamiento.md`

**Files:**
- Create: `semanas/02/source_material/04-estado-y-comportamiento.md`

**Word target:** ~800 words.

**Purpose:** Introduce the three-way relationship: **state** (data) → **DOM** (what's rendered) → **events** (what the user does). Frame "estado" as the magic word that unlocks better prompts.

**Required heading structure:**

```
# Estado, DOM y eventos: el triángulo dinámico

## Qué cambia cuando una página "hace algo"

## Tres conceptos, una historia

### Estado: el dato que vive detrás
### DOM: la representación viva
### Eventos: la voz del usuario

## El ciclo: evento → estado → DOM

## Por qué "estado" es la palabra mágica

## Cómo le pedís comportamiento a un LLM
```

**Required vocabulary (bold on first use):** **JavaScript**, **estado**, **DOM** (Document Object Model), **árbol del DOM**, **render**, **evento**, **listener**, **event handler**, **mutación del DOM**, **ciclo evento-estado-render**.

**Opening line:**

> Una página estática se entiende sola: hay HTML, lo dibuja el navegador, listo. Una página que *hace algo* — un contador, una lista que crece, un juego — es más interesante: tiene un triángulo que vale la pena saber nombrar.

**Section content notes:**

- **§ Qué cambia cuando una página "hace algo"** (~100 palabras): introduce la diferencia entre página estática y dinámica. Si lo único que hace tu página es mostrar texto, no necesitás JavaScript. Si pasa cualquier otra cosa cuando el usuario interactúa, hay tres piezas en juego.
- **§ Tres conceptos, una historia** (~280 palabras):
  - **§§ Estado** (~90 palabras): el *dato* que tu página recuerda — el número del contador, los items del todo, el modo dark/light. Vive en variables JS. Es invisible hasta que se dibuja.
  - **§§ DOM** (~100 palabras): "el HTML, pero vivo." El navegador parsea el HTML una vez al cargar y construye un **árbol del DOM**. El JS puede mutar ese árbol después: agregar nodos, cambiar atributos, esconder cosas. Lo que ves en pantalla = el DOM ahora.
  - **§§ Eventos** (~90 palabras): cualquier cosa que el usuario hace (click, tipear, scroll, mover el mouse) genera un evento. Vos registrás un **listener** para escuchar uno: "cuando se hace click en este botón, ejecutá esta función."
- **§ El ciclo: evento → estado → DOM** (~150 palabras): el patrón que se repite en toda app dinámica. Ejemplo concreto del contador:
  1. Estado inicial: `count = 0`. DOM muestra "0".
  2. El usuario hace click en el botón "+1". Esto dispara un evento.
  3. El listener actualiza el estado: `count = 1`.
  4. El listener actualiza el DOM: `span.textContent = count`.
  5. El usuario ve "1".

  El círculo se cierra cuando el siguiente click empieza el mismo ciclo. Conexión: la sección §Estado de `demo.html` te muestra este ciclo tres veces (contador, todo list, event log).
- **§ Por qué "estado" es la palabra mágica** (~150 palabras): cuando le pedís a una IA *"hacé que el botón cuente clicks"*, si nombrás "estado" — *"agregá un estado `count` que arranca en 0 y se incrementa al hacer click"* — el código sale predecible. Si no la nombrás, la IA puede:
  - Guardar el contador en un atributo del DOM (frágil)
  - Usar una variable global flotante (difícil de extender)
  - Mezclar dos cosas distintas en una sola variable

  Nombrar "estado" le dice a la IA: "esto es un dato, separalo, ponelo donde corresponde."
- **§ Cómo le pedís comportamiento a un LLM** (~120 palabras): ejemplo de prompt. Vago: *"Hacé un botón que cuente."* Específico: *"Agregá un estado `count` (número, inicial 0). Mostralo en un `<span id='count'>`. Cuando se haga click en el `<button id='inc'>+1</button>`, incrementá `count` y actualizá el `<span>`."*

**Closing thought:** El estado es el corazón de cualquier app que valga la pena. El próximo archivo cierra la anatomía con el empaque: por qué todo esto cabe en un solo archivo.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/04-estado-y-comportamiento.md` following the structure above.

- [ ] **Step 2: Self-check**

Verify the contador example walks through all 5 steps of the cycle. Verify "estado" is reframed as the magic word with concrete prompt before/after.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/04-estado-y-comportamiento.md
git commit -m "docs(semana-02): add 04-estado-y-comportamiento.md (state/DOM/events)"
```

---

## Task 6: Write `05-single-file-platform.md`

**Files:**
- Create: `semanas/02/source_material/05-single-file-platform.md`

**Word target:** ~650 words.

**Purpose:** Justify the single-file paradigm pedagogically and pragmatically. Why one HTML file beats a project scaffold when working with a free-tier web LLM. When the paradigm breaks (so they don't think it's universally good).

**Required heading structure:**

```
# El empaque: un archivo, una página

## ¿Por qué cabe todo en uno?

## Las tres ventajas

### Ventaja 1 — Cabe en el contexto
### Ventaja 2 — Despliegue por copy-paste
### Ventaja 3 — Cero toolchain

## Cuándo el paradigma se rompe

## Lo que ganás esta clase
```

**Required vocabulary (bold on first use):** **single-file platform**, **ventana de contexto** (context window), **toolchain**, **bundler**, **deploy**, **dependencia externa**, **CDN**.

**Opening line:**

> Toda página que vamos a construir esta clase vive en un solo archivo `.html`. No hay carpetas, no hay `node_modules`, no hay configuración. Hay un archivo. Ese mismo archivo es lo que le pasás al LLM, lo que abrís en el navegador y lo que subís al servidor.

**Section content notes:**

- **§ ¿Por qué cabe todo en uno?** (~100 palabras): aclaración técnica: HTML, CSS y JS pueden convivir en un solo archivo via `<style>` y `<script>` inline. No es un truco — es como funciona la web nativamente. Cuando un proyecto crece, se separa; cuando es chico (o el contexto del LLM es chico), se junta.
- **§ Las tres ventajas** (~350 palabras):
  - **§§ Cabe en el contexto** (~120 palabras): un LLM gratuito tiene una **ventana de contexto** limitada. Si tu proyecto son 12 archivos en 4 carpetas, no le entra; el modelo "ve" solo fragmentos y empieza a inventar. Si todo es un archivo, lo tiene completo siempre. Calidad de output sube proporcional a cuánto del proyecto puede ver el modelo.
  - **§§ Despliegue por copy-paste** (~100 palabras): copiás el contenido del archivo, lo pegás en un Gist, en GitHub Pages, en Netlify Drop, en cualquier servicio que sirva HTML estático. Cero pipeline, cero CI. Ideal para clase, para prototipos, para portfolios.
  - **§§ Cero toolchain** (~130 palabras): nada de `npm install`, nada de `webpack`, nada de versiones de Node. El alumno abre el archivo en un navegador y funciona. La distancia entre "tengo una idea" y "tengo algo corriendo" se vuelve cero. Esto es enorme cuando estás aprendiendo: cualquier obstáculo de tooling mata el momentum.
- **§ Cuándo el paradigma se rompe** (~150 palabras): honestidad pedagógica. El single-file no es universal:
  - Cuando el proyecto pasa los ~1000 líneas, leerlo se vuelve doloroso.
  - Cuando hay backend (próxima clase, semana 3 cubre el equivalente *single-file server*).
  - Cuando necesitás dependencias pesadas (un editor de texto rico, un motor 3D) — ahí entra una **dependencia externa** vía CDN, o se justifica un proyecto multi-archivo.
  - Cuando trabajás en equipo y necesitás merge granular.

  Para esta clase y para los TPs que dependan de un LLM gratuito, el paradigma sirve perfecto.
- **§ Lo que ganás esta clase** (~50 palabras): el archivo `demo.html` que vas a ver en cinco minutos es la prueba. Una página completa, con cinco demos interactivas, layout, estado, eventos, todo en un archivo. Si esto es posible en una página educativa, lo es para tu actividad grupal.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/05-single-file-platform.md` following the structure.

- [ ] **Step 2: Self-check**

Verify the three ventajas all appear and "cuándo se rompe" is honest about limitations. Verify reference to next week's "single-file server" concept (it's in the programa for semana 3).

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/05-single-file-platform.md
git commit -m "docs(semana-02): add 05-single-file-platform.md (paradigm rationale)"
```

---

## Task 7: Write `06-patrones-de-prompt-ui.md`

**Files:**
- Create: `semanas/02/source_material/06-patrones-de-prompt-ui.md`

**Word target:** ~900 words (largest, contains four full prompt examples).

**Purpose:** The payoff of the class. Four reusable prompt templates that students will literally copy-paste in the activity. Each one names a typical UI work-mode and gives both a template and a worked example.

**Required heading structure:**

```
# Cuatro patrones de prompt para construir UI con IA

## El cambio de mentalidad

## Patrón 1 — Describir el artefacto

### Cuándo usarlo
### Plantilla
### Ejemplo trabajado

## Patrón 2 — Iterar sobre el estado

### Cuándo usarlo
### Plantilla
### Ejemplo trabajado

## Patrón 3 — Arreglar el layout

### Cuándo usarlo
### Plantilla
### Ejemplo trabajado

## Patrón 4 — Tematizar y pulir

### Cuándo usarlo
### Plantilla
### Ejemplo trabajado

## Demo en vivo (referencia)
```

**Required vocabulary (bold on first use):** **patrón de prompt**, **artefacto**, **estado** (callback to file 04), **layout** (callback to file 03), **theming**, **CSS variable** (callback).

**Opening line:**

> Llegamos al payoff de la clase. Todo el vocabulario de los archivos anteriores existe para que estos cuatro patrones te salgan naturales. Cada patrón cubre uno de los modos de trabajo más comunes cuando construís UI con una IA.

**Section content notes:**

- **§ El cambio de mentalidad** (~120 palabras): no estás escribiendo código, estás *encargando* código. Eso es distinto a pedirle a un compañero que te ayude. La IA hace exactamente lo que decís — los patrones te ayudan a decir lo correcto. Cuatro patrones cubren ~80% del trabajo: arrancar de cero, evolucionar comportamiento, arreglar visual, polir.

Each patrón gets the same three subsections (~180 palabras cada patrón en total):

### Patrón 1 — Describir el artefacto

- **Cuándo usarlo:** primer prompt de un proyecto nuevo. La IA no tiene contexto; vos se lo das.
- **Plantilla:**

  ```
  Construí un [tipo de artefacto].
  Estructura: [secciones HTML, jerarquía].
  Estilo: [tono, paleta, tipografía].
  Comportamiento: [estados, eventos clave].
  Constraints: un solo archivo HTML, vanilla JS, sin dependencias externas.
  ```

- **Ejemplo trabajado:**

  *"Construí un Pomodoro timer. Estructura: `<header>` con título 'Pomodoro' y `<button>` de modo (estudio/descanso); `<main>` con un círculo grande mostrando tiempo restante en mm:ss y debajo `<button>` Iniciar/Pausar/Reiniciar; `<footer>` con contador de pomodoros completados. Estilo: minimalista, dark mode, sans-serif grande para el tiempo, paleta `#0f172a` fondo / `#e2e8f0` texto / `#6366f1` acento. Comportamiento: estado `mode` (estudio = 25 min, descanso = 5 min), estado `secondsLeft`, estado `isRunning`. Al terminar el contador suena un beep y cambia automáticamente al otro modo. Constraints: un archivo HTML, vanilla JS, sin dependencias."*

### Patrón 2 — Iterar sobre el estado

- **Cuándo usarlo:** ya tenés un artefacto andando y querés agregarle un nuevo comportamiento.
- **Plantilla:**

  ```
  Agregale al [artefacto] un estado [nombre] que [describe la transición].
  Cuando [condición]: [efecto en estado] y [efecto en DOM].
  Cuando [condición de retorno]: [restablecer].
  ```

- **Ejemplo trabajado:**

  *"Agregale al Pomodoro un estado `isPaused` (boolean). Cuando se hace click en Pausar: `isPaused = true`, el cronómetro deja de descender, el `<button>` cambia a 'Reanudar' y el círculo se vuelve gris. Cuando se hace click en Reanudar: `isPaused = false`, el contador continúa desde donde estaba, el círculo vuelve al color normal."*

### Patrón 3 — Arreglar el layout

- **Cuándo usarlo:** la página funciona pero el visual está mal acomodado.
- **Plantilla:**

  ```
  El [contenedor] está mal acomodado.
  Hacelo un [flex container | grid] con [parámetros].
  [Notas de espaciado y alineación].
  ```

- **Ejemplo trabajado:**

  *"El `<header>` está mal acomodado. Hacelo un flex container con `justify-content: space-between` para que el título quede a la izquierda y el `<button>` de modo a la derecha, ambos centrados verticalmente con `align-items: center`. Agregale 16px de padding horizontal."*

### Patrón 4 — Tematizar y pulir

- **Cuándo usarlo:** el artefacto funciona y querés darle una identidad visual cohesiva.
- **Plantilla:**

  ```
  Convertí el styling para que use variables CSS.
  Definí en :root: --[token]: [valor]. (repetir para cada token)
  Reemplazá todos los valores hardcodeados por estas variables.
  ```

- **Ejemplo trabajado:**

  *"Convertí el styling del Pomodoro para que use variables CSS. Definí en `:root`: `--color-bg: #0f172a`, `--color-text: #e2e8f0`, `--color-accent: #6366f1`, `--color-muted: #94a3b8`, `--space-md: 16px`, `--space-lg: 24px`, `--radius: 12px`, `--font-display: 'Inter', sans-serif`. Reemplazá todos los valores hardcodeados por estas variables. Asegurate que el contraste entre `--color-bg` y `--color-text` sea AA-accesible."*

- **§ Demo en vivo (referencia)** (~250 palabras): nota para el alumno de que en clase el profesor va a tomar un pedido pequeño ("hacé un dice roller") y va a aplicar los cuatro patrones en orden. La sección es para que el alumno pueda volver y seguir el guion después. Incluí estos cuatro prompts exactos en el archivo, uno por patrón (cada uno cabe en una slide):

  **Prompt 1 (Patrón 1 — Describir el artefacto):**

  > Construí un dice roller. Estructura: `<header>` con `<h1>` "Dice Roller"; `<main>` con un `<section>` que muestra el resultado en un cuadrado grande, debajo dos `<button>` ("Tirar" y "Reset"); `<footer>` con historial de últimas 5 tiradas. Estilo: dark mode, fondo `#0f172a`, texto `#e2e8f0`, acento `#6366f1`, sans-serif. El número del resultado en 4rem. Comportamiento: estado `result` (número 1–6, inicial 1). Al click en Tirar, random 1–6 y actualizar `result`. Al click en Reset, volver a 1. Constraints: un archivo HTML, vanilla JS, sin dependencias.

  **Prompt 2 (Patrón 2 — Iterar sobre el estado):**

  > Agregale al dice roller un estado `history` (array). Cada vez que se hace click en Tirar, además de actualizar `result`, agregá el resultado al array. Mostrá las últimas 5 tiradas en el footer como una lista horizontal separadas por comas. Al hacer click en Reset, vaciá `history` también.

  **Prompt 3 (Patrón 3 — Arreglar el layout):**

  > El `<header>` está mal acomodado. Hacelo un flex container con `justify-content: space-between` y `align-items: center`, padding `16px` horizontal. El `<main>` necesita estar centrado: convertilo en flex container con `flex-direction: column`, `align-items: center`, `gap: 24px`.

  **Prompt 4 (Patrón 4 — Tematizar y pulir):**

  > Convertí todo el styling para que use variables CSS. Definí en `:root`: `--color-bg: #0f172a`, `--color-text: #e2e8f0`, `--color-accent: #6366f1`, `--color-muted: #94a3b8`, `--space-md: 16px`, `--space-lg: 24px`, `--radius: 12px`, `--font-display: -apple-system, BlinkMacSystemFont, sans-serif`. Reemplazá todos los valores hardcoded por las variables correspondientes.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/06-patrones-de-prompt-ui.md` with all four patterns fully written, including templates and worked examples exactly as shown above. The Pomodoro example continues across patterns 1, 2, 4 to show evolution.

- [ ] **Step 2: Self-check**

Verify each of the four patterns has *Cuándo usarlo* + *Plantilla* + *Ejemplo trabajado*. Verify the four examples build on each other (Pomodoro running thread). Verify the demo en vivo section provides 4 short prompts for a dice roller demo.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/06-patrones-de-prompt-ui.md
git commit -m "docs(semana-02): add 06-patrones-de-prompt-ui.md (4 prompt patterns)"
```

---

## Task 8: Write `07-actividad-grupal.md`

**Files:**
- Create: `semanas/02/source_material/07-actividad-grupal.md`

**Word target:** ~700 words.

**Purpose:** Activity briefing. Students read this in the breakout rooms; it must be self-contained.

**Required heading structure:**

```
# Actividad grupal: construir un artefacto con ChatGPT Canvas

## Lo que van a practicar

## El ciclo de desarrollo asistido por IA

## Las cuatro tareas del ciclo

### Architect (una vez al inicio)
### Prompter
### Reviewer
### Tester

## Galería de ideas

## Constraints

## Entregable

## Presentación
```

**Required vocabulary (bold on first use):** **ChatGPT Canvas**, **Architect**, **Prompter**, **Reviewer**, **Tester**, **artefacto**, **iteración**.

**Opening line:**

> Tienen 60 minutos para construir un artefacto frontend en una sola página HTML, usando ChatGPT Canvas como su herramienta. Trabajan en grupos de 4. La actividad no es solo construir algo lindo — es practicar cómo se reparte el trabajo entre los humanos cuando la IA es la que escribe el código.

**Section content notes:**

- **§ Lo que van a practicar** (~80 palabras): coordinar el ciclo de desarrollo con IA bajo presión de tiempo. Aplicar los cuatro patrones de prompt vistos en clase. Distribuir las cuatro tareas del ciclo dentro del grupo (no es asignación rígida — es coordinación viva).
- **§ El ciclo de desarrollo asistido por IA** (~150 palabras): explicación del flujo Architect → Prompter ↔ Reviewer ↔ Tester. Incluir el diagrama ASCII del spec:

  ```
  Architect (decompose + first prompt)
           │
           ▼
     ┌─────────────┐
     │  Prompter   │ ← writes next prompt
     │     ↓       │
     │  Reviewer   │ ← reads LLM output, flags issues
     │     ↓       │
     │   Tester    │ ← runs it, breaks it, reports back
     └──────┬──────┘
            │ (loop until done)
            ▼
     Re-enter Architect on major scope changes
  ```

  Aclarar: el Architect pasa una sola vez al inicio (define qué se construye); después el grupo entra en loop entre Prompter, Reviewer y Tester hasta que el artefacto esté listo. Volver al Architect solo si cambia el alcance grande.

- **§ Las cuatro tareas del ciclo** (~250 palabras):

  - **§§ Architect (una vez al inicio):** descompone el artefacto en una spec que el LLM pueda implementar. Escribe el primer prompt usando el Patrón 1 — *Describir el artefacto*. Si después el grupo decide cambiar el alcance grande (de un Pomodoro a un Pomodoro multi-tarea), el Architect vuelve a entrar para re-especificar.
  - **§§ Prompter:** maneja el chat. Escribe los prompts siguientes (Patrones 2, 3, 4 según corresponda). Mantiene el foco — un cambio por prompt, no cuatro.
  - **§§ Reviewer:** lee cada respuesta del LLM antes de copiarla. Busca: APIs alucinadas, lógica que no hace lo que pediste, dependencias externas escondidas, regresiones en código que ya andaba. Aprueba o pide cambios.
  - **§§ Tester:** corre el artefacto en una pestaña aparte. Lo rompe a propósito (clicks rápidos, inputs vacíos, edge cases). Reporta lo que falla al Prompter para la próxima iteración.

  Los cuatro deben pasar; cómo los reparten es decisión del grupo. Mismo integrante puede rotar; pueden hacer dos a la vez. Pero si una de las cuatro tareas no se cumple, el proyecto se desvía de manera predecible.

- **§ Galería de ideas** (~80 palabras): no es asignación, es chispa. Pueden inventar lo que quieran si encaja en una página HTML.
  - Página de aterrizaje para un producto ficticio (fan page, startup parodia, página de un personaje).
  - Herramienta de un solo uso (editor de markdown, paleta de colores, Pomodoro, generador de contraseñas, calculadora de propinas).
  - Mini-juego (lanzador de dados, memory match, idle clicker, test de tipeo).
  - Off-the-wall: cualquier artefacto raro que entre en un archivo.
- **§ Constraints** (~60 palabras):
  - Un solo archivo `index.html`. No build tools, no separate CSS/JS files, no dependencias externas.
  - Una sola conversación de **ChatGPT Canvas** por grupo.
  - 60 minutos de tiempo de construcción.
- **§ Entregable** (~80 palabras): repositorio público en GitHub que contenga:
  - `index.html` — el artefacto funcional
  - `prompts.md` — la secuencia de prompts usados, en orden, con una anotación breve por prompt explicando qué intentaba lograr
  - `README.md` — descripción corta de qué es la página, quién la construyó, qué funcionó y qué no

  El profesor envía el link del repo en el chat de la sala antes de presentar.
- **§ Presentación** (~50 palabras): 5 minutos por grupo, cronometrados con el timer de Meet. Contenido a elección del grupo. Sugerencia: muestren el artefacto, cuenten una decisión de prompt que les enseñó algo (un éxito o un fracaso). Pero no hay rúbrica obligatoria.

**Tasks for the executor:**

- [ ] **Step 1: Create the file with the full prose**

Write `semanas/02/source_material/07-actividad-grupal.md` following the structure above. The ASCII diagram must be preserved exactly.

- [ ] **Step 2: Self-check**

Verify the cycle is described as sequence + loop (not four parallel roles). Verify entregable section lists the three required files. Verify constraint that ChatGPT Canvas is named explicitly.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/07-actividad-grupal.md
git commit -m "docs(semana-02): add 07-actividad-grupal.md (activity spec)"
```

---

## Task 9: Scaffold `demo.html` (hero + base styles + section nav)

**Files:**
- Create: `semanas/02/source_material/demo.html`

**Purpose:** Lay down the page skeleton, global CSS variables, base typography, and hero section. No interactive demos yet — those come in Tasks 10-14.

- [ ] **Step 1: Create the file with the scaffold**

Create `semanas/02/source_material/demo.html` with this exact content:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Conceptos del Frontend — una página que se enseña a sí misma</title>
  <style>
    /* === Variables (theming) === */
    :root {
      --color-bg: #0f172a;
      --color-surface: #1e293b;
      --color-surface-2: #334155;
      --color-text: #e2e8f0;
      --color-muted: #94a3b8;
      --color-accent: #6366f1;
      --color-accent-soft: rgba(99, 102, 241, 0.15);
      --color-success: #10b981;
      --color-warn: #f59e0b;
      --space-xs: 4px;
      --space-sm: 8px;
      --space-md: 16px;
      --space-lg: 24px;
      --space-xl: 48px;
      --radius: 12px;
      --radius-sm: 6px;
      --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;
      --transition: 200ms ease;
    }

    /* === Reset + base === */
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--color-bg);
      color: var(--color-text);
      line-height: 1.6;
    }
    h1, h2, h3 { line-height: 1.2; margin-top: 0; }
    h1 { font-size: 2.5rem; }
    h2 { font-size: 1.75rem; color: var(--color-accent); }
    h3 { font-size: 1.2rem; }
    p { margin: 0 0 var(--space-md) 0; }
    code {
      font-family: var(--font-mono);
      background: var(--color-surface);
      padding: 2px 6px;
      border-radius: var(--radius-sm);
      font-size: 0.9em;
    }
    button {
      font-family: inherit;
      font-size: 0.95rem;
      background: var(--color-accent);
      color: white;
      border: none;
      padding: var(--space-sm) var(--space-md);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: background var(--transition);
    }
    button:hover { background: #4f46e5; }
    button.secondary {
      background: var(--color-surface-2);
      color: var(--color-text);
    }
    button.secondary:hover { background: #475569; }

    /* === Layout === */
    .hero {
      padding: var(--space-xl) var(--space-lg);
      max-width: 900px;
      margin: 0 auto;
      text-align: center;
    }
    .hero p {
      color: var(--color-muted);
      font-size: 1.15rem;
      max-width: 600px;
      margin: 0 auto var(--space-lg) auto;
    }
    .hero nav {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-sm);
      justify-content: center;
      margin-top: var(--space-lg);
    }
    .hero nav a {
      color: var(--color-text);
      background: var(--color-surface);
      padding: var(--space-sm) var(--space-md);
      border-radius: var(--radius-sm);
      text-decoration: none;
      font-size: 0.9rem;
      transition: background var(--transition);
    }
    .hero nav a:hover { background: var(--color-surface-2); }

    main {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 var(--space-lg) var(--space-xl);
    }
    section.demo-section {
      background: var(--color-surface);
      border-radius: var(--radius);
      padding: var(--space-lg);
      margin-bottom: var(--space-xl);
    }
    section.demo-section h2 {
      margin-bottom: var(--space-md);
    }
    section.demo-section .lead {
      color: var(--color-muted);
      margin-bottom: var(--space-lg);
    }
    .demo-area {
      background: var(--color-bg);
      border-radius: var(--radius-sm);
      padding: var(--space-md);
      margin-top: var(--space-md);
    }

    footer {
      text-align: center;
      color: var(--color-muted);
      padding: var(--space-lg);
      font-size: 0.9rem;
      border-top: 1px solid var(--color-surface);
      margin-top: var(--space-xl);
    }
  </style>
</head>
<body>
  <header class="hero">
    <h1>Conceptos del Frontend</h1>
    <p>Explorá una página que se enseña a sí misma. Cada sección demuestra un concepto y al mismo tiempo está construida con ese concepto.</p>
    <nav>
      <a href="#estructura">Estructura</a>
      <a href="#estilo">Estilo</a>
      <a href="#estado">Estado</a>
      <a href="#dom">DOM</a>
      <a href="#single-file">Single-file</a>
    </nav>
  </header>

  <main>
    <section class="demo-section" id="estructura">
      <h2>1. Estructura — HTML semántico</h2>
      <p class="lead">Las etiquetas son sustantivos. La página entiende de qué trata por los nombres.</p>
      <!-- Task 10 fills this section -->
    </section>

    <section class="demo-section" id="estilo">
      <h2>2. Estilo — Layout y variables CSS</h2>
      <p class="lead">El CSS responde a "cómo se ven". Layout y variables son las dos perillas que vale la pena nombrar.</p>
      <!-- Task 11 fills this section -->
    </section>

    <section class="demo-section" id="estado">
      <h2>3. Estado y comportamiento</h2>
      <p class="lead">Estado es el dato detrás. DOM es lo que ves. Eventos son el puente.</p>
      <!-- Task 12 fills this section -->
    </section>

    <section class="demo-section" id="dom">
      <h2>4. El DOM — el árbol vivo</h2>
      <p class="lead">El HTML es texto. El DOM es la representación viva en la memoria del navegador.</p>
      <!-- Task 13 fills this section -->
    </section>

    <section class="demo-section" id="single-file">
      <h2>5. Single-file: todo en un archivo</h2>
      <p class="lead">Esta página entera vive en un solo .html. Vela.</p>
      <!-- Task 14 fills this section -->
    </section>
  </main>

  <footer>
    Material de clase — Semana 2 · Introducción a la ingeniería de software asistida por IA
  </footer>

  <script>
    // === App state ===
    // (populated by section initializers)

    // === Section initializers ===
    // Task 10: initEstructura()
    // Task 11: initEstilo()
    // Task 12: initEstado()
    // Task 13: initDOM()
    // Task 14: initSingleFile()
  </script>
</body>
</html>
```

- [ ] **Step 2: Open in a browser and verify the scaffold renders**

Run (from project root):

```bash
npm start
```

Open `http://localhost:3000/semanas/02/source_material/demo.html` in a browser.

Expected:
- Hero section displays "Conceptos del Frontend" centered with subtitle below.
- Five nav pills below the subtitle linking to each section.
- Five empty section cards on the page, each with title and lead paragraph.
- Footer at bottom.
- No console errors.

- [ ] **Step 3: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): scaffold demo.html with hero and section skeleton"
```

---

## Task 10: Demo §1 Estructura — semantic vs div-soup toggle

**Files:**
- Modify: `semanas/02/source_material/demo.html` (replace the comment `<!-- Task 10 fills this section -->`)

**Purpose:** A toggle button switches between two visually identical articles — one rendered with semantic tags, one with `<div>` everywhere. A "Ver código fuente" toggle reveals the underlying HTML for the currently shown version.

- [ ] **Step 1: Add the markup inside `<section id="estructura">`**

Replace the `<!-- Task 10 fills this section -->` comment with:

```html
      <div class="estructura-controls">
        <button id="btn-semantic" class="active">Semántico</button>
        <button id="btn-divsoup" class="secondary">Sopa de divs</button>
        <button id="btn-show-source" class="secondary">Ver código</button>
      </div>
      <div class="demo-area" id="estructura-render"></div>
      <pre class="estructura-source" id="estructura-source" hidden></pre>
```

- [ ] **Step 2: Add the supporting CSS inside the existing `<style>` block, before the closing `</style>` tag**

```css
    /* === §1 Estructura === */
    .estructura-controls {
      display: flex;
      gap: var(--space-sm);
      flex-wrap: wrap;
      margin-bottom: var(--space-md);
    }
    .estructura-controls button.active {
      background: var(--color-accent);
    }
    #estructura-render article {
      background: var(--color-surface-2);
      padding: var(--space-md);
      border-radius: var(--radius-sm);
    }
    #estructura-render header h3 { margin-top: 0; color: var(--color-accent); }
    #estructura-render nav { margin: var(--space-sm) 0; }
    #estructura-render nav a {
      color: var(--color-accent);
      margin-right: var(--space-md);
      text-decoration: none;
    }
    #estructura-render nav a:hover { text-decoration: underline; }
    #estructura-render section, #estructura-render .section-fake {
      margin-top: var(--space-md);
    }
    #estructura-render footer, #estructura-render .footer-fake {
      margin-top: var(--space-md);
      color: var(--color-muted);
      font-size: 0.85rem;
      border-top: 1px solid var(--color-surface);
      padding-top: var(--space-sm);
    }
    .estructura-source {
      background: var(--color-bg);
      border: 1px solid var(--color-surface-2);
      border-radius: var(--radius-sm);
      padding: var(--space-md);
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: var(--color-muted);
      margin-top: var(--space-md);
    }
```

- [ ] **Step 3: Add the JS inside the `<script>` block (after the `// Task 10: initEstructura()` comment line)**

```javascript
    // === §1 Estructura ===
    const estructuraVersions = {
      semantic: `<article>
  <header>
    <h3>Recetas de la abuela</h3>
    <nav>
      <a href="#">Inicio</a>
      <a href="#">Recetas</a>
      <a href="#">Sobre mí</a>
    </nav>
  </header>
  <section>
    <p>Bienvenidos al recetario familiar. Hoy: tarta de manzana.</p>
  </section>
  <footer>Última actualización: marzo 2026</footer>
</article>`,
      divsoup: `<div class="article-fake">
  <div class="header-fake">
    <div class="title-fake">Recetas de la abuela</div>
    <div class="nav-fake">
      <span><a href="#">Inicio</a></span>
      <span><a href="#">Recetas</a></span>
      <span><a href="#">Sobre mí</a></span>
    </div>
  </div>
  <div class="section-fake">
    <div>Bienvenidos al recetario familiar. Hoy: tarta de manzana.</div>
  </div>
  <div class="footer-fake">Última actualización: marzo 2026</div>
</div>`,
    };

    function initEstructura() {
      const render = document.getElementById('estructura-render');
      const source = document.getElementById('estructura-source');
      const btnSem = document.getElementById('btn-semantic');
      const btnDiv = document.getElementById('btn-divsoup');
      const btnSrc = document.getElementById('btn-show-source');
      let current = 'semantic';
      let sourceVisible = false;

      function paint() {
        render.innerHTML = estructuraVersions[current];
        source.textContent = estructuraVersions[current];
        btnSem.classList.toggle('active', current === 'semantic');
        btnSem.classList.toggle('secondary', current !== 'semantic');
        btnDiv.classList.toggle('active', current === 'divsoup');
        btnDiv.classList.toggle('secondary', current !== 'divsoup');
        source.hidden = !sourceVisible;
        btnSrc.textContent = sourceVisible ? 'Ocultar código' : 'Ver código';
      }

      btnSem.addEventListener('click', () => { current = 'semantic'; paint(); });
      btnDiv.addEventListener('click', () => { current = 'divsoup'; paint(); });
      btnSrc.addEventListener('click', () => { sourceVisible = !sourceVisible; paint(); });

      paint();
    }
    initEstructura();
```

- [ ] **Step 4: Verify in browser**

Reload `http://localhost:3000/semanas/02/source_material/demo.html`.

Expected:
- §1 section shows three buttons: "Semántico" (highlighted), "Sopa de divs", "Ver código".
- Below the buttons, an article renders with title "Recetas de la abuela", a nav with three links, a body paragraph, and a footer line.
- Click "Sopa de divs" → the article re-renders visually identically (might shift slightly because divs have no default styling, but the content is the same).
- Click "Ver código" → a code block appears below showing the HTML of whatever version is currently rendered.
- Toggle between Semántico/Sopa de divs while code is visible — the code block updates.

- [ ] **Step 5: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): add demo.html §1 Estructura semantic/div-soup toggle"
```

---

## Task 11: Demo §2 Estilo — flex/grid playground + theme switcher

**Files:**
- Modify: `semanas/02/source_material/demo.html`

**Purpose:** Two interactive panels. Top: a flexbox playground with buttons that change `justify-content`. Bottom: a theme switcher with three accent colors that updates a CSS variable live.

- [ ] **Step 1: Add the markup inside `<section id="estilo">`**

Replace `<!-- Task 11 fills this section -->` with:

```html
      <h3>Flexbox: una dimensión</h3>
      <div class="estilo-controls">
        <button data-jc="flex-start" class="jc-btn active">flex-start</button>
        <button data-jc="center" class="jc-btn secondary">center</button>
        <button data-jc="space-between" class="jc-btn secondary">space-between</button>
        <button data-jc="space-around" class="jc-btn secondary">space-around</button>
        <button data-jc="flex-end" class="jc-btn secondary">flex-end</button>
      </div>
      <div class="demo-area">
        <div class="flex-playground" id="flex-playground">
          <div class="flex-item">A</div>
          <div class="flex-item">B</div>
          <div class="flex-item">C</div>
        </div>
        <p class="estilo-current"><code id="flex-current">justify-content: flex-start</code></p>
      </div>

      <h3 style="margin-top: var(--space-lg)">Variables CSS: cambiá la perilla</h3>
      <div class="estilo-controls">
        <button data-accent="#6366f1" class="theme-btn active" style="background:#6366f1">Indigo</button>
        <button data-accent="#10b981" class="theme-btn secondary" style="background:#10b981">Esmeralda</button>
        <button data-accent="#f59e0b" class="theme-btn secondary" style="background:#f59e0b">Ámbar</button>
        <button data-accent="#ef4444" class="theme-btn secondary" style="background:#ef4444">Rojo</button>
      </div>
      <p class="estilo-current"><code id="theme-current">--color-accent: #6366f1</code></p>
```

- [ ] **Step 2: Add the supporting CSS in the `<style>` block**

```css
    /* === §2 Estilo === */
    .estilo-controls {
      display: flex;
      gap: var(--space-sm);
      flex-wrap: wrap;
      margin-bottom: var(--space-md);
    }
    .estilo-controls button.active { outline: 2px solid var(--color-text); }
    .flex-playground {
      display: flex;
      justify-content: flex-start;
      gap: var(--space-sm);
      background: var(--color-surface-2);
      padding: var(--space-md);
      border-radius: var(--radius-sm);
      min-height: 80px;
      transition: justify-content var(--transition);
    }
    .flex-item {
      background: var(--color-accent);
      color: white;
      padding: var(--space-md) var(--space-lg);
      border-radius: var(--radius-sm);
      font-weight: 600;
    }
    .estilo-current {
      color: var(--color-muted);
      margin-top: var(--space-sm);
      font-size: 0.9rem;
    }
```

- [ ] **Step 3: Add the JS inside the `<script>` block**

```javascript
    // === §2 Estilo ===
    function initEstilo() {
      const playground = document.getElementById('flex-playground');
      const current = document.getElementById('flex-current');
      const jcButtons = document.querySelectorAll('.jc-btn');
      jcButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const jc = btn.dataset.jc;
          playground.style.justifyContent = jc;
          current.textContent = `justify-content: ${jc}`;
          jcButtons.forEach(b => {
            b.classList.toggle('active', b === btn);
            b.classList.toggle('secondary', b !== btn);
          });
        });
      });

      const themeCurrent = document.getElementById('theme-current');
      const themeButtons = document.querySelectorAll('.theme-btn');
      themeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const accent = btn.dataset.accent;
          document.documentElement.style.setProperty('--color-accent', accent);
          themeCurrent.textContent = `--color-accent: ${accent}`;
          themeButtons.forEach(b => {
            b.classList.toggle('active', b === btn);
            b.classList.toggle('secondary', b !== btn);
          });
        });
      });
    }
    initEstilo();
```

- [ ] **Step 4: Verify in browser**

Reload. In §2:
- Five buttons for flexbox `justify-content`. Click each; the three labeled boxes (A/B/C) reposition. The code label below updates.
- Four theme buttons (Indigo / Esmeralda / Ámbar / Rojo). Click each; the entire page's accent color (links, h2, primary buttons elsewhere) changes immediately. The code label updates.

- [ ] **Step 5: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): add demo.html §2 Estilo flex playground and theme switcher"
```

---

## Task 12: Demo §3 Estado — counter + todo + event log

**Files:**
- Modify: `semanas/02/source_material/demo.html`

**Purpose:** Three side-by-side micro-demos that illustrate the state → DOM → events triangle.

- [ ] **Step 1: Add the markup inside `<section id="estado">`**

Replace `<!-- Task 12 fills this section -->` with:

```html
      <div class="estado-grid">
        <div class="estado-demo">
          <h3>Contador</h3>
          <p class="estado-state">estado: <code id="counter-state">count = 0</code></p>
          <div class="counter-display" id="counter-display">0</div>
          <div class="estado-controls">
            <button id="counter-dec" class="secondary">−1</button>
            <button id="counter-inc">+1</button>
            <button id="counter-reset" class="secondary">reset</button>
          </div>
        </div>

        <div class="estado-demo">
          <h3>Todo list</h3>
          <p class="estado-state">estado: <code id="todo-state">items = []</code></p>
          <form id="todo-form" class="todo-form">
            <input type="text" id="todo-input" placeholder="Nueva tarea..." required>
            <button type="submit">+</button>
          </form>
          <ul class="todo-list" id="todo-list"></ul>
        </div>

        <div class="estado-demo">
          <h3>Event log</h3>
          <p class="estado-state">cualquier click se registra abajo</p>
          <div class="event-target" id="event-target">Hacé click acá</div>
          <ol class="event-log" id="event-log"></ol>
        </div>
      </div>
```

- [ ] **Step 2: Add the supporting CSS**

```css
    /* === §3 Estado === */
    .estado-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: var(--space-md);
    }
    .estado-demo {
      background: var(--color-bg);
      padding: var(--space-md);
      border-radius: var(--radius-sm);
    }
    .estado-demo h3 { margin-top: 0; color: var(--color-text); }
    .estado-state { color: var(--color-muted); font-size: 0.85rem; }
    .estado-controls { display: flex; gap: var(--space-xs); flex-wrap: wrap; }
    .counter-display {
      font-size: 3rem;
      font-weight: 700;
      text-align: center;
      color: var(--color-accent);
      margin: var(--space-sm) 0;
    }
    .todo-form {
      display: flex;
      gap: var(--space-xs);
      margin-bottom: var(--space-sm);
    }
    .todo-form input {
      flex: 1;
      background: var(--color-surface-2);
      color: var(--color-text);
      border: 1px solid var(--color-surface-2);
      border-radius: var(--radius-sm);
      padding: var(--space-xs) var(--space-sm);
      font-family: inherit;
    }
    .todo-list {
      list-style: none;
      padding: 0;
      margin: 0;
      max-height: 140px;
      overflow-y: auto;
    }
    .todo-list li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--space-xs) var(--space-sm);
      background: var(--color-surface-2);
      border-radius: var(--radius-sm);
      margin-bottom: var(--space-xs);
      font-size: 0.9rem;
    }
    .todo-list button {
      background: transparent;
      color: var(--color-muted);
      padding: 0 var(--space-xs);
    }
    .todo-list button:hover { color: var(--color-warn); background: transparent; }
    .event-target {
      background: var(--color-accent-soft);
      border: 1px dashed var(--color-accent);
      border-radius: var(--radius-sm);
      padding: var(--space-md);
      text-align: center;
      cursor: pointer;
      user-select: none;
      margin-bottom: var(--space-sm);
    }
    .event-log {
      list-style: none;
      padding: 0;
      margin: 0;
      max-height: 120px;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--color-muted);
    }
    .event-log li { padding: 2px 0; border-bottom: 1px solid var(--color-surface); }
```

- [ ] **Step 3: Add the JS**

```javascript
    // === §3 Estado ===
    function initEstado() {
      // Counter
      let count = 0;
      const counterDisplay = document.getElementById('counter-display');
      const counterState = document.getElementById('counter-state');
      function paintCounter() {
        counterDisplay.textContent = count;
        counterState.textContent = `count = ${count}`;
      }
      document.getElementById('counter-inc').addEventListener('click', () => { count++; paintCounter(); });
      document.getElementById('counter-dec').addEventListener('click', () => { count--; paintCounter(); });
      document.getElementById('counter-reset').addEventListener('click', () => { count = 0; paintCounter(); });
      paintCounter();

      // Todo list
      let items = [];
      const todoList = document.getElementById('todo-list');
      const todoState = document.getElementById('todo-state');
      const todoForm = document.getElementById('todo-form');
      const todoInput = document.getElementById('todo-input');
      function paintTodos() {
        todoList.innerHTML = '';
        items.forEach((item, idx) => {
          const li = document.createElement('li');
          const span = document.createElement('span');
          span.textContent = item;
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.textContent = '×';
          btn.addEventListener('click', () => {
            items.splice(idx, 1);
            paintTodos();
          });
          li.appendChild(span);
          li.appendChild(btn);
          todoList.appendChild(li);
        });
        todoState.textContent = `items = [${items.map(i => `'${i.slice(0, 8)}${i.length > 8 ? '…' : ''}'`).join(', ')}]`;
      }
      todoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const value = todoInput.value.trim();
        if (!value) return;
        items.push(value);
        todoInput.value = '';
        paintTodos();
      });
      paintTodos();

      // Event log
      const target = document.getElementById('event-target');
      const log = document.getElementById('event-log');
      let eventCount = 0;
      target.addEventListener('click', (e) => {
        eventCount++;
        const li = document.createElement('li');
        const time = new Date().toLocaleTimeString();
        li.textContent = `[${time}] click #${eventCount} en (${e.offsetX}, ${e.offsetY})`;
        log.insertBefore(li, log.firstChild);
        while (log.children.length > 8) log.removeChild(log.lastChild);
      });
    }
    initEstado();
```

- [ ] **Step 4: Verify in browser**

Reload. In §3 you should see three demo cards in a row (or stacked on narrow viewports):
- Counter: shows "0", buttons +1 / −1 / reset work, the `count = N` label updates.
- Todo: type in input, press + or Enter, a row appears in the list with × to delete. The `items = [...]` label updates.
- Event log: click the dashed box, entries appear above with timestamp and coordinates. Cap at 8 entries.

- [ ] **Step 5: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): add demo.html §3 Estado counter, todo, event log"
```

---

## Task 13: Demo §4 DOM — live tree visualization

**Files:**
- Modify: `semanas/02/source_material/demo.html`

**Purpose:** Render the DOM subtree of section §3 as a nested indented tree. Hovering a node highlights the corresponding element on screen. Updates live (because §3's todo list mutates the DOM).

**Implementation note:** hand-rolled, no library. Walk the DOM with `Element.children`; render as nested `<ul>`. Use a `MutationObserver` so the tree updates when §3's todo list changes.

- [ ] **Step 1: Add the markup inside `<section id="dom">`**

Replace `<!-- Task 13 fills this section -->` with:

```html
      <p>Estás mirando el árbol del DOM de la sección §3 (estado y comportamiento). Cuando agregás o borrás items en el todo, este árbol se actualiza solo. Pasá el mouse sobre un nodo para resaltarlo arriba.</p>
      <div class="demo-area">
        <ul class="dom-tree" id="dom-tree"></ul>
      </div>
```

- [ ] **Step 2: Add the supporting CSS**

```css
    /* === §4 DOM === */
    .dom-tree, .dom-tree ul {
      list-style: none;
      padding-left: var(--space-md);
      margin: 0;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }
    .dom-tree li {
      padding: 2px 0;
      cursor: pointer;
      color: var(--color-muted);
      transition: color var(--transition);
    }
    .dom-tree li:hover > .dom-label { color: var(--color-accent); }
    .dom-label {
      display: inline-block;
      padding: 1px 6px;
      border-radius: 4px;
    }
    .dom-label .tag { color: var(--color-accent); }
    .dom-label .id { color: var(--color-warn); }
    .dom-label .cls { color: var(--color-success); }
    .dom-highlight {
      outline: 2px dashed var(--color-warn) !important;
      outline-offset: 4px;
    }
```

- [ ] **Step 3: Add the JS**

```javascript
    // === §4 DOM ===
    function initDOM() {
      const tree = document.getElementById('dom-tree');
      const root = document.getElementById('estado');
      let highlightedEl = null;

      function clearHighlight() {
        if (highlightedEl) {
          highlightedEl.classList.remove('dom-highlight');
          highlightedEl = null;
        }
      }

      function renderNode(el) {
        const li = document.createElement('li');
        const label = document.createElement('span');
        label.className = 'dom-label';
        const tag = `<span class="tag">${el.tagName.toLowerCase()}</span>`;
        const id = el.id ? `<span class="id">#${el.id}</span>` : '';
        const cls = el.className && typeof el.className === 'string'
          ? `<span class="cls">.${el.className.split(' ').filter(Boolean).join('.')}</span>`
          : '';
        label.innerHTML = `&lt;${tag}${id}${cls}&gt;`;
        li.appendChild(label);

        label.addEventListener('mouseenter', () => {
          clearHighlight();
          el.classList.add('dom-highlight');
          highlightedEl = el;
        });
        label.addEventListener('mouseleave', clearHighlight);

        if (el.children.length > 0) {
          const ul = document.createElement('ul');
          for (const child of el.children) {
            ul.appendChild(renderNode(child));
          }
          li.appendChild(ul);
        }
        return li;
      }

      function rebuild() {
        clearHighlight();
        tree.innerHTML = '';
        tree.appendChild(renderNode(root));
      }

      rebuild();

      const observer = new MutationObserver(() => rebuild());
      observer.observe(root, { childList: true, subtree: true });
    }
    initDOM();
```

- [ ] **Step 4: Verify in browser**

Reload. In §4 you should see a nested indented tree showing the structure of §3. Top node: `<section #estado .demo-section>`. Hover any leaf node — the corresponding element in §3 highlights with a yellow dashed outline. Add a todo in §3 — a new `<li>` node appears under the todo-list branch immediately.

- [ ] **Step 5: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): add demo.html §4 DOM live tree with highlight"
```

---

## Task 14: Demo §5 Single-file — view source modal

**Files:**
- Modify: `semanas/02/source_material/demo.html`

**Purpose:** A button opens a modal showing the page's own source HTML. Drives home that the entire teaching artifact lives in one file.

- [ ] **Step 1: Add the markup inside `<section id="single-file">`**

Replace `<!-- Task 14 fills this section -->` with:

```html
      <p>Esta página entera — los cinco demos, los toggles, el árbol del DOM, el theming — vive en <strong>un solo archivo HTML</strong>. Sin <code>node_modules</code>, sin pipeline, sin servidor. Sólo tres tecnologías inline: HTML, CSS, JS.</p>
      <div class="demo-area">
        <p>¿No me creés? Vela:</p>
        <button id="btn-view-source">Ver el código fuente</button>
        <p class="estado-state" style="margin-top: var(--space-sm)">
          También podés copiar este archivo, pegarlo en un Gist y servirlo como GitHub Pages.
        </p>
      </div>

      <div class="modal" id="source-modal" hidden>
        <div class="modal-backdrop"></div>
        <div class="modal-panel">
          <div class="modal-header">
            <h3>demo.html — código fuente</h3>
            <button id="btn-close-modal" class="secondary">Cerrar</button>
          </div>
          <pre id="source-content"></pre>
        </div>
      </div>
```

- [ ] **Step 2: Add the supporting CSS**

```css
    /* === §5 Single-file === */
    .modal {
      position: fixed;
      inset: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--space-md);
    }
    .modal[hidden] { display: none; }
    .modal-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
    }
    .modal-panel {
      position: relative;
      background: var(--color-surface);
      border-radius: var(--radius);
      max-width: 1000px;
      width: 100%;
      max-height: 80vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: var(--space-md);
      border-bottom: 1px solid var(--color-surface-2);
    }
    .modal-header h3 { margin: 0; }
    .modal-panel pre {
      margin: 0;
      padding: var(--space-md);
      overflow: auto;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--color-muted);
      line-height: 1.5;
      flex: 1;
    }
```

- [ ] **Step 3: Add the JS**

```javascript
    // === §5 Single-file ===
    function initSingleFile() {
      const btn = document.getElementById('btn-view-source');
      const modal = document.getElementById('source-modal');
      const close = document.getElementById('btn-close-modal');
      const content = document.getElementById('source-content');
      const backdrop = modal.querySelector('.modal-backdrop');

      btn.addEventListener('click', async () => {
        try {
          const response = await fetch(window.location.href);
          const text = await response.text();
          content.textContent = text;
        } catch (err) {
          content.textContent = '// No se pudo leer el archivo (estás abriendo desde el filesystem y el navegador bloquea fetch). Servilo con `npm start` para ver el código.';
        }
        modal.hidden = false;
      });

      function closeModal() { modal.hidden = true; }
      close.addEventListener('click', closeModal);
      backdrop.addEventListener('click', closeModal);
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.hidden) closeModal();
      });
    }
    initSingleFile();
```

- [ ] **Step 4: Verify in browser**

Reload. In §5, click "Ver el código fuente". A modal opens showing the entire source of `demo.html` (HTML + CSS + JS, all of it). Close via the Cerrar button, clicking outside, or pressing Escape.

- [ ] **Step 5: Commit**

```bash
git add semanas/02/source_material/demo.html
git commit -m "feat(semana-02): add demo.html §5 Single-file view-source modal"
```

---

## Task 15: Final polish + smoke test

**Files:**
- Modify: `semanas/02/source_material/demo.html` (only if smoke test reveals issues)

**Purpose:** End-to-end verification of the full demo. Catch interaction bugs between sections (e.g., theme switcher should change accent color of all five sections; DOM tree should still update after theme change; etc.).

- [ ] **Step 1: Walk through the smoke test in a browser**

Open `http://localhost:3000/semanas/02/source_material/demo.html`. For each item, mark pass/fail. If something fails, fix it inline before continuing.

  - [ ] Hero renders, nav pills clickable and scroll to each section.
  - [ ] §1 Estructura: toggle Semántico/Sopa de divs, source code reveal works.
  - [ ] §2 Estilo: all 5 flexbox buttons reposition the boxes; all 4 theme buttons change accent color across the page.
  - [ ] §3 Estado: counter +/- works; todo can add and delete; event log captures clicks.
  - [ ] §4 DOM tree renders, hover highlights, todo additions update the tree live.
  - [ ] §5 Source modal opens and closes (button, backdrop, Escape).
  - [ ] No console errors in DevTools.
  - [ ] Theme change in §2 propagates to flex-item color in §2's playground (verify a deep dependency).
  - [ ] Resize window to ~600px wide: §3's three demos stack instead of overflowing.

- [ ] **Step 2: Read through all 8 markdown files end-to-end**

Run:

```bash
ls semanas/02/source_material/
```

Expected:
- `index.md`
- `01-frontend-y-el-supervisor.md`
- `02-estructura-html.md`
- `03-estilo-css.md`
- `04-estado-y-comportamiento.md`
- `05-single-file-platform.md`
- `06-patrones-de-prompt-ui.md`
- `07-actividad-grupal.md`
- `demo.html`

Read each markdown file in order. Verify:
  - [ ] Voice consistent (Spanish, professor, second-person plural).
  - [ ] Vocabulary terms bolded on first use across files.
  - [ ] Cross-references resolve (e.g., file 02 mentions "demo.html §Estructura toggle" and that toggle exists in Task 10's output).
  - [ ] No file is over the word target by more than 20%.
  - [ ] No emojis.
  - [ ] No "TODO" / "TBD" / placeholder content.

- [ ] **Step 3: Commit any polish edits**

If you made any fixes during the smoke test:

```bash
git add semanas/02/source_material/
git commit -m "polish(semana-02): smoke-test fixes for source material and demo"
```

If no fixes needed, skip the commit.

- [ ] **Step 4: Final state check**

Run:

```bash
git log --oneline feature/semana-02-source-material
```

Expected: at least 1 spec commit + 8 markdown commits + 6 demo.html commits + maybe 1 polish commit = 15-16 commits on the branch.

Run:

```bash
git status
```

Expected: clean working tree.

---

## Self-review (already performed by plan author)

- **Spec coverage:** all 9 deliverables listed in the spec's source material file list have a dedicated task. Activity spec content matches Task 8's outline exactly. Demo.html sections (1–5) match the spec's six-section description (hero counts as 0; sections 1–5 are tasks 10–14).
- **Placeholder scan:** no "TBD", "TODO", or "implement later" in the plan body. Every code block is complete code; every prose task includes a heading structure + opening line + per-section notes substantial enough to write from.
- **Type consistency:** function names (`initEstructura`, `initEstilo`, `initEstado`, `initDOM`, `initSingleFile`), CSS variable names (`--color-accent` etc.), and DOM IDs (`estructura-render`, `flex-playground`, etc.) are consistent across tasks 9–15.
- **Open questions from spec resolved:**
  - "Whether `demo.html` includes a CDN dependency" → resolved: no CDN, hand-rolled DOM tree.
  - "Exact wording of the four prompt patterns" → resolved: defined in Task 7 (Pomodoro thread).
  - "Whether to provide a starter `prompts.md` template" → resolved: no template (per user decision in brainstorming).

---

## Execution recommendation

Execute as **subagent-driven** with one subagent per task. The markdown tasks (2–8) can run in parallel since they touch different files and don't depend on each other; tasks 9–14 must be sequential (they all modify `demo.html`). Task 15 is final and sequential.

**Suggested batching:**

1. Task 1 (index) — sequential, 1 subagent.
2. Tasks 2–8 (markdowns) — parallel, 7 subagents.
3. Tasks 9–14 (demo.html) — sequential, 1 subagent each.
4. Task 15 (smoke test) — sequential, 1 subagent.
