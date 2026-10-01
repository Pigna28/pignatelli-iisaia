# Semana 04 — Consolidación de slides via animaciones JS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reducir el deck de semana 04 de 115 → ~95-100 slides ejecutando 6 consolidaciones que reemplazan slides redundantes por transiciones de estado dentro de animaciones JS y CSS, sin recortar contenido pedagógico.

**Architecture:** Extiende `four-loop-anim.js` con una API `update` para mutar la fase/modo de instancias existentes sin remontar. Reusa la infraestructura CSS existente (`.lens-tracker`, `.tricotomia`) que ya está en `_scaffold.html`. Introduce un patrón "logically persistent" para el loop de la Parte 1 (mismo div, mismo lugar, atributos data en cada slide). Mantiene el flujo de assembly: cada sección sigue editándose en `_section-N.html`, y `_assemble.mjs` regenera `index.html`.

**Tech Stack:** JavaScript vanilla (sin frameworks), reveal.js 4.x con `fragmentshown`/`slidechanged` events, CSS transitions, HTML5 data attributes.

**Spec:** `docs/superpowers/specs/2026-05-17-semana-04-consolidacion-animaciones-design.md`

**Deviation from spec:** Auditoría reveló que la infraestructura CSS ya cubre lo que el spec proponía implementar para C4 (`.tricotomia` con `.show-1|2|3`) y C5 (`.lens-tracker` con `.on-loop|on-context` y transitions). El plan reemplaza la creación de un `tracker.js` (proposto en spec C5) por reuso del CSS existente + un toggle de clase para el flip de §11. No se crea archivo `tracker.js`.

---

## File Structure

**Archivos modificados:**

| Path | Cambio | Razón |
|------|--------|-------|
| `semanas/04/slides/four-loop-anim.js` | Refactor + extensión | Agregar API `update`, registry de instancias, modos `hallucinate` + `poison` |
| `semanas/04/slides/_scaffold.html` | Extensión | Agregar slot/CSS opcional para `part1-loop` host (C6); init script global de sync |
| `semanas/04/slides/_section-2.html` | Edit grueso | C1 (consolidar fases), C6 (data-loop-* attrs) |
| `semanas/04/slides/_section-3.html` | Edit | C6 (data-loop-* attrs) |
| `semanas/04/slides/_section-4.html` | Edit grueso | C3 (consolidar fill + numbers + rot), C4 (limpieza), C6 (data-loop-* attrs) |
| `semanas/04/slides/_section-5.html` | Edit grueso | C2 (consolidar modos), C6 (data-loop-* attrs) |
| `semanas/04/slides/_section-6.html` | Edit | C6 (data-loop-* attrs), C5 (merge opener si aplica) |
| `semanas/04/slides/_section-7.html` | Edit | C5 (eliminar slide opener, merge a primer slide de contenido) |
| `semanas/04/slides/_section-8.html` | Edit | C5 (eliminar opener), revisar `.tricotomia show-2` |
| `semanas/04/slides/_section-9.html` | Edit | C5 (eliminar opener), revisar `.tricotomia show-3` |
| `semanas/04/slides/_section-10.html` | Edit | C5 (eliminar opener) |
| `semanas/04/slides/_section-11.html` | Edit | C5 (eliminar opener, wire flip animado) |
| `semanas/04/slides/index.html` | Regenerado | Output del `_assemble.mjs` |

**Archivos NO creados:** ni `tracker.js`, ni archivos nuevos en `slides/`. Toda la lógica nueva va en archivos existentes.

**Workflow de cada cambio:** editar `_section-N.html` → `node semanas/04/slides/_assemble.mjs` → reload browser en `http://localhost:3000/semanas/04/slides/`.

---

## Phase 0 — Base infrastructure: `four-loop-anim.js` extensions

Antes de tocar slides, hacer las extensiones a la librería de animación que el resto del plan depende. Verificar que los slides existentes siguen renderizando idénticos después.

### Task 0.1: Agregar registry de instancias en `four-loop-anim.js`

**Files:**
- Modify: `semanas/04/slides/four-loop-anim.js`

- [ ] **Step 1: Leer el archivo actual** para confirmar la estructura del closure UMD y dónde está `allInstances`.

Run: `head -20 semanas/04/slides/four-loop-anim.js && grep -n 'allInstances\|initFourLoop\|return initFourLoop' semanas/04/slides/four-loop-anim.js`

- [ ] **Step 2: Cambiar `allInstances` para guardar opts originales**

En la línea donde se hace `allInstances.push({ containerId: opts.containerId, render: render });`, cambiar a:

```js
allInstances.push({
  containerId: opts.containerId,
  opts: opts,           // guardar opts originales para merge en update
  render: render
});
```

- [ ] **Step 3: Agregar función `updateFourLoop` antes del `return`**

Justo antes de `return initFourLoop;` al final del IIFE, agregar:

```js
function updateFourLoop(updateOpts) {
  if (!updateOpts || !updateOpts.containerId) return;
  var inst = null;
  for (var i = 0; i < allInstances.length; i++) {
    if (allInstances[i].containerId === updateOpts.containerId) {
      inst = allInstances[i];
      break;
    }
  }
  if (!inst) return;
  var container = document.getElementById(updateOpts.containerId);
  if (!container) return;

  // Merge update opts over original opts (phase/mode/fillPercent override)
  var merged = {};
  for (var k in inst.opts) merged[k] = inst.opts[k];
  if (updateOpts.phase !== undefined) merged.phase = updateOpts.phase;
  if (updateOpts.mode !== undefined) merged.mode = updateOpts.mode;
  if (updateOpts.fillPercent !== undefined) merged.fillPercent = updateOpts.fillPercent;

  var renderer = modeMap[merged.mode] || renderIntro;
  renderer(container, merged);

  // Update stored opts so subsequent updates merge over the new state
  inst.opts = merged;
}
```

- [ ] **Step 4: Cambiar el return para exportar `{ init, update }`**

Cambiar `return initFourLoop;` a:

```js
return { init: initFourLoop, update: updateFourLoop };
```

Y el wrapper UMD bottom debe exponer ambos como globals. Cambiar la sección del UMD wrapper donde dice algo como `root.initFourLoop = factory()` para que sea:

```js
var api = factory();
root.initFourLoop = api.init;       // backward-compat
root.updateFourLoop = api.update;   // nueva API
root.fourLoopAnim = api;             // namespace
```

(Ajustar exactamente al patrón UMD actual del archivo después de leerlo.)

- [ ] **Step 5: Regenerar index.html y verificar que slides existentes siguen rendereando**

Run: `node semanas/04/slides/_assemble.mjs`

Run: `npm start` (en otra terminal — si no está corriendo ya).

Abrir browser en `http://localhost:3000/semanas/04/slides/#/4` (§2 loop intro). Verificar:
- El loop se renderiza igual que antes (3 nodos: PENSAR · ACTUAR · OBSERVAR, arco de retorno, chips de salida).
- Sin errores en consola.

Recorrer rápidamente §3 (s3-loop-tool), §4 (s4-loop-fill), §5 (s5-loop-infinite, s5-loop-drift), §6 (s6-loop-cc), §10 (s10-loop-subagent), §11 (s11-loop-planmode, s11-loop-gate). Cada uno debe verse exactamente igual.

- [ ] **Step 6: Verificar que `window.updateFourLoop` está disponible**

En la consola del browser:
```js
typeof window.updateFourLoop // → "function"
typeof window.initFourLoop  // → "function"
```

- [ ] **Step 7: Commit**

```bash
git add semanas/04/slides/four-loop-anim.js
git commit -m "feat(s04): add updateFourLoop API for in-place mutation"
```

---

### Task 0.2: Agregar render mode `renderHallucinate`

**Files:**
- Modify: `semanas/04/slides/four-loop-anim.js`

- [ ] **Step 1: Identificar dónde agregar el nuevo renderer**

Run: `grep -n 'function render\|modeMap' semanas/04/slides/four-loop-anim.js`

Debería listar los renderers existentes y la definición de `modeMap`.

- [ ] **Step 2: Agregar la función `renderHallucinate` junto a las otras**

Inmediatamente después de `renderDrift` (alrededor de la línea 374), agregar:

