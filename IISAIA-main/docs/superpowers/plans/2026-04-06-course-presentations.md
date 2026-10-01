# Course Presentations Platform — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold an ICM-organized repo with reveal.js presentations for an 8-week AI-assisted development course.

**Architecture:** ICM hybrid structure — each week is a self-contained stage folder under `semanas/`. Shared theme and conventions live in `_config/`. Root `CLAUDE.md` and `CONTEXT.md` provide routing. Reveal.js loaded via npm, served with a local static server.

**Tech Stack:** reveal.js, HTML, CSS, Node.js (npm for dependency management + `serve` for local dev server)

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `package.json` | Dependencies (reveal.js, serve) and start script |
| Create | `.gitignore` | Exclude node_modules |
| Create | `CLAUDE.md` | Layer 0: project map + routing table |
| Create | `CONTEXT.md` | Layer 1: task routing |
| Create | `_config/slide-conventions.md` | Layer 3: slide formatting rules |
| Create | `_config/theme/variables.css` | CSS custom properties |
| Create | `_config/theme/custom.css` | Reveal.js theme overrides |
| Create | `shared/templates/week-template.html` | Base slide template |
| Create | `shared/CONTEXT.md` | Describes shared resources |
| Create | `semanas/01/CONTEXT.md` through `semanas/08/CONTEXT.md` | Per-week stage contracts |
| Create | `semanas/01/notas.md` | Week 1 lecture notes (migrated from semana_1.md) |
| Create | `semanas/01/slides/index.html` | Week 1 reveal.js presentation |
| Keep | `programa.md` | Canonical source for weekly topics (already exists) |
| Keep | `semana_1.md` | Original draft (kept as reference, replaced by semanas/01/notas.md) |

---

### Task 1: Git Init + Dependencies

**Files:**
- Create: `.gitignore`
- Create: `package.json`

- [ ] **Step 1: Initialize git repo**

```bash
cd /c/Users/Enzo/Documents/intro_desarrollo_asistido_IA
git init
```

- [ ] **Step 2: Create .gitignore**

```
node_modules/
```

- [ ] **Step 3: Create package.json**

```json
{
  "name": "intro-desarrollo-asistido-ia",
  "version": "1.0.0",
  "description": "Course presentations for Intro to AI-Assisted Software Development",
  "scripts": {
    "start": "npx serve . -l 3000"
  },
  "devDependencies": {
    "reveal.js": "^5.2.1",
    "serve": "^14.2.4"
  }
}
```

- [ ] **Step 4: Install dependencies**

```bash
npm install
```

Expected: `node_modules/` created with reveal.js and serve installed. No errors.

- [ ] **Step 5: Commit**

```bash
git add .gitignore package.json package-lock.json
git commit -m "feat: init repo with reveal.js and serve dependencies"
```

---

### Task 2: Theme Files

**Files:**
- Create: `_config/theme/variables.css`
- Create: `_config/theme/custom.css`

- [ ] **Step 1: Create variables.css**

```css
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --bg-code: #0f0f1a;
  --text-primary: #e0e0e0;
  --text-heading: #ffffff;
  --text-muted: #8892b0;
  --accent: #64ffda;
  --accent-secondary: #82aaff;
  --link: #82aaff;
  --link-hover: #64ffda;
  --code-text: #c3e88d;
  --font-body: 'Inter', 'Segoe UI', system-ui, sans-serif;
  --font-heading: 'Inter', 'Segoe UI', system-ui, sans-serif;
  --font-mono: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}
```

- [ ] **Step 2: Create custom.css**

