/**
 * Recibe los contactos del formulario de orientación en una hoja de Google.
 *
 * 1. Crea una hoja de Google (ej. "Fisiolab · Contactos web") en la cuenta del centro.
 * 2. Extensiones → Apps Script → borra todo y pega este archivo.
 * 3. Cambia CLAVE por una palabra larga y secreta (la misma va en Vercel).
 * 4. Implementar → Nueva implementación → Tipo: Aplicación web
 *      Ejecutar como: yo · Quién tiene acceso: cualquier usuario → Implementar.
 * 5. Copia la URL que termina en /exec.
 * 6. En Vercel → fisiolab-ec → Settings → Environment Variables:
 *      LEAD_WEBHOOK_URL = <URL /exec>?k=<CLAVE>
 *    y vuelve a desplegar (Deployments → Redeploy).
 */
const CLAVE = "CAMBIAR-POR-UNA-CLAVE-LARGA";

const COLUMNAS = ["recibido", "nombre", "celular", "whatsapp", "segmento", "puntaje",
  "servicio_sugerido", "motivo", "frustracion", "inicio", "origen", "pagina", "estado", "notas"];

function doPost(e) {
  if (!e || !e.parameter || e.parameter.k !== CLAVE) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false })).setMimeType(ContentService.MimeType.JSON);
  }
  const lead = JSON.parse(e.postData.contents || "{}");
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(COLUMNAS);
    hoja.setFrozenRows(1);
  }
  const r = lead.respuestas || {};
  const u = lead.utm || {};
  hoja.appendRow([
    lead.recibido, lead.nombre, "'" + lead.celular, lead.whatsapp, lead.segmento, lead.puntaje,
    lead.servicio_sugerido, r.motivo || "", r.frustracion || "", r.inicio || "",
    [u.utm_source, u.utm_campaign].filter(String).join(" / "), lead.pagina,
    lead.segmento === "llamada" ? "Llamar" : "Pendiente", ""
  ]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}
