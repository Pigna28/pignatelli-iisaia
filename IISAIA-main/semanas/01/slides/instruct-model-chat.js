/**
 * Instruct Model Chat Demo
 *
 * Two-panel UI showing a chat interface (left) and the raw text being
 * sent to the model (right). The "raw" panel renders the Llama 3.1
 * chat template explicitly so the audience sees the special tokens
 * (<|begin_of_text|>, <|start_header_id|>, <|eot_id|>, etc.) that
 * post-training added to the vocabulary.
 *
 * Uses /v1/completions with a hand-rendered template (instead of
 * /v1/chat/completions) so we have full control over what's displayed.
 *
 * Usage: initInstructModelChat({ containerId: 'instruct-demo' })
 */

function initInstructModelChat(opts) {
  var containerId = opts.containerId;
  var container = document.getElementById(containerId);
  if (!container) return;

  var modelId = opts.model || 'meta-llama/Llama-3.1-70B-Instruct';

  // State
  var endpointUrl = '';
  var systemPrompt = opts.systemPrompt != null ? opts.systemPrompt : '';
  var turns = []; // { role: 'user'|'assistant', content }
  var streamingAssistant = ''; // current in-progress assistant turn
  var maxTokens = opts.maxTokens != null ? opts.maxTokens : 512;
  var temperature = opts.temperature != null ? opts.temperature : 0.7;
  var showSpecialTokens = true;
  var abortController = null;
  var isGenerating = false;

  function esc(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // ==================== TEMPLATE RENDERING ====================
  // Llama 3.1 chat template. Returns the prompt string sent to the model.
  function renderTemplate(includeAssistantHeader) {
    var s = '<|begin_of_text|>';
    if (systemPrompt) {
      s += '<|start_header_id|>system<|end_header_id|>\n\n' + systemPrompt + '<|eot_id|>';
    }
    for (var i = 0; i < turns.length; i++) {
      var t = turns[i];
      s += '<|start_header_id|>' + t.role + '<|end_header_id|>\n\n' + t.content + '<|eot_id|>';
    }
    if (includeAssistantHeader) {
      s += '<|start_header_id|>assistant<|end_header_id|>\n\n';
    }
    return s;
  }

  // Render the template with HTML formatting for the raw-view panel.
  // - special tokens highlighted (or hidden)
  // - role headers in their accent color
  // - model output (the streaming/finished assistant turn) in --accent
  function renderTemplateHtml() {
    var html = '';
    var special = function(t) {
      if (!showSpecialTokens) return '';
      return '<span style="color: #e8508b;">' + esc(t) + '</span>';
    };
    var role = function(name) {
      var color = name === 'user' ? 'var(--accent-secondary)'
                : name === 'assistant' ? 'var(--accent)'
                : 'var(--text-muted)';
      return '<span style="color: ' + color + ';">' + name + '</span>';
    };

    html += special('<|begin_of_text|>');
    if (systemPrompt) {
      html += special('<|start_header_id|>') + role('system') + special('<|end_header_id|>') + (showSpecialTokens ? '\n\n' : ' ');
      html += '<span style="color: var(--text-muted);">' + esc(systemPrompt) + '</span>';
      html += special('<|eot_id|>');
    }

    for (var i = 0; i < turns.length; i++) {
      var t = turns[i];
      var contentColor = t.role === 'user' ? 'var(--text-primary)' : 'var(--accent)';
      html += special('<|start_header_id|>') + role(t.role) + special('<|end_header_id|>') + (showSpecialTokens ? '\n\n' : ' ');
      html += '<span style="color: ' + contentColor + ';">' + esc(t.content) + '</span>';
      html += special('<|eot_id|>');
    }

    // Streaming assistant turn (mid-generation): no closing eot_id yet
    if (isGenerating) {
      html += special('<|start_header_id|>') + role('assistant') + special('<|end_header_id|>') + (showSpecialTokens ? '\n\n' : ' ');
      html += '<span style="color: var(--accent);">' + esc(streamingAssistant) + '</span>';
      html += '<span style="color: var(--text-muted); animation: blink 1s infinite;">▍</span>';
    }
    return html;
  }

  // ==================== UI RENDER ====================
  function render() {
    var html = '<div style="display: flex; gap: 16px; height: 480px; font-size: 0.55em;">';

    // ----- Left panel: chat -----
    html += '<div style="flex: 1; display: flex; flex-direction: column; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--text-muted); overflow: hidden;">';

    // Header: endpoint URL
    html += '<div style="padding: 8px 12px; border-bottom: 1px solid var(--text-muted); display: flex; gap: 8px; align-items: center;">';
    html += '<input type="text" id="imc-endpoint" placeholder="URL del pod (ej: https://xxx-8000.proxy.runpod.net)" '
      + 'value="' + esc(endpointUrl) + '" '
      + 'style="flex: 1; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 4px; padding: 4px 8px; color: var(--text-primary); font-family: var(--font-mono); font-size: 0.9em;" />';
    var dotColor = endpointUrl ? 'var(--accent)' : 'var(--text-muted)';
    html += '<span style="width: 8px; height: 8px; border-radius: 50%; background: ' + dotColor + '; flex-shrink: 0;" title="' + (endpointUrl ? 'URL configurada' : 'Sin URL') + '"></span>';
    html += '</div>';

    // Optional system prompt input
    html += '<div style="padding: 4px 12px; border-bottom: 1px solid var(--text-muted); display: flex; gap: 8px; align-items: center; font-size: 0.85em;">';
    html += '<span style="color: var(--text-muted); flex-shrink: 0;">system:</span>';
    html += '<input type="text" id="imc-system" placeholder="(opcional) Eres un asistente útil..." '
      + 'value="' + esc(systemPrompt) + '" '
      + 'style="flex: 1; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 4px; padding: 3px 8px; color: var(--text-primary); font-family: var(--font-mono); font-size: 0.95em;" />';
    html += '</div>';

    // Messages
    html += '<div id="imc-messages" style="flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px;">';
    if (turns.length === 0 && !isGenerating) {
      html += '<div style="color: var(--text-muted); text-align: center; margin-top: 40px;">Escribe un mensaje para hablar con el modelo Instruct</div>';
    }
    for (var i = 0; i < turns.length; i++) {
      var msg = turns[i];
      if (msg.role === 'user') {
        html += '<div style="align-self: flex-end; background: var(--accent-secondary); color: var(--bg-primary); border-radius: 12px 12px 2px 12px; padding: 6px 12px; max-width: 80%; word-wrap: break-word;">'
          + esc(msg.content) + '</div>';
      } else {
        html += '<div style="align-self: flex-start; background: var(--bg-code); color: var(--text-primary); border-radius: 12px 12px 12px 2px; padding: 6px 12px; max-width: 85%; word-wrap: break-word; white-space: pre-wrap;">'
          + esc(msg.content) + '</div>';
      }
    }
    if (isGenerating && streamingAssistant) {
      html += '<div style="align-self: flex-start; background: var(--bg-code); color: var(--text-primary); border-radius: 12px 12px 12px 2px; padding: 6px 12px; max-width: 85%; word-wrap: break-word; white-space: pre-wrap;">'
        + esc(streamingAssistant) + '<span style="color: var(--text-muted);">▍</span></div>';
    }
    html += '</div>';

    // Error
    html += '<div id="imc-error" style="display: none; padding: 4px 12px; color: #ff6b6b; font-size: 0.9em;"></div>';

    // Settings row
    html += '<div style="padding: 6px 12px; display: flex; gap: 14px; align-items: center; font-size: 0.85em; color: var(--text-muted); border-top: 1px solid var(--text-muted);">';
    html += '<label style="display: flex; align-items: center; gap: 6px;">max_tokens';
    html += '<input type="number" id="imc-max-tokens" min="1" max="2048" step="1" value="' + maxTokens + '" '
      + 'style="width: 64px; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 3px; padding: 2px 6px; color: var(--text-primary); font-family: var(--font-mono); font-size: 1em;" />';
    html += '</label>';
    html += '<label style="display: flex; align-items: center; gap: 6px;">temperature';
    html += '<input type="number" id="imc-temperature" min="0" max="2" step="0.1" value="' + temperature + '" '
      + 'style="width: 56px; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 3px; padding: 2px 6px; color: var(--text-primary); font-family: var(--font-mono); font-size: 1em;" />';
    html += '</label>';
    html += '</div>';

    // Input
    html += '<div style="padding: 8px 12px; border-top: 1px solid var(--text-muted); display: flex; gap: 8px;">';
    html += '<input type="text" id="imc-input" placeholder="Escribe un mensaje..." '
      + 'style="flex: 1; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 4px; padding: 6px 10px; color: var(--text-primary); font-family: var(--font-body); font-size: 1em;" '
      + (isGenerating ? 'disabled' : '') + ' />';
    if (isGenerating) {
      html += '<button id="imc-stop" style="background: #ff6b6b; color: white; border: none; border-radius: 4px; padding: 6px 14px; cursor: pointer; font-family: var(--font-body); font-weight: bold;">Stop</button>';
    } else {
      html += '<button id="imc-send" style="background: var(--accent-secondary); color: var(--bg-primary); border: none; border-radius: 4px; padding: 6px 14px; cursor: pointer; font-family: var(--font-body); font-weight: bold;">Enviar</button>';
    }
    html += '<button id="imc-reset" style="background: var(--bg-code); color: var(--text-muted); border: 1px solid var(--text-muted); border-radius: 4px; padding: 6px 10px; cursor: pointer; font-family: var(--font-body);" title="Reset">Reset</button>';
    html += '</div>';

    html += '</div>'; // end left panel

    // ----- Right panel: raw template view -----
    html += '<div style="flex: 1; display: flex; flex-direction: column; background: var(--bg-secondary); border-radius: 8px; border: 1px dashed var(--accent); overflow: hidden;">';

    html += '<div style="padding: 8px 12px; border-bottom: 1px solid var(--text-muted); display: flex; justify-content: space-between; align-items: center;">';
    html += '<span style="color: var(--accent); font-weight: bold;">Template de chat aplicado</span>';
    html += '<label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--text-muted); font-size: 0.9em;">';
    html += '<input type="checkbox" id="imc-special-toggle" ' + (showSpecialTokens ? 'checked' : '') + ' style="cursor: pointer;" />';
    html += 'Mostrar tokens especiales';
    html += '</label>';
    html += '</div>';

    html += '<div id="imc-raw" style="flex: 1; overflow-y: auto; padding: 12px; font-family: var(--font-mono); font-size: 0.9em; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">';
    if (turns.length === 0 && !isGenerating) {
      html += '<span style="color: var(--text-muted);">El template de Llama 3.1 va a aparecer aquí cuando envíes el primer mensaje. Cada turno se enmarca con <code>&lt;|start_header_id|&gt;</code> y <code>&lt;|eot_id|&gt;</code>.</span>';
    } else {
      html += renderTemplateHtml();
    }
    html += '</div>';

    // Legend
    html += '<div style="padding: 6px 12px; border-top: 1px solid var(--text-muted); display: flex; gap: 14px; font-size: 0.85em; flex-wrap: wrap;">';
    html += '<span><span style="color: var(--accent-secondary);">user</span> / <span style="color: var(--accent);">assistant</span> / <span style="color: var(--text-muted);">system</span></span>';
    if (showSpecialTokens) {
      html += '<span><span style="color: #e8508b;">&lt;|...|&gt;</span> tokens especiales (post-training)</span>';
    }
    html += '</div>';

    html += '</div>'; // end right panel

    html += '</div>';
    container.innerHTML = html;
    bindEvents();

    var messagesDiv = document.getElementById('imc-messages');
    if (messagesDiv) messagesDiv.scrollTop = messagesDiv.scrollHeight;
    var rawDiv = document.getElementById('imc-raw');
    if (rawDiv) rawDiv.scrollTop = rawDiv.scrollHeight;
  }

  function bindEvents() {
    var endpointInput = document.getElementById('imc-endpoint');
    var systemInput = document.getElementById('imc-system');
    var chatInput = document.getElementById('imc-input');
    var sendBtn = document.getElementById('imc-send');
    var stopBtn = document.getElementById('imc-stop');
    var resetBtn = document.getElementById('imc-reset');
    var specialToggle = document.getElementById('imc-special-toggle');
    var maxTokensInput = document.getElementById('imc-max-tokens');
    var temperatureInput = document.getElementById('imc-temperature');

    if (endpointInput) {
      endpointInput.addEventListener('change', function() {
        endpointUrl = this.value.replace(/\/+$/, '');
        render();
      });
      endpointInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }

    if (systemInput) {
      systemInput.addEventListener('change', function() {
        systemPrompt = this.value;
        render();
      });
      systemInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }

    if (chatInput) {
      chatInput.addEventListener('keydown', function(e) {
        e.stopPropagation();
        if (e.key === 'Enter' && !isGenerating) {
          e.preventDefault();
          sendMessage();
        }
      });
      if (!isGenerating) {
        setTimeout(function() { chatInput.focus(); }, 50);
      }
    }

    if (sendBtn) sendBtn.addEventListener('click', function(e) { e.stopPropagation(); sendMessage(); });
    if (stopBtn) stopBtn.addEventListener('click', function(e) { e.stopPropagation(); stopGeneration(); });
    if (resetBtn) resetBtn.addEventListener('click', function(e) { e.stopPropagation(); resetChat(); });
    if (specialToggle) {
      specialToggle.addEventListener('change', function() {
        showSpecialTokens = this.checked;
        render();
      });
    }

    if (maxTokensInput) {
      maxTokensInput.addEventListener('change', function() {
        var val = parseInt(this.value, 10);
        if (!isNaN(val) && val > 0) maxTokens = val;
      });
      maxTokensInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }

    if (temperatureInput) {
      temperatureInput.addEventListener('change', function() {
        var val = parseFloat(this.value);
        if (!isNaN(val) && val >= 0) temperature = val;
      });
      temperatureInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }
  }

  function showError(msg) {
    var errorDiv = document.getElementById('imc-error');
    if (errorDiv) {
      errorDiv.textContent = msg;
      errorDiv.style.display = 'block';
      setTimeout(function() { if (errorDiv) errorDiv.style.display = 'none'; }, 5000);
    }
  }

  function sendMessage() {
    var input = document.getElementById('imc-input');
    if (!input) return;

    var text = input.value;
    if (!text.trim()) return;
    if (!endpointUrl) {
      showError('No conectado — ingresa la URL del pod');
      return;
    }

    turns.push({ role: 'user', content: text });
    streamingAssistant = '';
    isGenerating = true;
    render();
    generate();
  }

  function generate() {
    var prompt = renderTemplate(true);
    abortController = new AbortController();

    var body = {
      model: modelId,
      prompt: prompt,
      max_tokens: maxTokens,
      temperature: temperature,
      stream: true,
      stop: ['<|eot_id|>', '<|end_of_text|>'],
      skip_special_tokens: true
    };

    fetch(endpointUrl + '/v1/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: abortController.signal
    }).then(function(response) {
      if (response.status === 503) {
        showError('Modelo cargando, intenta en unos minutos');
        finishGeneration(false);
        return;
      }
      if (!response.ok) {
        showError('Error del servidor: ' + response.status);
        finishGeneration(false);
        return;
      }

      var reader = response.body.getReader();
      var decoder = new TextDecoder();
      var buffer = '';

      function readChunk() {
        reader.read().then(function(result) {
          if (result.done) {
            finishGeneration(true);
            return;
          }
          buffer += decoder.decode(result.value, { stream: true });
          var lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line || !line.startsWith('data: ')) continue;
            var data = line.slice(6);
            if (data === '[DONE]') {
              finishGeneration(true);
              return;
            }
            try {
              var parsed = JSON.parse(data);
              var choices = parsed.choices || [];
              if (choices.length > 0) {
                var token = choices[0].text || '';
                if (token) {
                  streamingAssistant += token;
                  updateStreaming();
                }
              }
            } catch (e) { /* skip */ }
          }
          readChunk();
        }).catch(function(err) {
          if (err.name === 'AbortError') return;
          showError('Error de conexión');
          finishGeneration(false);
        });
      }

      readChunk();
    }).catch(function(err) {
      if (err.name === 'AbortError') return;
      showError('Error de conexión');
      finishGeneration(false);
    });
  }

  function updateStreaming() {
    // Update chat bubble in place
    var messagesDiv = document.getElementById('imc-messages');
    if (messagesDiv) {
      var bubbles = messagesDiv.querySelectorAll('div[style]');
      var lastBubble = bubbles[bubbles.length - 1];
      if (lastBubble) {
        lastBubble.textContent = streamingAssistant;
        var cursor = document.createElement('span');
        cursor.style.color = 'var(--text-muted)';
        cursor.textContent = '▍';
        lastBubble.appendChild(cursor);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      } else {
        // No bubble yet — full re-render to add it
        render();
        return;
      }
    }
    // Update raw view
    var rawDiv = document.getElementById('imc-raw');
    if (rawDiv) {
      rawDiv.innerHTML = renderTemplateHtml();
      rawDiv.scrollTop = rawDiv.scrollHeight;
    }
  }

  function finishGeneration(commit) {
    isGenerating = false;
    abortController = null;
    if (commit && streamingAssistant) {
      turns.push({ role: 'assistant', content: streamingAssistant });
    }
    streamingAssistant = '';
    render();
  }

  function stopGeneration() {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
    finishGeneration(true);
  }

  function resetChat() {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
    isGenerating = false;
    turns = [];
    streamingAssistant = '';
    render();
  }

  render();
}