```css
@import url('./variables.css');

/* Base overrides */
.reveal {
  font-family: var(--font-body);
  font-size: 32px;
  color: var(--text-primary);
}

.reveal .slides {
  text-align: left;
}

/* Headings */
.reveal h1, .reveal h2, .reveal h3, .reveal h4 {
  font-family: var(--font-heading);
  color: var(--text-heading);
  font-weight: 600;
  text-transform: none;
}

.reveal h1 {
  font-size: 2em;
}

.reveal h2 {
  font-size: 1.5em;
  color: var(--accent);
}

.reveal h3 {
  font-size: 1.2em;
  color: var(--accent-secondary);
}

/* Paragraphs and lists */
.reveal p, .reveal li {
  line-height: 1.6;
  color: var(--text-primary);
}

.reveal ul, .reveal ol {
  margin-left: var(--spacing-lg);
}

.reveal li {
  margin-bottom: var(--spacing-sm);
}

/* Links */
.reveal a {
  color: var(--link);
  text-decoration: underline;
  text-decoration-color: transparent;
  transition: text-decoration-color 0.2s;
}

.reveal a:hover {
  color: var(--link-hover);
  text-decoration-color: var(--link-hover);
}

/* Code */
.reveal pre {
  background: var(--bg-code);
  border-radius: 8px;
  padding: var(--spacing-md);
  font-size: 0.55em;
  width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.reveal code {
  font-family: var(--font-mono);
  color: var(--code-text);
}

.reveal p code, .reveal li code {
  background: var(--bg-code);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85em;
}

/* Images */
.reveal img {
  max-height: 55vh;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Muted/secondary text */
.reveal .muted {
  color: var(--text-muted);
  font-size: 0.8em;
}

/* Blockquotes */
.reveal blockquote {
  border-left: 4px solid var(--accent);
  padding-left: var(--spacing-md);
  font-style: italic;
  color: var(--text-muted);
  background: rgba(100, 255, 218, 0.05);
  border-radius: 0 8px 8px 0;
}

/* Title slide styling */
.reveal .title-slide h1 {
  font-size: 2.5em;
  margin-bottom: var(--spacing-lg);
}

.reveal .title-slide .subtitle {
  color: var(--accent);
  font-size: 1.2em;
}

/* Section divider slides */
.reveal .section-divider {
  text-align: center;
}

.reveal .section-divider h2 {
  font-size: 2em;
}
```

- [ ] **Step 3: Commit**

```bash
git add _config/
git commit -m "feat: add dark theme with CSS custom properties"
```

---

### Task 3: Slide Conventions Document

**Files:**
- Create: `_config/slide-conventions.md`

- [ ] **Step 1: Create slide-conventions.md**

```markdown
# Slide Conventions

Rules for generating and formatting reveal.js presentations.

## Language
- Spanish, technical but accessible for diploma-level students.
- No AI-sounding filler: "revolucionario", "potenciar", "de vanguardia".

## Slide Density
- One main concept per slide. If it needs scrolling, split it.
- Title slides: week number + topic title + subtitle.
- Section divider slides: use `class="section-divider"` for major topic transitions.

## Headings
- Short, descriptive. No filler text.
- h1 for title slides only. h2 for slide headings. h3 for sub-points within a slide.

## Code Blocks
- Use reveal.js highlight plugin with language annotation.
- Add `data-line-numbers` attribute when highlighting specific lines.
- Keep code blocks under 15 lines per slide. Split into multiple slides if longer.

## Links
- Render as clickable `<a>` elements with descriptive text.
- Format: `<a href="URL" target="_blank">Descriptive Text</a>`

## Images
- Reference from `img/` folder relative to the slides directory.
- Use responsive sizing: `style="max-height: 50vh"`.
- Always include `alt` text.

## Speaker Notes
- Use `<aside class="notes">` inside each `<section>`.
- Contain the detailed explanation from the lecture draft.
- This is what the professor reads/says aloud. The slide shows only the key visual/concept.

## Progressive Reveals
- Use `class="fragment"` for building up concepts step by step.
- Use `class="fragment fade-in"` as default fragment style.

## Vertical Slides
- Use nested `<section>` for optional deep-dives.
- Example: a main slide introduces a paper, vertical slides show details.

## Transitions
- Use `none` or `fade`. No 3D or fancy transitions.

## Do NOT
- Add emojis to slides.
- Use gratuitous animations.
- Add placeholder or filler text.
- Use more than one font family.
```

