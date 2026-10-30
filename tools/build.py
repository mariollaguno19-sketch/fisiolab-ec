#!/usr/bin/env python3
"""Genera las páginas estáticas de Fisiolab.Ec.

No es necesario para el deploy: Vercel sirve los .html ya generados.
Se usa solo para editar header/footer/modal en un solo lugar:
    python3 tools/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://fisiolab-ec.vercel.app"  # {{DOMINIO}} — reemplazar por el dominio final

# ---------------------------------------------------------------- iconos
WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.4-1.5-.9-.8-1.5-1.8-1.6-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4c-1-1.6-1.5-3.4-1.5-5.2 0-5.4 4.4-9.8 9.8-9.8 2.6 0 5.1 1 6.9 2.9 1.9 1.9 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2C18.2 1.3 15.2 0 12 0 5.4 0 .1 5.3.1 11.9c0 2.1.6 4.2 1.6 6L0 24l6.3-1.7c1.7.9 3.7 1.4 5.7 1.4 6.6 0 11.9-5.3 11.9-11.9 0-3.2-1.2-6.2-3.5-8.4z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
XRAY = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 7v10M9 9h6M8.5 12h7M9 15h6"/></svg>'
STAR = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.8-4.9 4.6 1.3 6.5L12 17.2l-5.9 3.2 1.3-6.5L2.5 9.3l6.6-.8z"/></svg>'

NAV = [
    ("especialidades", "/especialidades", "Especialidades"),
    ("terapias", "/terapias", "Terapias"),
    ("servicios", "/servicios", "Servicios"),
    ("equipo", "/equipo", "Equipo"),
    ("ubicacion", "/ubicacion", "Ubicación"),
]



ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def wa_btn(service, text="Agendar por WhatsApp", cls="btn", src=""):
    s = f' data-src="{src}"' if src else ""
    return f'<a class="{cls}" href="#" data-wa="{service}"{s}>{WA}<span>{text}</span></a>'


def agendar_btn(service="", text="Agendar cita", cls="btn"):
    return f'<button type="button" class="{cls}" data-agendar="{service}">{WA}<span>{text}</span></button>'


def ph(name):
    return f'<span class="tag">{{{{{name}}}}}</span>'


def photo(label, sub, tag, cls="", style=""):
    st = f' style="{style}"' if style else ""
    return (f'<div class="photo {cls}"{st} role="img" aria-label="Espacio para foto: {label}">'
            f'<span class="tag">{{{{{tag}}}}}</span>'
            f'<span class="photo__cap"><b>{label}</b>{sub}</span></div>')


# ---------------------------------------------------------------- layout
def minify(css):
    """CSS inline en cada página: evita una petición que bloquea el render."""
    import re
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


FONTS = "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Onest:wght@400;500;600&display=swap"


def head(title, desc, path, extra=""):
    url = BASE + path
    css = minify((ROOT / "css/styles.css").read_text(encoding="utf-8"))
    return f'''<!doctype html>
<html lang="es-EC">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#2B6EA8">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_EC">
<meta property="og:site_name" content="Fisiolab.Ec">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}">
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"><style>.loader{{display:none}}</style></noscript>
<style>{css}</style>
<script>document.documentElement.classList.add("js");try{{if(sessionStorage.getItem("fl_seen")||matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("no-loader","is-loaded")}}catch(e){{}}</script>
{extra}</head>'''


def header(active):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if key == active else "", label) for key, href, label in NAV)
    dlinks = "".join(f'<a href="{href}">{label}</a>' for key, href, label in NAV)
    return f'''
<div class="loader" aria-hidden="true">
  <div class="loader__inner">
    <img class="loader__fig" src="/assets/icon-white-sm.png" width="70" height="118" alt="">
    <img class="loader__word" src="/assets/wordmark-white-md.png" width="168" height="40" alt="">
    <div class="loader__bar"><i></i></div>
    <span class="loader__note">Centro de Especialidades Médicas · Conocoto</span>
  </div>
</div>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="header header--on-brand">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Fisiolab.Ec, inicio">
      <img class="on-light" src="/assets/icon-blue-sm.png" width="20" height="34" alt="">
      <img class="on-light brand__word" src="/assets/wordmark-navy-sm.png" width="94" height="22" alt="Fisiolab.Ec">
      <img class="on-brand" src="/assets/icon-white-xs.png" width="20" height="34" alt="">
      <img class="on-brand brand__word" src="/assets/wordmark-white-sm.png" width="94" height="22" alt="Fisiolab.Ec">
    </a>
    <nav class="nav" aria-label="Principal">{links}</nav>
    {agendar_btn("", "Agendar", "btn btn--sm header__cta")}
    <button class="burger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="drawer"><span></span></button>
  </div>
</header>
<div class="drawer" id="drawer">
  <a href="/">Inicio</a>{dlinks}<a href="/profesionales">Profesionales</a>
  {agendar_btn("", "Agendar por WhatsApp", "btn btn--block")}
  <p class="drawer__meta">Matilde Albán E2-47 y Sucre, Conocoto<br><a href="#" data-tel data-tel-label>02-2070188</a></p>
</div>'''


MODAL_SERVICES = [
    ("especialidades", "Consulta con especialista", "Traumatología, cardiología y 10 más"),
    ("fisioterapia", "Fisioterapia", "Deportiva, neurológica, geriátrica"),
    ("robotica", "Terapia robótica", "Tecar, SIS, tracción, ondas de choque"),
    ("rayosx", "Rayos X", "Imagen en el centro"),
    ("pisada", "Marcha y pisada", "Análisis y plantillas"),
    ("home", "Atención a domicilio", "Fisiolab Home"),
    ("mefcare", "Paquetes MEFCare", "Planes de atención"),
    ("nutricion", "Nutrición", "Canal propio"),
    ("laboratorio", "Laboratorio clínico", "Canal propio"),
    ("general", "Aún no sé", "Te orientamos"),
]


def modal():
    opts = "".join(
        f'<button type="button" class="opt" data-pick-service="{k}">{t}<small>{s}</small></button>' for k, t, s in MODAL_SERVICES)
    return f'''
<div class="modal" id="agendar" role="dialog" aria-modal="true" aria-labelledby="agendar-t" aria-hidden="true">
  <div class="modal__scrim" data-close></div>
  <div class="modal__box">
    <button type="button" class="modal__close" data-close aria-label="Cerrar">×</button>
    <div class="steps" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
    <div class="modal__step">
      <h2 id="agendar-t">¿Qué necesitas agendar?</h2>
      <p class="muted small" style="margin:.6rem 0 0">Elige y te dejamos el mensaje listo para WhatsApp.</p>
      <div class="opts">{opts}</div>
    </div>
    <div class="modal__step">
      <h2>¿Es tu primera vez en Fisiolab?</h2>
      <div class="opts opts--1">
        <button type="button" class="opt" data-pick-visit="Es mi primera vez.">Sí, es mi primera vez</button>
        <button type="button" class="opt" data-pick-visit="Ya soy paciente.">Ya soy paciente</button>
        <button type="button" class="opt" data-pick-visit="Es para un familiar.">Es para un familiar</button>
      </div>
      <button type="button" class="modal__back" data-back="0">← Cambiar servicio</button>
    </div>
    <div class="modal__step">
      <h2>¿Para cuándo la necesitas?</h2>
      <div class="opts opts--1">
        <button type="button" class="opt" data-pick-when="Quisiera una cita esta semana.">Esta semana</button>
        <button type="button" class="opt" data-pick-when="Puedo en las próximas semanas.">En las próximas semanas</button>
        <button type="button" class="opt" data-pick-when="Por ahora quiero información.">Solo quiero información</button>
      </div>
      <button type="button" class="modal__back" data-back="1">← Atrás</button>
    </div>
    <div class="modal__step">
      <h2>Tu mensaje está listo.</h2>
      <div class="summary" data-summary></div>
      <a class="btn btn--block" href="#" target="_blank" rel="noopener" data-final>{WA}<span>Abrir WhatsApp</span></a>
      <p class="fine">No envíes diagnósticos ni datos médicos por este medio; el equipo los pide en consulta. Al escribirnos aceptas el <a href="/privacidad">aviso de privacidad</a>.</p>
      <button type="button" class="modal__back" data-back="0">← Empezar de nuevo</button>
    </div>
  </div>
</div>
<div class="toast" role="dialog" aria-live="polite" aria-label="Ayuda para agendar" aria-hidden="true">
  <b>¿No sabes qué especialista te toca?</b>
  <button type="button" class="toast__x" aria-label="Cerrar aviso">×</button>
  <p>Cuéntanos qué buscas y te orientamos por WhatsApp.</p>
  {agendar_btn("general", "Que me orienten", "btn btn--sm")}
</div>
<button type="button" class="wa-float" data-agendar="" aria-label="Agendar por WhatsApp"><span class="dot" aria-hidden="true"></span>{WA}<span>Agendar</span></button>'''


def footer():
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <p class="footer__big">Consulta, imagen y rehabilitación en Conocoto desde hace 15 años.</p>
        <p>Matilde Albán E2-47 y Sucre, Conocoto, Quito.<br>A dos cuadras del Centro de Salud Conocoto.</p>
        <p><a href="#" data-tel data-tel-label>02-2070188</a> · <a href="#" data-mail>fisio.lab@hotmail.com</a></p>
      </div>
      <div>
        <h2>Pacientes</h2>
        <ul>
          <li><a href="/especialidades">Especialidades médicas</a></li>
          <li><a href="/terapias">Fisioterapia y robótica</a></li>
          <li><a href="/servicios">MEFCare, pisada y Home</a></li>
          <li><a href="/equipo">Equipo e instalaciones</a></li>
          <li><a href="/ubicacion">Ubicación y preguntas</a></li>
        </ul>
      </div>
      <div>
        <h2>Unidades en Instagram</h2>
        <ul>
          <li><a href="#" data-social="clinicas">@fisiolab.ec_clinicas</a></li>
          <li><a href="#" data-social="mefcare">@mefcare</a></li>
          <li><a href="#" data-social="nutricion">@fisiolab.ec_nutricion</a></li>
          <li><a href="#" data-social="pisada">@fisiolab.ec_pisada</a></li>
          <li><a href="#" data-social="laboratorio">@fisiolab.ec_laboratorioclinico</a></li>
          <li><a href="#" data-social="fisiorespiratoria">@fisiolab.ec_fisiorespiratoria</a></li>
        </ul>
      </div>
      <div>
        <h2>Más canales</h2>
        <ul>
          <li><a href="#" data-social="facebook">Facebook</a></li>
          <li><a href="#" data-social="tiktok">TikTok</a></li>
          <li><a href="/profesionales">Edusalud para profesionales</a></li>
          <li><a href="#" data-social="edusalud">@fisiolab.ec_edusalud</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <span>© <span data-year>2026</span> Fisiolab.Ec &amp; MEF Care · Licencia de funcionamiento {ph("LICENCIA_FUNCIONAMIENTO")}</span>
      <span><a href="/privacidad">Aviso de privacidad</a></span>
    </div>
  </div>
</footer>
<script src="/js/main.js" defer></script>
</body>
</html>'''


def page(name, active, title, desc, path, main, extra_head=""):
    html = head(title, desc, path, extra_head) + f'\n<body data-page="{active}">' + header(active) + \
        f'\n<main id="main">{main}\n</main>' + modal() + footer()
    (ROOT / name).write_text(html, encoding="utf-8")


def page_hero(crumb, h1, lead, sub=None):
    s = ""
    if sub:
        s = '<nav class="subnav" aria-label="En esta página">' + "".join(f'<a href="#{a}">{t}</a>' for a, t in sub) + "</nav>"
    return f'''
<section class="page-hero">
  <img class="page-hero__fig" src="/assets/icon-white-lg.png" width="594" height="1000" alt="" loading="lazy">
  <div class="wrap">
    <p class="crumbs"><a href="/">Inicio</a> / {crumb}</p>
    <h1>{h1}</h1>
    <p class="lede">{lead}</p>
    {s}
  </div>
</section>'''


def cta_final(h="Escríbenos y <em>coordinamos tu cita.</em>", p="Eliges el servicio, te respondemos por WhatsApp y confirmamos día y hora. Sin formularios."):
    return f'''
<section class="cta">
  <img class="cta__fig" src="/assets/icon-white-lg.png" width="594" height="1000" alt="" loading="lazy">
  <div class="wrap">
    <h2 class="reveal">{h}</h2>
    <p class="reveal" data-d="1">{p}</p>
    <div class="cta__actions reveal" data-d="2">
      {agendar_btn("", "Agendar por WhatsApp", "btn btn--on-brand")}
      <a class="link" href="#" data-tel>Llamar al <span data-tel-label>02-2070188</span></a>
      <a class="link" href="#" data-maps>Cómo llegar</a>
    </div>
  </div>
</section>'''


ART = {
    "Tecarterapia": '''<svg class="tech__art" viewBox="0 0 160 100" aria-hidden="true">
  <line class="soft" x1="24" y1="18" x2="24" y2="82"/><line class="soft" x1="136" y1="18" x2="136" y2="82"/>
  <path class="draw" d="M24 50 C36 22 48 22 58 50 S80 78 92 50 S114 22 136 50"/>
  <path class="draw" d="M24 50 C36 36 48 36 58 50 S80 64 92 50 S114 36 136 50" style="opacity:.45"/>
  <g class="float"><rect class="draw" x="16" y="40" width="16" height="20" rx="3"/><rect class="draw" x="128" y="40" width="16" height="20" rx="3"/></g>
</svg>''',
    "Robot SIS": '''<svg class="tech__art" viewBox="0 0 160 100" aria-hidden="true">
  <ellipse class="soft" cx="80" cy="62" rx="66" ry="26"/><ellipse class="soft" cx="80" cy="62" rx="44" ry="17"/>
  <ellipse class="draw" cx="80" cy="62" rx="22" ry="8"/>
  <path class="draw" d="M58 62 C58 30 102 30 102 62"/><path class="draw" d="M36 62 C36 14 124 14 124 62"/>
  <g class="float"><rect class="draw" x="68" y="8" width="24" height="10" rx="3"/></g>
</svg>''',
    "Tracción vertebral computarizada": '''<svg class="tech__art" viewBox="0 0 160 100" aria-hidden="true">
  <line class="soft" x1="80" y1="6" x2="80" y2="94"/>
  <g class="slide"><rect class="draw" x="62" y="12" width="36" height="12" rx="5"/><rect class="draw" x="62" y="30" width="36" height="12" rx="5"/></g>
  <rect class="draw" x="62" y="52" width="36" height="12" rx="5"/><rect class="draw" x="62" y="70" width="36" height="12" rx="5"/>
  <path class="draw" d="M120 46 V14 M112 22 L120 14 L128 22"/><path class="draw" d="M40 54 V86 M32 78 L40 86 L48 78"/>
</svg>''',
    "Ondas de choque": '''<svg class="tech__art" viewBox="0 0 160 100" aria-hidden="true">
  <circle class="pulse" cx="42" cy="50" r="34"/><circle class="pulse" cx="42" cy="50" r="34"/><circle class="pulse" cx="42" cy="50" r="34"/>
  <circle class="draw" cx="42" cy="50" r="6"/>
  <path class="draw" d="M74 30 Q88 50 74 70"/><path class="draw" d="M92 20 Q112 50 92 80"/><path class="draw" d="M110 10 Q136 50 110 90"/>
</svg>''',
}


def tech_block():
    items = "".join(f'<article class="tech__item">{ART[t]}<h3>{t}</h3><p>{d}</p></article>' for t, d in ROBOTICS)
    return f'<div class="tech reveal">{items}</div>'

SERVICES = [
    ("especialidades", "/especialidades", "Especialidades médicas", "12 especialidades en consulta: traumatología, cardiología, neurología, dermatología y más.", "especialidades", "svc--feature"),
    ("fisioterapia", "/terapias#fisioterapia", "Fisioterapia avanzada", "Siete líneas de fisioterapia, de la deportiva a la geriátrica.", "fisioterapia", ""),
    ("robotica", "/terapias#robotica", "Terapia robótica", "Tecarterapia, Robot SIS, tracción computarizada y ondas de choque.", "robotica", "svc--tech"),
    ("mefcare", "/servicios#mefcare", "MEFCare paquetes", "Planes de atención agrupados en un solo paquete.", "mefcare", ""),
    ("pisada", "/servicios#pisada", "Marcha y pisada", "Análisis biomecánico con sensores y plantillas personalizadas.", "pisada", ""),
    ("nutricion", "/servicios#unidades", "Nutrición", "Nutrición clínica y deportiva, con su propio canal de atención.", "nutricion", ""),
    ("fisiorespiratoria", "/servicios#unidades", "Fisiorespiratoria", "Fisioterapia respiratoria para niños y adultos.", "fisiorespiratoria", ""),
    ("laboratorio", "/servicios#unidades", "Laboratorio clínico", "Exámenes de laboratorio con atención por canal propio.", "laboratorio", ""),
    ("home", "/servicios#home", "Fisiolab Home", "Médico, enfermería y fisioterapia en tu casa.", "home", "svc--wide"),
]

SPECIALTIES = [
    ("traumatologia", "Traumatología", "Huesos, articulaciones y lesiones",
     "Evalúa y trata lesiones y enfermedades de huesos, articulaciones, ligamentos y tendones: esguinces, fracturas, dolor de rodilla, hombro, cadera o columna.",
     "Consulta de especialidad. Si hace falta imagen, Rayos X en el mismo centro, y derivación a fisioterapia cuando el médico la indica."),
    ("nutricion-clinica", "Nutrición clínica y deportiva", "Alimentación según tu condición y actividad",
     "Plan de alimentación para condiciones de salud o para quienes entrenan y compiten.",
     "Consulta con evaluación nutricional. Se agenda por el WhatsApp de la unidad de Nutrición."),
    ("medicina-general", "Medicina general", "Primera consulta, cirugía menor y mayor",
     "Consulta de primer contacto para orientarte y, si corresponde, derivarte a la especialidad adecuada.",
     "Consulta médica, cirugía menor y coordinación de cirugía mayor."),
    ("cardiologia", "Cardiología", "Electrocardiograma, Holter y ecocardiograma",
     "Evalúa el corazón y la circulación: presión arterial, palpitaciones, controles prequirúrgicos y seguimiento.",
     "Consulta, electrocardiograma, Holter y ecocardiograma."),
    ("dermatologia", "Dermatología", "Piel, cabello y uñas",
     "Diagnóstico y tratamiento de condiciones de la piel, el cabello y las uñas.",
     "Consulta de especialidad."),
    ("neumologia", "Neumología", "Pulmones y vías respiratorias",
     "Evalúa condiciones respiratorias como asma, tos persistente o dificultad para respirar.",
     "Consulta de especialidad y coordinación con fisioterapia respiratoria cuando se indica."),
    ("neurologia", "Neurología", "Sistema nervioso",
     "Atiende condiciones del cerebro, la médula y los nervios: dolor de cabeza recurrente, mareos, hormigueos, temblores.",
     "Consulta de especialidad y coordinación con fisioterapia neurológica cuando se indica."),
    ("rayosx", "Imágenes · Rayos X", "Rayos X digital en el centro",
     "Estudios de Rayos X sin salir del centro, para que el especialista revise la imagen en la misma visita.",
     "Rayos X digital. Pregunta por WhatsApp qué estudio necesitas y si requiere orden médica."),
    ("reumatologia", "Reumatología", "Articulaciones y enfermedades autoinmunes",
     "Evalúa dolor e inflamación articular persistente y enfermedades reumáticas.",
     "Consulta de especialidad."),
    ("deportologia", "Deportología", "Medicina del deporte y prueba de esfuerzo",
     "Para deportistas y personas activas: evaluación antes de entrenar, lesiones deportivas y retorno a la actividad.",
     "Consulta de especialidad y prueba de esfuerzo."),
    ("vascular", "Cirugía vascular y angiología", "Venas, arterias y circulación",
     "Evalúa várices, problemas de circulación en piernas y otras condiciones vasculares.",
     "Consulta de especialidad."),
    ("neurocirugia", "Neurocirugía", "Columna, cerebro y nervios",
     "Valoración de condiciones de columna y sistema nervioso que pueden requerir manejo quirúrgico.",
     "Consulta de especialidad."),
]

PHYSIO = [
    ("Deportiva", "Para lesiones del deporte y para volver a entrenar con un plan."),
    ("Traumatológica", "Después de fracturas, esguinces, cirugías o lesiones de articulaciones."),
    ("Neurológica", "Para personas con condiciones del sistema nervioso que afectan el movimiento."),
    ("Manual ortopédica", "Técnicas manuales sobre articulaciones, músculos y columna."),
    ("Cardíaca", "Ejercicio supervisado para personas con condiciones cardíacas, según indicación médica."),
    ("Respiratoria", "Técnicas para la función respiratoria en niños y adultos."),
    ("Geriátrica", "Movilidad, equilibrio y fuerza para adultos mayores."),
]

ROBOTICS = [
    ("Tecarterapia", "Transfiere energía al tejido mediante corrientes capacitivas y resistivas. Se aplica en sesiones dentro del plan de fisioterapia."),
    ("Robot SIS", "Sistema super inductivo: estimulación con campo electromagnético de alta intensidad, sin contacto directo con la piel."),
    ("Tracción vertebral computarizada", "Tracción de columna cervical o lumbar con fuerza y tiempos controlados por computadora."),
    ("Ondas de choque", "Ondas acústicas aplicadas sobre una zona localizada, en sesiones cortas."),
]

FAQ = [
    ("¿Qué especialidades atienden?",
     'Doce: traumatología, nutrición clínica y deportiva, medicina general, cardiología, dermatología, neumología, neurología, imágenes Rayos X, reumatología, deportología, cirugía vascular y angiología, y neurocirugía. Las ves en detalle en <a href="/especialidades">Especialidades</a>.'),
    ("¿Necesito una referencia médica?",
     f'Para consulta de especialidad puedes agendar directamente por WhatsApp. Si ya tienes órdenes o exámenes previos, llévalos a tu cita. {ph("CONFIRMAR_REFERENCIA")}'),
    ("¿Cómo agendo?",
     "Por WhatsApp. Eliges el servicio en la web, se abre el chat con el mensaje listo y el equipo te confirma día y hora. También puedes llamar al 02-2070188."),
    ("¿Atienden a domicilio?",
     'Sí, con Fisiolab Home: médico general, enfermería y fisioterapia para pacientes con dificultad para desplazarse. <a href="/servicios#home">Ver Fisiolab Home</a>.'),
    ("¿Qué formas de pago aceptan?", ph("FORMAS_PAGO")),
    ("¿Tienen estacionamiento?", ph("PARQUEO")),
]


# ---------------------------------------------------------------- páginas
DIRECTORY = [
    ("Consulta e imagen", [
        ("Especialidades médicas", "12 especialidades: traumatología, cardiología, neurología, dermatología y más.", "/especialidades", "especialidades"),
        ("Rayos X", "Imagen digital en el centro, revisada por tu especialista en la misma visita.", "/especialidades#rayosx", "rayosx"),
        ("Laboratorio clínico", "Exámenes con atención por su propio WhatsApp.", "/servicios#laboratorio", "laboratorio"),
    ]),
    ("Rehabilitación", [
        ("Fisioterapia avanzada", "Siete líneas, de la deportiva a la geriátrica, con evaluación al inicio.", "/terapias#fisioterapia", "fisioterapia"),
        ("Terapia robótica", "Tecarterapia, Robot SIS, tracción computarizada y ondas de choque.", "/terapias#robotica", "robotica"),
        ("Fisiorespiratoria", "Fisioterapia respiratoria para niños y adultos.", "/servicios#fisiorespiratoria", "fisiorespiratoria"),
        ("Marcha y pisada", "Análisis con sensores, plantillas y recomendación de calzado.", "/servicios#pisada", "pisada"),
    ]),
    ("Planes y atención en casa", [
        ("Paquetes MEFCare", "Consultas y sesiones agrupadas en un solo plan.", "/servicios#mefcare", "mefcare"),
        ("Nutrición", "Clínica y deportiva, con su propio canal.", "/servicios#nutricion", "nutricion"),
        ("Fisiolab Home", "Médico, enfermería y fisioterapia en tu casa.", "/servicios#home", "home"),
    ]),
]


def directory():
    out = ""
    for gi, (g, rows) in enumerate(DIRECTORY):
        r = ""
        for name, desc, href, wa in rows:
            r += f'''
        <li><a class="dir__row" href="{href}">
          <span class="dir__name">{name}</span>
          <span class="dir__desc">{desc}</span>
          <span class="dir__go"><span class="circ circ--arrow">{ARROW}</span></span>
        </a></li>'''
        out += f'<div class="dir__group reveal" data-d="{gi}"><h3>{g}</h3><ul>{r}</ul></div>'
    return f'<div class="dir">{out}</div>'


def build_index():
    team = "".join(
        f'<div class="doc reveal" data-d="{i}">{photo("Retrato pendiente", "Fondo neutro, luz natural", "EQUIPO")}<h3>Nombre del especialista</h3><p>Especialidad · Reg. SENESCYT</p>{ph("REGISTRO_SENESCYT")}</div>'
        for i in range(4))
    finder = [("especialidades", "Un especialista", "12 especialidades"), ("fisioterapia", "Fisioterapia", "Evaluación y plan"),
              ("robotica", "Terapia robótica", "4 equipos"), ("rayosx", "Rayos X", "En el centro"),
              ("home", "Atención en casa", "Fisiolab Home"), ("general", "No estoy seguro", "Te orientamos")]
    fopts = "".join(f'<button type="button" data-agendar="{k}">{t}<span>{s}</span></button>' for k, t, s in finder)

    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": "Fisiolab.Ec & MEF Care — Centro de Especialidades Médicas",
        "url": BASE + "/",
        "logo": BASE + "/assets/logo-full-blue.png",
        "image": BASE + "/assets/og.jpg",
        "telephone": "+593-2-207-0188",
        "email": "fisio.lab@hotmail.com",
        "address": {"@type": "PostalAddress", "streetAddress": "Matilde Albán E2-47 y Sucre", "addressLocality": "Conocoto, Quito",
                    "addressRegion": "Pichincha", "addressCountry": "EC"},
        "areaServed": ["Conocoto", "Valle de los Chillos", "Quito"],
        "hasMap": "https://g.co/kgs/KzDytyt",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "51", "bestRating": "5"},
        "medicalSpecialty": ["Orthopedic", "Cardiovascular", "Dermatology", "Pulmonary", "Neurologic", "Radiography",
                             "Rheumatologic", "PhysicalTherapy", "DietNutrition", "Surgical"],
        "sameAs": ["https://www.instagram.com/fisiolab.ec_clinicas/", "https://www.instagram.com/mefcare/",
                   "https://www.facebook.com/fisiolab.ec", "https://www.tiktok.com/@fisiolab.ec"]
        # openingHoursSpecification: {{HORARIOS}} — agregar al confirmar horarios con el cliente
    }
    ld = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>\n"

    main = f'''
<section class="hero" id="inicio">
  <svg class="hero__rings" viewBox="0 0 1000 1000" aria-hidden="true"><circle cx="500" cy="500" r="200"/><circle cx="500" cy="500" r="320"/><circle cx="500" cy="500" r="440"/></svg>
  <img class="hero__fig" src="/assets/icon-white-lg.png" width="594" height="1000" alt="">
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <h1><span class="ln"><span>Consulta, imagen</span></span><span class="ln"><span>y rehabilitación</span></span><span class="ln"><span><em>bajo el mismo techo.</em></span></span></h1>
        <p class="hero__lede">Especialistas, Rayos X, fisioterapia y terapia robótica en Conocoto. Eliges el servicio y coordinamos tu cita por WhatsApp.</p>
        <div class="hero__actions">
          {agendar_btn("", "Agendar por WhatsApp", "btn btn--on-brand")}
          <a class="link" href="#servicios">Ver todos los servicios</a>
        </div>
      </div>
      <div class="finder">
        <h2>¿Qué necesitas hoy?</h2>
        <p>Toca una opción y te dejamos el mensaje listo.</p>
        <div class="finder__opts">{fopts}</div>
      </div>
    </div>
    <div class="proof">
      <ul aria-label="Datos del centro">
        <li><b>15 años</b>en el Valle de los Chillos</li>
        <li><b>4,6</b><span class="stars" aria-hidden="true">★★★★★</span>51 opiniones en Google</li>
        <li><b>Rayos X</b>digital dentro del centro</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec" id="servicios">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Todo el grupo,<br><em>en una sola puerta.</em></h2>
      <p class="reveal" data-d="1">Antes eran siete cuentas, varios números y una web que no los unía. Aquí está cada servicio de Fisiolab, ordenado por lo que necesitas.</p>
    </div>
    {directory()}
  </div>
</section>

<section class="sec sec--surface" id="clinica">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Del consultorio a la sala de terapia, <em>sin cambiar de dirección.</em></h2>
      <p class="reveal" data-d="1">Fisiolab empezó hace 15 años como centro de fisioterapia. Hoy es un Centro de Especialidades Médicas: el mismo equipo te acompaña de la consulta a la rehabilitación.</p>
    </div>
    <div class="route reveal">
      <svg class="route__line" preserveAspectRatio="none" viewBox="0 0 1000 2" aria-hidden="true"><line x1="0" y1="1" x2="1000" y2="1"/></svg>
      <ol>
      <li data-n="1"><span class="route__v"></span><h3>Consulta con el especialista</h3><p>Traumatología, neurología, cardiología o la especialidad que necesites.</p></li>
      <li data-n="2"><span class="route__v"></span><h3>Imagen en el mismo centro</h3><p>Rayos X digital sin salir del edificio. El especialista revisa la imagen ese día.</p></li>
      <li data-n="3"><span class="route__v"></span><h3>Rehabilitación con plan</h3><p>Fisioterapia y terapia robótica según la indicación médica.</p></li>
      <li data-n="4"><h3>Seguimiento o atención en casa</h3><p>Controles en el centro o con Fisiolab Home si te cuesta desplazarte.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="sec sec--deep" id="robotica">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Cuatro equipos de terapia robótica, <em>dentro de tu plan.</em></h2>
      <p class="reveal" data-d="1">No son sesiones sueltas: el fisioterapeuta decide cuál usar, cuántas sesiones y con qué intensidad, y te lo explica antes de empezar. <a class="link" style="color:#fff" href="/terapias#robotica">Conocer cada equipo</a></p>
    </div>
    {tech_block()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Las personas que <em>te atienden.</em></h2>
      <p class="reveal" data-d="1">Cada profesional con nombre, especialidad y registro SENESCYT verificable. <a class="link" href="/equipo">Ver equipo e instalaciones</a></p>
    </div>
    <div class="team">{team}</div>
  </div>
</section>

<section class="sec sec--surface" id="resenas">
  <div class="wrap rating">
    <div class="reveal"><div class="rating__num">4,6</div><div class="rating__stars" aria-hidden="true">★★★★★</div></div>
    <div class="reveal" data-d="1">
      <h2 class="h-l">51 pacientes opinaron en Google.</h2>
      <p class="muted" style="margin:1rem 0 1.5rem;max-width:46ch">Léelas directamente en Google Maps, sin filtros. {ph("RESEÑAS_GOOGLE")}</p>
      <a class="link" href="#" data-maps>Ver opiniones en Google</a>
    </div>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <aside class="pro reveal" aria-label="Educación para profesionales">
      <div><h2>¿Eres profesional de la salud?</h2><p>Cursos y talleres de Fisiolab Edusalud, aparte de la atención a pacientes.</p></div>
      <a class="link" href="/profesionales">Ver cursos</a>
    </aside>
  </div>
</section>
{cta_final()}'''
    page("index.html", "inicio",
         "Fisiolab.Ec | Especialidades médicas y fisioterapia en Conocoto, Quito",
         "Centro de Especialidades Médicas en Conocoto, Valle de los Chillos (Quito): 12 especialidades, Rayos X, fisioterapia avanzada y terapia robótica. Agenda por WhatsApp.",
         "/", main, ld)


def build_especialidades():
    items = ""
    for slug, name, sub, what, inc in SPECIALTIES:
        svc = {"nutricion-clinica": "nutricion_clinica", "medicina-general": "medicina_general"}.get(slug, slug)
        items += f'''
      <div class="acc__item" id="{slug}">
        <h3><button class="acc__btn" type="button" aria-expanded="false" aria-controls="p-{slug}">
          <span><span class="t">{name}</span><span class="s">{sub}</span></span><span class="acc__plus" aria-hidden="true"></span>
        </button></h3>
        <div class="acc__panel" id="p-{slug}" role="region"><div>
          <div class="acc__body">
            <div><h4>Qué atiende</h4><p>{what}</p></div>
            <div><h4>Qué incluye</h4><p>{inc}</p></div>
            <div>{wa_btn(svc, "Agendar", "btn btn--sm", "especialidades")}</div>
          </div>
        </div></div>
      </div>'''
    main = page_hero("Especialidades", "Doce especialidades, <em>un solo centro.</em>",
                     "Abre cada una para ver qué atiende y qué incluye. El botón de cada especialidad abre WhatsApp con ella ya escrita.") + f'''
<section class="sec" aria-labelledby="lista-esp">
  <div class="wrap">
    <div class="split split--wide">
      <div>
        <h2 class="sr-only" id="lista-esp">Listado de especialidades</h2>
        <div class="acc">{items}
        </div>
      </div>
      <aside class="sticky reveal">
        <h2 class="h-l">¿No sabes cuál <em>te corresponde?</em></h2>
        <p class="muted" style="margin:1rem 0 1.75rem">Agenda medicina general o cuéntanos qué buscas. Te orientamos por WhatsApp antes de la cita.</p>
        {agendar_btn("general", "Que me orienten")}
      </aside>
    </div>
  </div>
</section>
{cta_final("¿Ya sabes qué <em>especialidad necesitas?</em>", "Escríbenos por WhatsApp y te damos el primer turno disponible.")}'''
    page("especialidades.html", "especialidades",
         "Especialidades médicas en Conocoto, Quito | Fisiolab.Ec",
         "Traumatología, cardiología, neurología, dermatología, Rayos X y 7 especialidades más en Conocoto, Valle de los Chillos. Agenda por WhatsApp.",
         "/especialidades", main)


def build_terapias():
    physio = "".join(f'<div><dt>Fisioterapia {t.lower()}</dt><dd>{d}</dd></div>' for t, d in PHYSIO)
    main = page_hero("Terapias", "Rehabilitación con plan <em>y tecnología.</em>",
                     "Siete líneas de fisioterapia y cuatro equipos de terapia robótica. Todo empieza con una evaluación del fisioterapeuta.",
                     [("fisioterapia", "Fisioterapia avanzada"), ("robotica", "Terapia robótica"), ("como-funciona", "Cómo empezar")]) + f'''
<section class="sec" id="fisioterapia">
  <div class="wrap split">
    <div class="sticky">
      <h2 class="h-xl reveal">Siete líneas de <em>fisioterapia.</em></h2>
      <p class="muted reveal" data-d="1" style="margin:1.25rem 0 2rem;max-width:40ch">El fisioterapeuta revisa tu caso, define la línea de trabajo y te explica el plan de sesiones.</p>
      <div class="reveal" data-d="2">{wa_btn("fisioterapia", "Agendar fisioterapia", "btn", "terapias")}</div>
    </div>
    <dl class="deflist reveal">{physio}
      <div><dt>¿Te cuesta venir?</dt><dd>Fisiolab Home lleva la fisioterapia a tu casa. <a class="link" href="/servicios#home">Ver Fisiolab Home</a></dd></div>
    </dl>
  </div>
</section>

<section class="sec sec--deep" id="robotica">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Terapia robótica, <em>dentro del plan.</em></h2>
      <p class="reveal" data-d="1">Se usa como parte de tu fisioterapia, no como sesión suelta. El fisioterapeuta define el equipo, el número de sesiones y la intensidad.</p>
    </div>
    {tech_block()}
    <div class="notice" style="color:var(--on-brand-2)">{wa_btn("robotica", "Preguntar por terapia robótica", "btn btn--on-brand btn--sm", "terapias")} <span>Certificación de los equipos: {ph("CONFIRMAR_CERTIFICACION_BTL")}, se publica solo con documento.</span></div>
  </div>
</section>

<section class="sec" id="como-funciona">
  <div class="wrap split">
    <div>
      <h2 class="h-xl reveal">Cómo <em>empezar.</em></h2>
      <div class="route route--v reveal"><ol>
        <li data-n="1"><span class="route__v"></span><h3>Escribes por WhatsApp</h3><p>Eliges fisioterapia o terapia robótica y te damos día y hora.</p></li>
        <li data-n="2"><span class="route__v"></span><h3>Evaluación inicial</h3><p>El fisioterapeuta revisa tu caso y tus exámenes si los tienes.</p></li>
        <li data-n="3"><h3>Plan de sesiones</h3><p>Qué técnicas, cuántas sesiones y cómo se hace el seguimiento.</p></li>
      </ol></div>
      <div style="margin-top:2.5rem">{agendar_btn("fisioterapia", "Agendar evaluación")}</div>
    </div>
    {photo("Sala de terapia", "Foto de la sala con los equipos de robótica.", "FOTOS_INSTALACIONES", "reveal", "aspect-ratio:4/5")}
  </div>
</section>
{cta_final()}'''
    page("terapias.html", "terapias",
         "Fisioterapia y terapia robótica en Conocoto, Quito | Fisiolab.Ec",
         "Fisioterapia deportiva, traumatológica, neurológica, respiratoria y geriátrica. Tecarterapia, Robot SIS, tracción vertebral y ondas de choque en el Valle de los Chillos.",
         "/terapias", main)


def build_servicios():
    pk = "".join(f'''<div class="pkg reveal" data-d="{i}">{ph("PAQUETES_MEFCARE")}
        <h3>{n}</h3><p class="muted small" style="margin:0">Servicios incluidos, número de consultas o sesiones.</p><p class="pkg__price">Precio o “consultar”</p>
        <div>{wa_btn("mefcare", "Consultar", "btn btn--sm", "mefcare")}</div></div>''' for i, n in enumerate(["Nombre del paquete", "Nombre del paquete", "Nombre del paquete"]))
    main = page_hero("Servicios", "Cada servicio <em>con su canal.</em>",
                     "Paquetes de atención, análisis de pisada, nutrición, laboratorio, fisiorespiratoria y atención a domicilio.",
                     [("mefcare", "MEFCare"), ("pisada", "Marcha y pisada"), ("unidades", "Nutrición, laboratorio, respiratoria"), ("home", "Fisiolab Home")]) + f'''
<section class="sec" id="mefcare">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Paquetes MEFCare, <em>con precio claro.</em></h2>
      <p class="reveal" data-d="1">Agrupan consultas y sesiones en un solo plan, para que sepas cuánto vas a invertir antes de empezar. <a class="link" href="#" data-social="mefcare">@mefcare</a></p>
    </div>
    <div class="pkgs">{pk}</div>
  </div>
</section>

<section class="sec sec--surface" id="pisada">
  <div class="wrap split">
    <div>
      <h2 class="h-xl reveal">Cómo pisas, <em>medido con sensores.</em></h2>
      <p class="muted reveal" data-d="1" style="margin:1.25rem 0 0;max-width:44ch">Un análisis biomecánico de tu forma de caminar y pisar, para definir plantillas y calzado con datos.</p>
      <ul class="checks reveal" data-d="2">
        <li>Análisis biomecánico de la marcha con sensores</li>
        <li>Plantillas personalizadas</li>
        <li>Recomendación de calzado</li>
      </ul>
      <div class="hero__actions" style="margin:0">{wa_btn("pisada", "Agendar evaluación", "btn", "pisada")}<a class="link" href="#" data-social="pisada">@fisiolab.ec_pisada</a></div>
    </div>
    {photo("Evaluación de pisada", "Foto del equipo de sensores.", "FOTOS_INSTALACIONES", "reveal", "aspect-ratio:1")}
  </div>
</section>

<section class="sec" id="unidades">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Escribe directo <em>a la unidad.</em></h2>
      <p class="reveal" data-d="1">Nutrición y Laboratorio tienen su propio WhatsApp. Así te responde quien sabe del tema.</p>
    </div>
    <dl class="deflist reveal">
      <div id="nutricion"><dt>Nutrición</dt><dd>Nutrición clínica y deportiva: plan de alimentación según tu condición y tu actividad.
        <span class="act">{wa_btn("nutricion", "WhatsApp 0999882269", "btn btn--sm", "unidades")}<a class="link small" href="#" data-social="nutricion">@fisiolab.ec_nutricion</a></span></dd></div>
      <div id="laboratorio"><dt>Laboratorio clínico</dt><dd>Exámenes de laboratorio. Pregunta por preparación, toma de muestra y entrega de resultados.
        <span class="act">{wa_btn("laboratorio", "WhatsApp 0999887103", "btn btn--sm", "unidades")}<a class="link small" href="#" data-social="laboratorio">@fisiolab.ec_laboratorioclinico</a></span></dd></div>
      <div id="fisiorespiratoria"><dt>Fisiorespiratoria</dt><dd>Fisioterapia respiratoria para niños y adultos, con técnicas para la función pulmonar.
        <span class="act">{wa_btn("fisiorespiratoria", "Agendar", "btn btn--sm", "unidades")}<a class="link small" href="#" data-social="fisiorespiratoria">@fisiolab.ec_fisiorespiratoria</a></span></dd></div>
    </dl>
  </div>
</section>

<section class="sec sec--deep" id="home">
  <div class="wrap split">
    <div>
      <h2 class="h-xl reveal">Si te cuesta venir, <em>vamos a tu casa.</em></h2>
      <p class="reveal" data-d="1" style="color:var(--on-brand-2);margin:1.25rem 0 0;max-width:44ch">Fisiolab Home atiende a pacientes con dificultad para desplazarse: adultos mayores, personas en recuperación o con movilidad reducida.</p>
      <ul class="checks reveal" data-d="2"><li>Médico general a domicilio</li><li>Enfermería</li><li>Fisioterapia en casa</li></ul>
      {wa_btn("home", "Pedir atención a domicilio", "btn btn--on-brand", "home")}
    </div>
    {photo("Fisiolab Home", "Foto del equipo a domicilio, con autorización del paciente.", "FOTOS_INSTALACIONES", "reveal", "aspect-ratio:4/5")}
  </div>
</section>
{cta_final()}'''
    page("servicios.html", "servicios",
         "MEFCare, pisada, nutrición, laboratorio y atención a domicilio | Fisiolab.Ec",
         "Paquetes MEFCare, evaluación de marcha y pisada, nutrición, laboratorio clínico, fisioterapia respiratoria y Fisiolab Home a domicilio en Conocoto y el Valle de los Chillos.",
         "/servicios", main)


def build_equipo():
    team = "".join(
        f'<div class="doc reveal" data-d="{i % 4}">{photo("Retrato pendiente", "Fondo neutro, luz natural", "EQUIPO")}<h3>Nombre del especialista</h3><p>Especialidad · Reg. SENESCYT</p>{ph("REGISTRO_SENESCYT")}</div>'
        for i in range(8))
    gal = [("Fachada", "Entrada por la Matilde Albán", "g-a"), ("Recepción", "Llegada y espera", ""), ("Consultorio", "Consulta de especialidad", ""),
           ("Terapia robótica", "Tecar, SIS, tracción, ondas de choque", "g-d"), ("Rayos X", "Sala de imagen", ""), ("Sala de terapia", "Camillas y gimnasio", "")]
    g = "".join(photo(t, s, "FOTOS_INSTALACIONES", c + " reveal") for t, s, c in gal)
    main = page_hero("Equipo", "Quién te atiende <em>y dónde.</em>",
                     "El equipo médico con especialidad y registro SENESCYT, y el centro tal como es.",
                     [("equipo", "Equipo médico"), ("instalaciones", "Instalaciones")]) + f'''
<section class="sec" id="equipo">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">Especialistas con <em>nombre y registro.</em></h2>
      <p class="reveal" data-d="1">Puedes verificar el registro de cada profesional en la consulta pública de la SENESCYT.</p>
    </div>
    <div class="team">{team}</div>
  </div>
</section>

<section class="sec sec--surface" id="instalaciones">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h-xl reveal">El centro, <em>por dentro.</em></h2>
      <p class="reveal" data-d="1">Fotos reales del centro, sin imágenes de banco.</p>
    </div>
    <div class="gallery">{g}</div>
  </div>
</section>
{cta_final()}'''
    page("equipo.html", "equipo",
         "Equipo médico e instalaciones | Fisiolab.Ec Conocoto",
         "Conoce al equipo médico de Fisiolab.Ec y sus instalaciones en Conocoto, Valle de los Chillos: consultorios, sala de terapia, robótica y Rayos X.",
         "/equipo", main)


def build_ubicacion():
    import re
    faq = ""
    for i, (q, a) in enumerate(FAQ, 1):
        faq += f'''
      <div class="acc__item">
        <h3><button class="acc__btn" type="button" aria-expanded="false" aria-controls="faq-{i}"><span class="t" style="font-size:clamp(1.2rem,1.05rem + .6vw,1.5rem)">{q}</span><span class="acc__plus" aria-hidden="true"></span></button></h3>
        <div class="acc__panel" id="faq-{i}" role="region"><div><div class="acc__body" style="grid-template-columns:1fr"><p>{a}</p></div></div></div>
      </div>'''
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer",
                              "text": re.sub(r"<[^>]+>", "", a).replace("{{CONFIRMAR_REFERENCIA}}", "").strip()}} for q, a in FAQ[:4]]}
    ld = '<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + "</script>\n"
    main = page_hero("Ubicación", "A dos cuadras del <em>Centro de Salud Conocoto.</em>",
                     "Matilde Albán E2-47 y Sucre, Conocoto, Valle de los Chillos, Quito.",
                     [("como-llegar", "Cómo llegar"), ("preguntas", "Preguntas frecuentes")]) + f'''
<section class="sec" id="como-llegar">
  <div class="wrap split">
    <div class="reveal">
      <dl class="info">
        <div><dt>Dirección</dt><dd>Matilde Albán E2-47 y Sucre, Conocoto, Quito. A dos cuadras del Centro de Salud Conocoto.</dd></div>
        <div><dt>Horarios</dt><dd>{ph("HORARIOS")}<br><span class="muted">Confirma tu horario por WhatsApp antes de venir.</span></dd></div>
        <div><dt>Citas</dt><dd>WhatsApp 0983966770 · Fijo <a href="#" data-tel data-tel-label>02-2070188</a></dd></div>
        <div><dt>Unidades</dt><dd>Nutrición 0999882269 · Laboratorio 0999887103</dd></div>
        <div><dt>Correo</dt><dd><a href="#" data-mail>fisio.lab@hotmail.com</a></dd></div>
      </dl>
      <div class="hero__actions">{agendar_btn("", "Agendar por WhatsApp")}<a class="link" href="#" data-maps>Abrir en Google Maps</a></div>
    </div>
    <div class="map reveal" data-d="1">
      <div class="map__grid"></div>
      <div class="map__load">
        <span class="map__pin" aria-hidden="true"></span>
        <b class="serif" style="font-size:1.4rem;font-weight:400">Fisiolab.Ec · Conocoto</b>
        <button type="button" class="btn btn--sm" data-map-load>Cargar mapa</button>
        <span class="muted small">Se carga al tocarlo para que la página abra más rápido.</span>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--surface" id="preguntas">
  <div class="wrap split">
    <h2 class="h-xl reveal sticky">Lo que más <em>nos preguntan.</em></h2>
    <div class="acc reveal">{faq}
    </div>
  </div>
</section>
{cta_final()}'''
    page("ubicacion.html", "ubicacion",
         "Ubicación y horarios: Conocoto, Valle de los Chillos | Fisiolab.Ec",
         "Fisiolab.Ec está en Matilde Albán E2-47 y Sucre, Conocoto, Quito, a dos cuadras del Centro de Salud Conocoto. Horarios, teléfonos y preguntas frecuentes.",
         "/ubicacion", main, ld)


def build_profesionales():
    main = page_hero("Profesionales", "Cursos y talleres para <em>profesionales de la salud.</em>",
                     "Formación continua del equipo de Fisiolab Edusalud. Si eres paciente, vuelve al <a href=\"/\">inicio</a>.") + f'''
<section class="sec">
  <div class="wrap split">
    <div>
      <h2 class="h-xl reveal">Próximos <em>cursos.</em></h2>
      <p class="muted reveal" data-d="1" style="margin:1.25rem 0 2rem;max-width:44ch">Calendario, temarios y cupos se publican en Instagram y se confirman por WhatsApp. {ph("CALENDARIO_EDUSALUD")}</p>
      <div class="hero__actions" style="margin:0">{wa_btn("edusalud", "Pedir información", "btn", "edusalud")}<a class="link" href="#" data-social="edusalud">@fisiolab.ec_edusalud</a></div>
    </div>
    {photo("Taller o curso", "Foto de una sesión de formación.", "FOTOS_INSTALACIONES", "reveal", "aspect-ratio:4/3")}
  </div>
</section>'''
    page("profesionales.html", "profesionales",
         "Edusalud: cursos para profesionales de la salud | Fisiolab.Ec",
         "Cursos y talleres para profesionales de la salud de Fisiolab Edusalud en Quito.",
         "/profesionales", main)


def build_privacidad():
    main = page_hero("Privacidad", "Aviso de <em>privacidad.</em>",
                     "Borrador base según la Ley Orgánica de Protección de Datos Personales (LOPDP). Debe revisarlo el asesor legal del centro antes de publicar.") + f'''
<section class="sec">
  <div class="wrap legal">
    <p class="notice" style="margin-top:0">Texto final pendiente: {ph("AVISO_PRIVACIDAD")}</p>
    <h2>Responsable</h2>
    <p>Fisiolab.Ec &amp; MEF Care, Matilde Albán E2-47 y Sucre, Conocoto, Quito. Contacto: <a href="#" data-mail>fisio.lab@hotmail.com</a>. Razón social y RUC: {ph("RAZON_SOCIAL_RUC")}</p>
    <h2>Qué datos recibimos</h2>
    <p>Este sitio no tiene formularios. Cuando nos escribes por WhatsApp recibimos tu número, tu nombre de perfil y el mensaje que envías. El mensaje prellenado solo indica el servicio que te interesa; no pide datos de salud.</p>
    <h2>Para qué los usamos</h2>
    <p>Para responder tu consulta, coordinar tu cita y darte seguimiento sobre esa solicitud. No vendemos ni cedemos tus datos a terceros con fines comerciales.</p>
    <h2>Datos de salud</h2>
    <p>Los datos de salud son datos sensibles según la LOPDP. Se registran solo en tu historia clínica, dentro del centro, y no se solicitan por redes sociales ni por este sitio.</p>
    <h2>Mensajes de seguimiento</h2>
    <p>Si nos escribiste, podemos enviarte recordatorios relacionados con tu solicitud o tu cita. Puedes pedir que dejemos de escribirte en cualquier momento respondiendo “no deseo más mensajes”.</p>
    <h2>Medición del sitio</h2>
    <p>Usamos herramientas de medición para saber qué servicios se consultan más. {ph("HERRAMIENTAS_MEDICION")}</p>
    <h2>Tus derechos</h2>
    <p>Puedes solicitar acceso, rectificación, actualización, eliminación, oposición y portabilidad de tus datos escribiendo a <a href="#" data-mail>fisio.lab@hotmail.com</a>.</p>
  </div>
</section>'''
    page("privacidad.html", "privacidad", "Aviso de privacidad | Fisiolab.Ec",
         "Aviso de privacidad y tratamiento de datos personales de Fisiolab.Ec según la LOPDP.", "/privacidad", main)


def build_404():
    main = page_hero("404", "Esta página <em>ya no existe.</em>",
                     'La web de Fisiolab se renovó. Busca tu servicio en el <a href="/">inicio</a> o escríbenos por WhatsApp.')
    page("404.html", "404", "Página no encontrada | Fisiolab.Ec", "La página que buscas no existe.", "/404", main)


if __name__ == "__main__":
    for f in (build_index, build_especialidades, build_terapias, build_servicios, build_equipo,
              build_ubicacion, build_profesionales, build_privacidad, build_404):
        f()
    print("ok")
