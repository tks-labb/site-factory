#!/usr/bin/env python3
"""Ammori Group website builder.

Edit PROPERTIES (and COMPANY) below, then run:
    python3 clients/ammori-group/build.py
It writes sites/ammori-group/: index.html, one page per property, sitemap.xml, robots.txt.

Photos: put images in sites/ammori-group/assets/photos/ and set "photo" on a property
(e.g. "photos/crooks-1.jpg"). Without a photo, a gold line drawing of the building type is shown.
"""
import html, json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "sites" / "ammori-group"
BASE = "https://ammorigroup.com"

COMPANY = {
    "name": "Ammori Group",
    "email": "info@ammorigroup.com",
    "phone": "",  # e.g. "(248) 555-0100" — shown everywhere once filled in
    "street": "77 E. Long Lake Rd., Suite 100",
    "city": "Bloomfield Hills", "state": "MI", "zip": "48304",
    # Portfolio figures for the Acquisitions section. Leave "" to hide a figure.
    "asset_value": "",      # e.g. "$25M+"
    "total_sf": "",         # e.g. "110,000+ SF"
}

# status: "available" or "leased". sf: number or None. type is used for the filter.
PROPERTIES = [
    {
        "slug": "5600-crooks-road-troy-mi",
        "name": "5600 Crooks Road",
        "nickname": "Northfield Plaza",
        "city": "Troy", "state": "MI", "zip": "48098",
        "kind": "Office", "art": "office",
        "photo": "",
        "photos": [
            ("crooks-front", "Front of 5600 Crooks Road: brick and glass two-story office building with landscaping"),
            ("crooks-aerial-entrance", "Aerial view of 5600 Crooks Road with the Loccino restaurant entrance and parking"),
            ("crooks-aerial-site", "Aerial view of the 5600 Crooks Road site between Crooks Road and I-75, with parking on two sides"),
            ("crooks-aerial-parking", "Aerial view of 5600 Crooks Road showing the building, parking lots and surrounding office campus"),
            ("crooks-location-map", "Location map of 5600 Crooks Road in Troy near I-75, Aptiv, Gallagher Kaiser, Panera, Starbucks and Embassy Suites"),
        ],
        "highlights": [
            "Up to 35,838 SF available in one building",
            "Frontage on Crooks Road, about 24,981 cars per day",
            "Next to I-75, about 89,578 cars per day, with a nearby interchange",
            "Neighbors include Aptiv (about 1,300 employees) and Gallagher Kaiser (about 1,379 employees)",
            "Walk to Panera, Starbucks and Embassy Suites, with a future hotel and planned commercial development nearby",
            "Loccino Italian Grill on site, plus large surface parking lots on two sides",
        ],
        "summary": "A two-story office building on Crooks Road in Troy with suites from about 2,800 to 16,000 SF, office and medical-ready space, lower-level storage and a café with equipment in place.",
        "facts": [("Property type", "Office / medical office"), ("Available", "Up to 35,838 SF"), ("Parking", "Large lots on two sides"), ("Access", "Crooks Road and I-75")],
        "spaces": [
            {"suite": "Suite 105", "sf": 8334, "type": "Office", "note": "Build-to-suit. Can combine with Suite 103.", "status": "available"},
            {"suite": "Suite 103", "sf": 2858, "type": "Medical", "label": "Office / Medical", "note": "Can combine with Suite 105.", "status": "available"},
            {"suite": "Suite 210", "sf": 4083, "type": "Office", "note": "Second floor.", "status": "available"},
            {"suite": "Suite 220", "sf": 16068, "type": "Office", "note": "Second floor.", "status": "available"},
            {"suite": "LL1–LL7", "sf": None, "type": "Storage", "label": "Office storage", "note": "Seven lower-level storage units. Ask for sizes.", "status": "available"},
            {"suite": "Café", "sf": None, "type": "Restaurant", "label": "Restaurant / café", "note": "Café with equipment in place.", "status": "available"},
            {"suite": "Suite 104", "sf": None, "type": "Office", "note": "", "status": "leased"},
            {"suite": "Suite 200", "sf": None, "type": "Office", "note": "", "status": "leased"},
        ],
    },
    {
        "slug": "2151-w-liberty-street-ann-arbor-mi",
        "name": "2151 W Liberty Street",
        "nickname": "West Ann Arbor",
        "city": "Ann Arbor", "state": "MI", "zip": "48103",
        "kind": "Retail", "art": "retail",
        "photo": "",
        "summary": "A freestanding commercial building on W Liberty Street in West Ann Arbor, near W Stadium Blvd. About 14,990 SF that can be divided for smaller users.",
        "facts": [("Property type", "Freestanding retail / commercial"), ("Building size", "About 14,990 SF"), ("Divisible", "To about 4,000 SF"), ("Location", "W Liberty St near W Stadium Blvd")],
        "spaces": [
            {"suite": "Entire building", "sf": 14990, "type": "Retail", "label": "Retail / commercial", "note": "Freestanding. Divisible to about 4,000 SF.", "status": "available"},
        ],
    },
]

