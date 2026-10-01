# Semana 2 — Source material design

**Date:** 2026-05-02
**Author:** Enzo Pacilio (with brainstorming assist)
**Course:** Introducción a la ingeniería de software asistida por IA
**Week topic:** Arquitectura frontend y Vibe Coding

## Goal

Populate `semanas/02/source_material/` with content that `/build-class` can transform into a reveal.js presentation, plus a teaching-artifact HTML demo that anchors the lecture and serves as a take-home reference for students.

## Context

- **Audience:** ~25 students, mixed frontend skill (none → good).
- **Class duration:** 3 hours (180 min) on Google Meet, with breakout rooms for the activity.
- **Constraint:** ~30 min must be reserved for finishing semana 1's slides at the start.
- **Course thesis (from programa):** the student is "supervisor arquitectónico" — they direct AI, they don't write syntax.
- **Course evaluation modality:** TPs delivered as GitHub repos with README documenting the iterative Vibe Coding process.

## Non-goals

- Teaching students to hand-write HTML/CSS/JS production-ready. They're learning vocabulary to direct an LLM, not becoming frontend devs.
- Covering responsive design, accessibility deep-dives, animation, or advanced CSS topics. Strictly out of scope for week 2.
- Building a multi-file project scaffold. The single-file paradigm is core curriculum, not a limitation to apologize for.

## Framing

**Vocabulary-first.** The 60 min of new theory teaches students the *names* of frontend primitives so they can specify UI work to a web LLM with precision. Hands-on coding is minimal; reflection on prompting is heavy.

## Class structure (180 min total)

| Block | Time | What happens |
|-------|------|--------------|
| Carryover from semana 1 | 30 | Finish remaining LLM-fundamentals slides |
| Lead-in: why frontend literacy still matters | 7 | Supervisor framing applied to UI work. *"You don't need to write CSS. You need to know what to ask for."* |
| Anatomy walkthrough of the demo HTML | 25 | Five stops in the demo file: HTML semantics → CSS layout → JS state/events → DOM → single-file packaging. Live edits (change a CSS variable, toggle a class) so students see cause-and-effect. |
| Prompt patterns for UI | 20 | 4 reusable prompt templates. One live demo: take a request, prompt iteratively in ChatGPT Canvas, watch the artifact evolve. |
| Activity briefing | 8 | Cycle of AI-assisted UI dev (Architect once, then Prompter → Reviewer → Tester loop). Examples gallery. Constraints. Submission format. |
| Activity in breakout rooms | 60 | 6 random groups (5 of 4, 1 of 5) build their thing. Enzo circulates. |
| Group presentations | 30 | 6 groups × 5 min, Meet timer enforced. Content ungated — groups choose what to present. |

## Source material file list

Located at `semanas/02/source_material/`. Word-count target ~600–900 per markdown unless noted.

