// Recibe el formulario de orientación y lo reenvía a LEAD_WEBHOOK_URL
// (Google Apps Script, Make, Zapier o ManyChat). Variable de entorno en Vercel:
//   LEAD_WEBHOOK_URL = https://...
// Sin la variable, responde ok y deja el registro en los logs de Vercel.

const MAX = { nombre: 80, texto: 140 };

const clean = (v, n) => String(v == null ? "" : v).replace(/[<>]/g, "").trim().slice(0, n);

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false });
  }

  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  b = b || {};

  const celular = String(b.celular || "").replace(/\D/g, "");
  const nombre = clean(b.nombre, MAX.nombre);
  if (nombre.length < 2 || !/^09\d{8}$/.test(celular) || b.consentimiento !== true) {
    return res.status(400).json({ ok: false, error: "datos_invalidos" });
  }

  const respuestas = {};
  Object.entries(b.respuestas || {}).slice(0, 6).forEach(([k, v]) => { respuestas[clean(k, 30)] = clean(v, MAX.texto); });
  const utm = {};
  Object.entries(b.utm || {}).slice(0, 4).forEach(([k, v]) => { utm[clean(k, 20)] = clean(v, 80); });

  const lead = {
    nombre,
    celular,
    whatsapp: "https://wa.me/593" + celular.slice(1),
    segmento: ["llamada", "consulta", "video"].includes(b.segmento) ? b.segmento : "video",
    puntaje: Math.max(0, Math.min(10, Number(b.puntaje) || 0)),
    servicio_sugerido: clean(b.servicio_sugerido, 40),
    respuestas,
    utm,
    pagina: clean(b.pagina, 60),
    consentimiento: true,
    recibido: new Date().toISOString()
  };

  const url = process.env.LEAD_WEBHOOK_URL;
  if (!url) {
    console.log("lead (sin LEAD_WEBHOOK_URL)", JSON.stringify({ ...lead, celular: "***" + celular.slice(-3) }));
    return res.status(200).json({ ok: true, stored: false });
  }

  try {
    const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(lead) });
    return res.status(200).json({ ok: r.ok, stored: r.ok });
  } catch (e) {
    console.error("lead webhook error", e.message);
    return res.status(200).json({ ok: false, stored: false });
  }
};
