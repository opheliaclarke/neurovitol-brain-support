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

  /* ---------- exit-intent popup (REPEATABLE — fires on every exit intent) ---------- */
  function exitPopup() {
    var back = document.getElementById("nv-exit");
    if (!back) return;
    var open = false, cooldownUntil = 0, started = false;
    var t = 5 * 60, mini = back.querySelector(".cd-mini-v");
    function tickStart() {
      if (started || !mini) return; started = true;
      setInterval(function () {
        t = Math.max(0, t - 1);
        mini.textContent = pad(Math.floor(t / 60)) + ":" + pad(t % 60);
      }, 1000);
    }
    function show() {
      if (open) return;
      if (Date.now() < cooldownUntil) return; // brief debounce so one exit doesn't double-fire
      open = true;
      back.classList.add("show");
      tickStart();
    }
    function hide() { open = false; back.classList.remove("show"); cooldownUntil = Date.now() + 900; }
    // desktop: re-arms every time the cursor leaves through the top of the viewport
    document.addEventListener("mouseout", function (e) {
      if (!e.relatedTarget && e.clientY <= 0) show();
    });
    // mobile: fast scroll-up (back-to-top / leave intent), repeatable
    var lastY = window.scrollY;
    window.addEventListener("scroll", function () {
      if (window.scrollY < lastY - 70 && window.scrollY < 260) show();
      lastY = window.scrollY;
    }, { passive: true });
    // mobile: browser-back intent (pushState trap) re-arms each time
    try {
      history.pushState(null, "", location.href);
      window.addEventListener("popstate", function () {
        if (window.matchMedia("(max-width:720px)").matches) { show(); history.pushState(null, "", location.href); }
      });
    } catch (e) {}
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

  /* ---------- CTA interstitial: prepare user for the offer hand-off ---------- */
  function setInterCopy() {
    var inter = document.getElementById("nv-inter");
    if (!inter) return;
    var flow = (window.NV && window.NV.flow) || "vsl";
    var h = inter.querySelector("#nv-inter-h"), p = inter.querySelector("#nv-inter-p"),
        hl = inter.querySelector("#nv-inter-hl"), go = inter.querySelector("#nv-inter-go");
    if (flow === "dtc") {
      if (h) h.textContent = "Applying your 60% discount…";
      if (p) p.innerHTML = "Taking you to the official NeuroVitol® order page to <b>choose your bottle package</b>.";
      if (hl) hl.innerHTML = "Your <b>60% OFF + free shipping</b> is locked in — pick your package on the next page and check out securely.";
      if (go) go.textContent = "Choose My Package →";
    } else {
      if (h) h.textContent = "Taking you to NeuroVitol…";
      if (p) p.innerHTML = "You're being connected to the <b>official NeuroVitol® presentation</b>.";
      if (hl) hl.innerHTML = "▶ A short video explains how NeuroVitol works and how to claim today's <b>60% discount</b>. Let it load and <b>watch it through to the end</b> — the order page appears right after.";
      if (go) go.textContent = "Continue To The Presentation →";
    }
  }
  function ctaInterstitial() {
    var inter = document.getElementById("nv-inter");
    setInterCopy();
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
          // DTC (order/selection page) = minimal friction; VSL = give the user a beat to read
          var delay = ((window.NV && window.NV.flow) === "dtc") ? 900 : 1700;
          setTimeout(function () { if (inter.classList.contains("show")) window.location.href = url; }, delay);
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
