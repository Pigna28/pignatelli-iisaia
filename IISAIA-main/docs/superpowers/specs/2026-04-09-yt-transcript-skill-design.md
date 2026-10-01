# YouTube Transcript Extraction Skill

## Overview

A Claude Code skill that takes a YouTube video URL, extracts its full transcript, and transforms it into a set of topic-organized markdown files. The content preserves the speaker's original vocabulary, syntax, and perspective as closely as possible.

## Components

### 1. Python Script (existing: `tools/yt-transcript.py`)

Already built. Fetches the full transcript from YouTube and writes it to a file. Invoked with `--timestamps` so Claude has temporal context for topic boundary detection.

```bash
python tools/yt-transcript.py <url> --timestamps -o <output_dir>/transcript.txt
```

No modifications needed to the existing script.

### 2. Claude Skill (`~/.claude/skills/yt-transcript-to-md/SKILL.md`)

A skill file that instructs Claude on the full workflow when triggered.

## Skill Workflow

### Step 1: Gather Inputs

When triggered, the skill:
1. Takes the YouTube URL from the user's message
2. Asks the user for the output directory

### Step 2: Fetch Transcript

Run the Python script:
```bash
source tools/.venv/Scripts/activate && python tools/yt-transcript.py <url> --timestamps -o <output_dir>/transcript.txt
```

If the script fails (no transcript available, invalid URL), report the error and stop.

### Step 3: Process Transcript

Claude reads the transcript file in slices of ~500 lines using the Read tool (`offset`/`limit` parameters).

For each slice:
1. Read the slice
2. Identify if a new topic begins within the slice (based on subject matter shifts)
3. Accumulate content into the current topic buffer
4. When a topic boundary is found: finalize the previous topic's `.md` file, start a new buffer

Across slices, Claude maintains a running state:
- Current topic title (working name, may be refined when the topic ends)
- List of completed topics (title, filename, key terms)
- Whether the current slice ends mid-topic

### Step 4: Write Topic Files

Each topic is written to its own file as soon as its boundary is finalized.

**Filename format:** `NN-topic-slug.md` (zero-padded sequential number + kebab-case title)

**File structure:**
```markdown
# Topic Title

[Content paragraphs using the speaker's original words,
cleaned of filler but preserving vocabulary and syntax.
Organized into logical paragraphs for readability.]
```

No frontmatter, no metadata, no summaries. Just a title and the content.

**Content rules:**
- Preserve the speaker's original vocabulary, phrasing, and way of explaining
- Remove filler (um, uh, false starts, stutters)
- Remove pure repetition (where the speaker restates the exact same thing)
- Reorganize into readable paragraphs — not a wall of text, not bullet points
- Keep the original language of the video
- Do NOT summarize, paraphrase, or add interpretation

### Step 5: Write Index File

After all slices are processed, write `index.md` in the output directory:

```markdown
# [Video Title]

Source: [YouTube URL]
Language: [detected language]
Duration: [approx from last timestamp]
Topics: [N files]

## Contents

| # | Topic | Key Terms | File |
|---|-------|-----------|------|
| 1 | Topic title | term1, term2, term3 | [01-topic-slug.md](01-topic-slug.md) |
| 2 | ... | ... | ... |
```

Each row contains:
- Sequential number
- Topic title
- 3-7 key terms/concepts from that section
- Relative link to the file

## Edge Cases

- **Very long videos (3h+):** Handled naturally by iterating more 500-line slices.
- **No transcript available:** Report error and stop.
- **Ambiguous topic boundaries:** Err toward fewer, larger topics over many tiny ones.
- **Speaker revisits a topic:** Treat as a new topic file. Do not merge non-contiguous segments.
- **Non-Spanish/English videos:** Works with any language YouTube provides. Content stays in the original language.

## Output Example

For a video about machine learning basics:

```
output_dir/
  transcript.txt          # raw transcript (kept for reference)
  index.md                # navigation + key terms table
  01-que-es-ml.md         # first topic
  02-tipos-aprendizaje.md # second topic
  03-redes-neuronales.md  # third topic
  ...
```

## Token Consumption

Claude reads the full transcript exactly once (in 500-line slices via the Read tool). Output is the topic files + index. For a 3-hour video (~5000 lines of transcript), expect ~5000 lines of input reading + output writing across ~10 iterations. This is the minimum possible for full-fidelity content preservation since every word must pass through Claude.
