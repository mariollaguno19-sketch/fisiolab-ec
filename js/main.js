/* Fisiolab.Ec — script único del sitio
   Todo dato editable vive en CONFIG. Cambiar aquí, se aplica en todas las páginas. */

const CONFIG = {
  waMain: "593983966770",          // WhatsApp principal 0983966770
  waNutricion: "593999882269",     // 0999882269
  waLaboratorio: "593999887103",   // 0999887103
  waEdusalud: "593983966770",      // {{WHATSAPP_EDUSALUD}} — confirmar número propio; hoy usa el principal
  phone: "022070188",
  phoneLabel: "02-2070188",
  email: "fisio.lab@hotmail.com",
  maps: "https://maps.app.goo.gl/4i7tmCACJxaohSM86",
  mapsEmbed: "https://www.google.com/maps?q=Matilde+Alb%C3%A1n+E2-47+y+Sucre,+Conocoto,+Quito&output=embed",
  hub: "https://mylnker.com/grupofisiolabec",
  social: {
    clinicas: "https://www.instagram.com/fisiolab.ec_clinicas/",
    mefcare: "https://www.instagram.com/mefcare/",
    nutricion: "https://www.instagram.com/fisiolab.ec_nutricion/",
    pisada: "https://www.instagram.com/fisiolab.ec_pisada/",
    laboratorio: "https://www.instagram.com/fisiolab.ec_laboratorioclinico/",
    fisiorespiratoria: "https://www.instagram.com/fisiolab.ec_fisiorespiratoria/",
    edusalud: "https://www.instagram.com/fisiolab.ec_edusalud/",
    facebook: "https://www.facebook.com/fisiolab.ec",
    tiktok: "https://www.tiktok.com/@fisiolab.ec"
  },
  // Formulario de orientación. endpoint recibe los datos (api/lead.js los reenvía a LEAD_WEBHOOK_URL).
  lead: {
    endpoint: "/api/lead",
    video: "",          // {{VIDEO_EXPLICATIVO}} URL de YouTube (embed) o .mp4: qué hace la clínica, sin promesas
    callHours: "en horario de atención"   // {{HORARIOS}}
  },
  // Fondos de video / imagen. Dejar en "" hasta tener el material.
  // video: .mp4 1920x1080, 10-15 s, sin audio, < 4 MB. poster/image: .jpg 1920 px de ancho.
  media: {
    hero:           { video: "", poster: "" },   // {{VIDEO_HERO}} recorrido por el centro
    robotica:       { video: "", poster: "" },   // {{VIDEO_ROBOTICA}} equipos en uso
    cta:            { image: "" },               // {{FOTO_CTA}} recepción o fachada
    home:           { image: "" },               // {{FOTO_HOME}} atención a domicilio
    especialidades: { image: "" },               // {{FOTO_ESPECIALIDADES}}
    terapias:       { image: "" },               // {{FOTO_TERAPIAS}}
    servicios:      { image: "" },               // {{FOTO_SERVICIOS}}
    equipo:         { image: "" },               // {{FOTO_EQUIPO_GRUPAL}}
    ubicacion:      { image: "" },               // {{FOTO_FACHADA}}
    profesionales:  { image: "" }                // {{FOTO_EDUSALUD}}
  },
  // Servicio → número y mensaje. El mensaje nunca pide datos de salud.
  services: {
    general:            { label: "Cita general", n: "waMain" },
    especialidades:     { label: "Especialidades médicas", n: "waMain", msg: "una cita con un especialista" },
    traumatologia:      { label: "Traumatología", n: "waMain" },
    nutricion_clinica:  { label: "Nutrición clínica y deportiva", n: "waNutricion" },
    medicina_general:   { label: "Medicina general", n: "waMain" },
    cardiologia:        { label: "Cardiología", n: "waMain" },
    dermatologia:       { label: "Dermatología", n: "waMain" },
    neumologia:         { label: "Neumología", n: "waMain" },
    neurologia:         { label: "Neurología", n: "waMain" },
    rayosx:             { label: "Rayos X", n: "waMain" },
    reumatologia:       { label: "Reumatología", n: "waMain" },
    deportologia:       { label: "Deportología", n: "waMain" },
    vascular:           { label: "Cirugía vascular y angiología", n: "waMain" },
    neurocirugia:       { label: "Neurocirugía", n: "waMain" },
    fisioterapia:       { label: "Fisioterapia", n: "waMain" },
    robotica:           { label: "Terapia robótica", n: "waMain" },
    mefcare:            { label: "Paquetes MEFCare", n: "waMain", msg: "información de los paquetes MEFCare" },
    pisada:             { label: "Evaluación de marcha y pisada", n: "waMain", msg: "agendar una evaluación de marcha y pisada" },
    nutricion:          { label: "Nutrición", n: "waNutricion" },
    fisiorespiratoria:  { label: "Fisioterapia respiratoria", n: "waMain" },
    laboratorio:        { label: "Laboratorio clínico", n: "waLaboratorio", msg: "información para exámenes de laboratorio" },
    home:               { label: "Fisiolab Home (a domicilio)", n: "waMain", raw: "Hola, quiero agendar una atención a domicilio con Fisiolab Home." },
    edusalud:           { label: "Edusalud", n: "waEdusalud", raw: "Hola, soy profesional de la salud y quiero información de los cursos y talleres de Fisiolab Edusalud." }
  }
};