TYPES = ["Office", "Medical", "Retail", "Restaurant", "Storage"]

e = html.escape
def sf(n): return f"{n:,} SF" if n else "Ask for size"

ART = {
"office": '''<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice" aria-hidden="true" class="art"><defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1a17"/><stop offset="1" stop-color="#0d0d0c"/></linearGradient></defs><rect width="400" height="260" fill="url(#g{i})"/><g fill="none" stroke="#C9A35C" stroke-width="1.4"><path d="M60 214h280"/><rect x="70" y="112" width="260" height="102"/><path d="M70 146h260M70 180h260"/>{win}<path d="M184 214v-26h32v26"/><path d="M58 112h284"/><path d="M70 214v8M330 214v8" stroke-opacity=".5"/></g><g stroke="#C9A35C" stroke-opacity=".35"><path d="M40 222h320"/></g></svg>''',
"retail": '''<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice" aria-hidden="true" class="art"><defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1a17"/><stop offset="1" stop-color="#0d0d0c"/></linearGradient></defs><rect width="400" height="260" fill="url(#g{i})"/><g fill="none" stroke="#C9A35C" stroke-width="1.4"><path d="M50 214h300"/><rect x="74" y="98" width="252" height="116"/><path d="M66 98h268l-10-22H76z"/><rect x="96" y="132" width="78" height="60"/><rect x="226" y="132" width="78" height="60"/><path d="M186 214v-82h28v82"/><path d="M135 132v60M265 132v60"/><path d="M120 116h160" stroke-opacity=".6"/></g><g stroke="#C9A35C" stroke-opacity=".35"><path d="M30 222h340"/></g></svg>''',
}
def art(kind, i):
    win = "".join(f'<path d="M{x} 120v18M{x} 154v18" stroke-opacity=".55"/>' for x in range(86, 320, 20))
    return ART[kind].replace("{i}", str(i)).replace("{win}", win)

def media(p, i, cls="ph", k=0, big=False):
    if p.get("photos"):
        name, alt = p["photos"][k % len(p["photos"])]
        src = f"assets/photos/{name}{'' if big else '-sm'}.webp"
        w, h = (1600, 900) if big else (800, 450)
        return f'<div class="{cls}"><img src="{src}" alt="{e(alt)}" loading="{"eager" if big else "lazy"}" width="{w}" height="{h}"></div>'
    if p.get("photo"):
        return f'<div class="{cls}"><img src="assets/{e(p["photo"])}" alt="{e(p["name"])}, {e(p["city"])}, {e(p["state"])}" loading="lazy" width="1200" height="780"></div>'
    return f'<div class="{cls}">{art(p["art"], i)}</div>'

LOGO = '<img class="logo" src="assets/mark-sm.png" alt="" width="178" height="48">'

