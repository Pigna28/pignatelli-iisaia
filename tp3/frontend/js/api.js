let csrf = "";
export function setCSRF(value) { csrf = value; }

export async function api(path, {method = "GET", body} = {}) {
  let response;
  try {
    response = await fetch(path, {
      method, credentials: "same-origin",
      headers: {"Accept": "application/json", ...(body ? {"Content-Type": "application/json"} : {}),
        ...(method !== "GET" ? {"X-CSRF-Token": csrf} : {})},
      ...(body ? {body: JSON.stringify(body)} : {}),
    });
  } catch { throw new Error("No se pudo conectar con el servidor. Verificá la conexión y reintentá."); }
  if (response.status === 401) {
    throw new Error("La sesión venció. Ingresá nuevamente desde el enlace de inicio.");
  }
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || `El servidor respondió ${response.status}. Reintentá.`);
  }
  return response.status === 204 ? null : response.json();
}

export function csv(rows) {
  const columns = ["id", "chip_id", "macro", "metric", "measured_value", "unit", "passed", "measured_at"];
  const escape = value => {
    let text = String(value ?? "");
    // Evitar fórmulas al abrir texto no confiable en una planilla.
    if (typeof value === "string" && /^[\s]*[=+\-@]/.test(text)) text = "'" + text;
    return '"' + text.replaceAll('"', '""') + '"';
  };
  return "\uFEFF" + [columns.join(","), ...rows.map(row => columns.map(key => escape(row[key])).join(","))].join("\r\n");
}
