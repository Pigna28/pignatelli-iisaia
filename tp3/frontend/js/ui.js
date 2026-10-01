export const $ = selector => document.querySelector(selector);
export function notice(message, error = false) {
  const node = $("#notice");
  node.textContent = message; node.classList.toggle("error", error); node.hidden = false;
}
export function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
export function emptyTable(message) {
  const row = element("tr"), cell = element("td", message, "empty");
  cell.colSpan = 5; row.append(cell); $("#test-list").replaceChildren(row);
}
export function confirmDelete(message) {
  const dialog = $("#confirm-dialog");
  $("#confirm-message").textContent = message;
  return new Promise(resolve => {
    let confirmed = false;
    $("#confirm-delete").onclick = () => { confirmed = true; dialog.close(); };
    $("#cancel-delete").onclick = () => dialog.close();
    dialog.addEventListener("close", () => resolve(confirmed), {once: true});
    dialog.showModal(); $("#cancel-delete").focus();
  });
}
export function bindForm(id, save) {
  const form = $(id), dialog = form.closest("dialog");
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    if (submit.disabled) return;
    submit.disabled = true; form.querySelector(".form-error").textContent = "";
    try { await save(Object.fromEntries(new FormData(form))); dialog.close(); form.reset(); }
    catch (error) { form.querySelector(".form-error").textContent = error.message; }
    finally { submit.disabled = false; }
  });
}
export function openForm(id) {
  const dialog = $(id);
  dialog.querySelector(".form-error").textContent = "";
  dialog.showModal();
}
