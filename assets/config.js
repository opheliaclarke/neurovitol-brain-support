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
    // Link 1 (uid=566) — VSL (video sales letter) offer page. Use for COLD ad traffic.
    VSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?uid=566&sub1={gclid}&sub2={gbraid}&sub3={wbraid}",
    // Link 2 (no uid) — the BOTTLE-PACK SELECTION / ORDER page (this is our DTC for this
    // offer). Confirmed by the AM: lands users straight on the package-chooser. PRIMARY.
    TSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?sub1={gclid}&sub2={gbraid}&sub3={wbraid}",
    // Spare slot if a different direct-checkout link is ever provided.
    DTC: ""
  },
  // Which offer page every CTA points to: "TSL" | "VSL" | "DTC".
  // This pre-sell SEO site uses "TSL" — it's the package-selection/order page, so warm
  // buyers go straight to choosing a pack instead of sitting through the VSL video.
  primary: "TSL",

  // CTA hand-off style: "vsl" = "watch the short video" interstitial;
  // "dtc" = fast "securing your discount → order page" transition (no video promise).
  // Matched to primary=TSL (the order/selection page), so this is "dtc".
  flow: "dtc",

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
  // fall back to VSL if the chosen link slot is empty (e.g. DTC not pasted yet)
  var tmpl = cfg.links[key] || cfg.links.VSL || cfg.links.TSL;
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