def head(title, desc, path, extra_ld=None):
    page = 'home' if path == 'index.html' else 'inner'
    ld = {
        "@context": "https://schema.org", "@type": "RealEstateAgent", "name": COMPANY["name"],
        "url": BASE + "/", "email": COMPANY["email"],
        "description": "Ammori Group owns and manages commercial real estate in Metro Detroit and Ann Arbor, leasing office, medical and retail space directly to tenants.",
        "address": {"@type": "PostalAddress", "streetAddress": COMPANY["street"], "addressLocality": COMPANY["city"], "addressRegion": COMPANY["state"], "postalCode": COMPANY["zip"], "addressCountry": "US"},
        "areaServed": ["Metro Detroit, MI", "Ann Arbor, MI"],
    }
    if COMPANY["phone"]: ld["telephone"] = COMPANY["phone"]
    lds = [ld] + (extra_ld or [])
    url = BASE + "/" + ("" if path == "index.html" else path)
    return f'''<!doctype html>
<html lang="en" data-page="{page}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{BASE}/assets/logo.png">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..800&family=Cinzel:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
<script>(function(){{var d=document.documentElement;d.classList.add('js');try{{var t=localStorage.getItem('am_theme');if(t)d.setAttribute('data-theme',t);if(d.dataset.page==='home'&&!sessionStorage.getItem('am_intro')){{d.classList.add('intro');sessionStorage.setItem('am_intro','1');}}}}catch(e){{}}}})();</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top" id="top-bar">
  <div class="wrap">
    <a class="brand" href="index.html">{LOGO}<span class="wm">Ammori <b>Group</b></span></a>
    <nav class="nav" id="nav" aria-label="Main"><a href="index.html#spaces">Available spaces</a><a href="index.html#portfolio">Portfolio</a><a href="index.html#about">About</a><a href="index.html#acquisitions">Acquisitions</a><a class="btn btn-gold" href="index.html#contact">Contact</a></nav>
    <button class="theme-btn" id="theme-btn" type="button" aria-label="Switch to dark mode"><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg></button>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span></button>
  </div>
</header>
'''

def space_card(p, s, i, show_building=True):
    k = available(p).index(s) if s in available(p) else 0
    label = s.get("label", s["type"])
    building = f'<p class="bld"><a href="{p["slug"]}.html">{e(p["name"])}</a> · {e(p["city"])}, {e(p["state"])}</p>' if show_building else ""
    return f'''<article class="space rv" data-type="{e(s["type"])}">
          {media(p, i, k=k % max(1, len([x for x in p.get('photos', []) if 'map' not in x[0]]) or 1))}
          <div class="sp-body">
            <div class="sp-top"><h3>{e(s["suite"])}</h3><span class="tag"><i></i>Available</span></div>
            {building}
            <dl class="sp-meta"><div><dt>Size</dt><dd>{sf(s["sf"])}</dd></div><div><dt>Use</dt><dd>{e(label)}</dd></div></dl>
            <p class="note">{e(s["note"])}</p>
            <a class="btn btn-line inquire" href="index.html#contact" data-space="{e(p["name"])} – {e(s["suite"])}">Inquire about this space</a>
          </div>
        </article>'''

def available(p): return [s for s in p["spaces"] if s["status"] == "available"]

def property_card(p, i):
    av = available(p); total = sum(s["sf"] or 0 for s in av)
    return f'''<article class="prop rv">
          <a class="prop-link" href="{p["slug"]}.html" aria-label="{e(p["name"])}, {e(p["city"])}">{media(p, 100 + i, "ph tall")}</a>
          <div class="prop-body">
            <p class="eyebrow">{e(p["kind"])} · {e(p["city"])}, {e(p["state"])}</p>
            <h3><a href="{p["slug"]}.html">{e(p["name"])}</a></h3>
            <p>{e(p["summary"])}</p>
            <div class="prop-stats"><span><b>{len(av)}</b> available</span><span><b>{total:,}</b> SF listed</span></div>
            <a class="arrow-link" href="{p["slug"]}.html">View property <span aria-hidden="true">→</span></a>
          </div>
        </article>'''

