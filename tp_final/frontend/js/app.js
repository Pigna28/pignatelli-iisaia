import {api, csv, setCSRF} from "./api.js";
import {$, notice, element, emptyTable, confirmDelete, bindForm, openForm} from "./ui.js";

const state = {chips: [], selected: null, macro: "Tx", tests: [], canWrite: false, revision: 0};
const current = () => state.chips.find(chip => chip.id === state.selected);
const testPath = () => `/chips/${state.selected}/macros/${state.macro}/tests`;
const handle = fn => async (...args) => { try { await fn(...args); } catch (error) { notice(error.message, true); } };

function renderChips() {
  const query = $("#search").value.trim().toLocaleLowerCase();
  const chips = state.chips.filter(chip => `${chip.part_number} ${chip.board}`.toLocaleLowerCase().includes(query));
  const list = $("#chip-list"); list.replaceChildren(); list.setAttribute("aria-busy", "false");
  for (const chip of chips) {
    const button = element("button", undefined, "sample");
    button.setAttribute("aria-pressed", String(chip.id === state.selected));
    button.append(element("strong", chip.part_number), element("small", `${chip.board} · #${chip.id}`));
    button.onclick = handle(async () => { state.selected = chip.id; renderChips(); await loadTests(); });
    list.append(button);
  }
  if (!chips.length) list.append(element("p", query ? "No hay coincidencias." : "Todavía no hay muestras. Registrá la primera.", "empty"));
}

