/**
 * Base Model Chat Demo
 *
 * Two-panel UI showing a chat interface (left) and the raw text
 * being sent to the model (right). Demonstrates that a base LLM
 * is just autocompleting a text string, not "chatting."
 *
 * Usage: initBaseModelChat({ containerId: 'base-model-demo' })
 */

function initBaseModelChat(opts) {
  var containerId = opts.containerId;
  var container = document.getElementById(containerId);
  if (!container) return;

  var modelId = opts.model || 'meta-llama/Llama-3.1-70B';

  // State
  var endpointUrl = '';
  var maxTokens = opts.maxTokens != null ? opts.maxTokens : 256;
  var temperature = opts.temperature != null ? opts.temperature : 0.7;
  var rawSegments = []; // { text, type: 'user'|'model'|'special' }
  var chatMessages = []; // { text, role: 'user'|'model' }
  var showSpecialTokens = false;
  var abortController = null;
  var isGenerating = false;

  function esc(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function buildFullPrompt() {
    var prompt = '';
    for (var i = 0; i < rawSegments.length; i++) {
      if (rawSegments[i].type !== 'special') {
        prompt += rawSegments[i].text;
      }
    }
    return prompt;
  }

  function render() {
    var html = '<div style="display: flex; gap: 16px; height: 480px; font-size: 0.55em;">';

    // Left panel: Chat
    html += '<div style="flex: 1; display: flex; flex-direction: column; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--text-muted); overflow: hidden;">';

    // Header with endpoint URL
    html += '<div style="padding: 8px 12px; border-bottom: 1px solid var(--text-muted); display: flex; gap: 8px; align-items: center;">';
    html += '<input type="text" id="bmc-endpoint" placeholder="URL del pod (ej: https://xxx-8000.proxy.runpod.net)" '
      + 'value="' + esc(endpointUrl) + '" '
      + 'style="flex: 1; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 4px; padding: 4px 8px; color: var(--text-primary); font-family: var(--font-mono); font-size: 0.9em;" />';
    var dotColor = endpointUrl ? 'var(--accent)' : 'var(--text-muted)';
    html += '<span style="width: 8px; height: 8px; border-radius: 50%; background: ' + dotColor + '; flex-shrink: 0;" title="' + (endpointUrl ? 'URL configurada' : 'Sin URL') + '"></span>';
    html += '</div>';

    // Chat messages
    html += '<div id="bmc-messages" style="flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px;">';
    if (chatMessages.length === 0) {
      html += '<div style="color: var(--text-muted); text-align: center; margin-top: 40px;">Escribe un mensaje para ver como responde un modelo base (sin instruct)</div>';
    }
    for (var i = 0; i < chatMessages.length; i++) {
      var msg = chatMessages[i];
      if (msg.role === 'user') {
        html += '<div style="align-self: flex-end; background: var(--accent); color: var(--bg-primary); border-radius: 12px 12px 2px 12px; padding: 6px 12px; max-width: 80%; word-wrap: break-word;">'
          + esc(msg.text) + '</div>';
      } else {
        html += '<div style="align-self: flex-start; background: var(--bg-code); color: var(--text-primary); border-radius: 12px 12px 12px 2px; padding: 6px 12px; max-width: 80%; word-wrap: break-word; white-space: pre-wrap;">'
          + esc(msg.text) + '</div>';
      }
    }
    html += '</div>';

    // Error area
    html += '<div id="bmc-error" style="display: none; padding: 4px 12px; color: #ff6b6b; font-size: 0.9em;"></div>';

    // Settings row (max_tokens + temperature)
    html += '<div style="padding: 6px 12px; display: flex; gap: 14px; align-items: center; font-size: 0.85em; color: var(--text-muted); border-top: 1px solid var(--text-muted);">';
    html += '<label style="display: flex; align-items: center; gap: 6px;">max_tokens';
    html += '<input type="number" id="bmc-max-tokens" min="1" max="2048" step="1" value="' + maxTokens + '" '
      + 'style="width: 64px; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 3px; padding: 2px 6px; color: var(--text-primary); font-family: var(--font-mono); font-size: 1em;" />';
    html += '</label>';
    html += '<label style="display: flex; align-items: center; gap: 6px;">temperature';
    html += '<input type="number" id="bmc-temperature" min="0" max="2" step="0.1" value="' + temperature + '" '
      + 'style="width: 56px; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 3px; padding: 2px 6px; color: var(--text-primary); font-family: var(--font-mono); font-size: 1em;" />';
    html += '</label>';
    html += '</div>';

    // Input area
    html += '<div style="padding: 8px 12px; border-top: 1px solid var(--text-muted); display: flex; gap: 8px;">';
    html += '<input type="text" id="bmc-input" placeholder="Escribe un mensaje..." '
      + 'style="flex: 1; background: var(--bg-code); border: 1px solid var(--text-muted); border-radius: 4px; padding: 6px 10px; color: var(--text-primary); font-family: var(--font-body); font-size: 1em;" '
      + (isGenerating ? 'disabled' : '') + ' />';
    if (isGenerating) {
      html += '<button id="bmc-stop" style="background: #ff6b6b; color: white; border: none; border-radius: 4px; padding: 6px 14px; cursor: pointer; font-family: var(--font-body); font-weight: bold;">Stop</button>';
    } else {
      html += '<button id="bmc-send" style="background: var(--accent); color: var(--bg-primary); border: none; border-radius: 4px; padding: 6px 14px; cursor: pointer; font-family: var(--font-body); font-weight: bold;">Enviar</button>';
    }
    html += '<button id="bmc-reset" style="background: var(--bg-code); color: var(--text-muted); border: 1px solid var(--text-muted); border-radius: 4px; padding: 6px 10px; cursor: pointer; font-family: var(--font-body);" title="Reset">Reset</button>';
    html += '</div>';

    html += '</div>'; // end left panel

    // Right panel: Raw view
    html += '<div style="flex: 1; display: flex; flex-direction: column; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--accent); border-style: dashed; overflow: hidden;">';

    // Header
    html += '<div style="padding: 8px 12px; border-bottom: 1px solid var(--text-muted); display: flex; justify-content: space-between; align-items: center;">';
    html += '<span style="color: var(--accent); font-weight: bold;">Lo que realmente pasa</span>';
    html += '<label style="display: flex; align-items: center; gap: 6px; cursor: pointer; color: var(--text-muted); font-size: 0.9em;">';
    html += '<input type="checkbox" id="bmc-special-toggle" ' + (showSpecialTokens ? 'checked' : '') + ' style="cursor: pointer;" />';
    html += 'Mostrar tokens especiales';
    html += '</label>';
    html += '</div>';

    // Raw content
    html += '<div id="bmc-raw" style="flex: 1; overflow-y: auto; padding: 12px; font-family: var(--font-mono); font-size: 0.9em; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">';
    if (rawSegments.length === 0) {
      html += '<span style="color: var(--text-muted);">El texto completo que se envia al modelo aparece aca. No hay "turnos" ni "roles" — solo una cadena de texto que el modelo continua.</span>';
    } else {
      for (var i = 0; i < rawSegments.length; i++) {
        var seg = rawSegments[i];
        if (seg.type === 'special') {
          if (showSpecialTokens) {
            html += '<span style="color: #ff6b6b; background: #ff6b6b22; border-radius: 3px; padding: 0 3px;">' + esc(seg.text) + '</span>';
          }
        } else if (seg.type === 'user') {
          html += '<span style="color: var(--text-primary);">' + esc(seg.text) + '</span>';
        } else if (seg.type === 'model') {
          html += '<span style="color: var(--accent);">' + esc(seg.text) + '</span>';
        }
      }
    }
    html += '</div>';

    // Legend
    html += '<div style="padding: 6px 12px; border-top: 1px solid var(--text-muted); display: flex; gap: 16px; font-size: 0.85em;">';
    html += '<span><span style="color: var(--text-primary);">___</span> Tu texto</span>';
    html += '<span><span style="color: var(--accent);">___</span> Completado del modelo</span>';
    if (showSpecialTokens) {
      html += '<span><span style="color: #ff6b6b;">___</span> Tokens especiales</span>';
    }
    html += '</div>';

    html += '</div>'; // end right panel

    html += '</div>'; // end flex container

    container.innerHTML = html;

    // Bind events
    bindEvents();

    // Auto-scroll
    var messagesDiv = document.getElementById('bmc-messages');
    if (messagesDiv) messagesDiv.scrollTop = messagesDiv.scrollHeight;
    var rawDiv = document.getElementById('bmc-raw');
    if (rawDiv) rawDiv.scrollTop = rawDiv.scrollHeight;
  }

  function bindEvents() {
    var endpointInput = document.getElementById('bmc-endpoint');
    var chatInput = document.getElementById('bmc-input');
    var sendBtn = document.getElementById('bmc-send');
    var stopBtn = document.getElementById('bmc-stop');
    var resetBtn = document.getElementById('bmc-reset');
    var specialToggle = document.getElementById('bmc-special-toggle');

    if (endpointInput) {
      endpointInput.addEventListener('change', function() {
        endpointUrl = this.value.replace(/\/+$/, '');
        render();
      });
      // Prevent reveal.js key navigation while typing
      endpointInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }

    if (chatInput) {
      chatInput.addEventListener('keydown', function(e) {
        e.stopPropagation();
        if (e.key === 'Enter' && !isGenerating) {
          e.preventDefault();
          sendMessage();
        }
      });
      // Auto-focus when not generating
      if (!isGenerating) {
        setTimeout(function() { chatInput.focus(); }, 50);
      }
    }

    if (sendBtn) {
      sendBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        sendMessage();
      });
    }

    if (stopBtn) {
      stopBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        stopGeneration();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        resetChat();
      });
    }

    if (specialToggle) {
      specialToggle.addEventListener('change', function() {
        showSpecialTokens = this.checked;
        render();
      });
    }

    var maxTokensInput = document.getElementById('bmc-max-tokens');
    if (maxTokensInput) {
      maxTokensInput.addEventListener('change', function() {
        var val = parseInt(this.value, 10);
        if (!isNaN(val) && val > 0) maxTokens = val;
      });
      maxTokensInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }

    var temperatureInput = document.getElementById('bmc-temperature');
    if (temperatureInput) {
      temperatureInput.addEventListener('change', function() {
        var val = parseFloat(this.value);
        if (!isNaN(val) && val >= 0) temperature = val;
      });
      temperatureInput.addEventListener('keydown', function(e) { e.stopPropagation(); });
    }
  }

  function showError(msg) {
    var errorDiv = document.getElementById('bmc-error');
    if (errorDiv) {
      errorDiv.textContent = msg;
      errorDiv.style.display = 'block';
      setTimeout(function() {
        if (errorDiv) errorDiv.style.display = 'none';
      }, 5000);
    }
  }

  function sendMessage() {
    var input = document.getElementById('bmc-input');
    if (!input) return;

    var text = input.value;
    if (!text.trim()) return;

    if (!endpointUrl) {
      showError('No conectado — ingresa la URL del pod');
      return;
    }

    // Add user message to chat
    chatMessages.push({ text: text, role: 'user' });

    // Add to raw segments
    rawSegments.push({ text: text, type: 'user' });

    // Start generation
    isGenerating = true;
    chatMessages.push({ text: '', role: 'model' });
    render();

    generate();
  }

  function generate() {
    var prompt = buildFullPrompt();

    abortController = new AbortController();

    var body = {
      model: modelId,
      prompt: prompt,
      max_tokens: maxTokens,
      temperature: temperature,
      stream: true,
      skip_special_tokens: !showSpecialTokens
    };

    fetch(endpointUrl + '/v1/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: abortController.signal
    }).then(function(response) {
      if (response.status === 503) {
        showError('Modelo cargando, intenta en unos minutos');
        isGenerating = false;
        chatMessages.pop();
        render();
        return;
      }
      if (!response.ok) {
        showError('Error del servidor: ' + response.status);
        isGenerating = false;
        chatMessages.pop();
        render();
        return;
      }

      var reader = response.body.getReader();
      var decoder = new TextDecoder();
      var modelSegmentIndex = rawSegments.length;
      rawSegments.push({ text: '', type: 'model' });
      var modelMsgIndex = chatMessages.length - 1;
      var buffer = '';

      function readChunk() {
        reader.read().then(function(result) {
          if (result.done) {
            finishGeneration();
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
              finishGeneration();
              return;
            }
            try {
              var parsed = JSON.parse(data);
              var choices = parsed.choices || [];
              if (choices.length > 0) {
                var token = choices[0].text || '';
                if (token) {
                  rawSegments[modelSegmentIndex].text += token;
                  chatMessages[modelMsgIndex].text += token;
                  updateStreaming(modelSegmentIndex, modelMsgIndex);
                }
              }
            } catch (e) {
              // Skip unparseable lines
            }
          }

          readChunk();
        }).catch(function(err) {
          if (err.name === 'AbortError') return;
          showError('Error de conexion');
          finishGeneration();
        });
      }

      readChunk();

    }).catch(function(err) {
      if (err.name === 'AbortError') return;
      showError('Error de conexion');
      isGenerating = false;
      chatMessages.pop();
      render();
    });
  }

  function updateStreaming(segIndex, msgIndex) {
    // Update just the changing parts without full re-render
    var messagesDiv = document.getElementById('bmc-messages');
    if (messagesDiv) {
      var bubbles = messagesDiv.querySelectorAll('div[style]');
      var lastBubble = bubbles[bubbles.length - 1];
      if (lastBubble) {
        lastBubble.textContent = chatMessages[msgIndex].text;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }
    }

    var rawDiv = document.getElementById('bmc-raw');
    if (rawDiv) {
      // Rebuild raw content
      var rawHtml = '';
      for (var i = 0; i < rawSegments.length; i++) {
        var seg = rawSegments[i];
        if (seg.type === 'special') {
          if (showSpecialTokens) {
            rawHtml += '<span style="color: #ff6b6b; background: #ff6b6b22; border-radius: 3px; padding: 0 3px;">' + esc(seg.text) + '</span>';
          }
        } else if (seg.type === 'user') {
          rawHtml += '<span style="color: var(--text-primary);">' + esc(seg.text) + '</span>';
        } else if (seg.type === 'model') {
          rawHtml += '<span style="color: var(--accent);">' + esc(seg.text) + '</span>';
        }
      }
      rawDiv.innerHTML = rawHtml;
      rawDiv.scrollTop = rawDiv.scrollHeight;
    }
  }

  function finishGeneration() {
    isGenerating = false;
    abortController = null;

    // Check if special tokens appeared in the response
    var lastSeg = rawSegments[rawSegments.length - 1];
    if (lastSeg && lastSeg.type === 'model' && showSpecialTokens) {
      // Extract special tokens from the model output for display
      var text = lastSeg.text;
      var specialPattern = /<\|[^|]+\|>/g;
      var parts = [];
      var lastIndex = 0;
      var match;
      while ((match = specialPattern.exec(text)) !== null) {
        if (match.index > lastIndex) {
          parts.push({ text: text.slice(lastIndex, match.index), type: 'model' });
        }
        parts.push({ text: match[0], type: 'special' });
        lastIndex = match.index + match[0].length;
      }
      if (parts.length > 0) {
        if (lastIndex < text.length) {
          parts.push({ text: text.slice(lastIndex), type: 'model' });
        }
        // Replace the single segment with split segments
        rawSegments.splice(rawSegments.length - 1, 1);
        for (var i = 0; i < parts.length; i++) {
          rawSegments.push(parts[i]);
        }
      }
    }

    // Remove empty model messages
    if (chatMessages.length > 0 && chatMessages[chatMessages.length - 1].text === '') {
      chatMessages.pop();
    }

    render();
  }

  function stopGeneration() {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
    finishGeneration();
  }

  function resetChat() {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
    isGenerating = false;
    rawSegments = [];
    chatMessages = [];
    render();
  }

  // Initial render
  render();
}