def contact_section(heading="Tell us what you're looking for", lede="Share a few details and the right person on our team will get back to you, usually the same business day."):
    phone = f'<div><span class="k">Phone</span><a href="tel:{"".join(c for c in COMPANY["phone"] if c.isdigit())}">{e(COMPANY["phone"])}</a></div>' if COMPANY["phone"] else ""
    return f'''<section id="contact" class="contact dark">
    <div class="wrap grid2">
      <div class="rv">
        <p class="eyebrow">Contact</p>
        <h2>{e(heading)}</h2>
        <p class="lede">{e(lede)}</p>
        <div class="kv">
          <div><span class="k">Email</span><a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></div>
          {phone}
          <div><span class="k">Office</span><span>{e(COMPANY["street"])}<br>{e(COMPANY["city"])}, {COMPANY["state"]} {COMPANY["zip"]}</span></div>
          <div><span class="k">Markets</span><span>Metro Detroit and Ann Arbor, Michigan</span></div>
        </div>
      </div>
      <div class="rv">
        <form id="inquiry" name="inquiry" method="POST" data-netlify="true" netlify-honeypot="company_site" novalidate>
          <input type="hidden" name="form-name" value="inquiry">
          <p hidden><label>Leave this empty <input name="company_site"></label></p>
          <div class="row">
            <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required><span class="err" id="e-name" hidden>Enter your name.</span></div>
            <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err" id="e-email" hidden>Enter an email like name@company.com.</span></div>
          </div>
          <div class="row">
            <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="f-topic">I'm interested in</label><select id="f-topic" name="topic"><option>Leasing space</option><option>Selling a property to Ammori Group</option><option>Selling a business to Ammori Group</option><option>Something else</option></select></div>
          </div>
          <div class="field"><label for="f-msg">What are you looking for?</label><textarea id="f-msg" name="message" placeholder="Type of space, approximate size, timing, preferred area…" required></textarea><span class="err" id="e-msg" hidden>Tell us a little about what you need.</span></div>
          <button class="btn btn-gold" type="submit">Send message</button>
          <p class="err" id="e-send" hidden>Your message didn't send. Please try again or email {COMPANY["email"]}.</p>
        </form>
        <div class="sent" id="sent" hidden tabindex="-1"><strong>Thank you.</strong><p>Your message is on its way. We'll be in touch shortly.</p></div>
      </div>
    </div>
  </section>'''

def footer():
    links = "".join(f'<a href="{p["slug"]}.html">{e(p["name"])}, {e(p["city"])}</a>' for p in PROPERTIES)
    return f'''<footer>
  <div class="wrap fgrid">
    <div><a class="flogo" href="index.html" aria-label="Ammori Group home"><img src="assets/logo-light.webp" alt="Ammori Group, Real Estate and Property Management" width="520" height="412" loading="lazy"></a><p class="muted">Owner-operated commercial real estate in Metro Detroit and Ann Arbor.</p></div>
    <div><p class="k">Properties</p>{links}</div>
    <div><p class="k">Company</p><a href="index.html#about">About</a><a href="index.html#acquisitions">Acquisitions</a><a href="index.html#contact">Contact</a></div>
    <div><p class="k">Office</p><p class="muted">{e(COMPANY["street"])}<br>{e(COMPANY["city"])}, {COMPANY["state"]} {COMPANY["zip"]}<br><a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></p></div>
  </div>
  <div class="wrap fine"><span>© 2026 Ammori Group. All rights reserved.</span><span>Availability and sizes are approximate and subject to change.</span></div>
</footer>
<script src="assets/site.js" defer></script>
<script src="assets/chat.js" defer></script>
</body>
</html>
'''

def place_ld(p):
    return {"@context": "https://schema.org", "@type": "Place", "name": f'{p["name"]}, {p["city"]}',
            "address": {"@type": "PostalAddress", "streetAddress": p["name"], "addressLocality": p["city"], "addressRegion": p["state"], "postalCode": p["zip"], "addressCountry": "US"},
            "description": p["summary"]}

