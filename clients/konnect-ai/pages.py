#!/usr/bin/env python3
"""Builds konnectai.org sub-pages (sites/konnect-ai/*.html) and syncs the shared
header/footer into index.html. Run: python3 clients/konnect-ai/pages.py"""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parents[2] / "sites" / "konnect-ai"
BASE = "https://konnectai.org"
BOOK = "https://calendar.app.google/ZGPwJmMpcz3yWbkt5"
NAV = [("index.html#services", "Automation"), ("websites.html", "Websites"), ("index.html#industries", "Industries"), ("index.html#examples", "Examples"), ("index.html#faq", "FAQ")]

def head(title, desc, page):
    url = BASE + "/" + ("" if page == "index.html" else page)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B0C0F">
<meta name="color-scheme" content="light dark">
<meta name="format-detection" content="telephone=no">
<meta name="apple-mobile-web-app-title" content="Konnect AI">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Konnect AI">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"Konnect AI","url":"{BASE}/","description":"Custom AI automation systems and websites for businesses.","telephone":"+1-248-938-1582","email":"tristan@getkonnectai.com","founder":{{"@type":"Person","name":"Tristan Karim"}},"areaServed":"US"}}</script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <symbol id="logo" viewBox="-2 -2 104 104">
    <rect style="fill:currentColor" x="0" y="0" width="14.7" height="100"/>
    <polygon style="fill:currentColor" points="14.7,43 58.6,0 97.6,0 54.4,42 47.5,35 71,11.6 64.8,11.6 14.7,61"/>
    <polygon style="fill:currentColor" points="14.7,71 28.7,57 33,71 4,100 0,100 0,95"/>
    <polygon style="fill:currentColor" points="42.6,76 51.4,74 66.6,89 73,89 80,84 96,100 66.4,100"/>
    <line style="stroke:var(--accent)" x1="50" y1="58" x2="80" y2="45.5" stroke-width="7"/>
    <circle style="fill:var(--accent)" cx="85.5" cy="43" r="11"/>
    <line style="stroke:var(--red)" x1="44" y1="60" x2="77" y2="87" stroke-width="9"/>
    <circle style="fill:none;stroke:var(--bg);stroke-width:5" cx="44" cy="60" r="13"/>
    <circle style="fill:var(--red)" cx="44" cy="60" r="10.6"/>
  </symbol>
  <symbol id="check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="xmark" viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></symbol>
</defs></svg>
'''

def header(page):
    links = "".join(f'<li><a href="{h}"{" aria-current=page" if h == page else ""}>{l}</a></li>' for h, l in NAV)
    mlinks = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV) + '<a href="index.html#contact">Contact</a>'
    return f'''<header class="top" id="top-bar">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Konnect AI home"><svg class="logo" aria-hidden="true"><use href="#logo"/></svg>Konnect AI</a>
    <ul class="nav">{links}</ul>
    <a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Book a build call</a>
    <button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu">
      <svg class="b3" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
<nav class="menu" id="menu" hidden aria-label="Mobile">
  {mlinks}
  <a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Book a build call</a>
  <div class="meta"><a href="tel:+12489381582" style="font:inherit;border:0;padding:0">(248) 938-1582</a><span>tristan@getkonnectai.com</span></div>
</nav>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <a class="brand" href="index.html" style="font-size:15px"><svg class="logo" style="width:24px;height:24px" aria-hidden="true"><use href="#logo"/></svg>Konnect AI</a>
    <nav aria-label="Footer"><a href="index.html#services">Automation</a><a href="websites.html">Websites</a><a href="insurance-agencies.html">Insurance</a><a href="home-services.html">Home services</a><a href="local-businesses.html">Local businesses</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></nav>
    <span class="mono">tristan@getkonnectai.com · (248) 938-1582</span>
  </div>
</footer>