- [ ] **Step 2: Commit**

```bash
git add _config/slide-conventions.md
git commit -m "feat: add slide conventions document"
```

---

### Task 4: Reveal.js Slide Template

**Files:**
- Create: `shared/templates/week-template.html`
- Create: `shared/CONTEXT.md`

- [ ] **Step 1: Create week-template.html**

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Semana NN — TOPIC_TITLE</title>
  <link rel="stylesheet" href="../../node_modules/reveal.js/dist/reveal.css">
  <link rel="stylesheet" href="../../node_modules/reveal.js/dist/theme/black.css">
  <link rel="stylesheet" href="../../node_modules/reveal.js/plugin/highlight/monokai.css">
  <link rel="stylesheet" href="../../_config/theme/custom.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">

      <!-- Title Slide -->
      <section class="title-slide">
        <h1>Semana NN</h1>
        <p class="subtitle">TOPIC_TITLE</p>
        <p class="muted">Introduccion al desarrollo de software asistido por IA</p>
      </section>

      <!-- Section: Example -->
      <section>
        <section>
          <h2>Section Title</h2>
          <p>Main concept goes here.</p>
          <aside class="notes">
            Speaker notes: detailed explanation for the professor.
          </aside>
        </section>
        <!-- Vertical slide for deep-dive -->
        <section>
          <h3>Deep Dive</h3>
          <p>Additional detail.</p>
        </section>
      </section>

      <!-- Closing Slide -->
      <section class="section-divider">
        <h2>Preguntas?</h2>
      </section>

    </div>
  </div>

  <script src="../../node_modules/reveal.js/dist/reveal.js"></script>
  <script src="../../node_modules/reveal.js/plugin/highlight/highlight.js"></script>
  <script src="../../node_modules/reveal.js/plugin/notes/notes.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      slideNumber: true,
      transition: 'fade',
      plugins: [RevealHighlight, RevealNotes]
    });
  </script>
</body>
</html>
```

- [ ] **Step 2: Create shared/CONTEXT.md**

```markdown
# Shared Resources

## Contents
- `templates/week-template.html` — Base reveal.js template. Copy to `semanas/NN/slides/index.html` and replace placeholders (NN, TOPIC_TITLE) to start a new week.

## How to Use
1. Copy `templates/week-template.html` to `semanas/NN/slides/index.html`
2. Replace `NN` with the week number (e.g., `01`)
3. Replace `TOPIC_TITLE` with the week's topic from `programa.md`
4. Add slide `<section>` elements following `_config/slide-conventions.md`
```

- [ ] **Step 3: Commit**

```bash
git add shared/
git commit -m "feat: add reveal.js slide template and shared context"
```

---

### Task 5: ICM Root Context Files

**Files:**
- Create: `CLAUDE.md`
- Create: `CONTEXT.md`

- [ ] **Step 1: Create CLAUDE.md**

```markdown
# Intro al Desarrollo de Software Asistido por IA

Presentaciones HTML (reveal.js) para un curso de 8 semanas.

## Folder Map

| Path | Purpose |
|------|---------|
| `programa.md` | Programa oficial del curso (fuente canonica de temas semanales) |
| `_config/` | Tema visual y convenciones de slides (estable, compartido) |
| `_config/slide-conventions.md` | Reglas de formato y estructura de slides |
| `_config/theme/` | CSS del tema (variables.css, custom.css) |
| `shared/templates/` | Template base de reveal.js para todas las semanas |
| `semanas/NN/` | Contenido de cada semana (notas, slides, imagenes) |
| `semanas/NN/CONTEXT.md` | Contrato de la semana: inputs, proceso, outputs |
| `semanas/NN/notas.md` | Borrador/guion de la clase |
| `semanas/NN/slides/` | Presentacion reveal.js generada |
| `semanas/NN/img/` | Imagenes de la semana |
| `docs/` | Documentos de diseno y planes |

## Routing Table