def intro_html():
    """Opening motion graphic: 5600 Crooks Road draws itself in gold, windows light up, then the page is revealed."""
    p = PROPERTIES[0]; av = available(p)
    wins = []
    k = 0
    for row, y in enumerate((178, 240)):
        for x in range(176, 624, 32):
            d = 1.25 + ((k * 37) % 23) * 0.035 + row * 0.12
            wins.append(f'<rect class="w" x="{x}" y="{y}" width="18" height="34" style="--d:{d:.2f}s"/>')
            k += 1
    trees = "".join(
        f'<g class="tree"><path class="ln" style="--d:{d}s" pathLength="1" d="M{x} 330v-34"/><circle class="ln" style="--d:{d + .1:.2f}s" pathLength="1" cx="{x}" cy="{y}" r="{r}"/></g>'
        for x, y, r, d in ((88, 276, 24, 1.0), (122, 290, 15, 1.1), (712, 280, 22, 1.05), (742, 294, 13, 1.15)))
    svg = (
        '<svg class="ix-art" viewBox="0 0 800 400" aria-hidden="true">'
        '<defs><radialGradient id="ixglow" cx="50%" cy="66%" r="34%"><stop offset="0" stop-color="#C9A35C" stop-opacity=".30"/><stop offset="1" stop-color="#C9A35C" stop-opacity="0"/></radialGradient></defs>'
        '<rect class="ix-glow" x="0" y="0" width="800" height="400" fill="url(#ixglow)"/>'
        '<g fill="none" stroke="#C9A35C" stroke-width="1.6" stroke-linecap="round">'
        '<path class="ln" style="--d:.15s" pathLength="1" d="M30 330H770"/>'
        '<path class="ln" style="--d:.35s" pathLength="1" d="M150 330V156H650V330"/>'
        '<path class="ln" style="--d:.55s" pathLength="1" d="M132 156H668"/>'
        '<path class="ln" style="--d:.7s" pathLength="1" d="M150 222H650"/>'
        '<path class="ln" style="--d:.78s" pathLength="1" d="M150 284H650"/>'
        '<path class="ln" style="--d:.9s" pathLength="1" d="M360 296H440M372 296V330M428 296V330"/>'
        '<path class="ln thin" style="--d:1.0s" pathLength="1" d="M60 346H740"/>'
        '<path class="ln thin" style="--d:1.1s" pathLength="1" d="M110 362H690"/>'
        + trees +
        '</g><g fill="#C9A35C">' + "".join(wins) + '</g></svg>')
    return (
        '<div class="intro-ov" id="intro" aria-hidden="true">\n'
        '  <div class="ix-stage">\n    ' + svg + '\n'
        '    <div class="ix-copy">\n'
        '      <img class="ix-logo" src="assets/logo-light.webp" alt="" width="520" height="412">\n'
        '      <p class="ix-k">Presents</p>\n'
        f'      <p class="ix-t">{e(p["name"])}</p>\n'
        f'      <p class="ix-s">{e(p["city"])}, Michigan &middot; {len(av)} spaces now leasing</p>\n'
        '    </div>\n  </div>\n'
        '  <button class="ix-skip" type="button">Skip</button>\n'
        '</div>\n')


CHAT_FN_TEMPLATE = Path(__file__).with_name("chat_function.mjs.tpl")