```js
function renderHallucinate(container, opts) {
  var labels = opts.labels || {};
  var pensarLabel  = labels.pensar  || 'PENSAR';
  var actuarLabel  = labels.actuar  || 'ACTUAR';
  var observarLabel = labels.observar || 'OBSERVAR';

  var dimStyle = nodeStyle('opacity:0.45;color:var(--text-muted)');
  var errorStyle = litNodeStyle('#ff6b6b');  // red for hallucinated tool/result

  var html = '<div style="display:flex;flex-direction:column;align-items:center;padding:10px 0;">';
  html += '<div style="display:flex;align-items:center;gap:6px;">';
  html += nodeHtml(pensarLabel, null, dimStyle);
  html += arrowSvg({ width: 40, height: 24, lit: false });
  html += nodeHtml(actuarLabel, '(tool inventada)', errorStyle);
  html += arrowSvg({ width: 40, height: 24, lit: true });
  html += nodeHtml(observarLabel, '(resultado falso)', errorStyle);
  html += '</div>';
  html += '<div style="margin-top:2px;position:relative;width:366px;">';
  html += arrowSvg({ returnArc: true, arcWidth: 366, arcHeight: 36, lit: false });
  html += '<span style="position:absolute;bottom:2px;left:50%;transform:translateX(-50%);font-size:0.6em;color:var(--text-muted);font-family:var(--font-mono);">repetir</span>';
  html += '</div>';
  html += exitChipsHtml(false);
  html += caption('actúa sobre una premisa falsa');
  html += '</div>';
  container.innerHTML = html;
}
```

- [ ] **Step 3: Registrar en `modeMap`**

Encontrar la definición de `modeMap` (cerca de la línea 555) y agregar la entrada `'hallucinate': renderHallucinate,` junto a las demás.

- [ ] **Step 4: Regenerar y smoke-test**

Run: `node semanas/04/slides/_assemble.mjs`

En la consola del browser (estando en cualquier slide con la animación):
```js
updateFourLoop({ containerId: 's2-loop-intro', mode: 'hallucinate' })
```

