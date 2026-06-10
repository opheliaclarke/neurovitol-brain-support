# NeuroVitol — SEO site (neurovitol.shop)

Affiliate marketing/SEO site for **NeuroVitol Advanced Brain Support** (brain / cognitive support supplement, $200 payout). Built for **organic SEO + Google Search ads cross-bidding** in the US. Static site, GitHub Pages.

> **Compliance:** NeuroVitol is positioned strictly as a **dietary supplement** — supports memory/focus/clarity — **never** as a cure or treatment for any disease. Every page carries the FDA structure/function disclaimer.

## Key decisions (made autonomously — easy to change)
- **Domain:** `neurovitol.shop` = this **SEO** site (matches the GLPure pattern: `.shop` = SEO). Keep **`neurovitol.store`** for the **paid-ads** traffic site (separate build, separate domain so SEO and ad landers don't cannibalize).
- **Offer flow — VSL vs DTC (important):** for a *pre-sell SEO page like this*, **DTC (direct-to-cart/order form) converts better than VSL** — the page already does the selling, so don't make a warm buyer sit through a 20-min video. Config in `assets/config.js`:
  - `links.VSL` = link 1 (`uid=566`), `links.TSL` = link 2 (no uid), `links.DTC` = **paste the DTC/order-form link from the AM here**.
  - `primary` = which link every CTA uses (`"DTC"` recommended once you have it; currently `"VSL"` because that's the link we have — `nvOfferUrl` falls back to VSL if DTC is blank).
  - `flow` = interstitial style: `"vsl"` shows "watch the short video"; `"dtc"` shows a fast "securing your discount → checkout". Keep matched to `primary`.
  - All CTAs use `data-cta=""` → follow `primary`, so flipping one value switches the whole site.
  - ⚠️ Raw links used malformed macros (`{gbraid|`). Normalized to `{gclid}` / `{gbraid}` / `{wbraid}`.
- **gclid capture:** `config.js` reads `gclid`, `gbraid`, `wbraid` (also `msclkid`, `fbclid`, `ttclid`) from the landing URL, persists them in `sessionStorage`, and substitutes them into the outbound offer link on every CTA click. So a Google click → this lander → offer page passes `sub1=<real gclid>`.

## Cross-bidding / "NeuroVitol is better than {brand}"
- **Static comparison pages** (great for SEO, crawlable): `vs/<brand>.html` for Alpha Brain, Mind Lab Pro, NeuroZoom, Qualia Mind, Genius Wave, Synaptigen, Neuro-Thrive, Prevagen, Neuriva, Focus Factor, NooCube, BrainMD. Hub at `vs/index.html`.
- **Dynamic catch-all:** `vs.html?brand=<anything>` (also `?q=` / `?vs=`) renders "NeuroVitol vs {that brand}" from the query string — point competitor-keyword ads here for brands without a static page.

## Conversion features
- FOMO: countdown timer, live stock drip, flash-sale bar.
- **Exit-intent popup** (drama/FOMO) — desktop mouse-leave + mobile scroll-up/time fallback.
- Sticky mobile CTA bar.
- 60-day guarantee band, trust strip, review schema.

## SEO / AEO
- Per-page `<title>`/meta/description/keywords, canonical, Open Graph, Twitter.
- JSON-LD: Product + AggregateRating + Review, Organization, WebSite+SearchAction, FAQPage, BreadcrumbList, Article.
- `sitemap.xml` (30 URLs), `robots.txt` (allows AI crawlers: GPTBot, ClaudeBot, PerplexityBot, Google-Extended…), `llms.txt`, `.nojekyll`, `CNAME`.
- Deep internal interlinking (nav, footer, related comparisons, keyword tag cloud), blog cornerstone content.

## Build
Everything is generated from `build.py` (single source of truth):
```bash
python3 build.py
```
Edit product data / competitors / copy at the top of `build.py`, then rebuild. Affiliate links live in `assets/config.js` (not regenerated) so you can swap them without rebuilding.

## Files
- `index.html` — main landing page · `benefits` · `ingredients` · `how-it-works` · `reviews` · `faq` · `about` · `contact`
- `vs/` — comparison hub + 12 static brand pages · `vs.html` — dynamic comparison
- `blog/` — 4 cornerstone articles + index
- `legal/` — privacy, terms, disclaimer
- `assets/` — `styles.css`, `config.js` (affiliate + gclid), `main.js` (UX), `favicon.svg`, `og.svg`

## TODO (next session)
- Build the **ads site** on `neurovitol.store` (tighter, single-CTA, ad-policy-safe lander complementing the VSL).
- Add a real OG raster (`og.png`) if a richer social preview is wanted.
- Confirm with the AM **which** link is actually the VSL vs TSL and flip `primary` if needed.