def chat_function():
    lines = []
    for p in PROPERTIES:
        lines.append(f'- {p["name"]}, {p["city"]}, {p["state"]} {p["zip"]} ({p["kind"]}). {p["summary"]} Page: {BASE}/{p["slug"]}.html')
        for k, v in p["facts"]:
            lines.append(f'  - {k}: {v}')
        for h in p.get("highlights", []):
            lines.append(f'  - Highlight: {h}')
        for sp in available(p):
            size = f'{sp["sf"]:,} SF' if sp["sf"] else "size on request"
            lines.append(f'  - AVAILABLE: {sp["suite"]}: {size}, {sp.get("label", sp["type"])}. {sp["note"]}'.rstrip())
        leased = [sp["suite"] for sp in p["spaces"] if sp["status"] != "available"]
        if leased:
            lines.append(f'  - Currently leased (not available): {", ".join(leased)}')
    phone = f'Phone: {COMPANY["phone"]}. ' if COMPANY["phone"] else ""
    system = "\n".join([
        "You are the website assistant for Ammori Group, chatting with visitors on ammorigroup.com.",
        "",
        "About Ammori Group:",
        "- A Bloomfield Hills, Michigan real estate company that owns and manages its own commercial properties in Metro Detroit and Ann Arbor. It manages only its own buildings, never other owners' properties.",
        "- Tenants lease directly from ownership. Suites can often be combined or built to suit.",
        "- Acquisitions: Ammori Group is actively buying commercial buildings (office, medical office, retail, mixed-use, including value-add properties) and operating businesses, with or without real estate, in Metro Detroit, Ann Arbor and surrounding markets.",
        f'- Office: {COMPANY["street"]}, {COMPANY["city"]}, {COMPANY["state"]} {COMPANY["zip"]}. Email: {COMPANY["email"]}. {phone}'.rstrip(),
        f"- Inquiry form: {BASE}/#contact",
        "",
        "Current portfolio and availability (the only properties and spaces that exist; sizes are approximate):",
        *lines,
        "",
        "How to reply:",
        "- Keep replies short: two to four sentences, plain text, no markdown headings, bullets or tables.",
        "- Be professional, warm and helpful. Help visitors find a space that fits their size, use and location, and name the specific suite and building.",
        f'- Only state facts listed above. You do not know rents, lease terms, pricing, floor plans, parking ratios or exact dates; for those, ask the visitor to send the inquiry form or email {COMPANY["email"]}, and say the team usually replies the same business day.',
        "- Never invent properties, suites, tenants, prices or amenities. Never promise availability; spaces are subject to change.",
        '- If someone wants to sell a building or a business, welcome it and point them to the inquiry form (choose "Selling a property" or "Selling a business").',
        f"- When a visitor seems interested, invite them to send the inquiry form at {BASE}/#contact to ask about a tour.",
        "- Stay on topics related to Ammori Group, its properties, leasing and acquisitions. Politely decline unrelated requests.",
    ])
    fallback = f'I can\'t help with that here. For questions about our properties, use the inquiry form or email {COMPANY["email"]}.'
    tpl = CHAT_FN_TEMPLATE.read_text()
    return tpl.replace("__SYSTEM__", json.dumps(system, ensure_ascii=False)).replace("__FALLBACK__", json.dumps(fallback))


