# Pendientes del cliente — Fisiolab.Ec

Material a pedir a Fisiolab para pasar de prototipo a producción. Cada ítem aparece en la web con borde punteado y etiqueta `{{NOMBRE}}`.

| Placeholder | Qué pedir | Dónde aparece |
|---|---|---|
| `{{EQUIPO}}` | Por cada profesional (6–8): foto retrato con fondo neutro, nombre completo, especialidad | /equipo, inicio |
| `{{REGISTRO_SENESCYT}}` | Número de registro SENESCYT de cada profesional | /equipo, inicio |
| `{{FOTOS_INSTALACIONES}}` | Fotos reales: fachada, recepción, sala de terapia, equipos de robótica, Rayos X, consultorio, evaluación de pisada, Home (con autorización del paciente) | Inicio, /equipo, /terapias, /servicios |
| `{{VIGENCIA_PROMO}}` | Fecha de vigencia de los precios promocionales MEFCare y precio del Paquete Deportivo | /servicios#mefcare |
| Enlaces de pago MEFCare | Un link de pasarela por paquete; se pegan en `CONFIG.pay` de `js/main.js` y aparece el botón "Pagar en línea" | /servicios#mefcare |
| Ginecología y Urología | Aparecen en los paquetes pero no en las 12 especialidades: confirmar si se agregan | /especialidades |
| Perfil de Empresa en Google | La ficha ya está reclamada (4,6 · 51 opiniones). Pedir que agreguen a Orion como administrador; agregar el botón de sitio web; confirmar que el nombre de la ficha coincide con el letrero; aclarar si REHAB NOVA CENTER (mismo teléfono) es del grupo; cambiar la portada "regenerar tejidos y acelerar tu recuperación" (promesa de resultado) | Google Maps |
| `{{HORARIOS}}` | Horario por día (hoy está en una imagen; Google Maps dice "cierra 8 p. m.") | /ubicacion, schema |
| `{{FORMAS_PAGO}}` | Efectivo, tarjeta, transferencia, seguros/convenios | FAQ |
| `{{PARQUEO}}` | Si hay estacionamiento propio o cercano | FAQ |
| `{{CONFIRMAR_REFERENCIA}}` | Si se puede agendar especialidad sin referencia médica | FAQ |
| `{{CONFIRMAR_CERTIFICACION_BTL}}` | Documento que respalde la certificación BTL. Sin documento no se menciona | /terapias#robotica |
| `{{LICENCIA_FUNCIONAMIENTO}}` | Número de licencia ACESS / permiso de funcionamiento | Footer |
| `{{AVISO_PRIVACIDAD}}` | Revisión legal del borrador LOPDP | /privacidad |
| `{{RAZON_SOCIAL_RUC}}` | Razón social y RUC del responsable de datos | /privacidad |
| `{{DOMINIO}}` | Acceso al DNS de fisiolab.ec para apuntarlo a Vercel | canonical, sitemap, robots |
| `{{LOGO_VECTORIAL}}` | Logo en SVG/AI/PDF (hoy se recortó de un PNG) | Header, footer, favicon |
| `{{WHATSAPP_EDUSALUD}}` | Número propio de Edusalud si existe (hoy usa el principal) | /profesionales |
| `{{CALENDARIO_EDUSALUD}}` | Cursos y fechas vigentes | /profesionales |
| `{{GA4_ID}}` / `{{PIXEL_ID}}` | IDs de Google Analytics 4 y Meta Pixel (o acceso para crearlos) | js/main.js → ANALYTICS |
| `{{HERRAMIENTAS_MEDICION}}` | Confirmar herramientas para el aviso de privacidad | /privacidad |

## Fondos de video e imagen (opcionales)

Se activan en `js/main.js` → `CONFIG.media`. Sin archivo, la sección muestra su degradado y una etiqueta discreta.

| Espacio | Material | Formato |
|---|---|---|
| `{{VIDEO_HERO}}` | Recorrido corto por el centro (recepción → consultorio → sala de terapia) | .mp4 1920×1080, 10–15 s, sin audio, < 4 MB + foto .jpg de respaldo |
| `{{VIDEO_ROBOTICA}}` | Equipos de terapia robótica en uso, sin rostros de pacientes | .mp4 igual que arriba |
| `{{FOTO_CTA}}` | Recepción o fachada | .jpg 1920 px de ancho |
| `{{FOTO_HOME}}` | Atención a domicilio, con autorización escrita del paciente | .jpg 1920 px |
| `{{FOTO_ESPECIALIDADES}}` `{{FOTO_TERAPIAS}}` `{{FOTO_SERVICIOS}}` `{{FOTO_EQUIPO_GRUPAL}}` `{{FOTO_FACHADA}}` `{{FOTO_EDUSALUD}}` | Una foto horizontal por página interna | .jpg 1920 px |

En celular el video no se carga (se usa la foto de respaldo) para cuidar datos y velocidad.

## Formulario de orientación (captación con puntaje)

| Pendiente | Qué hacer |
|---|---|
| `LEAD_WEBHOOK_URL` | Seguir `tools/google-apps-script.gs` (5 min): crea la hoja, pega el script, publícalo y pon la URL en Vercel. Mientras no esté, el formulario pide al paciente confirmar por WhatsApp para que el contacto no se pierda. |
| `{{VIDEO_EXPLICATIVO}}` | Video de ~2 min del equipo explicando evaluación, plan y seguimiento, sin promesas de resultado. YouTube (URL embed) o .mp4 en `CONFIG.lead.video`. |
| `{{HORARIOS}}` en `CONFIG.lead.callHours` | Texto del horario en que se devuelven las llamadas. |
| `{{PLAZO_CONSERVACION}}` | Confirmar con el asesor legal cuánto tiempo se guardan los datos (borrador: 12 meses). |
| Responsable de llamadas | Quién llama a los contactos "llamada" y en qué plazo. Sin esto el formulario promete algo que nadie cumple. |

Puntaje: motivo (0–2) + frustración (0–2) + cuándo empezar (0–3). 5 o más → llamada · 3–4 → consulta de evaluación · 0–2 → video.

## Reseñas de Google en automático (parte de la línea de atención)

- Después de cada cita atendida, WhatsApp envía el enlace directo de reseña (pedir a Fisiolab el enlace "Pedir reseñas" de su ficha).
- Se pide a **todos** los pacientes: Google prohíbe filtrar a los satisfechos o dar descuentos a cambio. El puntaje del formulario no se usa para esto.
- Respuestas automáticas solo para 4–5 estrellas, con plantillas neutras que no confirman que la persona es paciente ni mencionan tratamientos. 3 estrellas o menos → alerta a gerencia.