| Task | Read |
|------|------|
| Generate/edit slides for week N | `semanas/NN/CONTEXT.md` |
| Draft/edit lecture notes | `semanas/NN/CONTEXT.md` + `programa.md` |
| Change theme or styling | `_config/theme/` |
| Check slide rules | `_config/slide-conventions.md` |
| Set up a new week | `shared/CONTEXT.md` + `programa.md` |
| Understand weekly topics | `programa.md` (schedule table at bottom) |

## Run

```bash
npm start
```

Then open `http://localhost:3000/semanas/NN/slides/` in a browser.
```

- [ ] **Step 2: Create CONTEXT.md**

```markdown
# Task Routing

## Draft Notes
1. Read `programa.md` — find the row for the target week in the schedule table
2. Use the week's topics as scope for `semanas/NN/notas.md`
3. Write or refine lecture notes in Spanish, technical but accessible

## Generate Slides
1. Read `semanas/NN/CONTEXT.md` for the week's stage contract
2. Read `semanas/NN/notas.md` for content
3. Read `_config/slide-conventions.md` for formatting rules
4. Copy `shared/templates/week-template.html` to `semanas/NN/slides/index.html` if starting fresh
5. Transform notes into reveal.js slides following conventions
6. Place detailed explanations in speaker notes

## Style / Theme Changes
1. Read and modify `_config/theme/variables.css` (colors, fonts, spacing)
2. Read and modify `_config/theme/custom.css` (component styles)
3. Changes apply to all weeks automatically

## New Week Setup
1. Read `shared/CONTEXT.md` for setup instructions
2. Create `semanas/NN/` folder structure (CONTEXT.md, notas.md, slides/, img/)
3. Copy template, populate CONTEXT.md with topics from `programa.md`
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md CONTEXT.md
git commit -m "feat: add ICM root context files (Layer 0 and Layer 1)"
```

---

### Task 6: Scaffold Week Folders (01-08)

**Files:**
- Create: `semanas/01/CONTEXT.md` through `semanas/08/CONTEXT.md`
- Create: `semanas/01/notas.md` through `semanas/08/notas.md` (empty placeholders for 02-08)
- Create: `semanas/01/slides/.gitkeep` through `semanas/08/slides/.gitkeep`
- Create: `semanas/01/img/.gitkeep` through `semanas/08/img/.gitkeep`

- [ ] **Step 1: Create directory structure for all 8 weeks**

```bash
for i in 01 02 03 04 05 06 07 08; do
  mkdir -p semanas/$i/slides semanas/$i/img
  touch semanas/$i/slides/.gitkeep semanas/$i/img/.gitkeep