async function loadTests() {
  const revision = ++state.revision, chip = current();
  state.tests = []; $("#export").disabled = true;
  $("#chip-title").textContent = chip ? chip.part_number : "Seleccioná una muestra";
  $("#chip-meta").textContent = chip ? `${chip.board} · Muestra #${chip.id} · Ensamblado: ${chip.assembled_at || "sin fecha"}` : "Registrá una muestra para comenzar.";
  $("#delete-chip").disabled = !chip || !state.canWrite;
  $("#new-test").disabled = !chip || !state.canWrite;
  $("#table-caption").textContent = `Ensayos de la macro ${state.macro}`;
  document.querySelectorAll("[data-macro]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.macro === state.macro)));
  $("#result-count").textContent = chip ? "Cargando…" : "Sin muestra seleccionada";
  if (!chip) { emptyTable("Elegí una muestra del inventario."); return; }
  emptyTable("Cargando ensayos…");
  try {
    const filter = $("#filter").value;
    const tests = await api(testPath() + (filter ? `?passed=${filter}` : ""));
    if (revision !== state.revision) return;
    state.tests = tests; renderTests();
  } catch (error) {
    if (revision !== state.revision) return;
    emptyTable("No se pudieron cargar los ensayos. Usá Actualizar datos para reintentar.");
    $("#result-count").textContent = "Datos no disponibles";
    throw error;
  }
}

function renderTests() {
  const list = $("#test-list"); list.replaceChildren();
  for (const test of state.tests) {
    const row = element("tr");
    row.append(element("td", test.metric), element("td", `${test.measured_value.toLocaleString("es-AR", {maximumSignificantDigits: 12})} ${test.unit}`));
    const result = element("td"); result.append(element("span", test.passed ? "Aprobado" : "Fallido", `badge${test.passed ? "" : " fail"}`));
    row.append(result, element("td", test.measured_at ? new Date(test.measured_at).toLocaleString("es-AR") : "Sin fecha"));
    const action = element("td"), button = element("button", "Eliminar", "danger");
    button.disabled = !state.canWrite; button.setAttribute("aria-label", `Eliminar ensayo ${test.metric} #${test.id}`);
    button.onclick = handle(async () => {
      const path = `/chips/${test.chip_id}/macros/${test.macro}/tests/${test.id}`;
      if (!await confirmDelete(`Se eliminará el ensayo ${test.metric} #${test.id}.`)) return;
      button.disabled = true;
      try { await api(path, {method: "DELETE"}); notice("Ensayo eliminado. La operación quedó en la bitácora."); await refresh(); }
      finally { button.disabled = !state.canWrite; }
    });
    action.append(button); row.append(action); list.append(row);
  }
  if (!state.tests.length) emptyTable("No hay ensayos para esta macro y filtro.");
  $("#result-count").textContent = `${state.tests.length} ensayo(s) en esta vista · Fechas en hora local`;
  $("#export").disabled = !state.tests.length;
}

async function refresh() {
  const [chips, summary] = await Promise.all([api("/chips"), api("/summary")]);
  state.chips = chips;
  if (!current()) state.selected = chips[0]?.id ?? null;
  for (const key of ["chips", "tests", "passed", "failed"]) $(`#stat-${key}`).textContent = summary[key];
  renderChips(); await loadTests();
  if ($("#audit-panel").open && state.canWrite) await loadAudit();
}

async function loadAudit() {
  const events = await api("/audit");
  $("#audit-list").replaceChildren(...events.map(event => element("li",
    `${new Date(event.occurred_at).toLocaleString("es-AR")} · ${event.action === "create" ? "Alta" : "Baja"} de ${event.resource === "chip" ? "muestra" : "ensayo"} #${event.resource_id} · ${event.actor}`)));
  if (!events.length) $("#audit-list").append(element("li", "Sin operaciones registradas."));
}

$("#search").oninput = renderChips;
$("#refresh").onclick = handle(refresh);
$("#filter").onchange = handle(loadTests);
document.querySelectorAll("[data-macro]").forEach(button => { button.onclick = handle(async () => { state.macro = button.dataset.macro; await loadTests(); }); });
document.querySelectorAll("[data-close]").forEach(button => { button.onclick = () => button.closest("dialog").close(); });
$("#new-chip").onclick = () => openForm("#chip-dialog");
let testTarget;
$("#new-test").onclick = () => {
  testTarget = testPath();
  $("#test-context").textContent = `${current().part_number} · ${current().board} · Macro ${state.macro}`;
  openForm("#test-dialog");
};
bindForm("#chip-form", async data => {
  if (!data.assembled_at) delete data.assembled_at;
  const chip = await api("/chips", {method: "POST", body: data});
  state.selected = chip.id; $("#search").value = "";
  notice("Muestra registrada."); await refresh().catch(error => notice(`Guardado confirmado. ${error.message}`, true));
});
bindForm("#test-form", async data => {
  data.measured_value = Number(data.measured_value); data.passed = data.passed === "true";
  if (data.measured_at) data.measured_at = new Date(data.measured_at).toISOString();
  else delete data.measured_at;
  await api(testTarget, {method: "POST", body: data});
  notice("Ensayo registrado."); await refresh().catch(error => notice(`Guardado confirmado. ${error.message}`, true));
});
$("#delete-chip").onclick = handle(async () => {
  const chip = current();
  if (!await confirmDelete(`Se eliminará ${chip.part_number} #${chip.id} y TODOS sus ensayos de Tx, Rx y PLL.`)) return;
  $("#delete-chip").disabled = true;
  try { await api(`/chips/${chip.id}`, {method: "DELETE"}); notice("Muestra y ensayos eliminados. Se conservó la auditoría."); await refresh(); }
  finally { $("#delete-chip").disabled = !current() || !state.canWrite; }
});
$("#export").onclick = () => {
  const url = URL.createObjectURL(new Blob([csv(state.tests)], {type: "text/csv;charset=utf-8"}));
  const link = element("a"); link.href = url; link.download = `chip-${state.selected}-${state.macro}.csv`;
  link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
$("#refresh-audit").onclick = handle(loadAudit);
$("#audit-panel").addEventListener("toggle", handle(async () => { if ($("#audit-panel").open) await loadAudit(); }));
$("#logout").onclick = handle(async () => { const data = await api("/logout", {method: "POST"}); window.location.assign(data.redirect); });

handle(async () => {
  const session = await api("/session"); setCSRF(session.csrf_token); state.canWrite = session.can_write;
  $("#identity").textContent = `${session.user.name} · ${state.canWrite ? "Operador" : "Lectura"}`;
  $("#mode").textContent = session.mode === "local" ? "Modo local · Sin identidad real" : "Sesión Auth0 · Laboratorio compartido";
  $("#new-chip").disabled = !state.canWrite; $("#logout").disabled = false;
  $("#audit-panel").hidden = !state.canWrite;
  await refresh();
})().catch(error => notice(error.message, true));