<script src="assets/site.js" defer></script>
<script src="assets/chat.js" defer></script>
</body>
</html>
'''

def hero(crumb, label, h1, lede, cta=True):
    btns = f'<div class="ctas rv d2"><a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Book a free build call <svg aria-hidden="true"><use href="#arrow"/></svg></a><a class="btn btn-ghost" href="#" data-open-chat>Ask our AI a question</a></div>' if cta else ""
    return f'''<section class="page-hero"><div class="wrap">
    <span class="crumbs rv"><a href="index.html">Home</a> / {crumb}</span>
    <span class="label rv">{label}</span>
    <h1 class="rv d1">{h1}</h1>
    <p class="rv d1">{lede}</p>{btns}
  </div></section>'''

def checks(items, icon="check"):
    return "".join(f'<li><svg aria-hidden="true"><use href="#{icon}"/></svg><span>{i}</span></li>' for i in items)

CTA = f'''<section class="cta"><div class="wrap"><div class="cta-box cta-split rv">
    <div class="cta-copy"><h2>Tell us the job. <span>We'll build it.</span></h2><p>A free call, a written plan and price, then we build it.</p></div>
    <div style="display:grid;gap:12px"><a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Book a free build call <svg aria-hidden="true"><use href="#arrow"/></svg></a><a class="btn btn-ghost" href="index.html#contact">Send us a message</a></div>
  </div></div></section>'''

PAGES = {}

# ---------- Websites ----------
PKGS = [
 ("Starter", False, "For businesses that need a professional site, fast.", ["One-page, mobile-first website", "Tap-to-call and a lead form that emails you", "Your services, hours, area and reviews", "Connected to your domain with the secure padlock", "Hosting and small text updates included"]),
 ("Growth", True, "For businesses that want the site to bring in work.", ["Everything in Starter", "Online booking button", "Extra pages for each main service", "Google Business Profile tune-up", "Monthly updates and lead-form checks"]),
 ("Website + AI", False, "Your site plus an AI system working behind it.", ["Everything in Growth", "AI chat or voice agent that answers 24/7", "Instant follow-up on every new lead", "Leads sent straight to your CRM or phone", "Built and supported by the same team"]),
]
pk = "".join(f'''<article class="pkg rv{" pop" if pop else ""}"><h3>{n}</h3><p class="for">{f}</p><p class="price">Custom quote</p><ul>{checks(items)}</ul><a class="btn {"btn-primary" if pop else "btn-ghost"}" href="{BOOK}" target="_blank" rel="noopener">Get a quote</a></article>''' for n, pop, f, items in PKGS)
PAGES["websites.html"] = ("Websites for Local Businesses | Konnect AI", "Mobile-first websites for local businesses with tap-to-call, lead forms, online booking, hosting and updates handled.", f'''
  {hero("Websites", "Websites", "Websites that make the <span>phone ring.</span>", "Most customers find a local business on their phone and call whoever looks most trustworthy. We build the site that wins that call, then keep it running.")}
  <section><div class="wrap">
    <div class="head rv"><span class="label">Packages</span><h2>Pick a starting point.</h2><p>Every site is designed for your business. You get a written price before any work starts.</p></div>
    <div class="pkgs">{pk}</div>
  </div></section>
  <section class="rule"><div class="wrap">
    <div class="head rv"><span class="label">What's included</span><h2>Built to bring in customers.</h2></div>
    <div class="promise">
      <div class="pr rv"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></svg><h3>Phone-first design</h3><p>Big buttons, fast loading and a call button that stays on screen.</p></div>
      <div class="pr rv d1"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 5h16v14H4z"/><path d="m4 7 8 6 8-6"/></svg><h3>Leads to your inbox</h3><p>Every form submission is emailed to you the moment it arrives.</p></div>
      <div class="pr rv d2"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><h3>Google-ready</h3><p>Clean structure and business details Google can read.</p></div>
      <div class="pr rv d3"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/></svg><h3>Hosting handled</h3><p>Secure hosting, the padlock and updates, all looked after.</p></div>
    </div>
  </div></section>
  <section><div class="wrap">
    <div class="head rv"><span class="label">How it works</span><h2>Live in days, not months.</h2></div>
    <ol class="steps" id="steps"><span class="bar" id="steps-bar" aria-hidden="true"></span>
      <li><span class="num">01</span><h3>Quick call</h3><p>We learn your business, services and customers.</p></li>
      <li><span class="num">02</span><h3>Short form</h3><p>You send your logo, photos and details in one 10-minute form.</p></li>
      <li><span class="num">03</span><h3>Preview</h3><p>You review a live preview and tell us what to change.</p></li>
      <li><span class="num">04</span><h3>Launch</h3><p>We connect your domain, test the form, and go live.</p></li>
    </ol>
  </div></section>
  <section class="rule"><div class="wrap">
    <div class="head rv"><span class="label">Questions</span><h2>Website FAQ.</h2></div>
    <div class="faq rv">
      <details><summary>Do I need to already have a domain?</summary><p>No. If you don't have one, we help you pick and set one up. If you do, we connect it without touching your email.</p></details>
      <details><summary>Who owns the website?</summary><p>You do. Your domain and content are yours, and the written plan spells out how the site files are handed over.</p></details>
      <details><summary>Can I make changes later?</summary><p>Yes. Send us what you want changed and we'll update it. Small text, price and hour updates are part of ongoing care.</p></details>
      <details><summary>Can you add AI to my website?</summary><p>Yes. We can add an AI assistant that answers questions and books appointments, like the one on this site.</p></details>
    </div>
  </div></section>
  {CTA}''')

# ---------- Industry pages ----------
def industry(slug, crumb, label, h1, lede, pains, gains, flow_title, flow, faqs):
    fl = "".join(f"<li>{s}</li>" for s in flow)
    fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    PAGES[slug] = (f"{crumb} | Konnect AI", lede, f'''
  {hero(crumb, label, h1, lede)}
  <section><div class="wrap">
    <div class="head rv"><span class="label">The difference</span><h2>Where the time goes, and where it could go.</h2></div>
    <div class="pain-gain">
      <div class="pain rv d1"><h3>Without automation</h3><ul>{checks(pains, "xmark")}</ul></div>
      <div class="gain rv d2"><h3>With a Konnect system</h3><ul>{checks(gains)}</ul></div>
    </div>
  </div></section>
  <section class="rule"><div class="wrap">
    <div class="head rv"><span class="label">Example build</span><h2>{flow_title}</h2><p>An example of a system we can build, step by step.</p></div>
    <div class="examples" style="grid-template-columns:1fr;max-width:640px"><article class="ex rv"><span class="mono who">example system</span><ol class="flow">{fl}</ol></article></div>
  </div></section>
  <section><div class="wrap">
    <div class="head rv"><span class="label">Questions</span><h2>Common questions.</h2></div>
    <div class="faq rv">{fq}</div>
  </div></section>
  {CTA}''')

industry("insurance-agencies.html", "Insurance Agencies", "AI automation for insurance agencies",
  "Quote faster. <span>Follow up every time.</span>",
  "Automation for independent insurance agencies: instant replies to quote requests, missing details collected for you, renewals and follow-ups that never slip.",
  ["Quote requests wait until someone is free", "Staff chase clients for missing details", "Renewals and cross-sell follow-ups slip", "Data is re-typed between forms, email and the agency system"],
  ["Every quote request gets a reply within minutes, day or night", "AI collects the missing details by text or email", "Renewal reminders and follow-ups go out on schedule", "Client details filed in your systems automatically"],
  "Quote requests answered while the office is closed",
  ["Quote form submitted at 9:40pm", "AI asks the missing questions by text", "Details filed in the agency system", "Agent gets a ready-to-quote summary", "Client booked for a morning call"],
  [("Will it work with our agency management system?", "We connect to the tools you already use. On the free call we look at your systems and confirm how the connection would work."), ("Does AI give insurance advice?", "No. The system collects information, answers general questions you approve, and books time with a licensed agent. Your agents give the advice."), ("Can it handle renewals?", "Yes. We can build reminders, renewal outreach and follow-up sequences around your book of business.")])

industry("home-services.html", "Home Services", "AI automation for home service companies",
  "Every missed call, <span>turned into a job.</span>",
  "For plumbers, HVAC, electricians, roofers and contractors: AI that answers when you can't, books jobs, and follows up on every estimate.",
  ["Calls go to voicemail while the crew is on a job", "Estimates go out and never get followed up", "Scheduling happens by phone tag", "Reviews only come in when customers remember"],
  ["An AI voice agent answers, gets the job details and books it", "Automatic estimate follow-ups by text and email", "Jobs land on your team calendar with the address", "Review requests sent after every completed job"],
  "Every missed call turned into a booked job",
  ["Call goes unanswered", "AI voice agent picks up", "Gets the job details and address", "Books the slot on the team calendar", "Sends a confirmation text"],
  [("Will callers know it's AI?", "We set it up to be clear and friendly. It handles the basics and passes anything complex to you."), ("Does it work with my scheduling software?", "Usually, yes. We connect to the calendars and job tools you already use."), ("Can you build my website too?", "Yes. We build websites for home service companies with tap-to-call and quote forms. See our websites page.")])

industry("local-businesses.html", "Local Businesses", "AI automation for local businesses",
  "Run the shop. <span>Let AI handle the rest.</span>",
  "For salons, spas, clinics, studios and shops: online booking, instant answers to common questions, reminders that cut no-shows, and a website that brings people in.",
  ["The phone rings with the same questions all day", "No-shows leave empty slots", "Booking only happens during business hours", "Your website doesn't bring in new customers"],
  ["An AI assistant answers common questions 24/7", "Automatic reminders before every appointment", "Customers book online any time", "A mobile-first website built to get calls and bookings"],
  "Questions answered and appointments booked after hours",
  ["Customer messages at 10pm asking about prices", "AI answers from your approved info", "Suggests an open time and books it", "Sends a reminder the day before", "Asks for a review after the visit"],
  [("Can it use my booking system?", "In most cases, yes. We connect to the booking tools you already use, or set one up for you."), ("What if a question is unusual?", "The assistant only answers from information you approve. Anything else is passed to you."), ("Do you build the website too?", "Yes. See our websites page for packages.")])

# ---------- Legal ----------
PAGES["privacy.html"] = ("Privacy Policy | Konnect AI", "How Konnect AI collects and uses information submitted through konnectai.org.", f'''
  {hero("Privacy", "Legal", "Privacy policy", "Last updated: November 17, 2026", cta=False)}
  <section><div class="wrap legal">
    <p>This policy explains what information Konnect AI ("we") collects through konnectai.org and how we use it.</p>
    <h2>Information we collect</h2>
    <ul><li><b>Information you send us:</b> your name, email, phone number and message when you use our contact or estimate forms.</li><li><b>Chat messages:</b> the messages you type into our AI assistant, so it can reply.</li><li><b>Booking details:</b> if you book a call, the scheduling tool collects the details you enter.</li><li><b>Basic technical data:</b> our hosting provider may log standard information such as IP address and browser type for security and reliability.</li></ul>
    <h2>How we use it</h2>
    <ul><li>To reply to your inquiry and provide our services.</li><li>To send you the information you asked for, such as an automation estimate.</li><li>To keep the website secure and working.</li></ul>
    <p>We do not sell your personal information.</p>
    <h2>Service providers</h2>
    <p>We use trusted providers to run the website: Netlify (hosting and form handling), Google (calendar booking), and Anthropic (the AI model behind our chat assistant). They process information on our behalf to provide these services.</p>
    <h2>Chat assistant</h2>
    <p>The AI assistant is automated and may make mistakes. Please don't share sensitive personal information, such as financial or health details, in the chat.</p>
    <h2>Your choices</h2>
    <p>You can ask us to access, correct or delete the information you've sent us by emailing tristan@getkonnectai.com.</p>
    <h2>Contact</h2>
    <p>Questions about this policy: tristan@getkonnectai.com or (248) 938-1582.</p>
    <p class="note-box">Template notice: this policy is a starting point. Have it reviewed for your business and location.</p>
  </div></section>''')

PAGES["terms.html"] = ("Terms of Use | Konnect AI", "Terms for using konnectai.org.", f'''
  {hero("Terms", "Legal", "Terms of use", "Last updated: November 17, 2026", cta=False)}
  <section><div class="wrap legal">
    <p>By using konnectai.org you agree to these terms.</p>
    <h2>Website content</h2>
    <p>Content on this site is for general information about Konnect AI's services. Examples, sample designs and the cost calculator are illustrations, not guarantees of results or savings.</p>
    <h2>AI assistant</h2>
    <p>The chat assistant is automated and may give incomplete or incorrect answers. It does not make offers, quotes or commitments on our behalf. Pricing and scope are agreed only in a written plan.</p>
    <h2>Services</h2>
    <p>Any project we take on is governed by a separate written agreement or plan. These terms do not create a client relationship.</p>
    <h2>Acceptable use</h2>
    <p>Don't misuse the site or the chat assistant, including attempts to disrupt it, send spam, or submit unlawful content.</p>
    <h2>Limitation of liability</h2>
    <p>The site is provided "as is". To the extent the law allows, Konnect AI isn't liable for damages arising from use of the site.</p>
    <h2>Contact</h2>
    <p>tristan@getkonnectai.com · (248) 938-1582</p>
    <p class="note-box">Template notice: these terms are a starting point. Have them reviewed for your business and location.</p>
  </div></section>''')

def build():
    for name, (title, desc, body) in PAGES.items():
        (OUT / name).write_text(head(title, desc, name) + header(name) + '\n<main id="top">' + body + '\n</main>\n\n' + FOOTER)
        print("built", name)
    # sync shared header/footer into the hand-built homepage
    idx = (OUT / "index.html").read_text()
    a = idx.index('<header class="top"'); b = idx.index('</nav>', idx.index('<nav class="menu"')) + 6
    idx = idx[:a] + header("index.html").rstrip() + idx[b:]
    a = idx.index('<footer>'); b = idx.index('</html>') + 7
    idx = idx[:a] + FOOTER.rstrip() + "\n"
    (OUT / "index.html").write_text(idx)
    print("synced index.html")
    urls = ["", *PAGES.keys()]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
