# RunPod Base Model Demo — Design Spec

## Purpose

Live class demo for Semana 01 that shows:
1. The compute required to run inference on a 405B parameter LLM (via RunPod dashboard)
2. How a base (non-instruct) model behaves — it autocompletes text, it doesn't "chat"
3. The illusion of conversation vs the reality of text continuation

## Components

### 1. Python Script — `tools/runpod-llama.py`

CLI tool to manage a RunPod pod running vLLM with Llama 3.1 405B base.

**Commands:**

- `python tools/runpod-llama.py start` — Creates pod, polls until RUNNING, prints endpoint URL. Saves pod ID to `.runpod-pod`.
- `python tools/runpod-llama.py status` — Checks pod state and whether vLLM is ready (hits `/v1/models`).
- `python tools/runpod-llama.py stop` — Terminates the pod.

**Pod configuration:**

| Setting | Value |
|---------|-------|
| GPU | 8x H100 80GB SXM |
| Image | `vllm/vllm-openai:latest` |
| Model | `meta-llama/Llama-3.1-405B` |
| Tensor parallelism | 8 |
| Dtype | fp8 |
| Exposed port | 8000 |
| CORS | `--allowed-origins "*"` |

**API key:** Read from `RUNPOD_API_KEY` environment variable.

**Dependencies:** `requests` (already in tools venv).

**RunPod API calls used:**

- `POST https://api.runpod.io/graphql` — create pod, get pod status, stop pod
- RunPod uses a GraphQL API for pod management

### 2. Chat UI — `semanas/01/slides/base-model-chat.js`

Vanilla JS module loaded by the slides. Builds its UI inside a container div on a dedicated slide.

**Layout: two panels side by side.**

**Left panel — "Chat":**

- Endpoint URL input at the top
- Chat message list (user messages right-aligned, model responses left-aligned)
- Text input + Send button at the bottom
- Stop button (visible during generation)
- Reset button

**Right panel — "Lo que realmente pasa":**

- Shows the raw text string being sent as the prompt
- User text and model completions in different colors
- As the conversation grows, the full concatenated string grows — making it visually obvious there are no "turns," just one long string
- Toggle checkbox: "Mostrar tokens especiales" — when on, `skip_special_tokens: false` in the API call, and BOS/EOS tokens are visible in the raw view
- The raw view auto-scrolls to bottom as tokens stream in

**API interaction:**

- Endpoint: `{podUrl}/v1/completions` (NOT chat/completions — base model)
- Method: POST with `stream: true`
- Parameters:
  - `prompt`: full concatenated conversation text
  - `max_tokens`: 256
  - `temperature`: 0.7
  - `skip_special_tokens`: controlled by toggle
  - `stream`: true
- Streaming via fetch + ReadableStream (SSE parsing)

**Stop behavior:** Aborts the fetch, keeps whatever tokens were received so far.

**Reset:** Clears both panels and the internal prompt string. Keeps the endpoint URL.

**Error states:**
- Empty/invalid URL: "No conectado — ingresa la URL del pod"
- 503 from vLLM: "Modelo cargando, intenta en unos minutos"
- Network error: "Error de conexion"

### 3. Slide Integration — `semanas/01/slides/index.html`

- New slide in the base models section with a container div
- `<script src="base-model-chat.js"></script>` at the bottom with the other animation scripts
- The slide is a full-width layout (no title eating vertical space — the panels are self-explanatory)

### 4. Config Files

- `.env.example`: add `RUNPOD_API_KEY=`
- `.gitignore`: add `.runpod-pod` and `.env`

## File Changes

| File | Type | Description |
|------|------|-------------|
| `tools/runpod-llama.py` | New | Pod management CLI |
| `semanas/01/slides/base-model-chat.js` | New | Chat UI + raw view |
| `semanas/01/slides/index.html` | Edit | Add demo slide + script tag |
| `.env.example` | New | Document required env vars |
| `.gitignore` | Edit | Add `.runpod-pod`, `.env` |

## Class Flow

1. During 15-min recess: `python tools/runpod-llama.py start`
2. Script prints endpoint URL and polls until ready
3. When covering compute section: open RunPod dashboard, show the 8x H100 pod
4. Navigate to the demo slide, paste the endpoint URL
5. Send prompts, show how the base model just autocompletes
6. Toggle special tokens to show BOS/EOS
7. After class: `python tools/runpod-llama.py stop`

## What This Does NOT Include

- No local proxy server
- No pre-baked prompts (all live)
- No instruct model comparison (out of scope)
- No persistent storage of conversations
