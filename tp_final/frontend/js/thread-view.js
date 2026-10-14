import {api} from './api.js';
import {$, notice, element, confirmDelete, bindForm, openForm} from './ui.js';

export const threadPath = thread => `/chips/${thread.chip_id}/macros/${thread.macro}/threads/${thread.id}`;
const labels = {in_progress: 'En progreso', passed: 'Aprobado', failed: 'Fallido'};
export function statusBadge(status) { return element('span', labels[status], `badge ${status}`); }
const safe = fn => async (...args) => { try { await fn(...args); } catch (error) { notice(error.message, true); } };

export class ThreadView {
  constructor(canWrite, changed) {
    this.canWrite = canWrite; this.changed = changed; this.thread = null; this.revision = 0;
    $('#close-thread').onclick = () => this.close();
    $('#add-step').onclick = () => this.editStep();
    bindForm('#step-form', async data => {
      for (const key of ['metric', 'unit', 'measured_at']) if (!data[key]) data[key] = null;
      data.measured_value = data.measured_value === '' ? null : Number(data.measured_value);
      if (data.measured_at) data.measured_at = new Date(data.measured_at).toISOString();
      await api(this.stepTarget, {method: this.editing ? 'PUT' : 'POST', body: data});
      await this.saved('Paso guardado. El estado del hilo se actualizó automáticamente.');
    });
    bindForm('#link-form', async data => {
      await api(this.evidenceTarget + '/links', {method: 'POST', body: data});
      await this.saved('Enlace agregado al paso.');
    });
    bindForm('#file-form', async data => {
      if (!data.file?.size) throw new Error('Seleccioná un archivo que no esté vacío.');
      if (data.file.size > 10 * 1024 * 1024) throw new Error('El archivo supera el límite de 10 MiB.');
      await api(this.evidenceTarget + '/files', {method: 'POST', body: data.file});
      await this.saved('Archivo guardado en el paso.');
    });
  }

