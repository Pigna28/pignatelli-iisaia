# Slide Generation Workflow — Design

**Date:** 2026-04-28
**Author:** Enzo (with Claude)
**Status:** Approved, ready for implementation plan

## Background

Week 01 of the AI-assisted development course produced a polished reveal.js deck through ~16 commits of section overhauls, redesigns, and animation work. The current `semanas/01/slides/index.html` is the de-facto canonical reference for the course's visual and didactic style.

For weeks 02–08, we want a workflow where:
- Content drops into `semanas/NN/source_material/`
- One conversation produces `semanas/NN/slides/index.html` matching the established style
- Corrections after generation are minimal — most quality comes from the workflow itself, not post-hoc fixes

The week 01 iterations revealed two distinct kinds of work: (a) structure/style decisions that are codifiable as rules, and (b) didactic-spine decisions (through-line, hook, analogy) that require creative judgment per section. The workflow must do both: bake (a) into rules and references, and force (b) into a deliberate brainstorming step before any HTML is generated.

## Goals

- A single command (`/build-class`) inside `semanas/NN/` triggers the full workflow: spine brainstorm → plan → generate → verify.
- A hard checkpoint at `semanas/NN/spine.md` lets the user review and edit the didactic spine before any slide HTML is generated. This is the cheapest place to fix mistakes.
- The full superpowers pipeline (`brainstorming` → `writing-plans` → `executing-plans` → `verification-before-completion` → `finishing-a-development-branch`) is preserved and used. The slide-generation skill *wraps* it; never replaces it.
- Week 01 is refactored into a clean canonical reference: extracted CSS class library, a pattern snippet library, and untouched JS animations. Visual output of week 01 stays byte-identical.
- Week 02 acts as a calibration pass — friction points feed back into the skill before week 03.

## Non-goals

- Replacing or skipping any superpowers skill.
- Extracting animation primitives or building a JS animation framework. Animations stay bespoke per week, with reuse encouraged but not enforced.
- Restructuring week 01's section order, speaker notes, or slide content. Refactor is style-only.
- Auto-generation of spine.md or plan.md without user confirmation.
- Auto-publishing, auto-translation, auto-image-generation.
- Multi-conversation flows. Everything happens in one conversation per week.

## Design overview

### The four-phase workflow

```
[ user ] /build-class                    (in semanas/NN/, content already in source_material/)
   ↓
[ Phase 1: Spine ] slide-generation skill wraps superpowers:brainstorming
   - reads source_material/*.md, programa.md row, _config rules, voice-and-didactics.md
   - asks pedagogy questions: whole-week through-line first (with 2–3 candidate framings),
     then per-section spine in source-material order
   - writes semanas/NN/spine.md
   ↓
[ HARD CHECKPOINT ] user reviews/edits spine.md, types "go" (or similar) to proceed
   ↓
[ Phase 2: Plan ] slide-generation skill wraps superpowers:writing-plans
   - one task per section in spine order + setup task + coherence-pass task
   - written to semanas/NN/plan.md
   ↓
[ Phase 3: Execute ] slide-generation skill wraps superpowers:executing-plans
   - generates section-by-section
   - per-section review checkpoint runs the slide-specific checklist
   ↓
[ Phase 4: Verify + finish ] superpowers:verification-before-completion
                          + superpowers:finishing-a-development-branch
```

Phase 1 → 2 has a hard checkpoint at spine.md. The other transitions flow without prompting unless a review checkpoint catches a problem.

### Why wrap rather than replace superpowers

`superpowers:brainstorming` enforces rigor (clarifying questions one at a time, written design doc, self-review). `writing-plans` produces auditable task lists. `executing-plans` enforces per-task review checkpoints. These behaviors are exactly what produced week 01's quality through manual iteration.

The slide-generation skill aims each phase at the slide-specific shape:
- **Brainstorm phase:** override the design-doc target (`spine.md` not `docs/superpowers/specs/`), use the spine schema, scope the "2–3 approaches" question to whole-week through-line framings only.
- **Plan phase:** override the chunking strategy (one task per section), reference spine entries in each task body.
- **Execute phase:** override the review checklist with slide-specific criteria (no bullet-list slides, voice match, pattern compliance, etc.).
- **Verify/finish phase:** vanilla — open the deck locally, walk through, commit.

## Components

### 1. Slash command

`.claude/commands/build-class.md` — single entry point. One line of body: invoke the slide-generation skill. Discoverable via `/help`. No arguments — the skill infers the week number from the current working directory.

### 2. Slide-generation skill

`tools/skills/slide-generation/SKILL.md` — the wrapping skill. Contains the per-phase scaffolding described above. Lives in `tools/skills/` (matches existing repo convention; gets propagated to `~/.claude/skills/` via the README setup step) so the skill is portable across environments — not Claude-Code-specific config.