done
```

- [ ] **Step 2: Create semanas/01/CONTEXT.md**

```markdown
# Semana 1 — Funcionamiento de LLMs

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 1 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives (papers, datasets)
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Introduccion al curso. Funcionamiento de LLMs. Tokens y tokenizacion. Naturaleza estocastica. Pre-training: escala de datos y deduplicacion, infraestructura de computo. Modelos base: autocompletado y cutoff date. Post-training: SFT, datasets conversacionales y de desarrollo de software. El "Yo" como simulacion. Alucinaciones: causas tecnicas y mitigacion (Search-grounding). RLHF. Razonamiento.
```

- [ ] **Step 3: Create semanas/02/CONTEXT.md**

```markdown
# Semana 2 — Arquitectura Frontend y Vibe Coding

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 2 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Arquitectura frontend y Vibe Coding. El trio web: estructura (HTML), estetica (CSS) e interactividad (JS). Teoria UI: layouts, estado, DOM y eventos. Paradigma single-file platform: ventajas para el manejo de contexto en IAs gratuitas. Entorno: instalacion de editor y live server. Practica: Vibe-codeo iterativo de una web app guiando a la IA con vocabulario tecnico.
```

- [ ] **Step 4: Create semanas/03/CONTEXT.md**

```markdown
# Semana 3 — Arquitectura Backend y Datos

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 3 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Arquitectura backend y datos. Teoria backend: cliente-servidor, protocolo HTTP (Verbos/Codigos), Rutas y Controladores. Datos: relaciones vs. documentos (SQL/NoSQL). Flujo y persistencia. Paradigma single-file server: logica y datos en un solo script (Python, FastAPI, SQLite) para contexto de IA. Entorno: Python, venv, FastAPI, Uvicorn. Practica: Vibe-codeo iterativo de una API REST + SQLite y tests de endpoints.
```

- [ ] **Step 5: Create semanas/04/CONTEXT.md**

```markdown
# Semana 4 — Entornos AI-Native e Integracion

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 4 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Entornos AI-Native e integracion. Modelos de desarrollo: programacion en pares (AI pair programming), planificacion exhaustiva (Agentic AI Coding). Entornos AI-Native: diferencias con IAs web (Cursor, Antigravity). Evolucion a multi-archivo y gestion del contexto (.cursorrules, Composer, archivos.md). Integracion sistemica: conexion frontend-backend-BD. Peticiones (Fetch/Axios). Practica: ensamblaje full-stack en Cursor/Antigravity.
```

- [ ] **Step 6: Create semanas/05/CONTEXT.md**

```markdown
# Semana 5 — Proyecto Integrador I: Ideacion e Ingenieria de Prompts

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 5 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Proyecto Integrador I: ideacion e ingenieria de prompts. Pensamiento computacional: descomposicion de problemas en instrucciones atomicas para delegacion efectiva. Estructura del prompt: contexto, instrucciones, ejemplos (few-shot) y restricciones. Arquitectura y entorno: definicion del proyecto final y configuracion de herramientas. Practica: generacion supervisada de codigo boilerplate.
```

- [ ] **Step 7: Create semanas/06/CONTEXT.md**

```markdown
# Semana 6 — Proyecto Integrador II: Refactorizacion y CLI

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 6 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Proyecto Integrador II: refactorizacion y CLI. El ciclo "Prompt-Build-Refactor". La refactorizacion como motor de desarrollo emergente. Depuracion (debugging) dirigida por IA. Navegacion asistida y mitigacion de danos colaterales. Herramientas CLI (Claude Code): ejecucion de IA en terminal para cambios masivos y analisis de errores complejos en todo el proyecto.
```

- [ ] **Step 8: Create semanas/07/CONTEXT.md**

```markdown
# Semana 7 — Calidad, Seguridad y Testing Asistido por IA

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 7 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Calidad, seguridad y testing asistido por IA. Buenas practicas: codigo limpio, mantenible y auto-documentacion. Validacion de resultados: estrategias para verificar la logica del codigo generado. Testing automatizado: generacion de pruebas unitarias via IA. Seguridad: IA como "auditora" (prevencion de inyecciones SQL/fugas de datos).
```

- [ ] **Step 9: Create semanas/08/CONTEXT.md**

```markdown
# Semana 8 — Demo Day: Presentacion Final

## Inputs

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Contenido de la clase |
| `../../programa.md` | Semana 8 row | Alcance y temas de la semana |
| `../../_config/slide-conventions.md` | All | Reglas de formato |
| `../../shared/templates/week-template.html` | All | Template base HTML |

## Process
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes
5. Use vertical slides for deep-dives
6. Reference images from `img/`

## Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Images referenced by slides |

## Topics
Demo Day: presentacion final. Exposicion del MVP funcional. Defensa del proceso: explicacion del ciclo de Vibe Coding, prompts efectivos, gestion de contexto y resolucion de alucinaciones. Apropiacion tecnologica: comprension estructural/logica del codigo para evitar la "caja negra", garantizando mantenimiento y escalabilidad a futuro.
```

- [ ] **Step 10: Create empty notas.md for weeks 02-08**

```bash
for i in 02 03 04 05 06 07 08; do
  touch semanas/$i/notas.md
