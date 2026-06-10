/* ============================================================
   NeuroVitol — affiliate / tracking config
   EDIT THIS FILE to swap links or flip the primary offer page.
   ============================================================ */
window.NV = {
  brand: "NeuroVitol",
  // ---- The two affiliate offer-page links (lckhighepcs.com) ----
  // Macros {source_id} {gclid} {gbraid} {wbraid} are substituted on this
  // landing page with the values captured from THIS page's URL.
  links: {
    // Link 1 (uid=566) — VSL (video sales letter) offer page. Use for COLD ad traffic.
    VSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?uid=566&source_id={source_id}&sub1={gclid}&sub2={gbraid}&sub3={wbraid}",
    // Link 2 (no uid) — the BOTTLE-PACK SELECTION / ORDER page (this is our DTC for this
    // offer). Confirmed by the AM: lands users straight on the package-chooser. PRIMARY.
    TSL: "https://www.lckhighepcs.com/2GXK7W/RJSXT8/?source_id={source_id}&sub1={gclid}&sub2={gbraid}&sub3={wbraid}",
    // Spare slot if a different direct-checkout link is ever provided.
    DTC: ""
  },
  // Which offer page every CTA points to: "TSL" | "VSL" | "DTC".
  primary: "TSL",

  // CTA hand-off style: "vsl" = "watch the short video" interstitial;
  // "dtc" = fast "securing your discount → order page" transition.
  flow: "dtc",

  // ---- Traffic-source split (network-side reporting) ----
  // ggax = Google Ads traffic · orga = organic/SEO + everything else.
  // A visit counts as ADS if the landing URL carries ANY Google click id
  // (gclid = normal, gbraid/wbraid = iOS/ATT) OR an explicit src=ggax
  // (set as the campaigns' Final URL suffix as a belt-and-braces signal).
  // The verdict is persisted in sessionStorage so it survives navigation
  // between pages before the CTA click.
  sources: { ads: "ggax", organic: "orga" },

  // Contact / NAP (must match offer page for trust + local SEO consistency)
  phone: "(888) 203-1709",
  email: "support@neurovitol.com",

  // FOMO config
  countdownMinutes: 10,      // hero + exit countdown length
  stock: 58                  // "packs remaining"
};

/* ---- capture click ids + traffic source from the landing URL ---- */
(function () {
  try {
    var p = new URLSearchParams(location.search);
    var keys = ["gclid", "gbraid", "wbraid", "msclkid", "fbclid", "ttclid"];
    var sawClickId = false;
    keys.forEach(function (k) {
      var v = p.get(k);
      if (v) {
        sawClickId = sawClickId || (k === "gclid" || k === "gbraid" || k === "wbraid");
        try { sessionStorage.setItem("nv_" + k, v); } catch (e) {}
      }
    });
    // explicit ads marker from the Final URL suffix (?src=ggax) — covers the
    // rare case where auto-tagging is stripped and no click id arrives.
    var src = (p.get("src") || p.get("source_id") || "").toLowerCase();
    if (sawClickId || src === "ggax") {
      try { sessionStorage.setItem("nv_source_id", "ggax"); } catch (e) {}
    }
  } catch (e) {}
})();

/* ---- resolve the traffic source: "ggax" (ads) or "orga" (SEO/other) ---- */
window.nvSourceId = function () {
  try {
    var saved = sessionStorage.getItem("nv_source_id");
    if (saved) return saved;
  } catch (e) {}
  try {
    var p = new URLSearchParams(location.search);
    if (p.get("gclid") || p.get("gbraid") || p.get("wbraid")) return window.NV.sources.ads;
    var src = (p.get("src") || p.get("source_id") || "").toLowerCase();
    if (src === "ggax") return window.NV.sources.ads;
  } catch (e) {}
  return window.NV.sources.organic;
};

/* ---- build the outbound offer URL with captured ids substituted ----
   ADS visit  -> ...?source_id=ggax&sub1=<gclid>&sub2=<gbraid>&sub3=<wbraid>
   SEO visit  -> ...?source_id=orga&sub1=&sub2=&sub3=
   On iOS (ATT) gclid is usually absent — Google sends gbraid (web) or
   wbraid (app) instead; both are captured so conversions can be uploaded
   back to Google Ads manually via the Sheets import. */
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
    .replace(/\{source_id\}/g, encodeURIComponent(window.nvSourceId()))
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
