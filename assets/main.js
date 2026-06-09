/* ============================================================
   NeuroVitol — UX: countdown, sticky CTA, exit popup, dynamic VS
   ============================================================ */
(function () {
  "use strict";

  /* ---------- countdown timers (.js-countdown) ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function startCountdowns() {
    var mins = (window.NV && window.NV.countdownMinutes) || 10;
    var els = document.querySelectorAll(".js-countdown");
    if (!els.length) return;
    var end = Date.now() + mins * 60000;
    function tick() {
      var left = Math.max(0, end - Date.now());
      var m = Math.floor(left / 60000), s = Math.floor((left % 60000) / 1000);
      els.forEach(function (el) {
        var mm = el.querySelector(".cd-m"), ss = el.querySelector(".cd-s");
        if (mm) mm.firstChild ? mm.childNodes[0].nodeValue = pad(m) : mm.textContent = pad(m);
        if (ss) ss.childNodes[0] ? ss.childNodes[0].nodeValue = pad(s) : ss.textContent = pad(s);
        var mini = el.querySelector(".cd-mini-v");
        if (mini) mini.textContent = pad(m) + ":" + pad(s);
      });
      if (left > 0) requestAnimationFrame(function(){});
    }
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- live stock drip ---------- */
  function stockDrip() {
    var els = document.querySelectorAll(".js-stock");
    if (!els.length) return;
    var n = (window.NV && window.NV.stock) || 58;
    function set() { els.forEach(function (e) { e.textContent = n; }); }
    set();
    setInterval(function () {
      if (n > 17 && Math.random() < 0.5) { n -= 1; set(); }
    }, 9000);
  }

  /* ---------- exit-intent popup ---------- */
  function exitPopup() {
    var back = document.getElementById("nv-exit");
    if (!back) return;
    var shown = false;
    function show() {
      if (shown) return;
      try { if (sessionStorage.getItem("nv_exit_done")) return; } catch (e) {}
      shown = true;
      back.classList.add("show");
      try { sessionStorage.setItem("nv_exit_done", "1"); } catch (e) {}
      // mini countdown inside popup
      var t = 5 * 60, mini = back.querySelector(".cd-mini-v");
      if (mini) {
        setInterval(function () {
          t = Math.max(0, t - 1);
          mini.textContent = pad(Math.floor(t / 60)) + ":" + pad(t % 60);
        }, 1000);
      }
    }
    function hide() { back.classList.remove("show"); }
    // desktop: mouse leaves top
    document.addEventListener("mouseout", function (e) {
      if (!e.relatedTarget && e.clientY <= 0) show();
    });
    // mobile: fast scroll-up or back-button intent + time fallback
    var lastY = window.scrollY;
    window.addEventListener("scroll", function () {
      if (window.scrollY < lastY - 60 && window.scrollY < 240) show();
      lastY = window.scrollY;
    }, { passive: true });
    setTimeout(function () { if (window.matchMedia("(max-width:720px)").matches) show(); }, 35000);
    back.addEventListener("click", function (e) { if (e.target === back) hide(); });
    var x = back.querySelector(".x"); if (x) x.addEventListener("click", hide);
    var stay = back.querySelector(".js-stay"); if (stay) stay.addEventListener("click", hide);
  }

  /* ---------- dynamic competitor comparison (?brand= or ?q=) ---------- */
  function dynamicVs() {
    var host = document.getElementById("nv-dynamic-brand");
    if (!host) return;
    var p = new URLSearchParams(location.search);
    var raw = p.get("brand") || p.get("q") || p.get("vs") || "";
    if (!raw) return;
    // sanitize -> title case, strip junk
    raw = raw.replace(/[^a-zA-Z0-9 \-']/g, " ").replace(/\s+/g, " ").trim().slice(0, 40);
    if (!raw) return;
    var nice = raw.replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    document.querySelectorAll(".js-brand").forEach(function (e) { e.textContent = nice; });
    host.style.display = "";
    if (document.title.indexOf("{") === -1)
      document.title = "NeuroVitol vs " + nice + " — Which Brain Supplement Is Better? (2026)";
  }

  /* ---------- CTA interstitial: prepare user for the VSL hand-off ---------- */
  function ctaInterstitial() {
    var inter = document.getElementById("nv-inter");
    function offer(a) {
      return (window.nvOfferUrl ? window.nvOfferUrl(a.getAttribute("data-cta") || "") : (a.getAttribute("href") || "#"));
    }
    document.querySelectorAll("a.js-cta").forEach(function (a) {
      if (a.closest("#nv-inter")) {
        // the "Continue" button inside the interstitial -> go straight to the offer
        a.addEventListener("click", function (e) { e.preventDefault(); window.location.href = offer(a); });
        return;
      }
      a.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return; // allow open-in-new-tab
        e.preventDefault();
        var url = offer(a);
        if (inter) {
          var go = inter.querySelector(".go"); if (go) go.href = url;
          inter.classList.add("show");
          setTimeout(function () { if (inter.classList.contains("show")) window.location.href = url; }, 1700);
        } else {
          window.location.href = url;
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    startCountdowns();
    stockDrip();
    exitPopup();
    ctaInterstitial();
    dynamicVs();
    // year in footer
    document.querySelectorAll(".js-year").forEach(function (e) { e.textContent = "2026"; });
  });
})();
