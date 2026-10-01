# Course Presentations Platform — Design Spec

## Overview

Replace PowerPoint presentations with HTML/CSS/JS slides for an 8-week course on "Introduction to AI-Assisted Software Development". The repo is organized using the Interpreted Context Methodology (ICM) for optimal Claude Code synergy.

## Repo Structure

```
intro_desarrollo_asistido_IA/
  CLAUDE.md                         # Layer 0: project map + routing table
  CONTEXT.md                        # Layer 1: task routing
  programa.md                       # Course program (canonical source for weekly topics)

  _config/                          # Layer 3: shared stable config
    slide-conventions.md            # Rules for slide structure, tone, formatting
    theme/
      custom.css                    # Reveal.js theme overrides
      variables.css                 # Color palette, fonts, spacing

  shared/
    templates/
      week-template.html            # Base reveal.js template for all weeks
    CONTEXT.md                      # Describes shared resources and how to use them

  semanas/
    01/
      CONTEXT.md                    # Layer 2: stage contract (Inputs, Process, Outputs)
      notas.md                      # Lecture draft / notes
      slides/
        index.html                  # Generated reveal.js presentation
      img/                          # Images for this week's slides
    02/ through 08/                 # Same structure per week

  docs/                             # Design docs (this file lives here)
  node_modules/                     # (gitignored)
  package.json                      # reveal.js dependency + start script
  .gitignore
```

## ICM Context Layers

### Layer 0 — `CLAUDE.md` (root, auto-loaded)

Project description, folder map, and routing table:

| Keyword | Route |
|---------|-------|
| "slides", "generate slides", "new slides" | `semanas/NN/CONTEXT.md` |
| "notes", "lecture notes", "notas" | `semanas/NN/CONTEXT.md` + `programa.md` |
| "theme", "styling", "CSS" | `_config/theme/` |
| "template" | `shared/templates/week-template.html` |
| "conventions" | `_config/slide-conventions.md` |
| "program", "weekly topics" | `programa.md` |

Target: under 80 lines, ~800 tokens.

### Layer 1 — `CONTEXT.md` (root)

Task routing with process descriptions:

- **Draft notes**: Read `programa.md` (week's row from schedule) for scope, produce/refine `semanas/NN/notas.md`
- **Generate slides**: Read `semanas/NN/notas.md` + `_config/slide-conventions.md` + `shared/templates/week-template.html`, produce `semanas/NN/slides/index.html`
- **Style/theme changes**: Read and modify `_config/theme/*.css`, changes apply globally
- **New week setup**: Create folder from template, populate `CONTEXT.md` with week's topic from `programa.md`

### Layer 2 — `semanas/NN/CONTEXT.md` (per week)

Stage contract with three sections:

**Inputs:**

| Source | Sections | Purpose |
|--------|----------|---------|
| `notas.md` | All | Lecture content to transform into slides |
| `programa.md` | Week N row from schedule table | Scope and themes for this week |
| `_config/slide-conventions.md` | All | Formatting and structure rules |
| `shared/templates/week-template.html` | All | Base HTML template |

**Process:**
1. Read `notas.md` and identify logical sections
2. Map sections to slides (one concept per slide, split dense content)
3. Generate `slides/index.html` following conventions and template
4. Place detailed explanations in speaker notes (`<aside class="notes">`)
5. Use vertical slide stacks for deep-dives within a topic
6. Add code examples with syntax highlighting where relevant
7. Reference images from `img/` (extract or create as needed)

**Outputs:**

| Artifact | Location | Description |
|----------|----------|-------------|
| Presentation | `slides/index.html` | Reveal.js slide deck |
| Images | `img/` | Any images referenced by slides |

### Layer 3 — `_config/slide-conventions.md`

Stable rules that apply to all weeks:

- **Language**: Spanish, technical but accessible for diploma-level students
- **Slide density**: One main concept per slide. If it needs scrolling, split it.
- **Headings**: Short, descriptive. No filler text.
- **Code blocks**: Use reveal.js highlight plugin with language annotation and line numbers when relevant
- **Links**: Render as clickable elements on the slide with descriptive text
- **Images**: Referenced from `img/`, sized responsively, with alt text
- **Speaker notes**: Contain the detailed explanation from the lecture draft. This is what the professor reads/says aloud — the slide itself shows only the key visual/concept.
- **Fragments**: Use `class="fragment"` for progressive reveals when building up a concept step by step
- **Vertical slides**: Use nested `<section>` for optional deep-dives (e.g., showing a paper's details)
- **No emojis in slides**
- **No gratuitous animations or transitions** — simple fade or none

## Reveal.js Setup

### Dependencies

`package.json` with:
- `reveal.js` as the sole dependency
- `npm start` script: runs `npx serve .` from repo root (zero-config static file server, included as a dev dependency)
- `serve` as a dev dependency

No build tools, no bundler. Edit HTML/CSS, refresh browser.

### Template (`shared/templates/week-template.html`)

- Loads reveal.js from `node_modules`
- Loads plugins: highlight (code), notes (speaker view), markdown (optional)
- Links to `_config/theme/custom.css`
- Structure: title slide placeholder, content section placeholders, closing slide
- Relative paths assume serving from repo root

### Theme (`_config/theme/`)

- `variables.css`: CSS custom properties for colors, fonts, spacing
- `custom.css`: Overrides on reveal.js dark theme base
- Dark background, light text, monospace accents for code
- Clean typography, consistent spacing scale
- Styled code blocks, link colors, image containers

## Weekly Workflow

1. **Draft notes**: Drop/write `notas.md` in `semanas/NN/` (or ask Claude Code to draft from `programa.md`)
2. **Generate slides**: Ask Claude Code "generate slides for week N"
3. **Serve locally**: `npm start`, open browser
4. **Iterate**: Request changes — split slides, add examples, adjust speaker notes
5. **Commit**: After each working state

## Git Strategy

- Initialize git repo
- `.gitignore`: `node_modules/`
- All content tracked: `.md`, `.html`, `.css`, images
- Feature branches per the user's global CLAUDE.md rules
- Commit after each working change

## What This Design Does NOT Include

- No CI/CD or deployment (local only for now)
- No PDF export setup (reveal.js supports it, can add later)
- No auto-generation pipeline (Claude Code is the "pipeline", invoked manually)
- No week content beyond week 1 (scaffolded as empty folders)