done
```

- [ ] **Step 11: Commit**

```bash
git add semanas/
git commit -m "feat: scaffold all 8 week folders with ICM stage contracts"
```

---

### Task 7: Migrate Week 1 Notes

**Files:**
- Create: `semanas/01/notas.md`

- [ ] **Step 1: Create semanas/01/notas.md from semana_1.md**

Read `semana_1.md` and extract the text content (without base64 images) into `semanas/01/notas.md`. Keep the structure (headings, paragraphs, links). Replace image references with placeholder comments like `<!-- imagen: description -->`. The original `semana_1.md` stays in the repo root as a reference.

The content should preserve:
- All headings: Pretraining, Tokenizacion, LLM como maquina estocastica, etc.
- All paragraph text and explanations
- All external links (HuggingFace, papers, tools)
- Image locations marked as `<!-- imagen: brief description of what was here -->`

- [ ] **Step 2: Commit**

```bash
git add semanas/01/notas.md
git commit -m "feat: migrate week 1 lecture notes from semana_1.md"
```

---

### Task 8: Week 1 Slides

**Files:**
- Create: `semanas/01/slides/index.html`

- [ ] **Step 1: Copy template to week 1**

```bash
cp shared/templates/week-template.html semanas/01/slides/index.html
```

- [ ] **Step 2: Build week 1 slides from notas.md**

Transform `semanas/01/notas.md` into reveal.js slides in `semanas/01/slides/index.html`. Follow `_config/slide-conventions.md`. The presentation should have these sections (mapped from the notes):

1. **Title slide**: "Semana 1 — Funcionamiento de LLMs"
2. **Pretraining section** (vertical stack):
   - Internet dataset (FineWeb, scale of data)
   - Tokenizacion (UTF-8 to tokens, Tiktokenizer link)
   - LLM como maquina estocastica (transformer visualization, inference)
   - Como la LLM aprende (training process, GPU infrastructure)
   - Limitaciones de modelos pre-entrenados (base models are not assistants)
3. **Post-Training section** (vertical stack):
   - Dataset de preguntas y respuestas (SFT, special tokens)
   - Evolucion a asistente (OpenAssistant, UltraChat, CodeAlpaca)
4. **Alucinaciones section** (vertical stack):
   - Explicacion (confident wrong answers, Orson Kovacs example)
   - Soluciones (Llama 3 approach, search grounding, context as working memory)
   - El "yo" de un modelo (no real self, statistical simulation)
5. **Reinforcement Learning section** (vertical stack):
   - Concept (trial and error, finding best responses)
   - DeepSeek (thinking tokens, eureka moments)
   - AlphaGo (imitation is not enough)
6. **Closing slide**: "Preguntas?"

Each slide should have:
- Clean, minimal content on the slide itself
- Speaker notes with the detailed explanation from `notas.md`
- Links rendered as clickable elements
- Image placeholders as comments where screenshots/diagrams would go

- [ ] **Step 3: Verify slides load correctly**

```bash
npm start
```

Open `http://localhost:3000/semanas/01/slides/` in a browser. Verify:
- Slides render with dark theme
- Navigation works (arrows, spacebar)
- Speaker notes appear (press `S`)
- Code blocks are syntax-highlighted
- Links are clickable

- [ ] **Step 4: Commit**

```bash
git add semanas/01/slides/index.html
git commit -m "feat: add week 1 reveal.js presentation"
```

---

### Task 9: Final Verification + Cleanup Commit

- [ ] **Step 1: Verify full repo structure**

```bash
find . -not -path './node_modules/*' -not -path './.git/*' | sort
```

Expected output should match the file map from the spec.

- [ ] **Step 2: Verify npm start works**

```bash
npm start
```

Navigate to `http://localhost:3000/semanas/01/slides/` — presentation loads and works.

- [ ] **Step 3: Review git log**

```bash
git log --oneline
```

Expected: 7 commits covering each task above.

- [ ] **Step 4: Final commit if any loose files**

```bash
git status
```

If any untracked files remain (docs/, programa.md), add and commit:

```bash
git add programa.md semana_1.md docs/
git commit -m "feat: add course program and design docs"
```
