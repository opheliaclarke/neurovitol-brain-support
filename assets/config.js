/* ============================================================
   NeuroVitol — affiliate / tracking config
   EDIT THIS FILE to swap links or flip the primary offer page.
   ============================================================ */
window.NV = {
  brand: "NeuroVitol",
  // ---- The two affiliate offer-page links (lckhighepcs.com) ----
  // Macros {gclid} {gbraid} {wbraid} are substituted on this landing page
  // with the values captured from THIS page's URL (set by Google auto-tagging).
  // NOTE: the raw links you provided used "{gbraid|" — that is malformed Google
  // macro syntax; normalized to {gbraid} / {wbraid} so substitution works.
  links: {
    // Link 1 (uid=566) — used as the VSL (video sales letter) offer page
    VSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?uid=566&sub1={gclid}&sub2={gbraid}&sub3={wbraid}",
    // Link 2 (no uid) — used as the TSL (text sales letter) offer page
    TSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?sub1={gclid}&sub2={gbraid}&sub3={wbraid}"
  },
  // Which offer page every CTA points to by default.
  // VSL converts best behind a strong landing experience (this site) — keep "VSL".
  // Flip to "TSL" in one edit if the network/AM says the text page performs better.
  primary: "VSL",

  // Contact / NAP (must match offer page for trust + local SEO consistency)
  phone: "(888) 203-1709",
  email: "support@neurovitol.com",

  // FOMO config
  countdownMinutes: 10,      // hero + exit countdown length
  stock: 58                  // "packs remaining"
};

/* ---- capture click ids from the landing URL & persist them ---- */
(function () {
  try {
    var p = new URLSearchParams(location.search);
    var keys = ["gclid", "gbraid", "wbraid", "msclkid", "fbclid", "ttclid"];
    keys.forEach(function (k) {
      var v = p.get(k);
      if (v) { try { sessionStorage.setItem("nv_" + k, v); } catch (e) {} }
    });
  } catch (e) {}
})();

/* ---- build the outbound offer URL with captured ids substituted ---- */
window.nvOfferUrl = function (which) {
  var cfg = window.NV;
  var key = (which || cfg.primary || "VSL").toUpperCase();
  var tmpl = cfg.links[key] || cfg.links.VSL;
  function get(k) {
    var p = new URLSearchParams(location.search);
    return p.get(k) || (function () { try { return sessionStorage.getItem("nv_" + k); } catch (e) { return ""; } })() || "";
  }
  return tmpl
    .replace(/\{gclid\}/g, encodeURIComponent(get("gclid")))
    .replace(/\{gbraid\}/g, encodeURIComponent(get("gbraid")))
    .replace(/\{wbraid\}/g, encodeURIComponent(get("wbraid")));
};

/* ---- wire every CTA: <a class="js-cta"> or [data-cta] ---- */
window.nvWireCtas = function () {
  var nodes = document.querySelectorAll("a.js-cta, a[data-cta], .js-cta a");
  nodes.forEach(function (a) {
    var which = a.getAttribute("data-cta") || "";
    a.href = window.nvOfferUrl(which);
    a.setAttribute("rel", "nofollow sponsored noopener");
    a.addEventListener("click", function () {
      // refresh just before navigation so latest ids are used
      a.href = window.nvOfferUrl(which);
    });
  });
};
document.addEventListener("DOMContentLoaded", window.nvWireCtas);