The SKILL.md body has a section per phase. Each phase section says: which superpowers skill to invoke, what overrides to apply, what reference files to load, what to do before and after.

### 3. Reference docs (loaded by the skill)

`tools/skills/slide-generation/voice-and-didactics.md`:
- **Voice:** second-person collaborative ("vamos a", "podés", "recordá"), Spanish technical-but-accessible, no AI filler ("revolucionario", "potenciar", "de vanguardia", "seamless", "leverage", "streamline").
- **Didactic principles distilled from week 01:**
  1. **Hook before explanation** — open with a mystery, question, or visual surprise when the section warrants it. Not every section. Never start with a definition.
  2. **Why before what** — motivate the filter before showing the filter; motivate the algorithm before naming it.
  3. **Layer-by-layer concept building** — each slide assumes only what came before.
  4. **Concrete numbers over abstractions** — "15 trillion tokens" not "a lot of data".
  5. **Analogies bridge to the familiar** — book pages = learning modes; spiders = web crawl. Use one when it earns its keep; skip when the topic is already concrete.
  6. **No bullet-list slides** — visual structure (comparison, flow, pattern) over reveals on bullets.
  7. **Live demo > prose explanation** when the concept is observable.
- **Anti-patterns to refuse:** bullet-list slides, emojis, AI-sounding filler, placeholder text, em-dash overuse, gratuitous gradients, glassmorphism.

`tools/skills/slide-generation/spine-template.md`:

```markdown
# Spine — Semana NN: <Topic>

**Whole-week through-line:** One paragraph. The single arc connecting all sections.

## Section N: <Title>
**Source material:** `source_material/NN-...md`
**Through-line:** (always) one sentence.
**Hook:** (optional, only when it serves the section)
**Key analogy:** (optional, only when one fits naturally)
**What students walk away knowing:** 1–3 bullets.
**Animations / interactive:** None | bespoke (describe) | reuse-existing (which from week 01).
**Slide budget:** rough count.
```

`tools/skills/slide-generation/animation-pattern.md`:
- The contract: each animation is its own `.js` file, exports `init{Name}({ containerId, ...opts })`, listens to `Reveal.on('slidechanged' / 'fragmentshown' / 'fragmenthidden')`, manipulates DOM directly. No framework.
- HTML wiring snippet:
  ```html
  <div id="x"></div>
  <script src="x.js"></script>
  <script>initX({ containerId: 'x' });</script>
  ```
- Catalogue of week 01 animations:
  - `tokenizer-anim` — generalizable to any "watch the data transform step by step" pattern.
  - `clickable-steps` — generalizable to any "multi-step explainer with detail-on-click" pattern.
  - `inference-anim` — generalizable to any "token-by-token generation" or "stochastic process simulation".
  - `training-anim` — content-specific (training loss curve), but the "live chart updates over time" pattern is reusable.
  - `base-model-chat`, `instruct-model-chat` — content-specific. Don't reuse.
  - `sft-anim`, `rl-anim`, `deepseek-anim` — content-specific. Don't reuse.
- **Default policy:** reuse a week 01 animation if it fits the spine; build a new animation only if the spine specifies a genuinely different visualization need.

### 4. CSS class library

`_config/theme/components.css` — extracted from the inline `<style>` block at the top of `semanas/01/slides/index.html` plus recurring inline `style="..."` patterns.

Classes to include (non-exhaustive — extracted during refactor):
- Existing inline-style classes: `.pipeline-box`, `.pipeline-arrow`, `.flow-step`, `.flow-arrow`, `.rl-attempt` (with `.correct`, `.wrong`), `.stage-box` (with `.highlight`), `.chat-mockup` and children, `.pipe-grid` and children, `.html-noise`.
- New classes extracted from recurring inline styles: `.comparison-2col`, `.code-block`, `.bg-secondary-card`, etc.

The component CSS is a sibling of `_config/theme/custom.css` and `variables.css`. Templates and slides import all three.

### 5. Pattern snippet library

`shared/patterns/` — one HTML snippet per recurring slide pattern. Each snippet is a bare-bones `<section>` using `components.css` classes, with placeholder content and a leading HTML comment explaining when to use it and pointing to the canonical week 01 example.

Patterns (initial set, extracted from week 01):
- `title-slide.html` — week opener
- `section-divider.html` — major topic transition
- `comparison-2col.html` — contrasting two concepts
- `pipeline-roadmap.html` — multi-stage process diagram, supports re-highlighting
- `flow-with-arrows.html` — sequential process
- `code-walkthrough.html` — code block with optional line highlighting
- `chat-mockup.html` — chat UI mockup with typing animation
- `clickable-steps.html` — multi-step explainer with click-to-reveal detail
- `data-table.html` — numerical comparison table
- `metaphor-pages.html` — concrete-domain metaphor (e.g., book pages for learning modes)

