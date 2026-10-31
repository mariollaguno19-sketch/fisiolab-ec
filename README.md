# Fisiolab.Ec — web del grupo (prototipo)

Prototipo de renovación de fisiolab.ec por Orion AI Studio. HTML, CSS y JS sin framework ni build: Vercel sirve los archivos tal cual.

## Páginas
`/` inicio · `/especialidades` · `/terapias` · `/servicios` · `/equipo` · `/ubicacion` · `/profesionales` · `/privacidad`

## Editar
- Números de WhatsApp, mensajes, redes y URLs: objeto `CONFIG` al inicio de `js/main.js`.
- Estilos y tokens de color: `css/styles.css` (se incrusta en cada página al generar).
- Textos, header, footer y modal: `tools/build.py`, luego `python3 tools/build.py` para regenerar los `.html`.

## Qué incluye
- Pantalla de carga con la figura del logo (primera vista de la sesión, mínimo 2,8 s, tope 4 s).
- Modal "Agendar" con pre-clasificación en 3 pasos (servicio → primera vez → urgencia) que arma el mensaje de WhatsApp.
- Aviso emergente suave, una vez por sesión.
- Pop-up de salida (cursor sale por arriba, 35 s sin actividad o subida rápida), una vez por sesión.
- Barra inferior en celular (Servicios · Orientación · Agendar) e índice fijo con la sección actual en páginas internas.
- `js/main.js` se carga con `?v=<huella>`: después de editarlo, correr `python3 tools/build.py`.
- Formulario de orientación con puntaje (inicio, #orientacion): 5+ puntos → llamada, 3–4 → consulta, 0–2 → video. Envía a `/api/lead`, que reenvía a `LEAD_WEBHOOK_URL`.
- Eventos `whatsapp_click`, `agendar_open`, `agendar_clasificado`, `orientacion_start`, `lead_submit` en `dataLayer` listos para GA4 y Meta Pixel.
- Schema.org `MedicalClinic` y `FAQPage`, sitemap, robots, redirecciones 301 de la web vieja.

Pendientes del cliente: ver `PENDIENTES.md`.
