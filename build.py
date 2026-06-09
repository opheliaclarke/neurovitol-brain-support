#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroVitol SEO site generator -> neurovitol.shop
Builds all HTML pages, competitor comparison pages, blog, legal, sitemap, robots, llms.txt.
Run:  python3 build.py
"""
import os, json, html, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://neurovitol.shop"
BRAND = "NeuroVitol"
PRODUCT = "NeuroVitol Advanced Brain Support"
PHONE = "(888) 203-1709"
EMAIL = "support@neurovitol.com"
TODAY = "2026-06-09"
OG = DOMAIN + "/assets/og.svg"

PRICES = [
    {"name":"Starter — 2 Bottles","supply":"2-Month Supply","per":"79","total":"158","was":"395","save":"60%","feat":False},
    {"name":"Most Popular — 3 Bottles","supply":"3-Month Supply","per":"59","total":"207","was":"591","save":"65%","feat":True},
    {"name":"Best Value — 6 Bottles","supply":"6-Month Supply","per":"49","total":"294","was":"1054","save":"72%","feat":False},
]

INGREDIENTS = [
    ("Bacopa Monnieri","BM","An adaptogenic herb used in Ayurvedic tradition for centuries to support memory, learning, and everyday cognitive performance. Bacosides are the studied compounds linked to its role in supporting recall and mental processing."),
    ("Lion's Mane","LM","A functional mushroom popular for supporting focus, clarity, and healthy neurological wellness. It is one of the most talked-about nootropic ingredients of 2026 for daily brain support."),
    ("Ginkgo Biloba","GB","One of the most widely used botanicals in the world for supporting healthy circulation and overall brain performance, helping deliver oxygen-rich blood flow that the mind relies on."),
    ("Phosphatidylserine","PS","A phospholipid that supports healthy brain-cell membrane structure and the cognitive activity behind daily focus, attention, and memory formation."),
    ("Vitamin B12","B12","An essential vitamin that supports normal neurological function and healthy energy metabolism — a foundational nutrient for steady mental stamina and clear thinking."),
]

BENEFITS6 = [
    ("brain","Supports Memory & Recall","Helps support everyday recall so names, details, and next steps feel easier to keep track of."),
    ("target","Promotes Steady Focus","Helps you stay engaged with work, reading, planning, conversations, and other mentally demanding tasks."),
    ("cloud","Reduces Brain Fog","Supports clearer thinking when stress, fatigue, and overload make your mind feel slow or scattered."),
    ("bolt","Supports Cognitive Energy","Helps promote more consistent mental stamina without leaning on harsh, stimulant-heavy formulas."),
    ("shield","Supports Healthy Brain Function","Provides daily nutritional support for healthy cognitive performance as part of a long-term routine."),
    ("sparkle","Promotes Mental Clarity","Helps your thoughts feel more organized, decisive, and easier to act on throughout the day."),
]

REVIEWS = [
    ("My Thoughts Feel Less Scattered","Dawn S.","After a few weeks with NeuroVitol, I felt more on top of my day. I wasn't bouncing between tasks as much, and it felt easier to sit down, focus, and finish what I started.","5"),
    ("Afternoons Feel Clearer Now","Jenny D.","I used to hit a wall every afternoon and lose my momentum. Since adding NeuroVitol to my routine, my mind feels steadier and it's easier to stay on task without feeling mentally drained.","5"),
    ("Focus Without The Harsh Jolt","John S.","My schedule is packed, and I wanted cognitive support without leaning on harsh energy products. NeuroVitol helps me feel more engaged, steady, and productive through busy days.","5"),
    ("Easy To Stay Consistent","Kelly L.","I wanted something simple for memory and clarity support that I'd actually remember to take. NeuroVitol fits my morning routine, and I feel more clear, prepared, and consistent.","4"),
]

METRICS = [("Focus Support","98"),("Mental Clarity","96"),("Memory Support","94"),("Daily Routine","90"),("Overall Satisfaction","92")]

FAQS = [
    ("What is NeuroVitol?", f"{PRODUCT} is a daily nootropic supplement formulated to help support memory, focus, mental clarity, and healthy cognitive performance. It's designed for adults who want a simple, dependable way to feel more mentally prepared for work, family, and everyday demands. It is a dietary supplement — not a drug — and is not intended to diagnose, treat, cure, or prevent any disease."),
    ("How do I use NeuroVitol?", "Take NeuroVitol daily as directed on the product label. Consistent use is recommended for best results — the formula is built for steady, long-term daily support rather than short bursts of stimulation."),
    ("How soon will I notice results?", "Results vary from person to person. Some users notice changes within a few weeks, while more noticeable benefits may build with consistent daily use over time."),
    ("What are the ingredients?", "NeuroVitol combines five well-known brain-support ingredients: Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine, and Vitamin B12. The formula is transparent so you know exactly what you're taking."),
    ("Is NeuroVitol safe for daily use?", "NeuroVitol is made with carefully selected ingredients and intended for daily use. As with any supplement, consult your healthcare provider before use if you are pregnant, nursing, under 18, or managing a medical condition."),
    ("Does NeuroVitol contain stimulants or cause jitters?", "NeuroVitol is created for daily cognitive support without relying on harsh, crash-prone stimulant positioning — it's a non-jittery, non-habit-forming daily approach."),
    ("Can I take it with other supplements or medications?", "If you are taking prescription medication or using other wellness products regularly, it's best to speak with your healthcare provider before combining them."),
    ("Is there a money-back guarantee?", "Yes. Every order is protected by a 60-day money-back guarantee. If you're not satisfied, simply return it within the guarantee window for a refund."),
    ("How much does NeuroVitol cost?", "During the current promotion, NeuroVitol is available from $49 per bottle on the 6-bottle package, $59 per bottle on the 3-bottle package, and $79 per bottle on the 2-bottle starter — all with free shipping."),
    ("Where can I buy NeuroVitol?", "NeuroVitol is available online with no prescription needed. Use any “Claim Offer” button on this site to reach the official secure checkout and lock in today's discount."),
]

# competitor slug -> (Display Name, category line, their_price, their_angle, our_edge_line)
COMPETITORS = {
    "alpha-brain": ("Alpha Brain", "Onnit's flagship nootropic", "$79.95 / 30ct", "a proprietary 'flow state' blend with caffeine-free focus claims", "NeuroVitol pairs Bacopa, Lion's Mane, Ginkgo, Phosphatidylserine and B12 in a transparent daily formula — with a lower per-bottle price and a 60-day money-back guarantee."),
    "mind-lab-pro": ("Mind Lab Pro", "an 11-in-1 'universal nootropic'", "$69 / 30-day", "a large multi-pathway stack at a premium price", "NeuroVitol focuses on five well-studied brain-support ingredients at up to $49/bottle with free shipping and a 60-day guarantee — simpler and easier on the wallet for daily use."),
    "neurozoom": ("NeuroZoom", "a 35-in-1 memory formula", "~$79 / bottle", "a very long ingredient list marketed through a video sales letter", "NeuroVitol keeps a transparent, focused five-ingredient formula so you know exactly what you're taking, backed by 7,500+ customers and a 60-day guarantee."),
    "qualia-mind": ("Qualia Mind", "Neurohacker's 28-ingredient stack", "$139 / bottle", "a high-ingredient-count premium stack at a premium price", "NeuroVitol delivers core daily brain support — memory, focus, clarity — from $49/bottle, a fraction of the premium price, with free shipping."),
    "genius-wave": ("The Genius Wave", "a digital theta-audio program", "~$39 download", "a 7-minute audio track rather than a nutritional supplement", "NeuroVitol is an actual daily brain-support supplement with five nutrient ingredients you take, not an audio file — built for steady, long-term cognitive wellness."),
    "synaptigen": ("Synaptigen", "a ClickBank brain supplement", "~$69 / bottle", "a VSL-driven 'brain regeneration' supplement", "NeuroVitol uses a transparent, jitter-free five-ingredient formula and a clear 60-day money-back guarantee with free shipping on every order."),
    "neuro-thrive": ("Neuro-Thrive", "a mitochondrial brain formula", "~$59 / bottle", "a mitochondria-focused memory supplement sold via VSL", "NeuroVitol's blend of Bacopa, Lion's Mane, Ginkgo, Phosphatidylserine and B12 targets memory, focus and clarity together — with packages from $49/bottle and free shipping."),
    "prevagen": ("Prevagen", "an apoaequorin memory supplement", "~$69 / 30ct", "a single-ingredient (apoaequorin) approach widely sold in pharmacies", "NeuroVitol uses five complementary brain-support ingredients instead of one, at a lower per-bottle cost, with a 60-day money-back guarantee."),
    "neuriva": ("Neuriva", "a coffee-fruit & PS supplement", "~$40 / 30ct", "a two-ingredient drugstore brain-health line", "NeuroVitol adds Bacopa, Lion's Mane and Ginkgo on top of Phosphatidylserine for broader daily cognitive support — with bulk pricing down to $49/bottle."),
    "focus-factor": ("Focus Factor", "a multivitamin-style brain supplement", "~$30 / 60ct", "a vitamin-heavy 'brain health' multivitamin", "NeuroVitol is a focused nootropic-style formula built around Bacopa, Lion's Mane and Ginkgo for memory and focus — not a general multivitamin."),
    "noocube": ("NooCube", "a multi-ingredient nootropic", "$64.99 / bottle", "a productivity-focused nootropic blend", "NeuroVitol offers transparent five-ingredient daily support from $49/bottle with free shipping and a 60-day guarantee — a straightforward everyday choice."),
    "brainmd": ("BrainMD", "Dr. Amen's brain-health line", "$59+ / bottle", "a doctor-branded range of multiple separate products", "NeuroVitol brings core daily brain support into one simple formula — memory, focus and clarity — from $49/bottle with a 60-day money-back guarantee."),
}

BLOG = [
    ("best-brain-supplements-2026", "The 12 Best Brain Supplements of 2026 (Ranked & Compared)",
     "A practical 2026 buyer's guide to the best brain supplements and nootropics for memory, focus, and mental clarity — what to look for, which ingredients matter, and how NeuroVitol compares."),
    ("how-to-get-rid-of-brain-fog", "How to Get Rid of Brain Fog: 9 Daily Habits That Actually Help",
     "Brain fog leaving you forgetful and unfocused? Here are 9 evidence-informed daily habits — plus the brain-support ingredients — that help you think clearly again."),
    ("best-nootropics-for-focus-and-memory", "Best Nootropics for Focus and Memory in 2026",
     "Nootropics for studying, work, and aging: which ingredients support focus and memory, how they work, and how to build a simple daily stack with NeuroVitol."),
    ("bacopa-lions-mane-ginkgo-guide", "Bacopa, Lion's Mane & Ginkgo: The Brain-Support Ingredient Guide",
     "A plain-English guide to the five brain-support ingredients in NeuroVitol — Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12 — and what each one does."),
]

# ---------------- icons (feather-ish, stroke=currentColor) ----------------
def _svg(p): return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                      'stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>')
ICONS = {
 "brain": _svg('<path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>'),
 "target": _svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>'),
 "cloud": _svg('<path d="M17.5 19a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.6 1.5A4 4 0 0 0 6.5 19Z"/><path d="M8 13l-1 3M12 13l-1 3M16 13l-1 3"/>'),
 "bolt": _svg('<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>'),
 "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>'),
 "sparkle": _svg('<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8Z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8Z"/>'),
 "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
 "truck": _svg('<path d="M3 6h11v9H3z"/><path d="M14 9h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>'),
 "lock": _svg('<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'),
 "leaf": _svg('<path d="M11 20A7 7 0 0 1 4 13C4 7 11 3 20 3c0 9-4 16-9 17Z"/><path d="M8 17c2-4 5-6 8-7"/>'),
 "heart": _svg('<path d="M19 5a5 5 0 0 0-7 0l-0 0-0-0a5 5 0 0 0-7 7l7 7 7-7a5 5 0 0 0 0-7Z"/>'),
 "star": _svg('<path d="M12 2 15 9l7 .6-5.3 4.6L18.5 21 12 17.2 5.5 21l1.8-6.8L2 9.6 9 9Z"/>'),
 "clock": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "pill": _svg('<rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(45 12 12)"/><path d="M9 9l6 6"/>'),
 "phone": _svg('<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>'),
 "mail": _svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
}
def icon(k): return ICONS.get(k, ICONS["check"])

# ---------------- shared chrome ----------------
def nav(prefix=""):
    return f'''<header class="site-head">
<div class="discount-bar">🔥 <b>FLASH SALE:</b> Up to 60% OFF + FREE Shipping applied automatically — ends soon</div>
<div class="wrap"><nav class="nav">
<a class="brand" href="{prefix}index.html"><span class="logo">{icon("brain")}</span> NeuroVitol</a>
<span class="spacer"></span>
<div class="nav-links">
<a href="{prefix}benefits.html">Benefits</a>
<a href="{prefix}ingredients.html">Ingredients</a>
<a href="{prefix}how-it-works.html">How It Works</a>
<a href="{prefix}reviews.html">Reviews</a>
<a href="{prefix}vs/index.html">Compare</a>
<a href="{prefix}faq.html">FAQ</a>
</div>
<a class="btn btn-cta js-cta" data-cta="VSL" href="#order" style="padding:11px 22px;font-size:.95rem">Claim 60% Off</a>
</nav></div></header>'''

def footer(prefix=""):
    pop = ", ".join([f'<a href="{prefix}vs/{s}.html">vs {c[0]}</a>' for s,c in list(COMPETITORS.items())])
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div>
<a class="brand" href="{prefix}index.html"><span class="logo">{icon("brain")}</span> NeuroVitol</a>
<p style="color:#a8adc9;max-width:320px">Daily brain-support for clearer thinking, sharper recall, and more reliable focus. A transparent five-ingredient nootropic formula trusted by 7,500+ customers.</p>
<p style="color:#a8adc9">{icon("phone")} {PHONE}<br>{icon("mail")} {EMAIL}</p>
</div>
<div><h4>Product</h4>
<a href="{prefix}benefits.html">Brain Benefits</a>
<a href="{prefix}ingredients.html">Ingredients</a>
<a href="{prefix}how-it-works.html">How It Works</a>
<a href="{prefix}reviews.html">Customer Reviews</a>
<a href="{prefix}faq.html">FAQ</a>
</div>
<div><h4>Compare</h4>
<a href="{prefix}vs/index.html">All Comparisons</a>
<a href="{prefix}vs/alpha-brain.html">vs Alpha Brain</a>
<a href="{prefix}vs/mind-lab-pro.html">vs Mind Lab Pro</a>
<a href="{prefix}vs/prevagen.html">vs Prevagen</a>
<a href="{prefix}vs/neuriva.html">vs Neuriva</a>
</div>
<div><h4>Learn</h4>
<a href="{prefix}blog/index.html">Brain Health Blog</a>
<a href="{prefix}blog/best-brain-supplements-2026.html">Best Brain Supplements 2026</a>
<a href="{prefix}blog/how-to-get-rid-of-brain-fog.html">Beat Brain Fog</a>
<a href="{prefix}about.html">About Us</a>
<a href="{prefix}contact.html">Contact</a>
</div>
</div>
<div class="foot-legal">
<p><b>† These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.</b> NeuroVitol is a dietary supplement intended to support general cognitive wellness — it is not a medication and is not a substitute for professional medical advice. Individual results vary. Consult your physician before use if you are pregnant, nursing, under 18, taking medication, or have a medical condition.</p>
<p>Popular comparisons: {pop}</p>
<p>&copy; <span class="js-year">2026</span> {BRAND}. All rights reserved. &nbsp;·&nbsp;
<a href="{prefix}legal/privacy.html">Privacy Policy</a> ·
<a href="{prefix}legal/terms.html">Terms &amp; Conditions</a> ·
<a href="{prefix}legal/disclaimer.html">Disclaimer</a></p>
</div>
</div></footer>'''

def sticky():
    return '''<div class="sticky-cta">
<div class="p"><b>NeuroVitol</b> — 60% OFF + Free Shipping · <span class="js-stock">58</span> packs left</div>
<a class="btn btn-cta js-cta" data-cta="VSL" href="#order">Claim Offer</a></div>'''

def exit_popup(prefix=""):
    return f'''<div class="modal-back" id="nv-exit"><div class="modal">
<button class="x" aria-label="Close">&times;</button>
<span class="burst">WAIT!</span>
<h3>Don't Leave Your Brain Hanging 🧠</h3>
<p>Your <b>60% OFF + FREE shipping</b> is still reserved — but only for the next few minutes. Once this timer hits zero, the discount is gone and prices jump back to full.</p>
<div class="cd-mini">Offer expires in <span class="cd-mini-v">05:00</span></div>
<p style="margin:6px 0 18px"><b>Over 7,500 customers</b> already made the switch to clearer, sharper days. Don't let brain fog win.</p>
<a class="btn btn-cta btn-block pulse js-cta" data-cta="VSL" href="#order">✅ Yes — Claim My 60% Discount</a>
<button class="btn btn-ghost btn-block js-stay" style="margin-top:10px">No thanks, I'll risk paying full price later</button>
<p class="tiny">60-day money-back guarantee · Free shipping · Secure checkout</p>
</div></div>'''

def cta_buttons(label="Claim 60% Off + Free Shipping"):
    return f'<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="#order">{label} →</a>'

def trust_strip():
    items = [("truck","Free Shipping on Every Order"),("shield","60-Day Money-Back Guarantee"),
             ("leaf","Non-Habit Forming"),("lock","Secure Checkout"),("star","4.9/5 · 6,000+ Reviews")]
    t = "".join([f'<div class="t">{icon(k)} {v}</div>' for k,v in items])
    return f'<div class="trust wrap">{t}</div>'

# ---------------- page shell ----------------
def page(path, title, desc, body, schema=None, prefix="", keywords="", canonical=None, robots="index,follow"):
    canon = canonical or (DOMAIN + "/" + path.replace("index.html","").lstrip("./"))
    if canon.endswith("/"): canon = canon
    sj = ""
    if schema:
        blocks = schema if isinstance(schema, list) else [schema]
        sj = "".join(['<script type="application/ld+json">'+json.dumps(b, ensure_ascii=False)+'</script>' for b in blocks])
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(keywords)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{OG}">
<meta property="og:site_name" content="{BRAND}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#4f46e5">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/styles.css">
{sj}
</head>
<body>
{nav(prefix)}
{body}
{footer(prefix)}
{sticky()}
{exit_popup(prefix)}
<script src="{prefix}assets/config.js"></script>
<script src="{prefix}assets/main.js"></script>
</body>
</html>'''
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(doc)

# ---------------- schema builders ----------------
def product_schema(prefix=""):
    return {
      "@context":"https://schema.org","@type":"Product","name":PRODUCT,"brand":{"@type":"Brand","name":BRAND},
      "description":"A daily nootropic dietary supplement formulated to support memory, focus, mental clarity and healthy cognitive performance with Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12.",
      "image":OG,"category":"Brain & Cognitive Support Supplement","url":DOMAIN+"/",
      "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"6000","bestRating":"5"},
      "review":[{"@type":"Review","author":{"@type":"Person","name":r[1]},"reviewRating":{"@type":"Rating","ratingValue":r[3],"bestRating":"5"},"reviewBody":r[2]} for r in REVIEWS],
      "offers":{"@type":"AggregateOffer","priceCurrency":"USD","lowPrice":"49","highPrice":"79","offerCount":"3","availability":"https://schema.org/InStock","url":DOMAIN+"/#order"}
    }
def faq_schema(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def org_schema():
    return {"@context":"https://schema.org","@type":"Organization","name":BRAND,"url":DOMAIN,"logo":OG,
            "contactPoint":{"@type":"ContactPoint","telephone":PHONE,"email":EMAIL,"contactType":"customer service"}}
def website_schema():
    return {"@context":"https://schema.org","@type":"WebSite","name":BRAND,"url":DOMAIN,
            "potentialAction":{"@type":"SearchAction","target":DOMAIN+"/vs.html?q={search_term_string}","query-input":"required name=search_term_string"}}
def article_schema(title, desc, url):
    return {"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
            "image":OG,"author":{"@type":"Organization","name":BRAND},"publisher":org_schema(),
            "datePublished":TODAY,"dateModified":TODAY,"mainEntityOfPage":url}

# ---------------- reusable HTML chunks ----------------
def pricing_block(prefix=""):
    cards=""
    for p in PRICES:
        feat="featured" if p["feat"] else ""
        tag='<span class="tag">Most Popular · Best Seller</span>' if p["feat"] else ""
        cards+=f'''<div class="price-card {feat}">{tag}
<h3>{p["name"]}</h3><div class="supply">{p["supply"]}</div>
<div class="per">${p["per"]}<small>/bottle</small></div>
<div class="was">${p["was"]} retail</div>
<div class="total">Total today: <b>${p["total"]}</b></div>
<span class="savebadge">You save {p["save"]}</span>
<ul>
<li>{icon("check")} {p["supply"]} of NeuroVitol</li>
<li>{icon("check")} FREE fast shipping</li>
<li>{icon("check")} 60-day money-back guarantee</li>
<li>{icon("check")} Non-habit forming daily formula</li>
</ul>
<a class="btn btn-cta btn-block pulse js-cta" data-cta="VSL" href="#">Add To Cart →</a>
<div class="secure">{icon("lock")} Safe &amp; secure checkout</div></div>'''
    return f'''<section id="order" class="soft"><div class="wrap center">
<span class="eyebrow">Choose Your Package &amp; Save More</span>
<h2>Lock In Your NeuroVitol Discount Today</h2>
<p class="lead narrow">NeuroVitol works best when you stay consistent. Stock up now, keep bottles on hand, and give your memory, focus, and clarity the daily support they deserve — every order ships <b>free</b>.</p>
<div class="countdown js-countdown"><div class="cd-box cd-m">10<span>MIN</span></div><div class="cd-box cd-s">00<span>SEC</span></div></div>
<p class="stock-line">🔥 Only <span class="js-stock">58</span> discounted packs remaining at this price</p>
<div class="price-grid" style="margin-top:26px">{cards}</div>
<p class="muted" style="margin-top:20px;font-size:.9rem">Prices shown reflect today's promotion and may change without notice. Free shipping applies to all U.S. orders.</p>
</div></section>'''

def guarantee_block():
    return f'''<section><div class="wrap"><div class="band">
<div class="seal"><b>60</b>DAY<br>GUARANTEE</div>
<h2>Try It Risk-Free for 60 Days</h2>
<p class="narrow" style="margin:0 auto 6px">We stand behind NeuroVitol with a full <b>60-day money-back guarantee</b>. Add it to your daily routine with confidence — if you're not satisfied for any reason, simply return it within 60 days for a refund. <b>Either you love it… or you don't pay.</b></p>
</div></div></section>'''

def faq_block(faqs, heading="Frequently Asked Questions"):
    items="".join([f'<details><summary>{q}</summary><div class="a">{a}</div></details>' for q,a in faqs])
    return f'''<section><div class="wrap"><div class="center"><span class="eyebrow">Answers</span><h2>{heading}</h2></div>
<div class="faq">{items}</div></div></section>'''

def keyword_footer(prefix=""):
    terms = ["brain supplement","nootropic for focus","memory supplement","brain fog supplement",
             "best brain supplement 2026","supplement for mental clarity","focus pills","cognitive support supplement",
             "Bacopa Monnieri","Lion's Mane","Ginkgo Biloba","Phosphatidylserine","brain health supplement",
             "supplement for studying","natural focus supplement","NeuroVitol reviews","NeuroVitol brain support"]
    tags="".join(['<a href="%svs.html?q=%s">%s</a>' % (prefix, html.escape(t.replace(" ","+")), t) for t in terms])
    return f'''<section class="soft2"><div class="wrap">
<h3 style="text-align:center">Popular Brain-Health Searches</h3>
<div class="tag-list" style="justify-content:center;max-width:880px;margin:0 auto">{tags}</div>
<p class="kw-footer" style="text-align:center;max-width:900px;margin:18px auto 0">NeuroVitol Advanced Brain Support is a daily nootropic supplement for memory, focus, mental clarity, brain fog, concentration, recall and healthy cognitive function — formulated with Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12. Looking for the best brain supplement of 2026, a nootropic for studying, or a non-jittery focus supplement? Compare NeuroVitol to Alpha Brain, Mind Lab Pro, Prevagen, Neuriva, Qualia Mind, NeuroZoom and more.</p>
</div></section>'''

# ================= PAGE BUILDERS =================
def build_index():
    ticks="".join([f'<li>{icon("check")} {t}</li>' for t in
        ["Supports memory, recall, and mental sharpness","Helps promote focus, clarity, and follow-through",
         "Built for simple, steady daily cognitive support","Non-habit forming · no harsh jitters or crash"]])
    chips="".join([f'<span class="chip">{icon(k)} {v}</span>' for k,v in
        [("star","4.9/5 · 6,000+ reviews"),("heart","7,500+ happy customers"),("truck","Free shipping"),("shield","60-day guarantee")]])
    ben="".join([f'''<div class="card"><div class="ic">{icon(k)}</div><h3>{t}</h3><p>{d}</p></div>''' for k,t,d in BENEFITS6])
    ings="".join([f'''<div class="ingredient"><div class="pic">{ab}</div><div><h3>{n}</h3><p>{d}</p></div></div>''' for n,ab,d in INGREDIENTS])
    revs="".join([f'''<div class="review"><div class="stars">{"★"*int(r[3])}{"☆"*(5-int(r[3]))}</div><h4>{r[0]}</h4><p>{r[2]}</p><div class="who"><span class="av">{r[1][0]}</span> {r[1]} · Verified Customer</div></div>''' for r in REVIEWS])
    bars="".join([f'''<div class="mbar"><div class="top"><span>{n}</span><span>{int(v)/20:.1f}/5</span></div><div class="track"><div class="fill" style="width:{v}%"></div></div></div>''' for n,v in METRICS])
    steps="".join([f'''<div class="card soft"><div class="ic">{icon(k)}</div><h3>{i}. {t}</h3><p>{d}</p></div>''' for i,(k,t,d) in enumerate([
        ("leaf","Nourish Brain Function","Supports important pathways involved in memory, attention, and everyday mental performance."),
        ("target","Support Focus &amp; Clarity","Helps support clearer thinking and steadier concentration when busy days try to pull you off track."),
        ("shield","Promote Long-Term Wellness","Supports healthy cognitive performance as part of a broader routine for brain health and follow-through.")],1)])
    body=f'''
<section class="hero"><div class="wrap"><div class="hero-grid">
<div>
<span class="eyebrow">Advanced Brain Support · Now Available Online</span>
<h1>Think Clearer. Remember More. Stay Focused — Every Single Day.</h1>
<p class="lead">{PRODUCT} is a daily nootropic supplement built to support memory, focus, mental clarity, and healthy cognitive performance — without harsh stimulants, jitters, or a crash.</p>
<ul class="benefit-ticks">{ticks}</ul>
{cta_buttons()}
<div class="hero-badges">{chips}</div>
</div>
<div class="hero-card">
<span class="save-flag">60% OFF</span>
<h3 style="margin-top:6px">Claim Today's NeuroVitol Discount</h3>
<div class="rating-row"><span class="stars">★★★★★</span> <b>4.9</b> <span class="muted">· 6,000+ reviews</span></div>
<p class="muted" style="margin:0 0 8px">Sale is <b style="color:#e11d48">LIVE</b> — your discount is reserved for:</p>
<div class="countdown js-countdown"><div class="cd-box cd-m">10<span>MIN</span></div><div class="cd-box cd-s">00<span>SEC</span></div></div>
<p class="stock-line">Stock: <span class="js-stock">58</span> discounted packs remaining</p>
<a class="btn btn-cta btn-block btn-lg pulse js-cta" data-cta="VSL" href="#order">Claim 60% Off Now →</a>
<p class="secure" style="margin-top:14px">{icon("lock")} Secure checkout · {icon("truck")} Free shipping · {icon("shield")} 60-day guarantee</p>
</div>
</div></div></section>
{trust_strip()}

<section><div class="wrap narrow center">
<span class="eyebrow">Sound Familiar?</span>
<h2>Feeling Mentally Foggy When You Need To Be Sharp?</h2>
<p class="lead">You push through the day, but your focus still doesn't feel like <i>you</i>. Stress, age, poor sleep, and nonstop demands can leave your memory slower, your focus scattered, and your thoughts less clear than they used to be — rereading the same line, forgetting small details, losing momentum by midday.</p>
<p>The good news: consistent daily cognitive support can help you feel more steady, focused, and mentally clear again. That's exactly what NeuroVitol is built for — supporting memory, attention, and sharper day-to-day thinking from the inside out.</p>
</div></section>

<section class="soft"><div class="wrap"><div class="center"><span class="eyebrow">The 6 Ways NeuroVitol Supports Your Mind</span>
<h2>Daily Support For A Clearer, Sharper Mind</h2>
<p class="lead narrow">NeuroVitol is designed to support the areas that matter most when your day demands a clear, reliable mind.</p></div>
<div class="grid g3" style="margin-top:30px">{ben}</div>
<div class="center" style="margin-top:34px">{cta_buttons("Support My Brain Today")}</div>
</div></section>

<section><div class="wrap"><div class="center"><span class="eyebrow">The Science · Honest, Transparent Formulation</span>
<h2>5 Brain-Support Ingredients You Can Actually Pronounce</h2>
<p class="lead narrow">Our transparent formula means you know exactly what you're taking — each ingredient selected for quality, relevance, and daily cognitive-support potential.</p></div>
<div class="grid g2" style="margin-top:30px">{ings}</div>
<div class="center" style="margin-top:24px"><a class="btn btn-ghost" href="ingredients.html">See the full ingredient science →</a></div>
</div></section>

<section class="soft"><div class="wrap"><div class="center"><span class="eyebrow">How It Works</span>
<h2>Three Steps To Steadier Daily Performance</h2></div>
<div class="grid g3" style="margin-top:30px">{steps}</div>
</div></section>

<section><div class="wrap"><div class="center"><span class="eyebrow">Real Customers · Real Daily Support</span>
<h2>Rated 4.9/5 by 6,000+ NeuroVitol Users</h2></div>
<div class="grid g2" style="margin:30px 0">{revs}</div>
<div class="metric-bars">{bars}</div>
</div></section>

{pricing_block()}
{guarantee_block()}
{faq_block(FAQS[:7])}
{keyword_footer()}
'''
    schema=[product_schema(), org_schema(), website_schema(), faq_schema(FAQS[:7])]
    page("index.html","NeuroVitol® Advanced Brain Support | Memory, Focus & Clarity Supplement",
         "NeuroVitol is a daily brain-support supplement for memory, focus & mental clarity with Bacopa, Lion's Mane, Ginkgo, Phosphatidylserine & B12. 60% off + free shipping & a 60-day guarantee.",
         body, schema=schema,
         keywords="NeuroVitol, brain supplement, nootropic, memory supplement, focus supplement, mental clarity, brain fog, cognitive support, Bacopa Monnieri, Lion's Mane, Ginkgo Biloba")

def build_benefits():
    ben="".join([f'''<div class="card"><div class="ic">{icon(k)}</div><h3>{t}</h3><p>{d}</p></div>''' for k,t,d in BENEFITS6])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › Benefits</div>
<span class="eyebrow">Brain Benefits</span>
<h1>The Cognitive Benefits of NeuroVitol</h1>
<p class="lead">From sharper memory to steadier focus and less brain fog — here's how NeuroVitol supports clearer thinking, reasoning, brainstorming, and reliable day-to-day mental performance.</p>
{cta_buttons()}</div></section>
<section><div class="wrap"><div class="grid g3">{ben}</div></div></section>
<section class="soft"><div class="wrap narrow prose">
<h2>Built for the way your brain actually works</h2>
<p>NeuroVitol Advanced Brain Support targets the everyday cognitive jobs you rely on most: holding details in memory, staying focused on a task, thinking clearly under pressure, and keeping consistent mental energy from morning to night. Instead of a harsh stimulant that spikes and crashes, NeuroVitol takes a steady, daily-support approach so your mind has what it needs to perform — reliably.</p>
<h3>Memory &amp; recall</h3><p>Bacopa Monnieri and Phosphatidylserine are included specifically for their traditional and structural roles in supporting memory formation and recall — helping names, numbers, and next steps feel easier to keep track of.</p>
<h3>Focus, concentration &amp; follow-through</h3><p>Lion's Mane and Ginkgo Biloba are favorites in the 2026 nootropic world for supporting attention, clarity, and healthy brain performance — so you can stay engaged with reading, planning, conversations, and demanding work.</p>
<h3>Less brain fog, more clarity</h3><p>When stress, fatigue, and overload make your mind feel slow or scattered, NeuroVitol is built to support clearer, more organized thinking — the kind that makes decisions and brainstorming feel easier.</p>
<h3>Reasoning &amp; brainstorming</h3><p>Clearer working memory and steadier focus are the foundation of good reasoning and creative brainstorming. By supporting those underlying systems daily, NeuroVitol helps you bring your full mental range to the table.</p>
</div></section>
{guarantee_block()}
{faq_block([f for f in FAQS if f[0] in ("What is NeuroVitol?","How soon will I notice results?","Does NeuroVitol contain stimulants or cause jitters?")])}
{keyword_footer()}'''
    page("benefits.html","NeuroVitol Benefits | Memory, Focus, Clarity & Less Brain Fog",
         "Discover the cognitive benefits of NeuroVitol: supports memory, focus, mental clarity, reasoning and brainstorming while helping fight brain fog — without harsh stimulants.",
         body, schema=[breadcrumb([("Home",DOMAIN+"/"),("Benefits",DOMAIN+"/benefits.html")]), product_schema()],
         keywords="NeuroVitol benefits, brain supplement benefits, memory support, focus support, brain fog, mental clarity, cognitive benefits")

def build_ingredients():
    ings="".join([f'''<div class="card"><div class="ic" style="background:var(--grad-teal);color:#fff">{icon("pill")}</div><h3>{n}</h3><p>{d}</p></div>''' for n,ab,d in INGREDIENTS])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › Ingredients</div>
<span class="eyebrow">Honest Ingredients · Transparent Formula</span>
<h1>What's Inside NeuroVitol</h1>
<p class="lead">No mystery “proprietary fog.” NeuroVitol uses five well-known brain-support ingredients, each chosen for quality, relevance, and daily cognitive-support potential.</p>
{cta_buttons()}</div></section>
<section><div class="wrap"><div class="grid g2">{ings}</div></div></section>
<section class="soft"><div class="wrap narrow prose">
<h2>Why these five ingredients?</h2>
<p>The 2026 brain-supplement market is crowded with formulas that list 20, 30, even 35 ingredients at doses too small to matter. NeuroVitol takes the opposite approach: a focused, transparent blend of five of the most recognized names in cognitive support, so every capsule does meaningful work and you always know exactly what you're putting in your body.</p>
<div class="note teal">{icon("leaf")} <b>Non-habit forming &amp; non-jittery.</b> NeuroVitol is built for steady daily support — not the spike-and-crash of stimulant-heavy “energy” products.</div>
<h3>Bacopa Monnieri</h3><p>An adaptogenic herb used in Ayurvedic tradition for centuries to support memory, learning, and everyday cognitive performance.</p>
<h3>Lion's Mane</h3><p>A functional mushroom that has become one of the most popular nootropic ingredients of 2026 for supporting focus, clarity, and healthy neurological wellness.</p>
<h3>Ginkgo Biloba</h3><p>One of the most widely used botanicals in the world for supporting healthy circulation and overall brain performance.</p>
<h3>Phosphatidylserine</h3><p>A phospholipid that supports healthy brain-cell membrane structure and the cognitive activity behind daily focus and memory.</p>
<h3>Vitamin B12</h3><p>An essential vitamin that supports normal neurological function and healthy energy metabolism — foundational for steady mental stamina.</p>
<div class="disclaimer">† These statements have not been evaluated by the Food and Drug Administration. NeuroVitol is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease. Consult your healthcare provider before use if you are pregnant, nursing, under 18, taking medication, or have a medical condition.</div>
</div></section>
{guarantee_block()}
{faq_block([f for f in FAQS if f[0] in ("What are the ingredients?","Is NeuroVitol safe for daily use?","Can I take it with other supplements or medications?")])}
{keyword_footer()}'''
    page("ingredients.html","NeuroVitol Ingredients | Bacopa, Lion's Mane, Ginkgo, PS & B12",
         "See exactly what's inside NeuroVitol: Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12 — a transparent five-ingredient brain-support formula.",
         body, schema=[breadcrumb([("Home",DOMAIN+"/"),("Ingredients",DOMAIN+"/ingredients.html")])],
         keywords="NeuroVitol ingredients, Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine, Vitamin B12, nootropic ingredients")

def build_how():
    steps="".join([f'''<div class="card"><div class="ic">{icon(k)}</div><h3>Step {i}: {t}</h3><p>{d}</p></div>''' for i,(k,t,d) in enumerate([
        ("leaf","Nourish brain function","NeuroVitol supplies daily nutritional support for the pathways involved in memory, attention, and mental performance."),
        ("target","Support focus &amp; clarity","With consistent use, the formula helps support clearer thinking and steadier concentration through busy, demanding days."),
        ("shield","Promote long-term wellness","NeuroVitol is built for the long game — supporting healthy cognitive performance as part of a daily brain-health routine.")],1)])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › How It Works</div>
<span class="eyebrow">How It Works</span>
<h1>The Science Behind Daily Cognitive Support</h1>
<p class="lead">NeuroVitol is designed to support the systems involved in mental clarity, focus, and recall — so you build steadier support instead of chasing short bursts of temporary stimulation.</p>
{cta_buttons()}</div></section>
<section><div class="wrap"><div class="grid g3">{steps}</div></div></section>
<section class="soft"><div class="wrap narrow prose">
<h2>Consistency beats stimulation</h2>
<p>Many brain products lean on caffeine or harsh stimulants for a quick jolt — followed by an afternoon crash. NeuroVitol is the opposite: a non-jittery, non-habit-forming daily formula. You take it once a day, as directed on the label, and let the ingredients support your brain consistently over time.</p>
<h2>A simple daily routine</h2>
<p>Take NeuroVitol daily as directed on the product label. Some users notice changes within a few weeks, while more noticeable benefits may build with consistent daily use over time. That's why the 3- and 6-bottle packages are the most popular — they keep you consistent without running out mid-routine.</p>
<div class="note indigo">{icon("clock")} <b>Best results come from consistency.</b> Brain support is a daily habit, not a one-time fix — keep bottles on hand so you never break the routine.</div>
</div></section>
{pricing_block()}
{guarantee_block()}
{keyword_footer()}'''
    page("how-it-works.html","How NeuroVitol Works | Daily Cognitive Support Explained",
         "How NeuroVitol works: a non-jittery daily nootropic that nourishes brain function, supports focus and clarity, and promotes long-term cognitive wellness with consistent use.",
         body, schema=[breadcrumb([("Home",DOMAIN+"/"),("How It Works",DOMAIN+"/how-it-works.html")])],
         keywords="how NeuroVitol works, daily cognitive support, nootropic mechanism, brain supplement how it works")

def build_reviews():
    revs="".join([f'''<div class="review"><div class="stars">{"★"*int(r[3])}{"☆"*(5-int(r[3]))}</div><h4>{r[0]}</h4><p>{r[2]}</p><div class="who"><span class="av">{r[1][0]}</span> {r[1]} · Verified Customer</div></div>''' for r in REVIEWS])
    bars="".join([f'''<div class="mbar"><div class="top"><span>{n}</span><span>{int(v)/20:.1f}/5</span></div><div class="track"><div class="fill" style="width:{v}%"></div></div></div>''' for n,v in METRICS])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › Reviews</div>
<span class="eyebrow">Real Customers · Real Daily Support</span>
<h1>NeuroVitol Reviews</h1>
<div class="rating-row" style="justify-content:center"><span class="stars" style="font-size:1.5rem">★★★★★</span> <b style="font-size:1.4rem">4.9</b> <span class="muted">based on 6,000+ reviews</span></div>
<p class="lead">Trusted by 7,500+ happy customers who wanted clearer thinking, sharper recall, and more reliable focus.</p>
{cta_buttons()}</div></section>
<section><div class="wrap"><div class="metric-bars" style="margin-bottom:36px">{bars}</div><div class="grid g2">{revs}</div></div></section>
<section class="soft"><div class="wrap narrow center">
<div class="note">Reviews reflect individual experiences and are not a guarantee of results. Individual results vary. NeuroVitol is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease.</div>
</div></section>
{guarantee_block()}
{keyword_footer()}'''
    page("reviews.html","NeuroVitol Reviews | 4.9/5 from 6,000+ Customers",
         "Read NeuroVitol reviews: rated 4.9/5 by 6,000+ customers for focus, mental clarity and memory support. See verified customer experiences and ratings.",
         body, schema=[breadcrumb([("Home",DOMAIN+"/"),("Reviews",DOMAIN+"/reviews.html")]), product_schema()],
         keywords="NeuroVitol reviews, NeuroVitol customer reviews, does NeuroVitol work, brain supplement reviews")

def build_faq():
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › FAQ</div>
<span class="eyebrow">Answers</span><h1>NeuroVitol — Frequently Asked Questions</h1>
<p class="lead">Everything you need to know about NeuroVitol Advanced Brain Support — ingredients, safety, results, pricing, and the 60-day guarantee.</p>
{cta_buttons()}</div></section>
{faq_block(FAQS)}
{guarantee_block()}
{keyword_footer()}'''
    page("faq.html","NeuroVitol FAQ | Ingredients, Safety, Results & Pricing",
         "NeuroVitol FAQ: what it is, how to use it, ingredients, safety, how soon you'll see results, pricing and the 60-day money-back guarantee.",
         body, schema=[faq_schema(FAQS), breadcrumb([("Home",DOMAIN+"/"),("FAQ",DOMAIN+"/faq.html")])],
         keywords="NeuroVitol FAQ, NeuroVitol questions, is NeuroVitol safe, NeuroVitol side effects, NeuroVitol guarantee")

def build_about():
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › About</div>
<span class="eyebrow">About</span><h1>About NeuroVitol</h1>
<p class="lead">NeuroVitol was created on a simple belief: sharper days are built with consistent, honest daily support — not hype, harsh stimulants, or 35-ingredient mystery blends.</p></div></section>
<section><div class="wrap narrow prose">
<p>NeuroVitol Advanced Brain Support is formulated to help adults feel more mentally prepared for work, family, and everyday demands. We combine five of the most recognized brain-support ingredients — Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine, and Vitamin B12 — into a transparent daily formula you can actually understand.</p>
<p>Today, more than 7,500 customers trust NeuroVitol as part of their daily wellness routine, and the formula holds a 4.9/5 average rating across 6,000+ reviews. Every order is backed by free shipping and a 60-day money-back guarantee, because we'd rather earn your trust than chase a quick sale.</p>
<h2>Questions? We're here.</h2>
<p>{icon("phone")} {PHONE}<br>{icon("mail")} <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>
{guarantee_block()}{keyword_footer()}'''
    page("about.html","About NeuroVitol | Honest, Transparent Brain Support",
         "About NeuroVitol — a transparent five-ingredient daily brain-support supplement trusted by 7,500+ customers, backed by a 60-day money-back guarantee.",
         body, schema=[org_schema(), breadcrumb([("Home",DOMAIN+"/"),("About",DOMAIN+"/about.html")])],
         keywords="about NeuroVitol, NeuroVitol company, NeuroVitol brand")

def build_contact():
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › Contact</div>
<span class="eyebrow">Contact</span><h1>Contact NeuroVitol Support</h1>
<p class="lead">Questions about your order, the ingredients, or the 60-day guarantee? Our team is happy to help.</p></div></section>
<section><div class="wrap narrow">
<div class="grid g2">
<div class="card"><div class="ic">{icon("phone")}</div><h3>Call Us</h3><p><a href="tel:+18882031709">{PHONE}</a></p></div>
<div class="card"><div class="ic">{icon("mail")}</div><h3>Email Us</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div>
<div class="note teal" style="margin-top:24px">{icon("shield")} <b>60-Day Money-Back Guarantee.</b> Not satisfied? Contact us within 60 days of purchase for a refund.</div>
</div></section>{keyword_footer()}'''
    page("contact.html","Contact NeuroVitol | Customer Support & Returns",
         f"Contact NeuroVitol customer support at {PHONE} or {EMAIL}. Questions about orders, ingredients, or the 60-day money-back guarantee — we're here to help.",
         body, schema=[org_schema(), breadcrumb([("Home",DOMAIN+"/"),("Contact",DOMAIN+"/contact.html")])],
         keywords="contact NeuroVitol, NeuroVitol support, NeuroVitol customer service, NeuroVitol returns")

def vs_table(name, their_price, prefix="../"):
    rows=[("Price (best value)","From $49/bottle","yes",their_price,"no"),
          ("Free shipping","Yes","yes","Varies","no"),
          ("Money-back guarantee","60 days","yes","Varies","no"),
          ("Transparent formula","5 named ingredients","yes","Varies","no"),
          ("Bacopa + Lion's Mane + Ginkgo","Yes","yes","Varies","no"),
          ("Non-habit forming / non-jittery","Yes","yes","Varies","no"),
          ("Buy online, no prescription","Yes","yes","Yes","yes")]
    tr=""
    for label,us,usok,them,themok in rows:
        uc='yes' if usok=='yes' else 'no'
        tc='yes' if themok=='yes' else 'no'
        usmark=f'<span class="{uc}">✔</span> ' if us in ("Yes",) else ''
        themark='✔' if them=='Yes' else ('✘' if them=='—' else them)
        tcls='yes' if them=='Yes' else ('no' if them in ('—','No') else '')
        tr+=f'<tr><td class="brandcol">{label}</td><td class="us">{us}</td><td class="{tcls}">{themark}</td></tr>'
    return f'''<table class="cmp"><tr><th>Feature</th><th>NeuroVitol</th><th>{name}</th></tr>{tr}</table>'''

def build_vs(slug, data):
    name, cat, price, angle, edge = data
    others=[f'<a href="{s}.html">vs {c[0]}</a>' for s,c in COMPETITORS.items() if s!=slug]
    related="".join([f'<a href="{s}.html">NeuroVitol vs {c[0]}</a>' for s,c in list(COMPETITORS.items())[:8] if s!=slug])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Compare</a> › vs {name}</div>
<span class="eyebrow">Brain Supplement Comparison · 2026</span>
<h1>NeuroVitol vs {name}: Which Brain Supplement Is Better?</h1>
<p class="lead">Comparing NeuroVitol Advanced Brain Support with {name} — {cat}. Here's how the two stack up on price, ingredients, guarantee, and everyday value in 2026.</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="#order">Try NeuroVitol — 60% Off →</a>
</div></section>
<section><div class="wrap narrow">
{vs_table(name, price)}
<div class="note indigo" style="margin-top:22px">{icon("sparkle")} <b>Bottom line:</b> {name} is {angle}. {edge}</div>
<div class="prose" style="margin-top:24px">
<h2>Why people switch from {name} to NeuroVitol</h2>
<p>Both NeuroVitol and {name} aim to support memory, focus, and mental clarity. The difference is approach. {name} is {angle}. NeuroVitol keeps things simple and transparent: five well-known brain-support ingredients — Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12 — in a non-jittery daily formula, from just $49 per bottle with free shipping and a 60-day money-back guarantee.</p>
<h3>NeuroVitol may be the better fit if you want:</h3>
<ul>
<li>A <b>transparent, easy-to-understand formula</b> instead of a long mystery list.</li>
<li><b>Lower per-bottle pricing</b> (down to $49) with free shipping on every order.</li>
<li>A genuine <b>60-day money-back guarantee</b> so you can try it risk-free.</li>
<li>A <b>non-habit-forming, non-jittery</b> daily approach — no crash.</li>
</ul>
<p class="muted">Comparison reflects publicly available information and typical positioning as of 2026; always check each brand's current label, pricing, and terms. NeuroVitol and {name} are separate products; this page is an independent comparison by NeuroVitol.</p>
</div>
</div></section>
<section class="soft" id="order"><div class="wrap narrow center">
<h2>Ready to try the simpler brain-support choice?</h2>
<p class="lead">Lock in up to 60% off NeuroVitol today — free shipping and a 60-day money-back guarantee included.</p>
<div class="countdown js-countdown"><div class="cd-box cd-m">10<span>MIN</span></div><div class="cd-box cd-s">00<span>SEC</span></div></div>
<p class="stock-line">Only <span class="js-stock">58</span> discounted packs remaining</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="#">Claim My NeuroVitol Discount →</a>
</div></section>
<section><div class="wrap"><h3 style="text-align:center">More NeuroVitol comparisons</h3>
<div class="tag-list" style="justify-content:center">{related}</div></div></section>'''
    schema=[breadcrumb([("Home",DOMAIN+"/"),("Compare",DOMAIN+"/vs/"),(f"vs {name}",DOMAIN+f"/vs/{slug}.html")]),
            {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"Is NeuroVitol better than {name}?","acceptedAnswer":{"@type":"Answer","text":f"NeuroVitol offers a transparent five-ingredient daily brain-support formula from $49/bottle with free shipping and a 60-day money-back guarantee. {name} is {angle}. {edge} Many users prefer NeuroVitol for its simplicity, price, and guarantee — though the best choice depends on your goals."}}]}]
    page(f"vs/{slug}.html", f"NeuroVitol vs {name} (2026): Which Brain Supplement Is Better?",
         f"NeuroVitol vs {name} compared: price, ingredients, guarantee and value. See why NeuroVitol may be the better daily brain-support supplement in 2026.",
         body, schema=schema, prefix="../",
         keywords=f"NeuroVitol vs {name}, {name} alternative, {name} vs NeuroVitol, best brain supplement, {name} review, NeuroVitol better than {name}")

def build_vs_index():
    cards="".join([f'''<a class="card" href="{s}.html" style="text-decoration:none"><div class="ic">{icon("target")}</div><h3>NeuroVitol vs {c[0]}</h3><p>Compare price, ingredients, guarantee and value vs {c[1]}.</p></a>''' for s,c in COMPETITORS.items()])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="../index.html">Home</a> › Compare</div>
<span class="eyebrow">2026 Brain Supplement Comparisons</span>
<h1>NeuroVitol vs The Competition</h1>
<p class="lead">See how NeuroVitol Advanced Brain Support compares to the most-searched brain supplements and nootropics of 2026 — on price, ingredients, guarantee, and everyday value.</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="../index.html#order">Try NeuroVitol — 60% Off →</a></div></section>
<section><div class="wrap"><div class="grid g3">{cards}</div>
<div class="note indigo" style="margin-top:26px">Searching for a specific brand? Try our <a href="../vs.html">instant comparison tool</a> — type any brain supplement name and see how NeuroVitol stacks up.</div>
</div></section>{keyword_footer("../")}'''
    page("vs/index.html","Compare NeuroVitol | vs Alpha Brain, Mind Lab Pro, Prevagen & More",
         "Compare NeuroVitol to the top brain supplements of 2026 — Alpha Brain, Mind Lab Pro, Prevagen, Neuriva, Qualia Mind, NeuroZoom and more. Price, ingredients & value.",
         body, prefix="../",
         schema=[breadcrumb([("Home",DOMAIN+"/"),("Compare",DOMAIN+"/vs/")])],
         keywords="NeuroVitol comparison, best brain supplement 2026, Alpha Brain alternative, Mind Lab Pro alternative, Prevagen alternative")

def build_vs_dynamic():
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="index.html">Home</a> › Compare</div>
<span class="eyebrow">Instant Brain Supplement Comparison</span>
<h1>NeuroVitol vs <span class="js-brand">Other Brain Supplements</span></h1>
<p class="lead">However you got here, the question is the same: which daily brain-support supplement is the smarter choice? Here's the honest case for NeuroVitol — transparent ingredients, fair price, and a 60-day guarantee.</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="#order">Try NeuroVitol — 60% Off →</a></div></section>
<section id="nv-dynamic-brand" style="display:none"><div class="wrap narrow">
<div class="note indigo">{icon("sparkle")} <b>NeuroVitol vs <span class="js-brand">that brand</span>:</b> NeuroVitol may be the better everyday choice — a transparent five-ingredient formula (Bacopa, Lion's Mane, Ginkgo, Phosphatidylserine, B12) from $49/bottle, with free shipping and a 60-day money-back guarantee.</div>
{vs_table('<span class="js-brand">Other Brand</span>', "Varies", prefix="")}
</div></section>
<section class="soft"><div class="wrap narrow prose">
<h2>Why NeuroVitol is worth a look vs <span class="js-brand">any brain supplement</span></h2>
<p>The brain-supplement aisle is crowded in 2026 — from drugstore names to $139 premium stacks and VSL-driven “miracle” pills. NeuroVitol keeps it simple: five well-known brain-support ingredients in a transparent daily formula, a non-jittery approach, and a real 60-day money-back guarantee. From just $49 per bottle with free shipping, it's an easy, low-risk way to support memory, focus, and mental clarity every day.</p>
<ul>
<li>{icon("check")} Transparent five-ingredient formula — no mystery blend</li>
<li>{icon("check")} From $49/bottle with free shipping on every order</li>
<li>{icon("check")} 60-day money-back guarantee — try it risk-free</li>
<li>{icon("check")} Non-habit forming, non-jittery daily support</li>
</ul>
<p>Browse our full set of <a href="vs/index.html">head-to-head comparisons</a> to see NeuroVitol next to Alpha Brain, Mind Lab Pro, Prevagen, Neuriva, Qualia Mind, NeuroZoom and more.</p>
</div></section>
<section id="order"><div class="wrap narrow center">
<h2>See the difference for yourself</h2>
<p class="lead">Lock in up to 60% off NeuroVitol today — free shipping + 60-day guarantee.</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="index.html#order">Claim My Discount →</a></div></section>
{keyword_footer()}'''
    page("vs.html","NeuroVitol vs Other Brain Supplements | Instant Comparison",
         "Compare NeuroVitol to any brain supplement. Transparent ingredients, $49/bottle pricing, free shipping and a 60-day guarantee — see why NeuroVitol may be the better choice.",
         body, robots="index,follow",
         schema=[breadcrumb([("Home",DOMAIN+"/"),("Compare",DOMAIN+"/vs.html")])],
         keywords="NeuroVitol vs, brain supplement comparison, best brain supplement, nootropic comparison, NeuroVitol alternative")

def build_blog_index():
    cards="".join([f'''<a class="card" href="{s}.html" style="text-decoration:none"><div class="ic">{icon("brain")}</div><h3>{t}</h3><p>{d}</p></a>''' for s,t,d in BLOG])
    body=f'''<section class="hero"><div class="wrap narrow center">
<div class="crumbs"><a href="../index.html">Home</a> › Blog</div>
<span class="eyebrow">Brain Health Blog</span><h1>NeuroVitol Brain Health Library</h1>
<p class="lead">Practical, no-hype guides on memory, focus, brain fog, and the nootropic ingredients that support clearer daily thinking in 2026.</p></div></section>
<section><div class="wrap"><div class="grid g2">{cards}</div></div></section>{keyword_footer("../")}'''
    page("blog/index.html","Brain Health Blog | NeuroVitol Guides on Focus, Memory & Nootropics",
         "The NeuroVitol brain-health blog: guides to the best brain supplements of 2026, beating brain fog, nootropics for focus and memory, and brain-support ingredients.",
         body, prefix="../", schema=[breadcrumb([("Home",DOMAIN+"/"),("Blog",DOMAIN+"/blog/")])],
         keywords="brain health blog, nootropics, brain supplements, brain fog, focus, memory")

def build_blog_posts():
    bodies={
    "best-brain-supplements-2026": f'''
<p class="lead">If you searched “best brain supplement 2026,” you've seen the chaos: 35-ingredient mystery pills, $139 premium stacks, and VSL “miracle” claims. This guide cuts through it — what actually matters, and how NeuroVitol fits.</p>
<h2>What to look for in a brain supplement</h2>
<ul>
<li><b>Transparent ingredients</b> at meaningful amounts — not a 30-item “proprietary blend.”</li>
<li><b>Recognized brain-support ingredients</b> like Bacopa Monnieri, Lion's Mane, Ginkgo Biloba and Phosphatidylserine.</li>
<li><b>A non-jittery, non-habit-forming</b> daily approach — no spike-and-crash stimulants.</li>
<li><b>A real money-back guarantee</b> so you can try it risk-free.</li>
</ul>
<h2>The most-searched brain supplements of 2026</h2>
<p>Names you'll see ranking and advertising this year include Alpha Brain, Mind Lab Pro, Qualia Mind, Prevagen, Neuriva, NeuroZoom, NooCube, Focus Factor and NeuroVitol. We compare them head-to-head on our <a href="../vs/index.html">comparison hub</a>.</p>
<h2>Where NeuroVitol fits</h2>
<p>NeuroVitol Advanced Brain Support takes the simple, transparent route: five well-known brain-support ingredients, a non-jittery daily formula, from $49/bottle with free shipping and a 60-day guarantee. For most people who just want steady daily support for memory, focus and clarity, it's an easy, low-risk place to start.</p>
<div class="note indigo">{icon("sparkle")} Compare NeuroVitol to <a href="../vs/alpha-brain.html">Alpha Brain</a>, <a href="../vs/mind-lab-pro.html">Mind Lab Pro</a>, <a href="../vs/prevagen.html">Prevagen</a> and more.</div>''',
    "how-to-get-rid-of-brain-fog": f'''
<p class="lead">Brain fog — that slow, scattered, forgetful feeling — usually isn't one problem. It's the sum of sleep, stress, hydration, movement, and nutrition. Here are 9 daily habits that help.</p>
<h2>9 daily habits to clear brain fog</h2>
<ol>
<li><b>Protect your sleep</b> — 7–9 hours; the brain consolidates memory overnight.</li>
<li><b>Hydrate first thing</b> — even mild dehydration scatters focus.</li>
<li><b>Move daily</b> — a brisk walk boosts blood flow to the brain.</li>
<li><b>Eat for steady energy</b> — protein + healthy fats over sugar spikes.</li>
<li><b>Single-task</b> — context-switching is a fog machine.</li>
<li><b>Sunlight early</b> — sets your circadian rhythm for sharper days.</li>
<li><b>Manage stress</b> — a few minutes of breathing resets attention.</li>
<li><b>Limit the afternoon caffeine crash</b> — favor steady support over jolts.</li>
<li><b>Support your brain nutritionally</b> — ingredients like Bacopa, Lion's Mane and Ginkgo are popular for daily clarity.</li>
</ol>
<h2>The supplement angle</h2>
<p>NeuroVitol is built specifically for this: a non-jittery daily formula to help support clearer thinking when stress, fatigue and overload make your mind feel slow. Pair it with the habits above for the best shot at foggy-free days.</p>
<div class="note teal">{icon("leaf")} See the <a href="../ingredients.html">five NeuroVitol ingredients</a> for fighting brain fog.</div>''',
    "best-nootropics-for-focus-and-memory": f'''
<p class="lead">“Nootropic” just means a compound used to support cognition. For everyday focus and memory, a handful of well-known ingredients do most of the heavy lifting.</p>
<h2>Ingredients worth knowing</h2>
<ul>
<li><b>Bacopa Monnieri</b> — traditionally used to support memory and learning.</li>
<li><b>Lion's Mane</b> — popular for focus, clarity and neurological wellness.</li>
<li><b>Ginkgo Biloba</b> — supports healthy circulation and brain performance.</li>
<li><b>Phosphatidylserine</b> — supports brain-cell structure behind focus and memory.</li>
<li><b>Vitamin B12</b> — supports normal neurological function and energy.</li>
</ul>
<h2>Building a simple daily stack</h2>
<p>You can buy each of these separately — or get all five in one transparent daily formula. NeuroVitol combines Bacopa, Lion's Mane, Ginkgo, Phosphatidylserine and B12 so you don't have to assemble (and crash through) a complicated stack.</p>
<div class="note indigo">{icon("sparkle")} See how NeuroVitol compares to <a href="../vs/qualia-mind.html">Qualia Mind</a> and <a href="../vs/noocube.html">NooCube</a>.</div>''',
    "bacopa-lions-mane-ginkgo-guide": f'''
<p class="lead">NeuroVitol uses five brain-support ingredients. Here's a plain-English guide to what each one does and why it's in the formula.</p>
<h2>The five ingredients</h2>
<h3>Bacopa Monnieri</h3><p>An Ayurvedic herb traditionally used to support memory, learning and everyday cognitive performance.</p>
<h3>Lion's Mane</h3><p>A functional mushroom popular in 2026 for supporting focus, clarity and healthy neurological wellness.</p>
<h3>Ginkgo Biloba</h3><p>One of the world's most-used botanicals for supporting healthy circulation and brain performance.</p>
<h3>Phosphatidylserine</h3><p>A phospholipid supporting healthy brain-cell membranes and the activity behind daily focus and memory.</p>
<h3>Vitamin B12</h3><p>An essential vitamin supporting normal neurological function and healthy energy metabolism.</p>
<div class="note teal">{icon("leaf")} Get all five in one daily formula — <a href="../index.html#order">try NeuroVitol with 60% off</a>.</div>'''}
    for s,t,d in BLOG:
        prose=bodies[s]
        body=f'''<section><div class="wrap narrow">
<div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Blog</a> › {t}</div>
<h1>{t}</h1>
<p class="muted">Updated {TODAY} · NeuroVitol Brain Health Library</p>
<div class="prose">{prose}</div>
<div style="margin:30px 0">{cta_buttons()}</div>
<div class="disclaimer">† These statements have not been evaluated by the Food and Drug Administration. NeuroVitol is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease. This article is for general information only and is not medical advice.</div>
</div></section>{keyword_footer("../")}'''
        page(f"blog/{s}.html", t+" | NeuroVitol", d, body, prefix="../",
             schema=[article_schema(t,d,DOMAIN+f"/blog/{s}.html"), breadcrumb([("Home",DOMAIN+"/"),("Blog",DOMAIN+"/blog/"),(t,DOMAIN+f"/blog/{s}.html")])],
             keywords="brain supplement, nootropic, brain fog, focus, memory, "+t)

def build_legal():
    legal_note=f'''<div class="disclaimer">For questions, contact {EMAIL} or {PHONE}.</div>'''
    privacy=f'''<h2>Privacy Policy</h2><p class="muted">Last updated {TODAY}</p>
<p>This Privacy Policy explains how {BRAND} ("we", "us") collects and uses information on neurovitol.shop.</p>
<h3>Information we collect</h3><p>We may collect information you provide (such as name and email if you contact us) and standard analytics data (pages visited, device, referring URL). We may use advertising identifiers such as Google Click Identifier (gclid) to measure ad performance.</p>
<h3>How we use information</h3><p>To operate and improve the site, respond to inquiries, measure marketing performance, and route visitors to the official NeuroVitol checkout.</p>
<h3>Cookies &amp; advertising</h3><p>We and our partners use cookies and similar technologies for analytics and advertising (including Google Ads). You can control cookies through your browser settings.</p>
<h3>Third parties</h3><p>Purchases are completed on the official NeuroVitol order page operated by the merchant/affiliate network; their privacy terms apply at checkout. We may earn a commission on qualifying purchases.</p>
<h3>Your choices</h3><p>Contact us to access or delete information we hold about you.</p>{legal_note}'''
    terms=f'''<h2>Terms &amp; Conditions</h2><p class="muted">Last updated {TODAY}</p>
<p>By using neurovitol.shop you agree to these terms. Content is provided for general informational purposes about the NeuroVitol supplement.</p>
<h3>Affiliate disclosure</h3><p>This website is an independent marketing and information site for NeuroVitol. We may receive compensation when you purchase through links on this site. This does not affect the price you pay.</p>
<h3>No medical advice</h3><p>Nothing on this site is medical advice. NeuroVitol is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease. Consult your physician before use.</p>
<h3>Pricing &amp; availability</h3><p>Prices, discounts, and stock shown are promotional and may change without notice. Final pricing is confirmed at the official checkout.</p>
<h3>Guarantee</h3><p>The 60-day money-back guarantee is administered by the merchant per the terms shown at checkout.</p>{legal_note}'''
    disc=f'''<h2>Disclaimer</h2><p class="muted">Last updated {TODAY}</p>
<p><b>† These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.</b></p>
<p>NeuroVitol is a dietary supplement intended to support general cognitive wellness. It is not a drug, is not a substitute for professional medical care, and results vary from person to person. Testimonials reflect individual experiences and are not a guarantee that anyone will achieve the same results.</p>
<p>Consult your healthcare provider before use if you are pregnant, nursing, under 18, taking medication, or have a medical condition. This site may contain affiliate links for which we may receive compensation.</p>
<h3>Marketing &amp; comparison disclaimer</h3><p>Comparisons to other brands reflect publicly available information and typical positioning as of 2026 and are the opinion of this site. All trademarks and brand names are the property of their respective owners; their use does not imply affiliation or endorsement.</p>{legal_note}'''
    for slug,title,content in [("privacy","Privacy Policy",privacy),("terms","Terms & Conditions",terms),("disclaimer","Disclaimer",disc)]:
        body=f'''<section><div class="wrap narrow prose">
<div class="crumbs"><a href="../index.html">Home</a> › {title}</div>{content}</div></section>'''
        page(f"legal/{slug}.html", f"{title} | {BRAND}", f"{title} for {BRAND} (neurovitol.shop).",
             body, prefix="../", robots="index,follow",
             keywords=f"NeuroVitol {title.lower()}")

# ---------------- assets: favicon, og placeholder, 404 ----------------
def build_static():
    fav='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f46e5"/><stop offset="1" stop-color="#9333ea"/></linearGradient></defs><rect width="48" height="48" rx="12" fill="url(#g)"/><g fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12a4 4 0 0 1 4 4v18a4 4 0 0 1-7.5.7 4 4 0 0 1-4.5-5 4.4 4.4 0 0 1-.5-8.3A4 4 0 0 1 12 14a4 4 0 0 1 7-2Z"/><path d="M29 12a4 4 0 0 0-4 4v18a4 4 0 0 0 7.5.7 4 4 0 0 0 4.5-5 4.4 4.4 0 0 0 .5-8.3A4 4 0 0 0 36 14a4 4 0 0 0-7-2Z"/></g></svg>'''
    with open(os.path.join(ROOT,"assets","favicon.svg"),"w",encoding="utf-8") as f: f.write(fav)
    # simple OG image (SVG) — used as og:image fallback
    og=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f46e5"/><stop offset="1" stop-color="#9333ea"/></linearGradient></defs><rect width="1200" height="630" fill="#0f1222"/><rect x="40" y="40" width="1120" height="550" rx="28" fill="url(#g)"/><text x="600" y="270" fill="#fff" font-family="Sora,Arial" font-weight="800" font-size="86" text-anchor="middle">NeuroVitol®</text><text x="600" y="350" fill="#ede9fe" font-family="Inter,Arial" font-size="40" text-anchor="middle">Advanced Brain Support</text><text x="600" y="440" fill="#fbbf24" font-family="Sora,Arial" font-weight="700" font-size="44" text-anchor="middle">Memory · Focus · Clarity · 60% OFF</text></svg>'''
    with open(os.path.join(ROOT,"assets","og.svg"),"w",encoding="utf-8") as f: f.write(og)
    # 404
    body='''<section class="hero"><div class="wrap narrow center">
<h1>Page Not Found</h1><p class="lead">That page wandered off — but your brain support is right here.</p>
<a class="btn btn-cta btn-lg pulse js-cta" data-cta="VSL" href="/index.html#order">Claim 60% Off NeuroVitol →</a>
<p style="margin-top:18px"><a href="/index.html">Back to home</a> · <a href="/vs/index.html">Compare</a> · <a href="/blog/index.html">Blog</a></p></div></section>'''
    page("404.html","Page Not Found | NeuroVitol","Page not found.",body,robots="noindex,follow")

def build_seo_files():
    urls=["/","/benefits.html","/ingredients.html","/how-it-works.html","/reviews.html","/faq.html",
          "/about.html","/contact.html","/vs.html","/vs/index.html","/blog/index.html"]
    urls+=[f"/vs/{s}.html" for s in COMPETITORS]
    urls+=[f"/blog/{s}.html" for s,_,_ in BLOG]
    urls+=["/legal/privacy.html","/legal/terms.html","/legal/disclaimer.html"]
    items=""
    for u in urls:
        pr="1.0" if u=="/" else ("0.8" if u.startswith("/vs") or u.startswith("/blog/best") else "0.6")
        items+=f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n"
    sm=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'
    open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8").write(sm)

    robots=f'''User-agent: *
Allow: /

# AI / answer engines
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
'''
    open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8").write(robots)

    llms=f'''# NeuroVitol — Advanced Brain Support

> {PRODUCT} is a daily nootropic dietary supplement that supports memory, focus, mental clarity and healthy cognitive performance. Formulated with Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine and Vitamin B12. Non-habit forming, non-jittery, made for steady daily support. Available online (no prescription) from $49/bottle with free shipping and a 60-day money-back guarantee. Rated 4.9/5 by 6,000+ customers; trusted by 7,500+.

## Key facts
- Product: {PRODUCT}
- Use: daily cognitive support — memory, focus, clarity, reasoning, less brain fog
- Ingredients: Bacopa Monnieri, Lion's Mane, Ginkgo Biloba, Phosphatidylserine, Vitamin B12
- Pricing: 2 bottles $158 ($79/ea) · 3 bottles $207 ($59/ea) · 6 bottles $294 ($49/ea); free shipping
- Guarantee: 60-day money-back
- Contact: {PHONE} · {EMAIL}
- Important: dietary supplement; not intended to diagnose, treat, cure, or prevent any disease

## Pages
- Home: {DOMAIN}/
- Benefits: {DOMAIN}/benefits.html
- Ingredients: {DOMAIN}/ingredients.html
- How It Works: {DOMAIN}/how-it-works.html
- Reviews: {DOMAIN}/reviews.html
- FAQ: {DOMAIN}/faq.html
- Comparisons: {DOMAIN}/vs/index.html
- Blog: {DOMAIN}/blog/index.html
'''
    open(os.path.join(ROOT,"llms.txt"),"w",encoding="utf-8").write(llms)
    open(os.path.join(ROOT,"CNAME"),"w",encoding="utf-8").write("neurovitol.shop\n")
    open(os.path.join(ROOT,".nojekyll"),"w",encoding="utf-8").write("")

def main():
    build_index(); build_benefits(); build_ingredients(); build_how(); build_reviews()
    build_faq(); build_about(); build_contact()
    build_vs_index(); build_vs_dynamic()
    for slug,data in COMPETITORS.items(): build_vs(slug,data)
    build_blog_index(); build_blog_posts()
    build_legal(); build_static(); build_seo_files()
    print("Built NeuroVitol site:")
    for dp,_,fs in os.walk(ROOT):
        for fn in fs:
            if fn.endswith((".html",".xml",".txt",".svg")) and "neurovitol_home" not in fn:
                print("  ", os.path.relpath(os.path.join(dp,fn),ROOT))

if __name__=="__main__":
    main()
