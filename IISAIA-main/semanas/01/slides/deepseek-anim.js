/**
 * DeepSeek R1 Animation
 *
 * Multi-step walkthrough of the DeepSeek R1 paper findings:
 * 1. Context: OpenAI o1 (Sep 2024) — impressive but secret
 * 2. DeepSeek R1 (Jan 2025) — open paper, open model
 * 3. Training dynamics: accuracy climbs, response length grows
 * 4. The "aha moment" — emergent self-correction
 * 5. Benchmark results vs o1
 *
 * Usage: initDeepSeekAnim({ containerId: 'deepseek-anim-demo' })
 */

function initDeepSeekAnim(opts) {
  var container = document.getElementById(opts.containerId);
  if (!container) return;

  var step = 0;
  var maxStep = 6;
  window._dsRewardExpanded = false;

  window._dsToggleReward = function() {
    window._dsRewardExpanded = !window._dsRewardExpanded;
    render();
  };

  function render() {
    var html = '<div style="font-size: 0.6em;">';

    if (step === 0) {
      // Timeline: the buildup
      html += '<div style="position: relative; padding-left: 14px; border-left: 2px solid var(--text-muted);">';

      // Q* rumors
      html += '<div style="margin-bottom: 12px; padding-left: 18px; position: relative;">';
      html += '<div style="position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--text-muted);"></div>';
      html += '<div style="color: var(--text-muted); font-weight: bold;">Nov 2023 &mdash; Rumores de "Q*" (Q-Star)</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Se filtra que OpenAI tiene un avance donde los modelos resuelven problemas de matemática que nunca vieron, usando RL. No confirman nada.</div>';
      html += '</div>';

      // Project Strawberry
      html += '<div style="margin-bottom: 12px; padding-left: 18px; position: relative;">';
      html += '<div style="position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--text-muted);"></div>';
      html += '<div style="color: var(--text-muted); font-weight: bold;">Jul 2024 &mdash; "Project Strawberry"</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Reportes vagos de un proyecto enfocado en razonamiento con un truco de entrenamiento para que el modelo "piense" antes de responder.</div>';
      html += '</div>';

      // o1 release
      html += '<div style="margin-bottom: 12px; padding-left: 18px; position: relative;">';
      html += '<div style="position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--accent-secondary);"></div>';
      html += '<div style="color: var(--accent-secondary); font-weight: bold;">Sep 2024 &mdash; OpenAI lanza o1-preview</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Confirman: está entrenado con RL para producir una cadena de pensamiento oculta. Resultados impresionantes en matemática y código.</div>';
      html += '<div style="color: #e74c3c; margin-top: 4px; font-weight: bold;">Pero ocultan los tokens de razonamiento y no publican ningún detalle técnico.</div>';
      html += '</div>';

      // o1 full
      html += '<div style="padding-left: 18px; position: relative;">';
      html += '<div style="position: absolute; left: -22px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--accent-secondary);"></div>';
      html += '<div style="color: var(--accent-secondary); font-weight: bold;">Dic 2024 &mdash; OpenAI lanza o1 completo</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Más benchmarks, nivel PhD en ciencia. La arquitectura sigue bajo llave. La industria sabe <em>qué</em> funciona, pero no <em>cómo</em>.</div>';
      html += '</div>';

      html += '</div>';

    } else if (step === 1) {
      // DeepSeek drops the bomb
      html += '<div style="display: flex; gap: 14px; align-items: center; margin-bottom: 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; font-size: 1.3em;">20 de enero 2025</div>';
      html += '<div style="color: var(--text-muted);">&mdash;</div>';
      html += '<div style="color: var(--text-primary); font-size: 1.1em;"><a href="https://arxiv.org/pdf/2501.12948" target="_blank" style="color: var(--accent);">DeepSeek publica R1</a> y lo hace open-source</div>';
      html += '</div>';

      html += '<div style="display: flex; gap: 10px;">';

      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; margin-bottom: 8px;">Lo que publican</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.8; font-size: 0.95em;">';
      html += '<div><span style="color: var(--accent);">&check;</span> Paper técnico completo</div>';
      html += '<div><span style="color: var(--accent);">&check;</span> Algoritmo: <strong style="color: var(--text-primary);">GRPO</strong> (Group Relative Policy Optimization)</div>';
      html += '<div><span style="color: var(--accent);">&check;</span> Pipeline de entrenamiento</div>';
      html += '<div><span style="color: var(--accent);">&check;</span> Pesos del modelo (open-source, licencia MIT)</div>';
      html += '</div>';
      html += '</div>';

      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; margin-bottom: 8px;">Resultados vs OpenAI o1</div>';
      html += '<table style="width: 100%; border-collapse: collapse; font-size: 0.95em;">';
      html += '<tr style="border-bottom: 1px solid rgba(136,146,176,0.3);"><td style="padding: 4px 0; color: var(--text-muted);">AIME 2024</td><td style="padding: 4px; text-align: right; color: var(--accent-secondary);">79.2%</td><td style="padding: 4px; text-align: right; color: var(--accent); font-weight: bold;">79.8%</td></tr>';
      html += '<tr style="border-bottom: 1px solid rgba(136,146,176,0.3);"><td style="padding: 4px 0; color: var(--text-muted);">MATH-500</td><td style="padding: 4px; text-align: right; color: var(--accent-secondary);">96.4%</td><td style="padding: 4px; text-align: right; color: var(--accent); font-weight: bold;">97.3%</td></tr>';
      html += '<tr><td style="padding: 4px 0; color: var(--text-muted);">Codeforces</td><td style="padding: 4px; text-align: right; color: var(--accent-secondary);">2,061</td><td style="padding: 4px; text-align: right; color: var(--text-primary);">2,029</td></tr>';
      html += '<tr><td></td><td style="padding: 4px; text-align: right; color: var(--accent-secondary); font-size: 0.85em;">o1</td><td style="padding: 4px; text-align: right; color: var(--accent); font-size: 0.85em;">R1</td></tr>';
      html += '</table>';
      html += '</div>';

      html += '</div>';

      html += '<div style="background: var(--bg-code); border-radius: 6px; padding: 8px 12px; margin-top: 10px; border-left: 3px solid #e74c3c;">';
      html += '<span style="color: #e74c3c; font-weight: bold;">Impacto:</span> ';
      html += '<span style="color: var(--text-muted);">caída masiva en acciones tech (Nvidia, etc.). OpenAI lanzó <strong style="color: var(--accent-secondary);">o3-mini</strong> días después para competir con la narrativa.</span>';
      html += '</div>';

    } else if (step === 2) {
      // The simple recipe
      html += '<div style="text-align: center; color: var(--text-muted); margin-bottom: 14px;">El descubrimiento central del paper:</div>';

      html += '<div style="background: var(--bg-secondary); border-radius: 8px; padding: 18px 20px; border: 1px solid var(--accent); max-width: 85%; margin: 0 auto;">';
      html += '<div style="color: var(--text-primary); font-size: 1.15em; line-height: 1.7; text-align: center;">';
      html += 'Se puede replicar el razonamiento de o1 con una señal de reward <strong style="color: var(--accent);">sorprendentemente simple</strong>:';
      html += '</div>';

      html += '<div style="display: flex; gap: 10px; margin-top: 14px;">';

      html += '<div id="ds-reward-precision" style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 12px; text-align: center; cursor: pointer; transition: border-color 0.2s;" onclick="window._dsToggleReward()">';
      if (!window._dsRewardExpanded) {
        html += '<div style="color: var(--accent); font-weight: bold; font-size: 1.1em; margin-bottom: 6px;">Reward de precisión</div>';
        html += '<div style="color: var(--text-primary); font-size: 1.05em;">¿Es correcta la respuesta?</div>';
        html += '<div style="color: var(--text-muted); font-size: 0.85em; margin-top: 6px;">Verificación directa contra la respuesta correcta. Sin red neuronal.</div>';
        html += '<div style="color: var(--text-muted); font-size: 0.75em; margin-top: 8px; font-style: italic;">Click para ver cómo funciona</div>';
      } else {
        html += '<div style="color: var(--accent); font-weight: bold; font-size: 1em; margin-bottom: 8px;">¿Cómo se verifica sin red neuronal?</div>';
        html += '<div style="text-align: left; line-height: 1.7;">';
        html += '<div style="background: var(--bg-secondary); border-radius: 4px; padding: 8px 10px; margin-bottom: 6px;">';
        html += '<div style="color: var(--accent-secondary); font-weight: bold; margin-bottom: 4px;">Matemática</div>';
        html += '<div style="color: var(--text-muted); font-size: 0.9em;">El modelo pone su respuesta final en un formato fijo (ej: <span style="color: var(--accent); font-family: var(--font-mono);">\\boxed{48}</span>). Se extrae y se compara con la clave: <span style="font-family: var(--font-mono);">48 == 48</span> &rarr; correcto.</div>';
        html += '</div>';
        html += '<div style="background: var(--bg-secondary); border-radius: 4px; padding: 8px 10px;">';
        html += '<div style="color: var(--accent-secondary); font-weight: bold; margin-bottom: 4px;">Código</div>';
        html += '<div style="color: var(--text-muted); font-size: 0.9em;">Se compila y ejecuta contra test cases predefinidos. ¿Pasan todos? &rarr; correcto.</div>';
        html += '</div>';
        html += '</div>';
        html += '<div style="color: var(--text-muted); font-size: 0.8em; margin-top: 8px;">No hay juicio subjetivo. La señal es binaria e inhackeable.</div>';
      }
      html += '</div>';

      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 12px; text-align: center;">';
      html += '<div style="color: var(--accent); font-weight: bold; font-size: 1.1em; margin-bottom: 6px;">Reward de formato</div>';
      html += '<div style="color: var(--text-primary); font-size: 1.05em;">¿Usó los tags &lt;think&gt;...&lt;/think&gt;?</div>';
      html += '<div style="color: var(--text-muted); font-size: 0.85em; margin-top: 6px;">Forzar que separe el razonamiento de la respuesta final.</div>';
      html += '</div>';

      html += '</div>';
      html += '</div>';

      html += '<div style="display: flex; gap: 10px; margin-top: 12px; max-width: 85%; margin-left: auto; margin-right: auto;">';

      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px; text-align: center;">';
      html += '<div style="color: #e74c3c; font-weight: bold; margin-bottom: 4px;">Sin reward model</div>';
      html += '<div style="color: var(--text-muted); font-size: 0.9em;">No se entrena una red neuronal para puntuar. Evita el problema de RLHF.</div>';
      html += '</div>';

      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px; text-align: center;">';
      html += '<div style="color: #e74c3c; font-weight: bold; margin-bottom: 4px;">Sin datos humanos de razonamiento</div>';
      html += '<div style="color: var(--text-muted); font-size: 0.9em;">Ningun humano le mostró cómo pensar paso a paso. El modelo lo descubre solo.</div>';
      html += '</div>';

      html += '</div>';

    } else if (step === 3) {
      // Training dynamics
      html += '<div style="color: var(--text-muted); margin-bottom: 10px;">A medida que avanza el RL, pasan dos cosas simultáneamente:</div>';
      html += '<div style="display: flex; gap: 12px;">';

      // Chart 1: Accuracy
      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; margin-bottom: 8px;">Precisión en AIME 2024 (pass@1)</div>';
      html += '<svg viewBox="0 0 300 150" style="width: 100%; height: auto;">';
      // Axes
      html += '<line x1="40" y1="10" x2="40" y2="130" stroke="var(--text-muted)" stroke-width="1"/>';
      html += '<line x1="40" y1="130" x2="290" y2="130" stroke="var(--text-muted)" stroke-width="1"/>';
      // Y labels
      html += '<text x="35" y="130" fill="var(--text-muted)" font-size="9" text-anchor="end">15%</text>';
      html += '<text x="35" y="90" fill="var(--text-muted)" font-size="9" text-anchor="end">35%</text>';
      html += '<text x="35" y="50" fill="var(--text-muted)" font-size="9" text-anchor="end">55%</text>';
      html += '<text x="35" y="15" fill="var(--text-muted)" font-size="9" text-anchor="end">71%</text>';
      // X label
      html += '<text x="165" y="148" fill="var(--text-muted)" font-size="9" text-anchor="middle">Steps de RL</text>';
      // Curve (ascending, slightly concave)
      html += '<path d="M 45,128 C 80,125 100,110 130,90 S 180,55 220,35 S 260,18 285,15" fill="none" stroke="var(--accent)" stroke-width="2.5"/>';
      // Grid lines
      html += '<line x1="40" y1="90" x2="290" y2="90" stroke="var(--text-muted)" stroke-width="0.3" stroke-dasharray="4"/>';
      html += '<line x1="40" y1="50" x2="290" y2="50" stroke="var(--text-muted)" stroke-width="0.3" stroke-dasharray="4"/>';
      html += '</svg>';
      html += '<div style="color: var(--text-muted); font-size: 0.85em; text-align: center;">De 15.6% a 71.0% &mdash; sin datos humanos de razonamiento</div>';
      html += '</div>';

      // Chart 2: Response length
      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 12px;">';
      html += '<div style="color: var(--accent-secondary); font-weight: bold; margin-bottom: 8px;">Largo promedio de respuesta</div>';
      html += '<svg viewBox="0 0 300 150" style="width: 100%; height: auto;">';
      // Axes
      html += '<line x1="40" y1="10" x2="40" y2="130" stroke="var(--text-muted)" stroke-width="1"/>';
      html += '<line x1="40" y1="130" x2="290" y2="130" stroke="var(--text-muted)" stroke-width="1"/>';
      // Y labels
      html += '<text x="35" y="130" fill="var(--text-muted)" font-size="9" text-anchor="end">corto</text>';
      html += '<text x="35" y="15" fill="var(--text-muted)" font-size="9" text-anchor="end">largo</text>';
      // X label
      html += '<text x="165" y="148" fill="var(--text-muted)" font-size="9" text-anchor="middle">Steps de RL</text>';
      // Curve (ascending, roughly linear with slight S)
      html += '<path d="M 45,125 C 80,120 110,100 140,80 S 200,40 250,22 S 275,17 285,15" fill="none" stroke="var(--accent-secondary)" stroke-width="2.5"/>';
      html += '</svg>';
      html += '<div style="color: var(--text-muted); font-size: 0.85em; text-align: center;">El modelo aprende solo a generar más tokens para pensar</div>';
      html += '</div>';

      html += '</div>';

      html += '<div style="background: var(--bg-code); border-radius: 6px; padding: 8px 14px; margin-top: 10px; display: flex; align-items: baseline; gap: 8px;">';
      html += '<span style="color: var(--accent); font-weight: bold; flex-shrink: 0;">Correlación:</span>';
      html += '<span style="color: var(--text-muted);">a medida que el modelo genera respuestas más largas, su precisión sube. Descubrió por su cuenta que necesita más tokens para pensar.</span>';
      html += '</div>';

    } else if (step === 4) {
      // The "aha moment"
      html += '<div style="color: var(--text-muted); margin-bottom: 10px;">El paper documenta un <strong style="color: var(--accent);">"aha moment"</strong> en un checkpoint intermedio del entrenamiento:</div>';

      html += '<div style="background: var(--bg-secondary); border-radius: 8px; padding: 14px; border: 1px solid var(--accent); font-family: var(--font-mono); font-size: 0.95em; line-height: 1.8;">';
      html += '<div style="color: var(--text-muted);">To solve the equation... let me try squaring both sides...</div>';
      html += '<div style="color: var(--text-muted);">a - sqrt(a+x) = x^2, so sqrt(a+x) = a - x^2...</div>';
      html += '<div style="color: var(--text-muted); opacity: 0.5;">(...several attempts...)</div>';
      html += '<div style="height: 6px;"></div>';
      html += '<div style="color: #e74c3c; font-weight: bold; font-size: 1.1em;">Wait, wait. Wait. That\'s an aha moment I can flag here.</div>';
      html += '<div style="color: var(--accent); font-weight: bold;">Let me reevaluate this step-by-step to identify the correct sum...</div>';
      html += '<div style="height: 6px;"></div>';
      html += '<div style="color: var(--text-muted);">We started with: sqrt(a - sqrt(a+x)) = x</div>';
      html += '<div style="color: var(--accent);">If I approach this differently... (restarts with new strategy)</div>';
      html += '</div>';

      html += '<div style="display: flex; gap: 10px; margin-top: 10px;">';
      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; margin-bottom: 4px;">Comportamientos emergentes</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Auto-verificación, backtracking, reformulación, explorar perspectivas alternativas</div>';
      html += '</div>';
      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px;">';
      html += '<div style="color: var(--accent); font-weight: bold; margin-bottom: 4px;">Nadie programó esto</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.5;">Propiedad emergente de la optimización. Solo se le dijo "¿es correcta la respuesta?" y esto salió.</div>';
      html += '</div>';
      html += '</div>';

    } else if (step === 5) {
      // Benchmark comparison
      html += '<div style="color: var(--text-muted); margin-bottom: 10px;">Comparación con otros modelos (datos del paper):</div>';

      html += '<table style="width: 100%; border-collapse: collapse; font-size: 0.95em;">';
      html += '<tr style="border-bottom: 1px solid var(--text-muted);">';
      html += '<th style="padding: 6px; text-align: left; color: var(--text-muted);">Benchmark</th>';
      html += '<th style="padding: 6px; text-align: right; color: var(--text-muted);">GPT-4o</th>';
      html += '<th style="padding: 6px; text-align: right; color: var(--text-muted);">Claude 3.5</th>';
      html += '<th style="padding: 6px; text-align: right; color: var(--accent-secondary);">OpenAI o1</th>';
      html += '<th style="padding: 6px; text-align: right; color: var(--accent);">DeepSeek R1</th>';
      html += '</tr>';

      var rows = [
        ['AIME 2024', '9.3', '16.0', '79.2', '79.8'],
        ['MATH-500', '74.6', '78.3', '96.4', '97.3'],
        ['Codeforces (Elo)', '759', '717', '2,061', '2,029'],
        ['MMLU', '87.2', '88.3', '91.8', '90.8'],
        ['LiveCodeBench', '32.9', '38.9', '63.4', '65.9'],
        ['GPQA Diamond', '49.9', '65.0', '75.7', '71.5'],
      ];

      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        var isReasoning = i < 3; // AIME, MATH, Codeforces
        html += '<tr style="border-bottom: 1px solid rgba(136,146,176,0.2);">';
        html += '<td style="padding: 5px 6px; color: var(--text-primary);">' + r[0] + '</td>';
        html += '<td style="padding: 5px 6px; text-align: right; color: var(--text-muted);">' + r[1] + '</td>';
        html += '<td style="padding: 5px 6px; text-align: right; color: var(--text-muted);">' + r[2] + '</td>';
        html += '<td style="padding: 5px 6px; text-align: right; color: var(--accent-secondary);">' + r[3] + '</td>';

        // Highlight R1 when it beats o1
        var r1Val = parseFloat(r[4].replace(',', ''));
        var o1Val = parseFloat(r[3].replace(',', ''));
        var r1Color = r1Val >= o1Val ? 'var(--accent)' : 'var(--text-primary)';
        var bold = r1Val >= o1Val ? 'font-weight: bold;' : '';
        html += '<td style="padding: 5px 6px; text-align: right; color: ' + r1Color + '; ' + bold + '">' + r[4] + '</td>';
        html += '</tr>';
      }

      html += '</table>';

      html += '<div style="display: flex; gap: 10px; margin-top: 10px;">';
      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px;">';
      html += '<span style="color: var(--accent); font-weight: bold;">Comparable a o1</span>';
      html += '<span style="color: var(--text-muted);"> en razonamiento &mdash; con el paper, los datos y el modelo publicados.</span>';
      html += '</div>';
      html += '<div style="flex: 1; background: var(--bg-code); border-radius: 6px; padding: 8px 12px;">';
      html += '<span style="color: var(--text-muted);">Modelos SFT (GPT-4o, Claude 3.5) quedan </span>';
      html += '<span style="color: #e74c3c; font-weight: bold;">muy atrás</span>';
      html += '<span style="color: var(--text-muted);"> en tareas de razonamiento.</span>';
      html += '</div>';
      html += '</div>';

    } else if (step === 6) {
      // Summary: what this means
      html += '<div style="display: flex; gap: 12px; align-items: stretch;">';

      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 14px;">';
      html += '<div style="color: var(--accent); font-weight: bold; font-size: 1.1em; margin-bottom: 10px;">Lo que DeepSeek demostró</div>';
      html += '<div style="line-height: 1.8; color: var(--text-muted);">';
      html += '<div style="margin-bottom: 6px;"><span style="color: var(--accent);">1.</span> No hacen falta datos humanos de razonamiento &mdash; RL puro con "¿es correcta la respuesta?" es suficiente</div>';
      html += '<div style="margin-bottom: 6px;"><span style="color: var(--accent);">2.</span> Las cadenas de pensamiento emergen espontáneamente &mdash; backtracking, verificación, reformulación</div>';
      html += '<div style="margin-bottom: 6px;"><span style="color: var(--accent);">3.</span> El modelo descubre por su cuenta que más tokens = mejor razonamiento</div>';
      html += '<div><span style="color: var(--accent);">4.</span> Como "48 == 48" no se puede falsear, el RL se puede correr por miles de steps sin que colapse</div>';
      html += '</div>';
      html += '</div>';

      html += '<div style="flex: 1; background: var(--bg-secondary); border-radius: 8px; padding: 14px; border: 1px solid var(--accent);">';
      html += '<div style="color: var(--accent); font-weight: bold; font-size: 1.1em; margin-bottom: 10px;">La implicación</div>';
      html += '<div style="color: var(--text-muted); line-height: 1.8;">';
      html += '<div style="margin-bottom: 8px;">La capacidad de razonar estaba <strong style="color: var(--text-primary);">latente</strong> en el modelo base &mdash; el RL solo le dio el incentivo para activarla.</div>';
      html += '<div>Modelos como <strong style="color: var(--accent-secondary);">o1, o3, Claude Opus, Gemini 2.5</strong> usan variantes de esta técnica. Es la frontera actual de la IA.</div>';
      html += '</div>';
      html += '</div>';

      html += '</div>';
    }

    html += '</div>';

    // Step labels
    var labels = [
      'El camino a los modelos de razonamiento',
      'DeepSeek publica todo',
      'La receta: sorprendentemente simple',
      'Dinámica del entrenamiento',
      'El "aha moment"',
      'Resultados: benchmarks',
      'Conclusión'
    ];

    // Controls
    html += '<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 0.6em;">';
    html += '<div style="color: var(--text-muted); font-style: italic;">' + labels[step] + '</div>';
    html += '<div style="display: flex; gap: 6px;">';
    if (step > 0) {
      html += '<button onclick="window._dsAnimPrev()" style="background: var(--bg-secondary); color: var(--text-muted); border: 1px solid var(--text-muted); border-radius: 4px; padding: 3px 12px; cursor: pointer; font-family: var(--font-body); font-size: 1em;">&larr;</button>';
    }
    if (step < maxStep) {
      html += '<button onclick="window._dsAnimNext()" style="background: var(--accent); color: var(--bg-primary); border: none; border-radius: 4px; padding: 3px 12px; cursor: pointer; font-family: var(--font-body); font-size: 1em; font-weight: bold;">Siguiente &rarr;</button>';
    }
    html += '</div></div>';

    container.innerHTML = html;
    if (window.Reveal && Reveal.layout) Reveal.layout();
  }

  window._dsAnimNext = function() {
    if (step < maxStep) {
      step++;
      window._dsRewardExpanded = false;
      render();
    }
  };

  window._dsAnimPrev = function() {
    if (step > 0) {
      step--;
      window._dsRewardExpanded = false;
      render();
    }
  };

  render();
}