const ANALYTICS = { ga4: "", metaPixel: "" }; // {{GA4_ID}} {{PIXEL_ID}} — se activan cuando el cliente los entregue

(function () {
  const d = document, root = d.documentElement;
  root.classList.add("js");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- WhatsApp ---------- */
  function waMessage(key, extra) {
    const s = CONFIG.services[key] || CONFIG.services.general;
    let m = s.raw ? s.raw : key === "general"
      ? "Hola, quiero agendar una cita en Fisiolab."
      : "Hola, quiero " + (s.msg ? s.msg : "agendar una cita de " + s.label) + " en Fisiolab.";
    if (extra) m += " " + extra;
    return m;
  }
  function waUrl(key, extra) {
    const s = CONFIG.services[key] || CONFIG.services.general;
    return "https://wa.me/" + CONFIG[s.n] + "?text=" + encodeURIComponent(waMessage(key, extra));
  }
  function track(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params));
    if (window.fbq) window.fbq("trackCustom", name, params);
  }
  // Enlaces directos con data-wa="servicio"
  d.querySelectorAll("[data-wa]").forEach(a => {
    a.href = waUrl(a.dataset.wa);
    a.target = "_blank"; a.rel = "noopener";
    a.addEventListener("click", () => track("whatsapp_click", { service: a.dataset.wa, source: a.dataset.src || location.pathname }));
  });
  // Datos de contacto rellenados desde CONFIG
  d.querySelectorAll("[data-tel]").forEach(a => { a.href = "tel:+593" + CONFIG.phone.slice(1); });
  d.querySelectorAll("[data-tel-label]").forEach(e => { e.textContent = CONFIG.phoneLabel; });
  d.querySelectorAll("[data-mail]").forEach(a => { a.href = "mailto:" + CONFIG.email; a.textContent = CONFIG.email; });
  d.querySelectorAll("[data-maps]").forEach(a => { a.href = CONFIG.maps; a.target = "_blank"; a.rel = "noopener"; });
  d.querySelectorAll("[data-social]").forEach(a => { a.href = CONFIG.social[a.dataset.social]; a.target = "_blank"; a.rel = "noopener"; });

  /* ---------- Loader (primera vista de la sesión) ----------
     Secuencia: la figura se levanta, se estira, entra el wordmark y la cortina sube.
     Dura al menos 2.8 s para que la animación se vea completa; tope duro de 4 s. */
  const loader = d.querySelector(".loader");
  if (loader) {
    if (store.get("fl_seen") || reduce) { loader.remove(); }
    else {
      store.set("fl_seen", "1");
      d.body.style.overflow = "hidden";
      const t0 = performance.now(), MIN = 2800, MAX = 4000;
      let closed = false;
      const done = () => {
        if (closed) return; closed = true;
        loader.classList.add("is-done"); d.body.style.overflow = "";
        root.classList.add("is-loaded");
        setTimeout(() => loader.remove(), 1100);
      };
      const later = () => setTimeout(done, Math.max(0, MIN - (performance.now() - t0)));
      if (d.readyState === "complete") later(); else addEventListener("load", later, { once: true });
      setTimeout(done, MAX);
    }
  }
  if (!loader || !d.body.contains(loader)) root.classList.add("is-loaded");

  /* ---------- Header ---------- */
  const header = d.querySelector(".header");
  const wa = d.querySelector(".wa-float");
  let ticking = false;
  const hero = d.querySelector(".hero, .page-hero");
  function onScroll() {
    const y = scrollY;
    header && header.classList.toggle("is-scrolled", y > 8);
    if (header && hero) header.classList.toggle("header--on-brand", y < hero.offsetHeight - 40);
    wa && wa.classList.toggle("is-visible", y > 420 || d.body.dataset.page !== "inicio");
    ticking = false;
  }
  addEventListener("scroll", () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  const burger = d.querySelector(".burger"), drawer = d.querySelector(".drawer");
  if (burger && drawer) {
    burger.addEventListener("click", () => {
      const open = burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", open);
      drawer.classList.toggle("is-open", open);
      root.classList.toggle("is-locked", open);
    });
    drawer.addEventListener("click", e => { if (e.target.closest("a")) { burger.click(); } });
  }

  /* ---------- Acordeón ---------- */
  d.querySelectorAll(".acc__btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".acc__item");
      const open = !item.classList.contains("is-open");
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open);
    });
  });
  // Abrir el ítem si llega por ancla (#traumatologia)
  if (location.hash) {
    const t = d.getElementById(location.hash.slice(1));
    const b = t && t.querySelector(".acc__btn");
    if (b && b.getAttribute("aria-expanded") === "false") b.click();
  }

  /* ---------- Reveal ---------- */
  const rev = d.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
    rev.forEach(el => io.observe(el));
  } else rev.forEach(el => el.classList.add("is-in"));
  // Respaldo: si el observador no dispara (pestaña oculta, render sin scroll), mostrar todo.
  setTimeout(() => rev.forEach(el => { const r = el.getBoundingClientRect(); if (r.top < innerHeight) el.classList.add("is-in"); }), 4500);

  /* ---------- Mapa ligero: se carga al pedirlo ---------- */
  d.querySelectorAll("[data-map-load]").forEach(btn => btn.addEventListener("click", () => {
    const box = btn.closest(".map");
    const f = d.createElement("iframe");
    f.src = CONFIG.mapsEmbed; f.title = "Mapa de Fisiolab.Ec en Conocoto"; f.loading = "lazy"; f.referrerPolicy = "no-referrer-when-downgrade";
    box.appendChild(f); btn.closest(".map__load").remove();
  }));

  /* ---------- Modal: agendar con pre-clasificación ---------- */
  const modal = d.getElementById("agendar");
  let lastFocus = null;
  const state = { service: null, visit: null, when: null };
  function setStep(n) {
    modal.querySelectorAll(".modal__step").forEach((s, i) => s.classList.toggle("is-active", i === n));
    modal.querySelectorAll(".steps i").forEach((s, i) => s.classList.toggle("on", i <= n));
    const first = modal.querySelector(".modal__step.is-active button, .modal__step.is-active a");
    first && first.focus({ preventScroll: true });
  }
  function openModal(service) {
    if (!modal) return;
    lastFocus = d.activeElement;
    state.service = service && CONFIG.services[service] ? service : null;
    state.visit = state.when = null;
    modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false");
    root.classList.add("is-locked");
    setStep(state.service ? 1 : 0);
    track("agendar_open", { service: state.service || "sin_elegir" });
    closeToast(true);
  }
  function closeModal() {
    modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true");
    root.classList.remove("is-locked");
    lastFocus && lastFocus.focus && lastFocus.focus();
  }
  function finish() {
    const extra = [state.visit, state.when].filter(Boolean).join(" ");
    const link = modal.querySelector("[data-final]");
    link.href = waUrl(state.service || "general", extra);
    modal.querySelector("[data-summary]").innerHTML =
      "<b>" + (CONFIG.services[state.service] || CONFIG.services.general).label + "</b><br>" +
      waMessage(state.service || "general", extra).replace(/</g, "&lt;");
    setStep(3);
    track("agendar_clasificado", { service: state.service, visit: state.visit, when: state.when });
  }
  if (modal) {
    d.querySelectorAll("[data-agendar]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); openModal(b.dataset.agendar); }));
    modal.querySelectorAll("[data-close]").forEach(b => b.addEventListener("click", closeModal));
    modal.querySelectorAll("[data-pick-service]").forEach(b => b.addEventListener("click", () => { state.service = b.dataset.pickService; setStep(1); }));
    modal.querySelectorAll("[data-pick-visit]").forEach(b => b.addEventListener("click", () => { state.visit = b.dataset.pickVisit; setStep(2); }));
    modal.querySelectorAll("[data-pick-when]").forEach(b => b.addEventListener("click", () => { state.when = b.dataset.pickWhen; finish(); }));
    modal.querySelectorAll("[data-back]").forEach(b => b.addEventListener("click", () => setStep(+b.dataset.back)));
    modal.querySelector("[data-final]").addEventListener("click", () => { track("whatsapp_click", { service: state.service, source: "modal_agendar" }); setTimeout(closeModal, 300); });
    d.addEventListener("keydown", e => {
      if (!modal.classList.contains("is-open")) return;
      if (e.key === "Escape") closeModal();
      if (e.key === "Tab") { // trampa de foco
        const f = [...modal.querySelectorAll(".modal__close, .modal__step.is-active button, .modal__step.is-active a")];
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---------- Toast: una vez por sesión, a los 25 s o al 55 % de scroll ---------- */
  const toast = d.querySelector(".toast");
  let toastShown = !!store.get("fl_toast");
  function showToast() {
    if (toastShown || !toast || (modal && modal.classList.contains("is-open"))) return;
    toastShown = true; store.set("fl_toast", "1");
    toast.classList.add("is-open"); toast.setAttribute("aria-hidden", "false");
  }
  function closeToast(silent) {
    if (!toast) return;
    toast.classList.remove("is-open"); toast.setAttribute("aria-hidden", "true");
    if (silent) { toastShown = true; }
  }
  if (toast) {
    toast.querySelector(".toast__x").addEventListener("click", () => closeToast());
    toast.querySelector("[data-agendar]") && toast.querySelector("[data-agendar]").addEventListener("click", () => closeToast());
    setTimeout(showToast, 25000);
    addEventListener("scroll", function h() {
      if (scrollY / (d.body.scrollHeight - innerHeight) > .55) { showToast(); removeEventListener("scroll", h); }
    }, { passive: true });
  }

  /* ---------- Fondos de video / imagen ---------- */
  const saveData = navigator.connection && navigator.connection.saveData;
  d.querySelectorAll("[data-media]").forEach(box => {
    const m = CONFIG.media[box.dataset.media];
    if (!m || !(m.video || m.image || m.poster)) return;
    box.classList.add("has-media");
    const ready = () => box.classList.add("is-ready");
    if (m.video && !reduce && !saveData && innerWidth >= 760) {
      const v = d.createElement("video");
      Object.assign(v, { muted: true, loop: true, playsInline: true, autoplay: true, preload: "none" });
      v.setAttribute("muted", ""); v.setAttribute("playsinline", "");
      if (m.poster) v.poster = m.poster;
      v.addEventListener("loadeddata", ready, { once: true });
      // el video se pide después de la carga para no competir con el contenido
      addEventListener("load", () => { v.src = m.video; v.play().catch(() => {}); }, { once: true });
      if (d.readyState === "complete") { v.src = m.video; v.play().catch(() => {}); }
      box.appendChild(v);
    } else if (m.image || m.poster) {
      const i = new Image(); i.alt = ""; i.loading = box.closest(".hero") ? "eager" : "lazy"; i.decoding = "async";
      i.onload = ready; i.src = m.image || m.poster; box.appendChild(i);
    }
  });

  /* ---------- Orientación: formulario con puntaje ----------
     Cada respuesta suma puntos. 5 o más: le llamamos. 3 o 4: le proponemos consulta.
     Menos de 3: ve un video de cómo trabaja la clínica. Nunca se piden síntomas ni diagnósticos. */
  // Guardar UTM de la primera visita para saber de dónde vino el contacto
  try {
    const q = new URLSearchParams(location.search), utm = {};
    ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(k => { if (q.get(k)) utm[k] = q.get(k); });
    if (Object.keys(utm).length && !store.get("fl_utm")) store.set("fl_utm", JSON.stringify(utm));
  } catch (e) {}

  const quiz = d.getElementById("quiz");
  if (quiz) {
    const steps = [...quiz.querySelectorAll(".quiz__step")];
    const bar = quiz.querySelector(".quiz__bar");
    const count = quiz.querySelector("[data-count]");
    const back = quiz.querySelector(".quiz__back");
    const answers = {};
    let i = 0;
    const show = n => {
      i = n;
      steps.forEach((s, k) => s.classList.toggle("is-active", k === n));
      const total = steps.filter(s => !s.dataset.result).length;
      bar.style.setProperty("--p", Math.min(1, (n + 1) / total));
      count.textContent = n < total ? (n + 1) + " de " + total : "Listo";
      back.hidden = n === 0 || n >= total;
      if (n > 0) quiz.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    };
    quiz.querySelectorAll(".qopt").forEach(b => b.addEventListener("click", () => {
      const q = b.closest("[data-q]");
      q.querySelectorAll(".qopt").forEach(o => o.setAttribute("aria-checked", o === b));
      answers[q.dataset.q] = { v: b.dataset.v, s: +b.dataset.s, label: b.textContent.trim() };
      if (i === 0) track("orientacion_start", {});
      setTimeout(() => show(i + 1), 260);
    }));
    back.addEventListener("click", () => show(Math.max(0, i - 1)));

    const form = quiz.querySelector("form");
    const field = name => form.querySelector('[name="' + name + '"]');
    const invalid = (el, bad) => { (el.closest(".field") || el.closest(".consent")).classList.toggle("is-invalid", bad); return bad; };
    form.addEventListener("submit", e => {
      e.preventDefault();
      const nombre = field("nombre").value.trim();
      let cel = field("celular").value.replace(/\D/g, "");
      if (cel.startsWith("593")) cel = "0" + cel.slice(3);
      const bad = [
        invalid(field("nombre"), nombre.length < 2),
        invalid(field("celular"), !/^09\d{8}$/.test(cel)),
        invalid(field("consentimiento"), !field("consentimiento").checked)
      ].some(Boolean);
      if (bad) { form.querySelector(".is-invalid input").focus(); return; }
      if (field("empresa").value) return; // trampa para bots

      const score = Object.values(answers).reduce((a, b) => a + b.s, 0);
      const segment = score >= 5 ? "llamada" : score >= 3 ? "consulta" : "video";
      const service = { dolor: "especialidades", lesion: "fisioterapia", familiar: "home", prevenir: "medicina_general", averiguo: "general" }[(answers.motivo || {}).v] || "general";
      let utm = {}; try { utm = JSON.parse(store.get("fl_utm") || "{}"); } catch (e) {}
      const payload = {
        nombre, celular: cel, segmento: segment, puntaje: score, servicio_sugerido: service,
        respuestas: Object.fromEntries(Object.entries(answers).map(([k, a]) => [k, a.label])),
        consentimiento: true, pagina: location.pathname, utm, fecha: new Date().toISOString()
      };
      fetch(CONFIG.lead.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), keepalive: true }).catch(() => {});
      track("lead_submit", { segment, score, service });

      const res = quiz.querySelector('[data-result="' + segment + '"]');
      res.querySelectorAll("[data-name]").forEach(n => n.textContent = nombre.split(" ")[0]);
      res.querySelectorAll("[data-cel]").forEach(n => n.textContent = cel);
      res.querySelectorAll("[data-hours]").forEach(n => n.textContent = CONFIG.lead.callHours);
      res.querySelectorAll("[data-lead-wa]").forEach(a => {
        a.href = waUrl(service, "Soy " + nombre + ", completé la orientación en la web.");
        a.target = "_blank"; a.rel = "noopener";
      });
      const v = res.querySelector(".video");
      if (v && CONFIG.lead.video && !v.dataset.loaded) {
        v.dataset.loaded = "1"; v.innerHTML = "";
        const url = CONFIG.lead.video;
        const el = /\.mp4($|\?)/.test(url) ? Object.assign(d.createElement("video"), { src: url, controls: true, playsInline: true })
          : Object.assign(d.createElement("iframe"), { src: url, title: "Cómo trabaja Fisiolab", allow: "autoplay; encrypted-media; picture-in-picture", allowFullscreen: true, loading: "lazy" });
        v.appendChild(el);
      }
      show(steps.indexOf(res));
    });
    show(0);
  }

  /* ---------- Año ---------- */
  d.querySelectorAll("[data-year]").forEach(e => e.textContent = new Date().getFullYear());
})();
