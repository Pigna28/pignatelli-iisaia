import {api, csv, setCSRF} from './api.js';
import {$, notice, element, emptyTable, confirmDelete, bindForm, openForm} from './ui.js';
import {ThreadView, threadPath, statusBadge} from './thread-view.js';

const state = {chips: [], selected: null, macro: 'Tx', threads: [], canWrite: false, revision: 0, overview: null};
const current = () => state.chips.find(chip => chip.id === state.selected);
const basePath = () => `/chips/${state.selected}/macros/${state.macro}/threads`;
const handle = fn => async (...args) => {
  try { await fn(...args); } catch (error) { notice(error.message, true); }
};
const viewer = new ThreadView(() => state.canWrite, () => refresh());

function renderChips() {
  const query = $('#search').value.trim().toLocaleLowerCase();
  const chips = state.chips.filter(chip => `${chip.part_number} ${chip.board}`.toLocaleLowerCase().includes(query));
  const list = $('#chip-list'); list.replaceChildren(); list.setAttribute('aria-busy', 'false');
  for (const chip of chips) {
    const button = element('button', undefined, 'sample');
    button.setAttribute('aria-pressed', String(chip.id === state.selected));
    button.append(element('strong', chip.part_number), element('small', `${chip.board} · #${chip.id}`));
    button.onclick = handle(() => selectChip(chip.id)); list.append(button);
  }
  if (!chips.length) list.append(element('p', query ? 'No hay coincidencias.' : 'Todavía no hay muestras. Registrá la primera.', 'empty'));
}

async function selectChip(id, macro = state.macro) {
  state.selected = id; state.macro = macro; viewer.close();
  renderChips(); await loadThreads();
}