def index():
    all_av = [(p, s) for p in PROPERTIES for s in available(p)]
    total = sum(s["sf"] or 0 for _, s in all_av)
    cities = sorted({p["city"] for p in PROPERTIES})
    used = [t for t in TYPES if any(s["type"] == t for _, s in all_av)]
    chips = '<button type="button" class="chip" aria-pressed="true" data-f="all">All <span>' + str(len(all_av)) + '</span></button>' + "".join(
        f'<button type="button" class="chip" aria-pressed="false" data-f="{t}">{t} <span>{sum(1 for _, s in all_av if s["type"] == t)}</span></button>' for t in used)
    cards = "\n        ".join(space_card(p, s, i) for i, (p, s) in enumerate(all_av))
    props = "\n        ".join(property_card(p, i) for i, p in enumerate(PROPERTIES))
    kinds = ", ".join(sorted({p["kind"] for p in PROPERTIES}))
    snap = [("Properties owned", str(len(PROPERTIES))), ("Markets", " · ".join(cities)), ("Property types", "Office · Medical · Retail")]
    if COMPANY["total_sf"]: snap.insert(1, ("Square feet owned", COMPANY["total_sf"]))
    if COMPANY["asset_value"]: snap.insert(0, ("Real estate asset value", COMPANY["asset_value"]))
    snap_html = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in snap)
    body = intro_html() + f'''<main id="main">
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow rv">Owner-operated commercial real estate · Metro Detroit</p>
        <h1 class="rv d1">Space to grow, in buildings <em>we own.</em></h1>
        <p class="lede rv d2">Ammori Group owns and manages its own office, medical and retail properties. Lease directly from ownership, with straightforward terms and space that can be built around your business.</p>
        <div class="ctas rv d3"><a class="btn btn-gold" href="#spaces">View available spaces <span aria-hidden="true">→</span></a><a class="btn btn-ghost" href="#contact">Talk to our team</a></div>
      </div>
      <div class="hero-panel rv d2">
        <div class="hero-art" aria-hidden="true">{art("office", 999)}</div>
        <p class="panel-tag"><span class="dot"></span>Leasing now in {" &amp; ".join(cities)}</p>
        <dl class="stats">
          <div><dd data-count="{len(all_av)}">{len(all_av)}</dd><dt>Spaces available</dt></div>
          <div><dd data-count="{total}">{total:,}</dd><dt>Square feet listed</dt></div>
          <div><dd data-count="{len(PROPERTIES)}">{len(PROPERTIES)}</dd><dt>Owned properties</dt></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="why">
    <div class="wrap">
      <div class="three">
        <div class="rv"><span class="num">01</span><h3>Deal directly with ownership</h3><p>We own every building we lease. No outside landlord, no layers of approval, faster answers.</p></div>
        <div class="rv d1"><span class="num">02</span><h3>Space built around you</h3><p>Combine suites, build to suit, or start small and expand within the same building as you grow.</p></div>
        <div class="rv d2"><span class="num">03</span><h3>Managed by the owner</h3><p>We manage only our own properties, so the buildings get the attention of the people who own them.</p></div>
      </div>
    </div>
  </section>

  <section id="spaces" class="spaces">
    <div class="wrap">
      <div class="sec-head rv"><p class="eyebrow">Availability</p><h2>Available spaces</h2><p>Office, medical, retail and specialty space ready to lease. Pick a space to send an inquiry, or contact us for something that isn't listed.</p></div>
      <div class="chips rv" role="group" aria-label="Filter by type">{chips}</div>
      <div class="grid3" id="space-grid">
        {cards}
      </div>
      <p class="empty" id="empty" hidden>Nothing in that category right now. <a href="#contact">Tell us what you need</a> and we'll let you know when it opens up.</p>
    </div>
  </section>

  <section id="portfolio" class="portfolio light2">
    <div class="wrap">
      <div class="sec-head rv"><p class="eyebrow">Portfolio</p><h2>Our properties</h2><p>Every building below is owned and managed by Ammori Group.</p></div>
      <div class="grid2 props">
        {props}
      </div>
    </div>
  </section>

  <section id="about" class="about">
    <div class="wrap grid2">
      <div class="rv"><p class="eyebrow">About</p><h2>Owners, not middlemen.</h2></div>
      <div class="rv d1 prose">
        <p>Ammori Group is a Bloomfield Hills real estate company that owns and operates commercial property across Metro Detroit and Ann Arbor. We don't manage buildings for other owners. Every property in our portfolio is our own, which means decisions about leasing, improvements and service are made by the people who own the building.</p>
        <p>For tenants, that means direct conversations, flexible layouts and a landlord who is invested in the property for the long term.</p>
      </div>
    </div>
  </section>

  <section id="acquisitions" class="acq dark">
    <div class="wrap grid2">
      <div class="rv">
        <p class="eyebrow">Acquisitions</p>
        <h2>We're growing our portfolio.</h2>
        <p class="lede">Ammori Group is actively looking to buy commercial buildings and established businesses in Michigan. If you're thinking about selling, we can move quickly and keep the process simple.</p>
        <ul class="ticks"><li>Office, medical office, retail and mixed-use buildings</li><li>Value-add properties with vacancy or deferred upkeep</li><li>Operating businesses, with or without real estate</li><li>Metro Detroit, Ann Arbor and surrounding markets</li></ul>
        <a class="btn btn-gold" href="#contact" data-topic="Selling a property to Ammori Group">Tell us about your property</a>
      </div>
      <div class="rv d1">
        <div class="snap"><p class="k">Portfolio at a glance</p><dl>{snap_html}</dl></div>
      </div>
    </div>
  </section>

  {contact_section()}
</main>
'''
    desc = f"Ammori Group owns and manages commercial real estate in {' and '.join(cities)}, Michigan. Lease office, medical and retail space directly from ownership. {len(all_av)} spaces available now."
    return head("Ammori Group | Office, Medical & Retail Space for Lease in Metro Detroit", desc, "index.html", [place_ld(p) for p in PROPERTIES]) + body + footer()