  close() { this.thread = null; this.revision++; $('#thread-detail').hidden = true; }
  async open(thread, focus = true) {
    const revision = ++this.revision; this.thread = thread;
    $('#thread-detail').hidden = false; $('#thread-title').textContent = thread.title;
    $('#thread-description').textContent = ''; $('#thread-meta').replaceChildren(); $('#add-step').disabled = true;
    $('#step-list').replaceChildren(element('p', 'Cargando pasos…', 'empty'));
    if (focus) { $('#thread-detail').scrollIntoView({behavior: 'smooth'}); $('#thread-title').focus(); }
    try {
      const detail = await api(threadPath(thread));
      if (revision !== this.revision) return;
      this.thread = detail; this.render();
    } catch (error) {
      if (revision !== this.revision) return;
      $('#step-list').replaceChildren(element('p', 'No se pudo cargar el hilo. Usá Actualizar datos.', 'empty')); throw error;
    }
  }
  async reload() { if (this.thread) await this.open(this.thread, false); }
  async saved(message) {
    notice(message);
    try { await this.reload(); await this.changed(); }
    catch (error) { notice(`Guardado confirmado. ${error.message}`, true); }
  }
  editStep(step = null) {
    const form = $('#step-form'); form.reset(); this.editing = Boolean(step);
    this.stepTarget = threadPath(this.thread) + '/steps' + (step ? `/${step.id}` : '');
    $('#step-dialog-title').textContent = step ? 'Editar paso' : 'Agregar paso al hilo';
    for (const key of ['title', 'notes', 'status', 'metric', 'measured_value', 'unit']) {
      form.elements[key].value = step?.[key] ?? (key === 'status' ? 'in_progress' : '');
    }
    if (step?.measured_at) {
      const date = new Date(step.measured_at);
      form.elements.measured_at.value = new Date(date - date.getTimezoneOffset() * 60000).toISOString().slice(0, 19);
    }
    openForm('#step-dialog');
  }
  evidence(step) {
    this.evidenceTarget = threadPath(this.thread) + `/steps/${step.id}/attachments`;
    $('#evidence-context').textContent = `${this.thread.title} · ${step.title}`;
    $('#file-form').reset(); $('#link-form').reset();
    document.querySelectorAll('#evidence-dialog .form-error').forEach(node => node.textContent = '');
    $('#evidence-dialog').showModal();
  }
  render() {
    const thread = this.thread;
    $('#thread-title').textContent = thread.title;
    $('#thread-description').textContent = thread.description || 'Sin descripción adicional.';
    $('#thread-meta').replaceChildren(statusBadge(thread.status), element('span', `${thread.part_number} #${thread.chip_id} · ${thread.board} · ${thread.macro} · ${thread.step_count} paso(s)`));
    $('#add-step').disabled = !this.canWrite();
    $('#step-list').replaceChildren(...thread.steps.map((step, index) => this.stepCard(step, index)));
    if (!thread.steps.length) $('#step-list').append(element('p', 'Este hilo está en progreso. Agregá el primer paso para registrar pruebas y evidencias.', 'empty'));
  }
  stepCard(step, index) {
    const card = element('article', undefined, `step-card ${step.status}`);
    const header = element('div', undefined, 'step-heading');
    header.append(element('h3', `${index + 1}. ${step.title}`), statusBadge(step.status)); card.append(header);
    card.append(element('p', step.notes || 'Sin notas.', 'step-notes'));
    if (step.metric !== null) card.append(element('p', `${step.metric}: ${step.measured_value} ${step.unit}`, 'measurement'));
    card.append(element('p', `Creado: ${new Date(step.created_at).toLocaleString('es-AR')} · Actualizado: ${new Date(step.updated_at).toLocaleString('es-AR')}` + (step.measured_at ? ` · Medición: ${new Date(step.measured_at).toLocaleString('es-AR')}` : ''), 'muted'));
    const attachments = element('ul', undefined, 'evidence-list');
    for (const item of step.attachments) {
      const li = element('li'), link = element('a', `${item.kind === 'file' ? 'Archivo' : 'Enlace'}: ${item.name}`);
      link.href = item.kind === 'file' ? threadPath(this.thread) + `/steps/${step.id}/attachments/${item.id}/download` : item.url;
      if (item.kind === 'link') { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
      li.append(link);
      if (item.kind === 'file') li.append(element('small', `${Math.max(1, Math.ceil(item.size / 1024))} KiB`));
      if (this.canWrite()) {
        const remove = element('button', 'Quitar', 'quiet');
        const path = threadPath(this.thread) + `/steps/${step.id}/attachments/${item.id}`;
        remove.setAttribute('aria-label', `Quitar evidencia ${item.name}`);
        remove.onclick = safe(async () => {
          if (!await confirmDelete(`Se quitará «${item.name}» de este paso.`)) return;
          remove.disabled = true;
          try { await api(path, {method: 'DELETE'}); await this.saved('Evidencia eliminada.'); }
          finally { remove.disabled = false; }
        }); li.append(remove);
      }
      attachments.append(li);
    }
    card.append(element('h4', `Evidencias (${step.attachments.length}/20)`), attachments);
    if (!step.attachments.length) card.append(element('p', 'Todavía no se adjuntaron archivos ni enlaces.', 'muted'));
    if (this.canWrite()) {
      const actions = element('div', undefined, 'step-actions');
      const add = element('button', 'Adjuntar evidencia', 'primary'); add.onclick = () => this.evidence(step);
      const edit = element('button', 'Editar paso', 'quiet'); edit.onclick = () => this.editStep(step);
      const remove = element('button', 'Eliminar paso', 'danger');
      const path = threadPath(this.thread) + `/steps/${step.id}`;
      remove.onclick = safe(async () => {
        if (!await confirmDelete(`Se eliminará el paso «${step.title}» y sus archivos.`)) return;
        remove.disabled = true;
        try { await api(path, {method: 'DELETE'}); await this.saved('Paso eliminado.'); }
        finally { remove.disabled = false; }
      }); actions.append(add, edit, remove); card.append(actions);
    }
    return card;
  }
}
