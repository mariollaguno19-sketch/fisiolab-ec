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
  maps: "https://g.co/kgs/KzDytyt",
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
      d.body.style.overflow = open ? "hidden" : "";
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
    d.body.style.overflow = "hidden";
    setStep(state.service ? 1 : 0);
    track("agendar_open", { service: state.service || "sin_elegir" });
    closeToast(true);
  }
  function closeModal() {
    modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true");
    d.body.style.overflow = "";
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

  /* ---------- Año ---------- */
  d.querySelectorAll("[data-year]").forEach(e => e.textContent = new Date().getFullYear());
})();