Verificar visualmente: el nodo `actuar` muestra "(tool inventada)" en rojo (#ff6b6b), `observar` muestra "(resultado falso)" en rojo, los demás dimmed.

Después restaurar:
```js
updateFourLoop({ containerId: 's2-loop-intro', mode: 'intro' })
```

- [ ] **Step 5: Commit**

```bash
git add semanas/04/slides/four-loop-anim.js
git commit -m "feat(s04): add 'hallucinate' render mode to four-loop"
```

---

### Task 0.3: Agregar render mode `renderPoison`

**Files:**
- Modify: `semanas/04/slides/four-loop-anim.js`

- [ ] **Step 1: Agregar la función `renderPoison`**

Inmediatamente después de `renderHallucinate`, agregar:

```js
function renderPoison(container, opts) {
  var b = buildBaseRow(opts);

  var html = '<div style="display:flex;align-items:flex-start;gap:20px;padding:10px 0;justify-content:center;">';

  // Left: cycle (dimmed slightly to emphasize the rot is in the context, not the loop itself)
  html += '<div style="display:flex;flex-direction:column;align-items:center;">';
  html += '<div style="display:flex;align-items:center;gap:6px;">';
  html += nodeHtml(b.pensarLabel,  null, b.pensarStyle);
  html += arrowSvg({ width: 36, height: 24, lit: b.arrowPA_lit });
  html += nodeHtml(b.actuarLabel,  null, b.actuarStyle);
  html += arrowSvg({ width: 36, height: 24, lit: b.arrowAO_lit });
  html += nodeHtml(b.observarLabel, null, b.observarStyle);
  html += '</div>';
  html += '<div style="margin-top:2px;position:relative;width:354px;">';
  html += arrowSvg({ returnArc: true, arcWidth: 354, arcHeight: 34, lit: false });
  html += '<span style="position:absolute;bottom:2px;left:50%;transform:translateX(-50%);font-size:0.6em;color:var(--text-muted);font-family:var(--font-mono);">repetir</span>';
  html += '</div>';
  html += exitChipsHtml(false);
  html += '</div>';

  // Right: context bar with RED noise chips
  html += '<div style="display:flex;flex-direction:column;align-items:center;margin-top:4px;">';
  html += '<div style="font-size:0.6em;color:var(--text-muted);margin-bottom:6px;letter-spacing:0.04em;">ventana de contexto</div>';
  html += '<div style="width:36px;height:130px;border:2px solid var(--text-muted);border-radius:6px;background:var(--bg-code);position:relative;overflow:hidden;">';
  html += '<div style="position:absolute;bottom:0;left:0;right:0;height:108px;display:flex;flex-direction:column-reverse;flex-wrap:wrap;align-content:flex-start;gap:2px;padding:2px;">';
  var chipCount = 36;
  for (var i = 0; i < chipCount; i++) {
    // Mix: 1/3 red noise, 2/3 normal
    var isNoise = (i % 3 === 0);
    var color = isNoise ? '#ff6b6b' : 'var(--accent-secondary)';
    var opacity = isNoise ? '0.85' : '0.55';
    html += '<div style="width:10px;height:10px;border-radius:2px;background:' + color + ';opacity:' + opacity + ';"></div>';
  }
  html += '</div>';
  html += '</div>';
  html += '<div style="font-size:0.55em;color:#ff6b6b;margin-top:5px;text-align:center;max-width:80px;font-weight:700;">el agente alimenta su propio rot</div>';
  html += '</div>';

  html += '</div>';
  container.innerHTML = html;
}
```

- [ ] **Step 2: Registrar en `modeMap`**

Agregar `'poison': renderPoison,` junto a las otras entradas.

- [ ] **Step 3: Regenerar y smoke-test**

Run: `node semanas/04/slides/_assemble.mjs`

En consola del browser:
```js
updateFourLoop({ containerId: 's4-loop-fill', mode: 'poison' })
```

Verificar: ciclo del loop dim a la izquierda; barra a la derecha con chips mezclados (1/3 rojos, 2/3 normales); caption "el agente alimenta su propio rot" en rojo.

Restaurar:
```js
updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill' })
```

- [ ] **Step 4: Commit**

```bash
git add semanas/04/slides/four-loop-anim.js
git commit -m "feat(s04): add 'poison' render mode to four-loop"
```

---

### Task 0.4: Agregar parámetro `fillPercent` a `renderFill`

**Files:**
- Modify: `semanas/04/slides/four-loop-anim.js`

- [ ] **Step 1: Localizar el `height:76px` literal en `renderFill`**

Run: `grep -n "height:76px" semanas/04/slides/four-loop-anim.js`

Está cerca de la línea 304-305 dentro de `renderFill`.

- [ ] **Step 2: Reemplazar el literal por un cálculo basado en `opts.fillPercent`**

En `renderFill`, reemplazar:

```js
html += '<div style="position:absolute;bottom:0;left:0;right:0;height:76px;display:flex;flex-direction:column-reverse;flex-wrap:wrap;align-content:flex-start;gap:2px;padding:2px;">';
// Render small token chips
var chipCount = 24;
```

por:

```js
// fillPercent: 0-100. Default 60 (mantiene comportamiento original: 76/126 ≈ 60%).
var fillPercent = typeof opts.fillPercent === 'number' ? opts.fillPercent : 60;
// El bar es 130px outer, 126px inner (2px border each side). 76px ≈ 60%.
var fillHeight = Math.round(126 * (fillPercent / 100));
var chipCount = Math.round(40 * (fillPercent / 100));  // 24 chips at 60% scales similarly
html += '<div style="position:absolute;bottom:0;left:0;right:0;height:' + fillHeight + 'px;display:flex;flex-direction:column-reverse;flex-wrap:wrap;align-content:flex-start;gap:2px;padding:2px;transition:height 600ms ease;">';
```

- [ ] **Step 3: Verificar smoke**

Run: `node semanas/04/slides/_assemble.mjs`

En consola del browser:
```js
updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill', fillPercent: 20 })
// La barra se reduce visiblemente a ~20% con transición animada.

updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill', fillPercent: 90 })
// La barra crece a ~90%.

updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill' })
// Vuelve al default ~60%.
```

- [ ] **Step 4: Commit**

```bash
git add semanas/04/slides/four-loop-anim.js
git commit -m "feat(s04): add fillPercent parameter to fill mode"
```

---

## Phase 1 — C1: §2 fases (Pensar / Actuar / Observar)

Consolidar §2.3, §2.4, §2.5 en un solo slide con h2 + card + fase iluminada sincronizados via fragments.

### Task 1.1: Leer el estado actual de §2.3, §2.4, §2.5

**Files:**
- Read: `semanas/04/slides/_section-2.html` (líneas ~270-336)

- [ ] **Step 1: Capturar el markup actual de las tres slides**

Run: `sed -n '272,336p' semanas/04/slides/_section-2.html`

Anotar las tres `<aside class="notes">` para tenerlas a mano al mergear.

---

### Task 1.2: Reemplazar §2.3 + §2.4 + §2.5 por slide consolidado

**Files:**
- Modify: `semanas/04/slides/_section-2.html`

- [ ] **Step 1: Borrar las tres `<section>` actuales (de §2.3, §2.4, §2.5)**

Las tres `<section>` que se borran van desde el comentario `<!-- §2.3 · Pensar -->` (línea ~272) hasta el cierre `</section>` de §2.5 (línea ~336).

- [ ] **Step 2: Insertar el nuevo slide consolidado en su lugar**

```html
<!-- §2.3 · Tres fases (consolidado: Pensar / Actuar / Observar) -->
<section data-loop-mode="intro" data-loop-phase="pensar">
  <h2 data-phase-h2="pensar" class="s2-h2-phase">Pensar — formular el próximo paso</h2>
  <h2 data-phase-h2="actuar" class="s2-h2-phase fragment current-visible">Actuar — usar una herramienta</h2>
  <h2 data-phase-h2="observar" class="s2-h2-phase fragment current-visible">Observar — leer el resultado</h2>

  <div class="s2-loop-wrap">
    <div id="s2-loop-phases"></div>
  </div>

  <div class="s2-phase-card s2-phase-card-stage" data-phase-card="pensar">
    <h3>Pensar</h3>
    <p>El agente razona sobre el estado actual: qué sabe, qué le falta saber, qué hipótesis tiene. No es pensamiento lineal — es el modelo formulando el próximo paso en función de lo que observó antes.</p>
    <p class="s2-produces">Produce: una decisión sobre qué acción tomar a continuación.</p>
  </div>
  <div class="s2-phase-card s2-phase-card-stage actuar fragment current-visible" data-phase-card="actuar">
    <h3>Actuar</h3>
    <p>El agente usa una herramienta: corre un comando, edita un archivo, llama a una API, lee un directorio. La acción produce un efecto en el entorno.</p>
    <p class="s2-produces">Produce: un cambio en el entorno — algo que antes no era verdad, ahora lo es.</p>
  </div>
  <div class="s2-phase-card s2-phase-card-stage observar fragment current-visible" data-phase-card="observar">
    <h3>Observar</h3>
    <p>El agente lee el resultado de la acción: el output del comando, el contenido del archivo, la respuesta HTTP. Eso nuevo entra a su contexto y alimenta la próxima vuelta de pensar.</p>
    <p class="s2-produces">Produce: información nueva en el contexto — el insumo de la siguiente vuelta.</p>
  </div>

  <aside class="notes">
    <p><strong>Cada press abajo cambia simultáneamente h2, fase iluminada en la animación, y card. Tres estados; entrar al slide ya es el primer estado (pensar). Señalar el nodo iluminado en cada estado.</strong></p>
    <p><u>Slide consolidado de las tres fases del loop. Reemplaza tres slides previos (Pensar/Actuar/Observar). La animación persiste; solo cambia la fase iluminada. El card de abajo se reemplaza también (no se acumula).</u></p>
    <p><em>"La primera fase se llama pensar. El agente recibe lo que hay en su contexto — el objetivo original, lo que observó en la vuelta anterior, la historia de lo que hizo — y razona sobre eso. No es lineal: no sigue un script. El modelo formula cuál es el próximo paso útil dado todo lo que sabe en ese momento. Qué hipótesis tiene, qué le falta ver, qué tiene sentido probar ahora. Lo que produce esta fase es una decisión: qué acción viene a continuación."</em></p>
    <p><em>"La segunda fase es actuar. Y acá hay algo importante: actuar no significa 'escribir texto'. Significa invocar una herramienta. Correr un comando en la terminal, editar un archivo, hacer una llamada HTTP, leer un directorio. La herramienta produce un efecto en el entorno. Algo que antes no era verdad, ahora lo es. El archivo tiene una línea nueva. El test corrió. El servidor respondió. Las tools en detalle las vemos en la siguiente sección — por ahora lo que importa es que actuar siempre toca algo concreto fuera del modelo."</em></p>
    <p><em>"Tercera fase: observar. El agente lee el resultado de lo que acaba de hacer. El output del comando, el contenido del archivo, el código HTTP de la respuesta. Todo eso entra a su contexto. Y eso es clave: no es que el agente 'vio' el resultado y lo olvidó. Lo que observa queda en la ventana, disponible para el próximo pensar. Eso es lo que hace que cada vuelta del loop sepa más que la anterior. Y después repite — hasta que una condición de corte decide que terminó. ¿Qué se ve cuando el loop completo trabaja sobre un problema real?"</em></p>
  </aside>
</section>
```

- [ ] **Step 3: Agregar CSS scoped en el `<style>` de §2** (para que el h2 y los cards no salten en altura entre fragments)

Localizar el `<style>` al principio de `_section-2.html` y agregar antes del cierre `</style>`:

```css
/* C1 — fases consolidadas: forzar min-height para evitar saltos */
.s2-h2-phase {
  min-height: 1.4em;
}
.s2-phase-card-stage {
  min-height: 200px;
}
/* Posicionar los h2 superpuestos: solo el current-visible se ve */
.reveal section .s2-h2-phase.fragment.current-visible {
  position: absolute;
  top: var(--s2-h2-top, 0);  /* sin offset — Reveal centra los slides */
  left: 0;
  right: 0;
  margin: 0;
}
/* Mantener el h2 base (sin .fragment) ocupando el slot de altura */
```

Nota: el manejo de h2 múltiples con `current-visible` puede requerir ajuste fino al verificar visualmente. Si el `position: absolute` causa problemas, alternativa: envolver los 3 h2 en un `<div class="s2-h2-stack">` con `position: relative` y `min-height` fijo, y los h2 hijos con `position: absolute; inset: 0;`.

- [ ] **Step 4: Agregar/modificar el init block de §2** (al final de `_section-2.html`)

Buscar el bloque init script de §2 (entre los marcadores `<!-- INIT-SCRIPTS-S2-START -->` y `<!-- INIT-SCRIPTS-S2-END -->`, o similar — chequear primero).

Run: `grep -n 'INIT-SCRIPTS' semanas/04/slides/_section-2.html`

Si existe, modificar el bloque para reemplazar las inicializaciones de `s2-loop-pensar`, `s2-loop-actuar`, `s2-loop-observar` por una sola inicialización + un listener:

```html
<!-- INIT-SCRIPTS-S2-START -->
<script>
  // ... otros inits existentes (s2-loop-intro, s2-loop-corte, s2-demo-steps, etc.) ...

  // C1 — Loop consolidado de las tres fases
  initFourLoop({ containerId: 's2-loop-phases', mode: 'intro', phase: 'pensar' });

  // Sync de phase con fragments
  Reveal.on('fragmentshown', function(e) {
    var phase = e.fragment.dataset.phaseH2 || e.fragment.dataset.phaseCard;
    if (phase && document.getElementById('s2-loop-phases')) {
      updateFourLoop({ containerId: 's2-loop-phases', mode: 'intro', phase: phase });
    }
  });

  Reveal.on('fragmenthidden', function(e) {
    // Al volver atrás: el current-visible anterior queda visible. Detectamos cuál es y aplicamos.
    var container = document.getElementById('s2-loop-phases');
    if (!container) return;
    var currentH2 = document.querySelector('.s2-h2-phase[data-phase-h2]:not(.fragment), .s2-h2-phase.fragment.visible.current-visible');
    var phase = currentH2 ? currentH2.dataset.phaseH2 : 'pensar';
    updateFourLoop({ containerId: 's2-loop-phases', mode: 'intro', phase: phase });
  });
</script>
<!-- INIT-SCRIPTS-S2-END -->
```

(Las inits originales para `s2-loop-pensar`, `s2-loop-actuar`, `s2-loop-observar` se borran porque esos containers ya no existen.)

- [ ] **Step 5: Regenerar y verificar**

Run: `node semanas/04/slides/_assemble.mjs`

Abrir browser en `http://localhost:3000/semanas/04/slides/`. Navegar a §2 (3ra sección).

Verificación específica:
- Al llegar al slide consolidado, debe verse: h2 "Pensar — formular el próximo paso", animación con PENSAR iluminado, card "Pensar" debajo.
- Press abajo: h2 cambia a "Actuar — usar una herramienta", nodo ACTUAR iluminado, card "Actuar".
- Press abajo: h2 "Observar — leer el resultado", nodo OBSERVAR iluminado, card "Observar".
- Press arriba dos veces: vuelve a pensar correctamente.
- Sin saltos verticales en la página al cambiar de fragment.
- No hay errores en consola.

- [ ] **Step 6: Commit**

```bash
git add semanas/04/slides/_section-2.html semanas/04/slides/index.html
git commit -m "feat(s04): consolidate §2 phase slides (Pensar/Actuar/Observar) into one"
```

---

## Phase 2 — C2: §5 modos de falla

Consolidar el slide de clickable-steps con los 4 modos + los 2 slides separados de animación (s5-loop-infinite, s5-loop-drift) en uno solo donde clickear un chip muta la animación al modo correspondiente.

### Task 2.1: Auditar el estado actual de §5

**Files:**
- Read: `semanas/04/slides/_section-5.html`

- [ ] **Step 1: Mapear los 7 slides actuales de §5**

Run: `grep -n '<section\|s5-loop-infinite\|s5-loop-drift\|s5-modes' semanas/04/slides/_section-5.html`

Anotar: qué slide tiene los chips clickeables, cuál tiene cada animación, qué textos/cards corresponden a cada modo.

- [ ] **Step 2: Leer el bloque de init de §5**

Run: `grep -n 'INIT-SCRIPTS\|initFourLoop\|s5-modes\|s5-loop' semanas/04/slides/_section-5.html`

Anotar las llamadas a `initFourLoop` para `s5-loop-infinite` y `s5-loop-drift`, y la setup de `clickable-steps` para `s5-modes`.

---

### Task 2.2: Borrar los 2 slides de animación dedicada en §5

**Files:**
- Modify: `semanas/04/slides/_section-5.html`

- [ ] **Step 1: Borrar las dos `<section>` que contienen `s5-loop-infinite` y `s5-loop-drift`**

Localizar y eliminar (con sus respectivas `<aside class="notes">`). Mantener todos los otros slides.

---

### Task 2.3: Modificar el slide de los 4 chips para que muestre la animación + detail

**Files:**
- Modify: `semanas/04/slides/_section-5.html`

- [ ] **Step 1: Localizar el slide con `<div id="s5-modes"></div>`**

Es el slide que renderiza los 4 chips clickeables. Buscar la `<section>` que lo contiene.

- [ ] **Step 2: Modificar la estructura del slide**

Reemplazar el contenido del slide (entre `<section>` y `</section>`) con:

```html
<section data-loop-mode="intro" data-loop-phase="none">
  <h2>Cuatro modos de falla nuevos</h2>

  <div class="s5-modes-layout">
    <div id="s5-modes" class="s5-modes-chips"></div>
    <div id="s5-loop" class="s5-loop-host"></div>
  </div>

  <div id="s5-mode-detail" class="s5-mode-detail">
    <p class="s5-mode-detail-placeholder">Click en un modo para ver cómo se manifiesta en el loop.</p>
  </div>

  <aside class="notes">
    <p><strong>Click en cada chip muestra la animación del loop en ese modo de falla y un detalle conceptual. Clickear modos en cualquier orden — el orden narrativo es: loop infinito → deriva → alucinar tools → envenenar contexto, pero podés ir libre.</strong></p>
    <p><u>Slide consolidado de los 4 modos. Cada modo tiene su animación y su mini-card de descripción; el alumno puede explorar libremente.</u></p>
    <p><em>"Cuando el modelo solo sugería, el peor caso era una sugerencia mala — la rechazabas y listo. Cuando el agente actúa sobre tu repo, el peor caso es un entorno que ya cambió. Hay cuatro modos de falla nuevos que tenés que reconocer, cada uno conectado a una pieza que ya vimos."</em></p>
    <p><em>"Loop infinito: ninguna de las condiciones de corte se cumple. El agente sigue girando vuelta tras vuelta sin converger. Es la falla del §2 — sin condición de corte, el loop no termina."</em></p>
    <p><em>"Deriva de objetivo: el agente arrancó persiguiendo A pero terminó haciendo otra cosa. La instrucción original quedó sepultada en observaciones más recientes; el modelo perdió de vista por qué empezó."</em></p>
    <p><em>"Alucinar tools o resultados: la alucinación que conocíamos de la semana 1 ahora actúa sobre una premisa falsa. El agente fabrica una tool que no existe, fabrica un resultado que no recibió, y sigue actuando como si fuera real."</em></p>
    <p><em>"Envenenar el propio contexto: la versión activa del context rot del §4. El agente lee basura, lee más basura para responder a la basura, y termina alimentando su propio rot. Cuando algo falla así, no le creés a la IA, creés a la máquina: ¿el archivo cambió de verdad? ¿el test corre de verdad?"</em></p>
  </aside>
</section>
```

- [ ] **Step 3: Agregar CSS scoped al inicio de `_section-5.html`**

Dentro del `<style>` de §5, agregar:

```css
.s5-modes-layout {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: var(--spacing-md);
  align-items: start;
  margin-top: var(--spacing-md);
}
.s5-modes-chips {
  /* Container para los chips clickeables del clickable-steps */
}
.s5-loop-host {
  /* Container para la animación del loop */
}
.s5-mode-detail {
  margin-top: var(--spacing-md);
  min-height: 80px;
  padding: var(--spacing-sm);
  background: var(--bg-secondary);
  border-radius: 8px;
}
.s5-mode-detail-placeholder {
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
}
```

- [ ] **Step 4: Modificar el init block de §5**

Buscar el bloque INIT-SCRIPTS de §5 y reemplazar las llamadas a `initFourLoop({ containerId: 's5-loop-infinite', ... })` y `'s5-loop-drift'` por una sola inicialización del nuevo host:

```html
<!-- INIT-SCRIPTS-S5-START -->
<script>
  // Init de la animación principal en modo neutro
  initFourLoop({ containerId: 's5-loop', mode: 'intro' });

  // Mapping de modo de falla a config de la animación + texto detail
  var s5ModeMap = {
    'loop-infinito': {
      mode: 'infinite',
      title: 'Loop infinito',
      body: 'Ninguna condición de corte del §2 se cumple. El agente sigue girando vuelta tras vuelta sin converger.'
    },
    'deriva': {
      mode: 'drift',
      title: 'Deriva de objetivo',
      body: 'Arrancó persiguiendo A pero terminó en otra cosa. La instrucción original quedó sepultada en observaciones más recientes.'
    },
    'alucinar-tools': {
      mode: 'hallucinate',
      title: 'Alucinar tools/resultados',
      body: 'La alucinación de S1 ahora actúa sobre la premisa falsa: el agente fabrica una tool o un resultado y sigue como si fuera real.'
    },
    'envenenar-contexto': {
      mode: 'poison',
      title: 'Envenenar el contexto',
      body: 'La versión activa del context rot del §4. El agente lee basura, lee más basura para responder, alimenta su propio rot.'
    }
  };

  // Init de los chips clickeables (clickable-steps API ya existente)
  // NOTA: clickable-steps API exacta debe inspeccionarse — esta es la forma esperada.
  initClickableSteps({
    containerId: 's5-modes',
    steps: [
      { id: 'loop-infinito', label: 'Loop infinito' },
      { id: 'deriva', label: 'Deriva de objetivo' },
      { id: 'alucinar-tools', label: 'Alucinar tools' },
      { id: 'envenenar-contexto', label: 'Envenenar contexto' }
    ],
    onSelect: function(stepId) {
      var config = s5ModeMap[stepId];
      if (!config) return;
      updateFourLoop({ containerId: 's5-loop', mode: config.mode });
      var detail = document.getElementById('s5-mode-detail');
      if (detail) {
        detail.innerHTML = '<h4 style="margin:0 0 var(--spacing-xs); color:var(--accent);">' +
          config.title + '</h4><p style="margin:0;">' + config.body + '</p>';
      }
    },
    onDeselect: function() {
      updateFourLoop({ containerId: 's5-loop', mode: 'intro' });
      var detail = document.getElementById('s5-mode-detail');
      if (detail) {
        detail.innerHTML = '<p class="s5-mode-detail-placeholder">Click en un modo para ver cómo se manifiesta en el loop.</p>';
      }
    }
  });
</script>
<!-- INIT-SCRIPTS-S5-END -->
```

- [ ] **Step 5: Verificar la API real de `clickable-steps.js`**

Run: `cat semanas/04/slides/clickable-steps.js`

Si la API expuesta no coincide con `initClickableSteps({ containerId, steps, onSelect, onDeselect })` — adaptar al patrón real. Probablemente sea una función global tipo `setupClickableSteps(elementId, options)`. Ajustar el código del Step 4 a esa firma exacta.

- [ ] **Step 6: Regenerar y verificar**

Run: `node semanas/04/slides/_assemble.mjs`

Abrir browser en §5 (5ta sección). Verificación:
- Slide muestra h2 + 4 chips a la izquierda + animación del loop en intro a la derecha + detail vacío con placeholder.
- Click en "Loop infinito" → animación entra a modo infinite (arco de retorno engrosado/pulsante), detail muestra título "Loop infinito" y descripción.
- Click en "Deriva" → animación entra a modo drift (PENSAR muestra "objetivo: A → tarea B" tachado), detail actualizado.
- Click en "Alucinar tools" → animación a modo hallucinate (actuar/observar en rojo).
- Click en "Envenenar contexto" → animación a modo poison (chips rojos en la barra).
- Click en el chip activo (deselect) → animación vuelve a intro, detail vuelve a placeholder.
- Sin errores en consola.

- [ ] **Step 7: Commit**

```bash
git add semanas/04/slides/_section-5.html semanas/04/slides/index.html
git commit -m "feat(s04): consolidate §5 failure modes (4 modes click-to-show)"
```

---

## Phase 3 — C3: §4 fill + números + rot

Consolidar §4.3 (loop fill anim) + §4.4 (token numbers table) + §4.6 (rot diagram) en 2 slides (no 1 — el rot merece su momento).

### Task 3.1: Auditar el estado actual de §4

**Files:**
- Read: `semanas/04/slides/_section-4.html`

- [ ] **Step 1: Mapear los slides afectados**

Run: `grep -n '<section\|s4-loop-fill\|s4-token\|s4-rot' semanas/04/slides/_section-4.html`

Confirmar que los 3 slides están donde el spec asume: §4.3 (fill anim), §4.4 (numbers table), §4.6 (rot diagram).

---

### Task 3.2: Modificar §4.3 para slide A consolidado (fill + numbers como anotaciones)

**Files:**
- Modify: `semanas/04/slides/_section-4.html`

- [ ] **Step 1: Reemplazar el slide §4.3 con la versión consolidada**

```html
<!-- §4.3 · Slide A: El loop llena la ventana (con números como anotaciones reveladas) -->
<section data-loop-mode="fill" data-loop-phase="none">
  <h2>El loop llena la ventana</h2>

  <div class="s4-fill-layout">
    <div id="s4-loop-fill" class="s4-fill-anim"></div>

    <div class="s4-token-annotations">
      <div class="s4-token-anno fragment" data-fill="20">
        <span class="s4-token-anno-val">300 líneas ≈ 1.5–2.5k tokens</span>
        <span class="s4-token-anno-label">un archivo típico</span>
      </div>
      <div class="s4-token-anno fragment" data-fill="60">
        <span class="s4-token-anno-val">20 archivos ≈ 30–50k tokens</span>
        <span class="s4-token-anno-label">solo en observaciones</span>
      </div>
      <div class="s4-token-anno fragment" data-fill="95">
        <span class="s4-token-anno-val">ventana útil ≈ 200k tokens</span>
        <span class="s4-token-anno-label">una sesión larga la consume</span>
      </div>
    </div>
  </div>

  <aside class="notes">
    <p><strong>Slide A de §4: la barra se llena animadamente al revelarse cada anotación. Tres reveals: 20% (un archivo), 60% (20 archivos), 95% (cerca del límite). Cada reveal hace crecer la barra y muestra el número.</strong></p>
    <p><u>Consolidación de §4.3 (animación fill) + §4.4 (tabla de números). Los números son ahora anotaciones sobre el bar, no una tabla aparte.</u></p>
    <p><em>"Fijense en la barra de la ventana de contexto. Arranca casi vacía. Cada vuelta del loop agrega tokens. Un pensamiento del modelo: tokens. Una llamada a herramienta: tokens. La respuesta de esa herramienta: tokens. Todo se apila."</em></p>
    <p><em>"Pongámosle números: un archivo de código de tamaño mediano — 300 líneas con comentarios — ocupa entre 1.500 y 2.500 tokens. Parece chico."</em></p>
    <p><em>"Pero leé veinte archivos de ese tamaño — y en una sesión real leés veinte archivos sin darte cuenta — y ya gastaste entre 30.000 y 50.000 tokens solo en observaciones. Sin contar los pensamientos del modelo. Sin contar los logs de herramientas."</em></p>
    <p><em>"Los modelos actuales tienen ventanas que rondan los 200.000 tokens. En una sesión larga, la ventana se consume más rápido de lo que intuís. Ese es el punto."</em></p>
  </aside>
</section>
```

- [ ] **Step 2: Eliminar el slide §4.4 (numbers table standalone)**

Borrar la `<section>` que contiene `s4-token-numbers` y su respectiva `<aside class="notes">`.

- [ ] **Step 3: Agregar CSS scoped al `<style>` de §4**

```css
.s4-fill-layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: var(--spacing-lg);
  align-items: center;
  margin-top: var(--spacing-md);
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}
.s4-fill-anim { /* la animación */ }
.s4-token-annotations {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}
.s4-token-anno {
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--bg-secondary);
  border-left: 3px solid var(--accent);
  border-radius: 6px;
}
.s4-token-anno-val {
  display: block;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 700;
}
.s4-token-anno-label {
  display: block;
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 4px;
}
```

- [ ] **Step 4: Modificar el init block de §4**

```html
<!-- INIT-SCRIPTS-S4-START -->
<script>
  // Otros inits existentes (s4-demo-steps si existe, etc.) ...

  // Slide A: fill anim arranca en 10% (casi vacía); crece al revelarse cada anotación
  initFourLoop({ containerId: 's4-loop-fill', mode: 'fill', fillPercent: 10 });

  Reveal.on('fragmentshown', function(e) {
    if (e.fragment.dataset.fill) {
      var pct = parseInt(e.fragment.dataset.fill, 10);
      updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill', fillPercent: pct });
    }
  });

  Reveal.on('fragmenthidden', function(e) {
    // Al volver atrás, recalcular el nivel
    var visibleFills = document.querySelectorAll('.s4-token-anno.visible[data-fill]');
    var maxPct = 10;
    visibleFills.forEach(function(el) {
      var pct = parseInt(el.dataset.fill, 10);
      if (pct > maxPct) maxPct = pct;
    });
    updateFourLoop({ containerId: 's4-loop-fill', mode: 'fill', fillPercent: maxPct });
  });
</script>
<!-- INIT-SCRIPTS-S4-END -->
```

- [ ] **Step 5: Regenerar y verificar slide A**

Run: `node semanas/04/slides/_assemble.mjs`

Browser en §4. Navegar al slide A. Verificación:
- Al cargar: barra a ~10% (casi vacía); 3 anotaciones a la derecha, todas ocultas.
- Press abajo: anotación "300 líneas ≈ 1.5–2.5k tokens" aparece + barra crece a 20% (con transición animada de ~600ms).
- Press abajo: aparece "20 archivos ≈ 30–50k tokens" + barra a 60%.
- Press abajo: aparece "ventana útil ≈ 200k" + barra a 95%.
- Press arriba: la anotación más reciente se oculta + barra reduce.

---

### Task 3.3: Modificar §4.6 para slide B consolidado (fill final + rot)

**Files:**
- Modify: `semanas/04/slides/_section-4.html`

- [ ] **Step 1: Modificar el slide §4.6 (rot diagram)**

Mantener la estructura del rot diagram existente pero agregar al inicio del slide la barra de fill en estado lleno (no animado — es el "estado final" implícito desde el slide A).

```html
<!-- §4.6 · Slide B: Context rot — la ventana llena empieza a trabajar contra vos -->
<section data-loop-mode="fill" data-loop-phase="none">
  <h2>Context rot — cómo ocurre</h2>

  <div class="s4-rot-with-fill">
    <div id="s4-rot-fill-final" class="s4-rot-fill-anchor"></div>
    <div class="s4-rot-diagram">
      <!-- (Mantener el contenido existente del rot-diagram aquí) -->
    </div>
  </div>

  <p style="text-align:center;margin-top:16px;font-size:0.72em;color:var(--text-muted);font-style:italic;">
    la instrucción no desapareció — pero la señal se diluyó en el ruido
  </p>

  <aside class="notes">
    <!-- (Mantener las notes existentes del rot diagram) -->
  </aside>
</section>
```

(El bloque `s4-rot-diagram` interno se conserva del slide original.)

- [ ] **Step 2: Agregar CSS para el layout de slide B**

```css
.s4-rot-with-fill {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: var(--spacing-md);
  align-items: start;
}
.s4-rot-fill-anchor {
  /* Animación del fill en estado final */
}
```

- [ ] **Step 3: Init de la barra fill en estado final**

Agregar al INIT-SCRIPTS-S4:

```js
initFourLoop({ containerId: 's4-rot-fill-final', mode: 'fill', fillPercent: 95 });
```

- [ ] **Step 4: Verificar slide B**

Browser en §4 slide B (después del slide A consolidado). Verificación:
- A la izquierda: animación del loop con barra llena al 95% (estado de salida del slide A).
- A la derecha: rot diagram con las capas (instrucción enterrada en la base, observaciones encima).
- El caption sobre la "señal diluida" está debajo.

- [ ] **Step 5: Commit**

```bash
git add semanas/04/slides/_section-4.html semanas/04/slides/index.html
git commit -m "feat(s04): consolidate §4 fill + numbers into one anim, slide B keeps rot"
```

---

## Phase 4 — C4: Tricotomía — auditar y limpiar

La infraestructura `.tricotomia` con `.show-1/2/3` ya existe en `_scaffold.html` y ya se usa en §4 (show-1), §8 (show-2), §9 (show-3). El trabajo es identificar si hay slides redundantes que también muestran la tabla y eliminarlos.

### Task 4.1: Auditar slides de tricotomía

**Files:**
- Read: `semanas/04/slides/_section-4.html`, `_section-8.html`, `_section-9.html`

- [ ] **Step 1: Encontrar todas las apariciones**

Run: `grep -n 'class="tricotomia' semanas/04/slides/_section-*.html`

Esperado: §4 una vez (show-1), §8 una vez (show-2), §9 una vez (show-3).

- [ ] **Step 2: Si hay slides adicionales en §4 o §9 que muestren tricotomía repetida**

Por ejemplo, si §9 tiene dos slides — uno con show-2 y otro con show-3 — el primero es redundante (ya viene de §8 con show-2). Eliminar el redundante. Lo mismo en §4 si hay un slide solo de "adelanto" además del show-1 ya integrado.

Run: `grep -B 5 'class="tricotomia' semanas/04/slides/_section-4.html` para ver el contexto.

Si la auditoría confirma que cada sección usa la tricotomía solo una vez y en el `.show-N` correcto, **no hay slides para eliminar**. Saltar al Task 4.2.

---

### Task 4.2: Verificar coherencia visual entre §4 / §8 / §9

**Files:**
- Read: regenerated `index.html`

- [ ] **Step 1: Regenerar y abrir browser**

Run: `node semanas/04/slides/_assemble.mjs`

- [ ] **Step 2: Verificar visualmente**

Navegar a §4 — la tricotomía aparece con los tres rótulos visibles, columnas 2-3 dimmed (show-1).

Navegar a §8 — la tricotomía aparece con filas 1-2 completas iluminadas, fila 3 solo con rótulo iluminado (show-2).

Navegar a §9 — la tricotomía aparece con las 3 filas completamente iluminadas (show-3).

Las tres apariciones tienen idéntica geometría (mismas columnas, misma altura por fila). La transición show-1 → show-2 → show-3 leída en orden cuenta la historia.

- [ ] **Step 3: Si todo se ve bien, no hay commit que hacer en esta phase**

Si en Task 4.1 se identificaron y eliminaron slides redundantes, el commit va acá:

```bash
git add semanas/04/slides/_section-*.html semanas/04/slides/index.html
git commit -m "fix(s04): remove redundant tricotomía slides — cross-section progression"
```

Si no se eliminó nada, no se hace commit en Phase 4.

---

## Phase 5 — C5: Tracker — eliminar openers redundantes, wire flip animado

El `.lens-tracker` ya existe con `.on-loop` / `.on-context` y CSS transitions (300ms). Cada sección §7-§11 hoy tiene un slide opener dedicado al tracker. El trabajo: (a) eliminar el opener cuando sea posible mergeando al primer slide de contenido, (b) wire un toggle de clase animado para el flip en §11.

### Task 5.1: Auditar el opener de cada sección §7-§11

**Files:**
- Read: `_section-7.html`, `_section-8.html`, `_section-9.html`, `_section-10.html`, `_section-11.html`

- [ ] **Step 1: Para cada sección, identificar el opener y el primer slide de contenido**

Run: `grep -n 'Opener\|<section\|lens-tracker' semanas/04/slides/_section-{7,8,9,10,11}.html`

Para cada sección, anotar:
- Líneas del opener.
- Líneas del primer slide de contenido.
- Si el opener tiene contenido más allá del tracker + sub-label + un hook narrativo, o si es minimalista (solo tracker + sub-label).

- [ ] **Step 2: Decidir si el merge es viable por sección**

Si el opener tiene mucho contenido propio (hook largo, key analogy), no mergear — dejarlo como está. Eliminar solo los openers minimalistas.

Output esperado de la auditoría: tabla por sección "opener: keep / merge / delete" con justificación corta.

---

### Task 5.2: Aplicar la decisión de merge por sección

**Files:**
- Modify: el `_section-N.html` correspondiente

Para cada sección donde la decisión sea "merge":

- [ ] **Step 1: Mover el `<div class="lens-tracker on-context">` al inicio del primer slide de contenido**

Como header del slide, antes del `<h2>`. Mantener el `sub-label` que está debajo del tracker.

- [ ] **Step 2: Eliminar la `<section>` opener completa**

Incluyendo su `<aside class="notes">`.

- [ ] **Step 3: Mover/mergear las speaker notes del opener al primer slide de contenido**

Como el opener no tenía reveals propios, su `<em>` block se prepend al primer `<em>` del primer slide de contenido.

---

### Task 5.3: Wire flip animado en §11

**Files:**
- Modify: `semanas/04/slides/_section-11.html`

- [ ] **Step 1: Modificar el opener de §11 para arrancar en `on-context`**

El slide opener actual de §11 tiene `<div class="lens-tracker on-loop">` directamente. Cambiar a:

```html
<div class="lens-tracker on-context" id="s11-tracker">
  <div class="pole pole-context">CONTEXTO</div>
  <div class="lens-sep">↔</div>
  <div class="pole pole-loop">LOOP</div>
</div>
<p class="sub-label">hasta acá, todo aterrizó acá</p>

<!-- Fragment trigger invisible que dispara el flip -->
<div class="fragment" data-flip-tracker="loop" data-sub-label="control del flujo" aria-hidden="true"></div>
```

(Ajustar la estructura DOM al patrón exacto que el opener tiene hoy.)

- [ ] **Step 2: Wire el listener en el init block de §11**

```html
<!-- INIT-SCRIPTS-S11-START -->
<script>
  // Otros inits existentes ...

  Reveal.on('fragmentshown', function(e) {
    if (e.fragment.dataset.flipTracker) {
      var tracker = document.getElementById('s11-tracker');
      if (!tracker) return;
      setTimeout(function() {
        tracker.classList.remove('on-context');
        tracker.classList.add('on-loop');
        // Update sub-label si existe el elemento
        var sub = tracker.parentElement.querySelector('.sub-label');
        if (sub) sub.textContent = e.fragment.dataset.subLabel || sub.textContent;
      }, 200);
    }
  });

  Reveal.on('fragmenthidden', function(e) {
    if (e.fragment.dataset.flipTracker) {
      var tracker = document.getElementById('s11-tracker');
      if (!tracker) return;
      tracker.classList.remove('on-loop');
      tracker.classList.add('on-context');
      var sub = tracker.parentElement.querySelector('.sub-label');
      if (sub) sub.textContent = 'hasta acá, todo aterrizó acá';
    }
  });
</script>
<!-- INIT-SCRIPTS-S11-END -->
```

- [ ] **Step 3: Regenerar y verificar el flip**

Run: `node semanas/04/slides/_assemble.mjs`

Browser en §11 slide opener:
- Al cargar: tracker con CONTEXTO iluminado, sub-label "hasta acá, todo aterrizó acá".
- Press abajo (revela el fragment trigger): después de ~200ms, transición CSS de 300ms — CONTEXTO se apaga, LOOP se enciende, sub-label cambia a "control del flujo".
- Press arriba: vuelta a contexto.
- La transición debe verse explícitamente (no es un cambio instantáneo).

- [ ] **Step 4: Commit**

```bash
git add semanas/04/slides/_section-*.html semanas/04/slides/index.html
git commit -m "feat(s04): merge tracker openers, animate flip in §11"
```

---

## Phase 6 — C6: Loop persistente en Parte 1

El cambio más invasivo. Migrar todos los slides de §2-§6 que montan la animación a un patrón "logically persistent": un único container `#part1-loop` declarado en el scaffold, posicionado igual en cada slide, y un init script global que escucha `slidechanged` y mutate la animación según `data-loop-mode` / `data-loop-phase` del `<section>` activo.

### Task 6.1: Agregar el host `#part1-loop` y el sync script al scaffold

**Files:**
- Modify: `semanas/04/slides/_scaffold.html`

- [ ] **Step 1: Agregar CSS para el host en el `<style>` del scaffold**

```css
/* C6 — Part 1 loop animation host (logically persistent across §2-§6) */
.part1-loop-host {
  position: relative;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: var(--spacing-md) auto;
  max-width: 760px;
}
.part1-loop-host[hidden] {
  display: none;
}
```

- [ ] **Step 2: Agregar el sync script al final del scaffold**

Inmediatamente después del bloque `Reveal.initialize(...)`:

```html
<script>
  // C6 — Sincronizar la animación del loop con data-loop-mode/data-loop-phase del slide activo
  (function() {
    var part1Initialized = false;

    function syncPart1Loop() {
      var slide = Reveal.getCurrentSlide();
      if (!slide) return;
      var mode  = slide.dataset.loopMode;
      var phase = slide.dataset.loopPhase || 'none';
      var fillPercent = slide.dataset.loopFill ? parseInt(slide.dataset.loopFill, 10) : undefined;
      var host  = document.getElementById('part1-loop');
      if (!host) return;

      if (!mode) {
        // Este slide no usa la animación
        host.hidden = true;
        return;
      }

      host.hidden = false;
      var opts = {
        containerId: 'part1-loop',
        mode: mode,
        phase: phase === 'none' ? undefined : phase
      };
      if (fillPercent !== undefined) opts.fillPercent = fillPercent;

      if (!part1Initialized) {
        window.initFourLoop(opts);
        part1Initialized = true;
      } else {
        window.updateFourLoop(opts);
      }
    }

    Reveal.on('ready', syncPart1Loop);
    Reveal.on('slidechanged', syncPart1Loop);
  })();
</script>
```

- [ ] **Step 3: Verificar que el scaffold sigue siendo válido**

Run: `node semanas/04/slides/_assemble.mjs`

El assembly debe completar sin warnings.

- [ ] **Step 4: Smoke en browser**

Abrir browser. El deck debe cargar sin errores. Los slides existentes que tienen sus propias instancias de `four-loop` (s2-loop-intro, s2-loop-corte, etc.) siguen funcionando — el host `#part1-loop` no se interpone porque ningún slide lo tiene todavía.

---

### Task 6.2: Migrar §2 a usar `#part1-loop` (slides intro + corte)

**Files:**
- Modify: `semanas/04/slides/_section-2.html`

§2 tiene actualmente animaciones en: `s2-loop-intro` (slide "no da una respuesta — entra en loop"), `s2-loop-phases` (consolidado de C1), `s2-loop-corte` (slide de condiciones de corte).

Decisión: el slide consolidado de C1 (`s2-loop-phases`) **mantiene su container propio** porque tiene lógica de fragment-driven phase sync local. Solo migramos `s2-loop-intro` y `s2-loop-corte` a usar `#part1-loop`.

- [ ] **Step 1: En el slide "No da una respuesta: entra en un loop" (§2.2)**

Reemplazar:
```html
<div class="s2-loop-wrap">
  <div id="s2-loop-intro"></div>
</div>
```

por:
```html
<div class="part1-loop-host">
  <div id="part1-loop"></div>
</div>
```

Agregar al `<section>` los data attrs:
```html
<section data-loop-mode="intro" data-loop-phase="none">
```

- [ ] **Step 2: En el slide "Condiciones de corte" (§2.10)**

Reemplazar:
```html
<div class="s2-loop-wrap" style="margin-bottom:0;">
  <div id="s2-loop-corte"></div>
</div>
```

por la misma estructura `part1-loop-host` y agregar `data-loop-mode="intro"` al `<section>`. El "corte" se cuenta visualmente con los chips de salida que `renderIntro` ya muestra; no necesita un mode dedicado.

- [ ] **Step 3: Borrar las llamadas `initFourLoop({ containerId: 's2-loop-intro' ... })` y `'s2-loop-corte'` del init block de §2**

(El init de `s2-loop-phases` se mantiene.)

- [ ] **Step 4: Modificar también el `<section>` de §2.2 caption (regla nueva)**

Eliminar el texto "La firma de la semana." del caption. El caption queda:

```html
<p style="text-align:center;margin-top:18px;font-size:0.78em;color:var(--text-muted);font-style:italic;">
  Todo lo que sigue actúa sobre este ciclo.
</p>
```

- [ ] **Step 5: Regenerar y verificar**

Run: `node semanas/04/slides/_assemble.mjs`

Browser:
- §2 slide intro: animación se ve en el slot `part1-loop`. Cambio visualmente imperceptible vs antes.
- §2 slide consolidado (C1): la animación es la del container local `s2-loop-phases` — no afecta a `part1-loop`.
- §2 slide condiciones de corte: animación en `part1-loop`.
- Sin errores en consola.

- [ ] **Step 6: Commit**

```bash
git add semanas/04/slides/_section-2.html semanas/04/slides/index.html
git commit -m "feat(s04): migrate §2 intro+corte loops to persistent host"
```

---

### Task 6.3: Migrar §3 a usar `#part1-loop`

**Files:**
- Modify: `semanas/04/slides/_section-3.html`

- [ ] **Step 1: Encontrar el slide que monta `s3-loop-tool`**

Run: `grep -n 's3-loop-tool\|<section' semanas/04/slides/_section-3.html`

- [ ] **Step 2: Reemplazar el container por `part1-loop-host`**

Reemplazar el `<div>` que contiene `s3-loop-tool` por:

```html
<div class="part1-loop-host">
  <div id="part1-loop"></div>
</div>
```

- [ ] **Step 3: Agregar data attrs al `<section>`**

```html
<section data-loop-mode="tool" data-loop-phase="none">
```

- [ ] **Step 4: Borrar la llamada `initFourLoop({ containerId: 's3-loop-tool' ... })` del init de §3**

- [ ] **Step 5: Regenerar y verificar §3**

Run: `node semanas/04/slides/_assemble.mjs`

Browser §3: animación con actuar+observar iluminados en --accent-secondary, "(llamada)" y "(resultado)" como sublabels — idéntica visualmente al `renderTool` original.

- [ ] **Step 6: Commit**

```bash
git add semanas/04/slides/_section-3.html semanas/04/slides/index.html
git commit -m "feat(s04): migrate §3 tool loop to persistent host"
```

---

### Task 6.4: Migrar §4 a usar `#part1-loop`

**Files:**
- Modify: `semanas/04/slides/_section-4.html`

§4 tiene `s4-loop-fill` (slide A consolidado de C3) y `s4-rot-fill-final` (slide B). Ambos son fill mode con distinto fillPercent.

Decisión: el slide A (fill animado con fragment-driven fillPercent) tiene lógica local — mantiene su container `s4-loop-fill`. El slide B (rot diagram con fill estático) se puede migrar a `part1-loop` con `data-loop-mode="fill" data-loop-fill="95"`.

- [ ] **Step 1: En el slide B (§4.6), reemplazar `s4-rot-fill-final` por `part1-loop`**

Reemplazar la estructura:
```html
<div id="s4-rot-fill-final" class="s4-rot-fill-anchor"></div>
```
por:
```html
<div class="part1-loop-host s4-rot-fill-anchor">
  <div id="part1-loop"></div>
</div>
```

(Y agregar `data-loop-mode="fill" data-loop-fill="95"` al `<section>` de slide B.)

- [ ] **Step 2: Borrar la llamada `initFourLoop({ containerId: 's4-rot-fill-final' ... })` del init de §4**

- [ ] **Step 3: Regenerar y verificar §4 slide B**

Browser §4 slide B: barra al 95% (lleno) a la izquierda del rot diagram.

**Nota importante:** cuando se navega del slide A (que usa `s4-loop-fill`) al slide B (que ahora usa `part1-loop`), la barra "salta" de un container a otro porque son DOM nodes distintos. Es aceptable — el slide A tiene fill dinámico fragment-driven, no se puede mergear con el sync slide-level de `part1-loop` sin perder esa funcionalidad.

- [ ] **Step 4: Commit**

```bash
git add semanas/04/slides/_section-4.html semanas/04/slides/index.html
git commit -m "feat(s04): migrate §4 slide B rot fill to persistent host"
```

---

### Task 6.5: Migrar §5 a usar `#part1-loop`

**Files:**
- Modify: `semanas/04/slides/_section-5.html`

§5 después de C2 tiene `s5-loop` (la animación que muta con click en chips). Esta tiene lógica de click handlers — **mantener container local `s5-loop`**, no migrar.

- [ ] **Step 1: Confirmar que no quedan otros mounts de loop en §5**

Run: `grep -n 'initFourLoop\|four-loop' semanas/04/slides/_section-5.html`

Debe aparecer solo `s5-loop` (post-C2). No hay migración que hacer en §5.

---

### Task 6.6: Migrar §6 a usar `#part1-loop`

**Files:**
- Modify: `semanas/04/slides/_section-6.html`

§6 monta `s6-loop-cc` (el loop con labels de Claude Code: Edit/Bash/Read).

- [ ] **Step 1: Encontrar el container actual**

Run: `grep -n 's6-loop-cc\|<section\|data-loop' semanas/04/slides/_section-6.html`

- [ ] **Step 2: Reemplazar por `part1-loop-host`**

```html
<div class="part1-loop-host">
  <div id="part1-loop"></div>
</div>
```

Y agregar `data-loop-mode="cc"` al `<section>`.

- [ ] **Step 3: Borrar la llamada `initFourLoop({ containerId: 's6-loop-cc' ... })` del init de §6**

- [ ] **Step 4: Regenerar y verificar §6**

Browser §6 slide CC: animación con labels "(texto razonando)" / "(Edit · Bash · Read · Write)" / "(resultado)" en --accent.

- [ ] **Step 5: Commit**

```bash
git add semanas/04/slides/_section-6.html semanas/04/slides/index.html
git commit -m "feat(s04): migrate §6 CC loop to persistent host"
```

---

### Task 6.7: Recorrer Parte 1 completa para validar persistencia

**Files:**
- Read: `semanas/04/slides/index.html` (generated)

- [ ] **Step 1: Walkthrough completo §1 → §6**

Abrir browser en `http://localhost:3000/semanas/04/slides/`. Navegar slide por slide desde el comienzo hasta el final de §6.

Para cada slide donde se espera animación del loop en `part1-loop`:
- Animación aparece en el slot (posición consistente).
- Sin parpadeo notable al cambiar de slide.
- Modo y phase correctos (verificar contra los `data-loop-mode` / `data-loop-phase` del slide).

Para cada slide donde NO se espera animación:
- El host `#part1-loop` está oculto (`hidden`).

- [ ] **Step 2: Verificar consola**

No deben aparecer:
- "Cannot read property of null" (significa que el host no se encontró).
- "Renderer undefined" (significa que el `data-loop-mode` es inválido).

- [ ] **Step 3: Verificar conteo final de slides**

```bash
grep -c '^      <section\|^<section' semanas/04/slides/_section-*.html | awk -F: '{sum+=$2; print $0} END {print "TOTAL:", sum}'
```

Debe estar entre 95 y 100 (recordando que el conteo original era 115).

- [ ] **Step 4: No hay commit en esta task** (es solo validación)

---

## Phase 7 — Cierre y validación final

### Task 7.1: Recorrer el deck completo end-to-end

**Files:**
- Read: `semanas/04/slides/index.html`

- [ ] **Step 1: Walkthrough §1 → §12**

Navegar todo el deck. En cada sección, prestar atención a:
- §2: las tres fases consolidadas (1 slide en lugar de 3) — h2/animación/card sincronizados.
- §4: slide A con fill animado, slide B con rot.
- §5: click en cada uno de los 4 chips, animación cambia, detail aparece.
- §7-§11: tracker en cada sección, sub-label correcto. §11 flip animado.
- §4/§8/§9: tricotomía progresiva.

- [ ] **Step 2: Verificar speaker notes con `s`**

Abrir notes view con la tecla `s` en cada slide consolidado:
- §2 slide consolidado de fases: 3 `<em>` blocks (uno por estado).
- §5 slide consolidado de modos: 5 `<em>` blocks (intro + 4 modos).
- §4 slide A: 4 `<em>` blocks.

- [ ] **Step 3: Test con Spacebar (modo presentación lineal)**

Cerrar notes view, mover por el deck con Spacebar de principio a fin. Verificar que ningún fragment se queda colgado, ninguna animación falla.

---

### Task 7.2: Cleanup y documentación

**Files:**
- Modify: `semanas/04/spine.md` (opcional)

- [ ] **Step 1: Si el spine.md mencionaba slides eliminados por nombre**

Run: `grep -n '§2.4\|§2.5\|§4.4\|§5\.' semanas/04/spine.md`

Si las menciones a slides eliminados (§2.4, §2.5, §4.4) son obsoletas, dejar nota en el spine pero NO reescribir — el spine es histórico. El cambio se documenta en commits.

- [ ] **Step 2: Verificar git status final**

```bash
git status semanas/04/slides/ docs/superpowers/
```

Solo debe haber archivos modificados que ya se commitearon. No quedan untracked relevantes a esta consolidación.

- [ ] **Step 3: Verificar log**

```bash
git log --oneline -n 20
```

Esperado: una secuencia de commits con `feat(s04):` prefijo, uno por cada tarea con commit.

---

## Self-Review (post-write)

**Spec coverage:**
- C1 §2 fases → Phase 1 ✓
- C2 §5 modos → Phase 2 ✓
- C3 §4 fill+rot → Phase 3 ✓
- C4 tricotomía → Phase 4 (audit/cleanup) ✓
- C5 tracker → Phase 5 ✓
- C6 loop persistente → Phase 6 ✓
- Cambios base en four-loop-anim.js → Phase 0 ✓
- updateFourLoop API → Task 0.1 ✓
- renderHallucinate, renderPoison → Tasks 0.2, 0.3 ✓
- fillPercent parameter → Task 0.4 ✓
- §2.2 caption fix → incluido en Task 6.2 Step 4 ✓

**Type consistency:** `updateFourLoop`, `initFourLoop`, `data-loop-mode`, `data-loop-phase`, `data-loop-fill` se usan consistentemente. `data-phase-h2` / `data-phase-card` específico de C1.

**Riesgos abiertos:**
- API exacta de `clickable-steps.js` no verificada en este plan — Task 2.3 Step 5 fuerza la verificación antes de wireare.
- Posición CSS de los h2 múltiples con `current-visible` en C1 puede requerir ajuste fino (anotado en Task 1.2 Step 3).
- El "salto" entre containers distintos al pasar de slide A → slide B en §4 (Task 6.4 Step 3) es aceptable pero no ideal.

**Verificación pedida al usuario:** cada Phase tiene un commit y un walkthrough explícito. No hay tests automatizados — la verificación es visual en browser.