`shared/patterns/README.md` — index table mapping pattern → when to use → snippet file → canonical week 01 example (with line number).

### 6. Week 01 refactor

Scope (medium per Q4 of brainstorm):
- Move inline `<style>` from `slides/index.html` (~lines 1–250) to `_config/theme/components.css`.
- Replace recurring inline `style="..."` patterns with class equivalents.
- Extract pattern snippets from week 01 slides into `shared/patterns/<name>.html` with placeholder content.

NOT in scope:
- JS animations (untouched).
- Section order, speaker notes, content (untouched).
- Animation primitives extraction.

Verification: open the deck before and after; walk through every slide; visual output should be byte-identical (or as close as practical).

## File layout summary

**Created:**
```
tools/skills/slide-generation/
├── SKILL.md
├── voice-and-didactics.md
├── spine-template.md
└── animation-pattern.md

.claude/commands/
└── build-class.md

_config/theme/
└── components.css

shared/patterns/
├── README.md
├── title-slide.html
├── section-divider.html
├── comparison-2col.html
├── pipeline-roadmap.html
├── flow-with-arrows.html
├── code-walkthrough.html
├── chat-mockup.html
├── clickable-steps.html
├── data-table.html
└── metaphor-pages.html
```

**Modified:**
```
semanas/01/slides/index.html        # inline <style> + recurring style="..." → class attributes
shared/templates/week-template.html # imports components.css
shared/CONTEXT.md                   # /build-class flow replaces "copy template" instructions
_config/slide-conventions.md        # adds links to voice-and-didactics, pattern catalogue, animation pattern
```

**Created per future week (during workflow execution):**
```
semanas/NN/spine.md
semanas/NN/plan.md
semanas/NN/slides/index.html
```

## The per-section review checklist

The lever for "minimum corrections". Phase 3's per-section review checkpoint runs:

- [ ] No bullet-list slides — every slide has visual structure (comparison / flow / pattern from `shared/patterns/`).
- [ ] Voice matches `voice-and-didactics.md` — second-person collaborative, no AI filler.
- [ ] One concept per slide.
- [ ] No emojis.
- [ ] Speaker notes present, ~80–200 words each.
- [ ] Section opens with hook from spine if spine specifies one.
- [ ] Key analogy from spine appears as a slide if spine specifies one.
- [ ] All "what students walk away knowing" bullets are addressed somewhere in the section.
- [ ] Patterns used are from `shared/patterns/`, OR a new pattern is introduced *and* documented in the catalogue if genuinely needed.
- [ ] Inline `style="..."` is minimized — uses `components.css` classes where one exists.
- [ ] Animations follow the `init{Name}({ containerId })` contract from `animation-pattern.md`.

After the checklist passes, the section's slides are shown to the user; user can request changes before approving and moving to the next section.

## Risks and mitigations

1. **Pattern over-fitting.** The pattern catalogue is extracted from one week. Future weeks may need patterns that don't exist yet. *Mitigation:* the skill's policy explicitly allows new patterns, but they must be added to `shared/patterns/` *and* the catalogue table during Phase 3, not silently inlined. Catalogue grows instead of fragmenting.

2. **Spine schema mismatch on different content shapes.** Week 01 source material was a Karpathy transcript split into 9 prose chapters. Future weeks may have bullet outlines, slide drafts, hand-written notes, code-heavy examples. *Mitigation:* the spine schema is content-agnostic. The skill reads whatever's in `source_material/` without assuming a specific shape.

3. **The "minimum corrections" claim is unverified.** We won't know whether the workflow achieves it until week 02 runs. *Mitigation:* week 02 is a calibration pass. Capture friction points and update the skill before week 03.

4. **Spine-to-slides drift on long generation.** With ~40 slides per deck and large output, Claude may lose track of the spine partway through Phase 3. *Mitigation:* the per-section review checkpoint forces re-grounding at every section boundary. If drift still occurs, add an explicit "re-read spine.md at the start of each section task" instruction to the skill.

## Open questions deliberately punted

- Whether Phase 3 should orchestrate parallel subagents (one per section) for speed, vs. sequential generation. Default: sequential. Revisit if generation is too slow in week 02.
- Whether spine.md should track a "revision history" or just be overwritten on each `/build-class` run. Default: overwrite — git provides history.

## Calibration plan

After week 02 runs through the workflow:
1. Note where the spine schema didn't fit the section's needs.
2. Note where the per-section review checklist missed problems that required hand-fixing.
3. Note where the pattern catalogue lacked a needed pattern.
4. Update the skill, voice-and-didactics, spine-template, and pattern catalogue accordingly before week 03.
