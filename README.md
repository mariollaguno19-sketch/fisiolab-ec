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
- Eventos `whatsapp_click`, `agendar_open`, `agendar_clasificado` en `dataLayer` listos para GA4 y Meta Pixel.
- Schema.org `MedicalClinic` y `FAQPage`, sitemap, robots, redirecciones 301 de la web vieja.

Pendientes del cliente: ver `PENDIENTES.md`.
