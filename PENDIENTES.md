# Pendientes del cliente — Fisiolab.Ec

Material a pedir a Fisiolab para pasar de prototipo a producción. Cada ítem aparece en la web con borde punteado y etiqueta `{{NOMBRE}}`.

| Placeholder | Qué pedir | Dónde aparece |
|---|---|---|
| `{{EQUIPO}}` | Por cada profesional (6–8): foto retrato con fondo neutro, nombre completo, especialidad | /equipo, inicio |
| `{{REGISTRO_SENESCYT}}` | Número de registro SENESCYT de cada profesional | /equipo, inicio |
| `{{FOTOS_INSTALACIONES}}` | Fotos reales: fachada, recepción, sala de terapia, equipos de robótica, Rayos X, consultorio, evaluación de pisada, Home (con autorización del paciente) | Inicio, /equipo, /terapias, /servicios |
| `{{PAQUETES_MEFCARE}}` | Nombre de cada paquete, qué incluye, precio o "consultar" | /servicios#mefcare |
| `{{RESEÑAS_GOOGLE}}` | Opcional: 3–4 reseñas reales copiadas de Google con nombre y fecha. Sin esto se muestra solo el 4.6 ★ | Inicio |
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