async function loadThreads() {
  const revision = ++state.revision, chip = current();
  state.threads = []; $('#export').disabled = true;
  $('#chip-title').textContent = chip ? chip.part_number : 'Seleccioná una muestra';
  $('#chip-meta').textContent = chip ? `${chip.board} · Muestra #${chip.id} · Ensamblado: ${chip.assembled_at || 'sin fecha'}` : 'Registrá una muestra para comenzar.';
  $('#delete-chip').disabled = !chip || !state.canWrite;
  $('#new-thread').disabled = !chip || !state.canWrite;
  $('#table-caption').textContent = `Hilos de ensayo de la macro ${state.macro}`;
  document.querySelectorAll('[data-macro]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.macro === state.macro)));
  $('#result-count').textContent = chip ? 'Cargando…' : 'Sin muestra seleccionada';
  if (!chip) { emptyTable('Elegí una muestra del inventario.'); return; }
  emptyTable('Cargando hilos…');
  try {
    const filter = $('#filter').value;
    const threads = await api(basePath() + (filter ? `?status=${filter}` : ''));
    if (revision !== state.revision) return;
    state.threads = threads; renderThreads();
  } catch (error) {
    if (revision !== state.revision) return;
    emptyTable('No se pudieron cargar los hilos. Usá Actualizar datos para reintentar.');
    $('#result-count').textContent = 'Datos no disponibles'; throw error;
  }
}

function renderThreads() {
  const list = $('#test-list'); list.replaceChildren();
  for (const thread of state.threads) {
    const row = element('tr'), title = element('td');
    const open = element('button', thread.title, 'thread-link');
    open.onclick = handle(() => viewer.open(thread)); title.append(open);
    const status = element('td'); status.append(statusBadge(thread.status));
    row.append(title, status, element('td', String(thread.step_count)), element('td', new Date(thread.created_at).toLocaleDateString('es-AR')));
    const action = element('td'), remove = element('button', 'Eliminar', 'danger');
    remove.disabled = !state.canWrite; remove.setAttribute('aria-label', `Eliminar hilo ${thread.title} #${thread.id}`);
    remove.onclick = handle(async () => {
      if (!await confirmDelete(`Se eliminará el hilo «${thread.title}», sus pasos y archivos.`)) return;
      remove.disabled = true;
      try { await api(threadPath(thread), {method: 'DELETE'}); viewer.close(); notice('Hilo eliminado. Se conservó la auditoría.'); await refresh(); }
      finally { remove.disabled = !state.canWrite; }
    });
    action.append(remove); row.append(action); list.append(row);
  }
  if (!state.threads.length) emptyTable('No hay hilos para esta macro y filtro.');
  $('#result-count').textContent = `${state.threads.length} hilo(s) en esta vista · Abrí un hilo para ver sus pasos`;
  $('#export').disabled = !state.threads.length;
}

let overviewRevision = 0;
const overviewTitles = {chips: 'Todas las muestras registradas', tests: 'Todos los ensayos realizados', passed: 'Ensayos aprobados', failed: 'Ensayos fallidos', in_progress: 'Ensayos en progreso'};
async function loadOverview() {
  const key = state.overview, revision = ++overviewRevision;
  if (!key) return;
  $('#overview-list').replaceChildren(element('p', 'Cargando listado…', 'empty'));
  const rows = await api(key === 'chips' ? '/chips' : '/threads' + (key === 'tests' ? '' : `?status=${key}`));
  if (revision !== overviewRevision || key !== state.overview) return;
  $('#overview-title').textContent = `${overviewTitles[key]} (${rows.length})`;
  $('#overview-list').replaceChildren(...rows.map(row => {
    const button = element('button', undefined, 'overview-item');
    button.append(element('strong', key === 'chips' ? row.part_number : row.title));
    button.append(element('small', key === 'chips' ? `${row.board} · Muestra #${row.id}` : `${row.part_number} #${row.chip_id} · ${row.board} · ${row.macro} · ${row.step_count} paso(s)`));
    if (key !== 'chips') button.append(statusBadge(row.status));
    button.onclick = handle(async () => {
      $('#search').value = ''; $('#filter').value = '';
      await selectChip(key === 'chips' ? row.id : row.chip_id, row.macro || 'Tx');
      if (key !== 'chips') await viewer.open(row);
      else { $('#workspace').scrollIntoView({behavior: 'smooth'}); $('#chip-title').focus(); }
    });
    return button;
  }));
  if (!rows.length) $('#overview-list').append(element('p', 'No hay registros en esta sección.', 'empty'));
}

async function refresh() {
  const [chips, summary] = await Promise.all([api('/chips'), api('/summary')]);
  state.chips = chips;
  if (!current()) state.selected = chips[0]?.id ?? null;
  for (const key of Object.keys(overviewTitles)) $(`#stat-${key}`).textContent = summary[key];
  renderChips(); await loadThreads();
  if (state.overview) await loadOverview();
  if ($('#audit-panel').open && state.canWrite) await loadAudit();
}

async function loadAudit() {
  const events = await api('/audit');
  const actions = {create: 'Alta', update: 'Actualización', delete: 'Baja'};
  const resources = {chip: 'muestra', test: 'medición histórica', thread: 'hilo', step: 'paso', attachment: 'evidencia'};
  $('#audit-list').replaceChildren(...events.map(event => element('li', `${new Date(event.occurred_at).toLocaleString('es-AR')} · ${actions[event.action]} de ${resources[event.resource]} #${event.resource_id} · ${event.actor}`)));
  if (!events.length) $('#audit-list').append(element('li', 'Sin operaciones registradas.'));
}

document.querySelectorAll('[data-overview]').forEach(button => {
  button.onclick = handle(async () => {
    state.overview = button.dataset.overview; $('#overview').hidden = false;
    document.querySelectorAll('[data-overview]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    $('#overview-title').textContent = overviewTitles[state.overview];
    $('#overview').scrollIntoView({behavior: 'smooth'}); $('#overview-title').focus();
    try { await loadOverview(); } catch (error) { $('#overview-list').replaceChildren(element('p', 'No se pudo cargar el listado. Usá Actualizar datos.', 'empty')); throw error; }
  });
});
$('#close-overview').onclick = () => {
  state.overview = null; overviewRevision++; $('#overview').hidden = true;
  document.querySelectorAll('[data-overview]').forEach(item => item.setAttribute('aria-pressed', 'false'));
};
$('#search').oninput = renderChips;
$('#refresh').onclick = handle(async () => { await refresh(); await viewer.reload(); });
$('#filter').onchange = handle(loadThreads);
document.querySelectorAll('[data-macro]').forEach(button => { button.onclick = handle(() => selectChip(state.selected, button.dataset.macro)); });
document.querySelectorAll('[data-close]').forEach(button => { button.onclick = () => button.closest('dialog').close(); });
$('#new-chip').onclick = () => openForm('#chip-dialog');
let threadTarget;
$('#new-thread').onclick = () => {
  threadTarget = basePath(); $('#thread-context').textContent = `${current().part_number} · ${current().board} · Macro ${state.macro}`;
  openForm('#thread-dialog');
};
bindForm('#chip-form', async data => {
  if (!data.assembled_at) delete data.assembled_at;
  const chip = await api('/chips', {method: 'POST', body: data});
  viewer.close(); state.selected = chip.id; $('#search').value = '';
  notice('Muestra registrada.'); await refresh().catch(error => notice(`Guardado confirmado. ${error.message}`, true));
});
bindForm('#thread-form', async data => {
  const thread = await api(threadTarget, {method: 'POST', body: data});
  $('#filter').value = ''; notice('Hilo creado en progreso. Agregá sus pasos y evidencias.');
  try { await refresh(); await viewer.open(thread, false); }
  catch (error) { notice(`Guardado confirmado. ${error.message}`, true); }
});
$('#delete-chip').onclick = handle(async () => {
  const chip = current();
  if (!await confirmDelete(`Se eliminará ${chip.part_number} #${chip.id}, TODOS sus hilos, pasos y archivos de Tx, Rx y PLL.`)) return;
  $('#delete-chip').disabled = true;
  try { await api(`/chips/${chip.id}`, {method: 'DELETE'}); viewer.close(); notice('Muestra y hilos eliminados. Se conservó la auditoría.'); await refresh(); }
  finally { $('#delete-chip').disabled = !current() || !state.canWrite; }
});
$('#export').onclick = () => {
  const url = URL.createObjectURL(new Blob([csv(state.threads)], {type: 'text/csv;charset=utf-8'}));
  const link = element('a'); link.href = url; link.download = `hilos-chip-${state.selected}-${state.macro}.csv`;
  link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
$('#refresh-audit').onclick = handle(loadAudit);
$('#audit-panel').addEventListener('toggle', handle(async () => { if ($('#audit-panel').open) await loadAudit(); }));
$('#logout').onclick = handle(async () => { const data = await api('/logout', {method: 'POST'}); window.location.assign(data.redirect); });
handle(async () => {
  const session = await api('/session'); setCSRF(session.csrf_token); state.canWrite = session.can_write;
  $('#identity').textContent = `${session.user.name} · ${state.canWrite ? 'Operador' : 'Lectura'}`;
  $('#mode').textContent = session.mode === 'local' ? 'Modo local · Sin identidad real' : 'Sesión Auth0 · Laboratorio compartido';
  $('#new-chip').disabled = !state.canWrite; $('#logout').disabled = false;
  $('#audit-panel').hidden = !state.canWrite; await refresh();
})();