def gallery_html(p):
    photos = p.get("photos") or []
    hl = p.get("highlights") or []
    if not photos and not hl: return ""
    tiles = "".join(
        f'<button class="g-tile{" wide" if n == 0 else ""}" type="button" data-full="assets/photos/{name}.webp" data-alt="{e(alt)}" aria-label="View larger: {e(alt)}"><img src="assets/photos/{name}-sm.webp" alt="{e(alt)}" loading="lazy" width="800" height="450"></button>'
        for n, (name, alt) in enumerate(photos))
    items = "".join(f"<li>{e(h)}</li>" for h in hl)
    return f'''<section class="gallery-sec">
    <div class="wrap grid-gal">
      <div class="rv"><p class="eyebrow">The property</p><h2>Location highlights</h2><ul class="ticks light">{items}</ul></div>
      <div class="gallery rv d1">{tiles}</div>
    </div>
  </section>
  <dialog class="lightbox" id="lightbox" aria-label="Photo"><img alt=""><button class="lb-x" type="button" aria-label="Close">✕</button><button class="lb-prev" type="button" aria-label="Previous photo">‹</button><button class="lb-next" type="button" aria-label="Next photo">›</button></dialog>'''

def property_page(p, i):
    av = available(p); leased = len(p["spaces"]) - len(av)
    cards = "\n        ".join(space_card(p, s, 200 + j, show_building=False) for j, s in enumerate(av))
    facts = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p["facts"])
    others = "".join(property_card(o, 300 + k) for k, o in enumerate(PROPERTIES) if o is not p)
    leased_note = f'<p class="muted small">{leased} other suite{"s" if leased != 1 else ""} in this building {"are" if leased != 1 else "is"} currently leased.</p>' if leased else ""
    body = f'''<main id="main">
  <section class="phero">
    <div class="wrap grid2">
      <div>
        <p class="crumbs rv"><a href="index.html">Home</a> / <a href="index.html#portfolio">Portfolio</a> / {e(p["name"])}</p>
        <p class="eyebrow rv">{e(p["kind"])} · {e(p["city"])}, {e(p["state"])} {e(p["zip"])}</p>
        <h1 class="rv d1">{e(p["name"])}</h1>
        <p class="lede rv d2">{e(p["summary"])}</p>
        <div class="ctas rv d3"><a class="btn btn-gold" href="#avail">See {len(av)} available space{"s" if len(av) != 1 else ""}</a><a class="btn btn-ghost" href="#contact" data-space="{e(p["name"])}">Inquire about this building</a></div>
      </div>
      <div class="rv d2">{media(p, 400 + i, "ph tall framed", big=True)}</div>
    </div>
  </section>
  <section class="facts-sec">
    <div class="wrap"><dl class="facts rv">{facts}</dl></div>
  </section>
  {gallery_html(p)}
  <section id="avail" class="spaces">
    <div class="wrap">
      <div class="sec-head rv"><p class="eyebrow">Availability</p><h2>Available at {e(p["name"])}</h2>{leased_note}</div>
      <div class="grid3">
        {cards}
      </div>
    </div>
  </section>
  <section class="portfolio light2">
    <div class="wrap">
      <div class="sec-head rv"><p class="eyebrow">More from our portfolio</p><h2>Other properties</h2></div>
      <div class="grid2 props">{others}</div>
    </div>
  </section>
  {contact_section(f"Interested in {p['name']}?", "Tell us the size and type of space you need and when you'd like to move in. We'll follow up with availability, floor plans and a time to tour.")}
</main>
'''
    title = f'{p["name"]}, {p["city"]}, {p["state"]} | {p["kind"]} Space for Lease | Ammori Group'
    desc = f'{p["kind"]} space for lease at {p["name"]}, {p["city"]}, {p["state"]}. {len(av)} space{"s" if len(av) != 1 else ""} available, leased directly by owner Ammori Group.'
    return head(title, desc, p["slug"] + ".html", [place_ld(p)]) + body + footer()

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(index())
    for i, p in enumerate(PROPERTIES):
        (OUT / f'{p["slug"]}.html').write_text(property_page(p, i))
    urls = [""] + [p["slug"] + ".html" for p in PROPERTIES]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n")
    fn = OUT / "netlify" / "functions"; fn.mkdir(parents=True, exist_ok=True)
    (fn / "chat.mjs").write_text(chat_function())
    (OUT / "package.json").write_text('{\n  "name": "ammori-group-site",\n  "private": true,\n  "type": "module",\n  "dependencies": {\n    "@anthropic-ai/sdk": "1.4.0"\n  }\n}\n')
    print("built", ", ".join(["index.html"] + [p["slug"] + ".html" for p in PROPERTIES]))

if __name__ == "__main__":
    build()
