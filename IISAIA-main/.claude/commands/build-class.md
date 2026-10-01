---
description: Generate or refine the reveal.js deck for the current semana, using source_material/ as input. Triggers the slide-generation skill which wraps the full superpowers pipeline (brainstorming → writing-plans → executing-plans → verification → finishing-branch). Hard checkpoint at semanas/NN/spine.md before any HTML is generated.
---

The user wants to build slides for the current week. The current working directory should be `semanas/NN/` for some N.

Invoke the `slide-generation` skill via the Skill tool. The skill handles everything from spine brainstorm to final commit.

If the current directory is not `semanas/NN/`, ask the user which week they're targeting and `cd` there (or have them) before proceeding.