| File | Purpose | Class block |
|------|---------|-------------|
| `00-index.md` | Reading order + one-paragraph summary of each file. Short. | (meta) |
| `01-frontend-y-el-supervisor.md` | Why frontend literacy matters even when the LLM writes the code. The five-part anatomy preview (HTML / CSS / JS / state / packaging). | Lead-in |
| `02-estructura-html.md` | Semantic HTML as nouns. Document outline. The ~12 tags that matter. Structure before styling. | Anatomy walkthrough |
| `03-estilo-css.md` | Box model. Flexbox + grid as the two layout primitives. Type + color as the two aesthetic primitives. CSS variables as the LLM-friendly tuning surface. | Anatomy walkthrough |
| `04-estado-y-comportamiento.md` | The three-way relationship: state (data) → DOM (what's on screen) → events (what the user does). Why "state" is the word that unlocks better prompts. | Anatomy walkthrough |
| `05-single-file-platform.md` | Why one HTML file beats a project scaffold for web LLMs: context window, copy-paste deployment, no toolchain. When the paradigm breaks. | Anatomy walkthrough |
| `06-patrones-de-prompt-ui.md` | 4 reusable prompt templates: *describe-the-artifact*, *iterate-on-state*, *fix-the-layout*, *theme-and-polish*. Live-demo script. | Prompt patterns |
| `07-actividad-grupal.md` | Cycle of AI-assisted UI dev. Examples gallery. Constraints. Submission spec. | Activity briefing |
| `demo.html` | The "Frontend Showroom" teaching artifact (single file). | Anatomy walkthrough — the prop |

All copy in Spanish (matches course language).

## Demo HTML — "The Frontend Showroom"

A single HTML file that is both a styled frontend-concepts reference and a working artifact demonstrating every concept it teaches. The medium is the message.

### Sections (top to bottom)

1. **Hero** — *"Conceptos del Frontend — explorá una página que se enseña a sí misma"*
2. **§ Estructura (HTML semántico)** — a styled article rendered with semantic tags; toggle button swaps to "div soup" so students see the difference visually + in source.
3. **§ Estilo (CSS layout + variables)** — a flex/grid playground with buttons that change `justify-content`, `gap`, `grid-template-columns`. A theme switcher (light/dark/accent) driven by CSS variables.
4. **§ Estado y comportamiento** — three small demos: a counter, a tiny todo list, an event log that prints every click. Each demo shows state → DOM → events.
5. **§ El DOM** — a live DOM-tree visualization that mirrors the page; clicking a node highlights it on screen.
6. **§ Single-file** — a meta section with a "Ver código fuente" button that pops the page's own source in a modal.

### Constraints

- One HTML file. No external CSS, no external JS, no CDN dependencies (or one CDN max if absolutely required for the DOM-tree visualization).
- Uses semantic HTML throughout (so the lecture can point at it).
- Uses CSS variables for theming (so a live edit during lecture changes the look immediately).
- Visually pleasant — students should want to remix it. Not "school-y."

### Why this artifact

- Each section maps cleanly to one stop in the anatomy walkthrough.
- Mixed-level audience: beginners see a working artifact they can imitate; advanced students get a refresher with concepts named explicitly.
- Take-home reference: students can revisit it after class.

## Activity spec (`07-actividad-grupal.md` content outline)

### 1. Why this activity (1 paragraph)

Practicing how to coordinate the cycle of AI-assisted UI development under real time pressure. Distributing the cycle's stages within a group is part of the lesson.

### 2. The cycle of AI-assisted UI development

Framed as sequence + loop, not parallel roles:

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

- **Architect** — once at the start, decomposes the artifact into a spec the LLM can implement; writes the first prompt. Re-enters when the group decides to change scope.
- **Prompter** — drives the chat. Stays focused on one thing per prompt.
- **Reviewer** — reads every output. Flags hallucinated APIs, subtle logic bugs, mismatches with the spec.
- **Tester** — runs the artifact in a browser tab. Breaks it on purpose. Reports findings back to Prompter.

Groups decide how to distribute these — same person rotating through, or different people on different stages. The lesson is the cycle, not the role assignment.

### 3. Examples gallery (pick freely or invent your own)

- Landing page for a fictional product (fan page, fake startup, parody site)
- Single-purpose tool (markdown editor, color picker, Pomodoro, password generator)
- Mini-game (dice roller, memory match, idle clicker, typing test)
- Off-the-wall: any creative artifact that fits in one HTML file

### 4. Constraints

- Single HTML file (no build tools, no separate CSS/JS files)
- One **ChatGPT Canvas** chat session per group
- 60 min build window
- Submission: GitHub repo containing `index.html`, `prompts.md`, `README.md`

### 5. Submission

- `index.html` — the working artifact
- `prompts.md` — the sequence of prompts used, in order, with a brief annotation per prompt describing what it was trying to do
- `README.md` — short description of what the page is, who built it, what worked / what didn't

### 6. Presentation format

- 5 min per group, tracked by Meet timer
- Content ungated — groups choose what to show

## Group composition

- 6 random groups (five of 4 students, one of 5).
- Random assignment (no level balancing).

## Open implementation questions (deferred to writing-plans)

- Whether to provide a small starter prompt in `prompts.md` template or leave it blank.
- Whether `demo.html` includes a CDN dependency (e.g., a tiny tree-view library) or implements the DOM-tree visualization from scratch.
- Exact wording of the four prompt patterns in `06-patrones-de-prompt-ui.md`.

## Success criteria

- All 8 markdown files + `demo.html` exist in `semanas/02/source_material/`.
- `demo.html` runs standalone in a browser and demonstrates every concept the markdowns describe.
- `/build-class` can transform the source material into a coherent slide deck without manual gap-filling.
- Class fits in 180 min including the 30-min carryover.
