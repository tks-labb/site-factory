#!/usr/bin/env python3
"""Builds konnectai.org sub-pages (sites/konnect-ai/*.html) and syncs the shared
header/footer into index.html. Run: python3 clients/konnect-ai/pages.py"""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parents[2] / "sites" / "konnect-ai"
BASE = "https://konnectai.org"
BOOK = "https://calendar.app.google/ZGPwJmMpcz3yWbkt5"
NAV = [("index.html#services", "Services"), ("reviews.html", "Reviews"), ("index.html#industries", "Industries"), ("index.html#examples", "Examples"), ("index.html#faq", "FAQ")]

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
<script>/* logo intro: first visit, refresh, or logo click */(function(){{try{{var d=document.documentElement,s=sessionStorage,n=performance.getEntriesByType("navigation")[0],t=n&&n.type;if(!s.getItem("k_seen")||t==="reload"||s.getItem("k_logo")){{d.classList.add("intro")}}s.setItem("k_seen","1");s.removeItem("k_logo")}}catch(e){{}}}})()</script>
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

INTRO = """<div class="intro-ov" aria-hidden="true"><div class="intro-stage">
  <svg class="intro-logo" viewBox="-2 -2 104 104">
    <rect class="ip ip-stem" x="0" y="0" width="14.7" height="100"/>
    <polygon class="ip ip-arm" points="14.7,43 58.6,0 97.6,0 54.4,42 47.5,35 71,11.6 64.8,11.6 14.7,61"/>
    <polygon class="ip ip-low" points="14.7,71 28.7,57 33,71 4,100 0,100 0,95"/>
    <polygon class="ip ip-leg" points="42.6,76 51.4,74 66.6,89 73,89 80,84 96,100 66.4,100"/>
    <line class="ip ip-bl" x1="50" y1="58" x2="80" y2="45.5" pathLength="1"/>
    <circle class="ip ip-bn" cx="85.5" cy="43" r="11"/>
    <line class="ip ip-rl" x1="44" y1="60" x2="77" y2="87" pathLength="1"/>
    <circle class="ip ip-gap" cx="44" cy="60" r="13"/>
    <circle class="ip ip-rn" cx="44" cy="60" r="10.6"/>
    <circle class="ip ip-ring" cx="44" cy="60" r="10.6"/>
  </svg>
  <div class="intro-word">""" + "".join(f'<span style="--i:{i}">{"&nbsp;" if c == " " else c}</span>' for i, c in enumerate("Konnect AI")) + """</div>
</div><p class="intro-skip">Tap to skip</p></div>
"""

MENU_BTN = """<button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span class="mb"><i></i><i></i><i></i></span></button>"""

def header(page):
    links = "".join(f'<li><a href="{h}"{" aria-current=page" if h == page else ""}>{l}</a></li>' for h, l in NAV)
    mlinks = "".join(f'<a href="{h}" style="--i:{i}">{l}</a>' for i, (h, l) in enumerate(NAV + [("index.html#contact", "Contact")]))
    return f"""{INTRO}<header class="top" id="top-bar">
  <div class="wrap">
    <a class="brand" href="index.html" data-intro-link aria-label="Konnect AI home"><svg class="logo" aria-hidden="true"><use href="#logo"/></svg>Konnect AI</a>
    <ul class="nav">{links}</ul>
    <a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a build call</a>
    {MENU_BTN}
  </div>
</header>
<nav class="menu" id="menu" hidden aria-label="Mobile">
  {mlinks}
  <a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a free build call</a>
  <div class="meta"><a href="tel:+12489381582" style="font:inherit;border:0;padding:0">(248) 938-1582</a><span>tristan@getkonnectai.com</span></div>
</nav>
<div class="actionbar" id="actionbar"><a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a free call</a><button class="ab-chat" type="button" data-open-chat aria-label="Ask our AI"><span class="kc-dot" aria-hidden="true"></span>Ask AI</button></div>
"""

FOOTER = '''<footer>
  <div class="wrap">
    <a class="brand" href="index.html" style="font-size:15px"><svg class="logo" style="width:24px;height:24px" aria-hidden="true"><use href="#logo"/></svg>Konnect AI</a>
    <nav aria-label="Footer"><a href="index.html#services">Services</a><a href="reviews.html">Reviews</a><a href="index.html#industries">Industries</a><a href="index.html#contact">Contact</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></nav>
    <span class="mono">tristan@getkonnectai.com · (248) 938-1582</span>
  </div>
  <div class="wrap areas"><span class="mono">Service areas:</span> AREA_LINKS</div>
</footer>

<script src="assets/site.js" defer></script>
<script src="assets/chat.js" defer></script>
<script src="assets/builder.js" defer></script>
<script src="assets/motion.js" defer></script>
</body>
</html>
'''

def hero(crumb, label, h1, lede, cta=True):
    btns = f'<div class="ctas rv d2"><a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a free build call <svg aria-hidden="true"><use href="#arrow"/></svg></a><a class="btn btn-ghost" href="#" data-open-chat>Ask our AI a question</a></div>' if cta else ""
    return f'''<section class="page-hero"><div class="wrap">
    <span class="crumbs rv"><a href="index.html">Home</a> / {crumb}</span>
    <span class="label rv">{label}</span>
    <h1 class="rv d1">{h1}</h1>
    <p class="rv d1">{lede}</p>{btns}
  </div></section>'''

def checks(items, icon="check"):
    return "".join(f'<li><svg aria-hidden="true"><use href="#{icon}"/></svg><span>{i}</span></li>' for i in items)

CTA = f'''<section class="cta"><div class="wrap"><div class="cta-box cta-split rv">
    <div class="cta-copy"><h2>Tell us the job. <span>We'll build it.</span></h2><p>More clients, more time back, less busywork. A free call, a written plan and price, then we build it.</p></div>
    <div style="display:grid;gap:12px"><a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a free build call <svg aria-hidden="true"><use href="#arrow"/></svg></a><a class="btn btn-ghost" href="index.html#contact">Send us a message</a></div>
  </div></div></section>'''

PAGES = {}

# ---------- Reviews ----------
# Real client quotes, published with permission. Keep wording exactly as approved.
REVIEWS = [
 ("Marcus Bennett", "Insurance agency owner", "I like that my agents can open the CRM in the morning and see exactly who needs a call. We used to keep that list in three different places."),
 ("Dan Kowalski", "HVAC owner", "When I’m in an attic, I’m probably missing your call. Having a text go out asking what you need makes it a lot easier to pick things back up when I get to the truck."),
 ("Elena Morales", "Salon owner", "Clients message me at 10 p.m. asking if I have anything open Saturday. Now they can pick a time while they’re thinking about it, and I wake up to a booking."),
 ("Priya Shah", "Mortgage broker", "The detail I appreciate most is seeing the last conversation before I call someone back. I can pick up where we left off without asking them to repeat everything."),
 ("Lauren Mitchell", "Real estate agent", "I wanted the follow-up texts to sound like me. Konnect AI worked through the wording with me until it sounded like something I’d actually send."),
]
def initials(n): return "".join(w[0] for w in n.split()[:2])
def review_card(n, role, q, cls="rcard"):
    return f'<figure class="{cls}"><blockquote>“{q}”</blockquote><figcaption><span class="rav" aria-hidden="true">{initials(n)}</span><span><b>{n}</b><small>{role}</small></span></figcaption></figure>'

feat = REVIEWS[0]
rest = "".join(f'<div class="rv d{(i % 3) + 1}">{review_card(*r)}</div>' for i, r in enumerate(REVIEWS[1:]))
PAGES["reviews.html"] = ("Client Reviews | Konnect AI", "What insurance agents, HVAC owners, salon owners, mortgage brokers and real estate agents say about working with Konnect AI.", f"""
  {hero("Reviews", "Client reviews", "In their <span>own words.</span>", "Business owners on what changed after Konnect AI built their systems.")}
  <section><div class="wrap">
    <div class="rfeat rv">{review_card(*feat, cls="rcard big")}</div>
    <div class="rgrid">{rest}</div>
  </div></section>
  {CTA}""")

def reviews_strip():
    cards = "".join(review_card(*r) for r in REVIEWS)
    return f"""  <section id="reviews" class="rule">
    <div class="wrap">
      <div class="head rv"><span class="label">Reviews</span><h2>What our clients say.</h2></div>
    </div>
    <div class="rmarquee rv" aria-label="Client reviews"><div class="rtrack">{cards}<div class="rdup" aria-hidden="true">{cards}</div></div></div>
    <div class="wrap" style="margin-top:28px"><a class="btn btn-ghost rv" href="reviews.html">Read all reviews <svg aria-hidden="true"><use href="#arrow"/></svg></a></div>
  </section>"""

# ---------- Industry pages ----------
INDUSTRIES = []
def industry(slug, crumb, label, h1, lede, pains, gains, flow_title, flow, faqs, blurb):
    INDUSTRIES.append((slug, crumb, blurb))
    fl = "".join(f"<li>{x}</li>" for x in flow)
    fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    PAGES[slug] = (f"{crumb} | Konnect AI", lede, f"""
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
  {CTA}""")

CRM_Q = ("Will it work with the software we already use?", "Almost always. We connect to the CRMs, calendars, phones and industry tools you already use, and confirm the details on the free call.")
NOT_ADVICE = lambda who: ("Does the AI give professional advice?", f"No. It collects information, answers general questions you approve, and books time with {who}. The advice always comes from you.")

industry("insurance-agencies.html", "Insurance Agencies", "AI automation for insurance agencies", "Quote faster. <span>Follow up every time.</span>",
  "Instant replies to quote requests, missing details collected for you, and renewals and follow-ups that never slip.",
  ["Quote requests wait until someone is free", "Staff chase clients for missing details", "Renewals and cross-sell follow-ups slip", "Call lists live in several different places"],
  ["Every quote request gets a reply within minutes", "AI collects missing details by text or email", "Renewal reminders go out on schedule", "One CRM view of exactly who needs a call today"],
  "Quote requests answered while the office is closed",
  ["Quote form submitted at 9:40pm", "AI asks the missing questions by text", "Details filed in the agency system", "Agent gets a ready-to-quote summary", "Client booked for a morning call"],
  [CRM_Q, NOT_ADVICE("a licensed agent"), ("Can it handle renewals?", "Yes. We build reminders, renewal outreach and follow-up sequences around your book of business.")],
  "Quote replies, renewals and a clean daily call list.")
industry("home-services.html", "HVAC, Plumbing & Electrical", "AI automation for home service companies", "Every missed call, <span>turned into a job.</span>",
  "AI that texts back when you're on a job, books the work, and follows up on every estimate.",
  ["Calls go to voicemail while you're on a job", "Estimates go out and never get followed up", "Scheduling happens by phone tag", "Reviews only come in when customers remember"],
  ["Missed callers get a text asking what they need", "Automatic estimate follow-ups", "Jobs land on the team calendar with the address", "Review requests after every completed job"],
  "Every missed call turned into a booked job",
  ["Call goes unanswered", "Text goes out asking what they need", "Customer replies with the job details", "Job booked on the team calendar", "Confirmation text sent"],
  [("Will callers know it's automated?", "We make it clear and friendly. It handles the basics and passes anything complex to you."), CRM_Q, ("Can it ask for reviews?", "Yes. A review request can go out automatically after each completed job.")],
  "Missed-call text back, booking and estimate follow-up.")
industry("local-businesses.html", "Salons & Spas", "AI automation for salons and spas", "Bookings while <span>you sleep.</span>",
  "Clients book any time, common questions get answered instantly, and reminders cut no-shows.",
  ["Clients message after hours and wait until morning", "The same questions all day: prices, openings, parking", "No-shows leave empty chairs", "Rebooking depends on remembering to ask"],
  ["Clients pick an open time the moment they ask", "Instant answers from your approved info", "Reminders before every appointment", "Automatic rebooking nudges"],
  "A 10pm message turned into a Saturday booking",
  ["Client messages at 10pm about Saturday", "AI shows the open times", "Client picks a slot and books", "Reminder sent the day before", "Review request after the visit"],
  [("Does it work with my booking app?", "In most cases, yes. We connect to the booking tool you already use or set one up."), ("What if a question is unusual?", "It only answers from information you approve and passes anything else to you."), ("Can you build my website too?", "Yes. We build mobile-first sites with online booking.")],
  "After-hours booking, reminders and fewer no-shows.")
industry("mortgage-brokers.html", "Mortgage Brokers", "AI automation for mortgage brokers", "Pick up right <span>where you left off.</span>",
  "Every lead answered fast, documents collected automatically, and the full conversation in front of you before every call.",
  ["Leads go cold while you're in closings", "Chasing borrowers for documents by email", "Asking clients to repeat what they told you last time", "Rate updates and check-ins fall through"],
  ["Instant first reply to every new lead", "Automatic document checklists and reminders", "Last conversation summarized before each callback", "Scheduled check-ins with past and future clients"],
  "A new lead to a ready-to-review file",
  ["Lead fills out the pre-qual form", "AI replies and books a call", "Document checklist sent automatically", "Reminders until every document arrives", "You get a summary before the call"],
  [CRM_Q, NOT_ADVICE("a licensed loan officer"), ("Can it send document reminders?", "Yes. It tracks what's missing and sends polite reminders until the file is complete.")],
  "Fast lead replies, document chasing and call prep.")
industry("real-estate.html", "Real Estate Agents", "AI automation for real estate agents", "Follow-up that <span>sounds like you.</span>",
  "Every lead gets a quick, personal reply, showings get booked, and follow-ups go out in your own voice.",
  ["Online leads wait hours for a reply", "Follow-up texts feel generic or never get sent", "Showing requests bounce between texts and email", "Past clients hear from you once a year"],
  ["A fast reply to every lead, day or night", "Follow-up texts written in your voice", "Showings booked straight onto your calendar", "Regular check-ins with your sphere"],
  "A portal lead to a booked showing",
  ["Lead asks about a listing at 8pm", "AI replies in your voice", "Asks about timeline and budget", "Books a showing on your calendar", "Follow-up sequence starts automatically"],
  [("Will texts sound like a robot?", "No. We work through the wording with you until it sounds like something you'd actually send."), CRM_Q, ("Can it work with lead portals?", "Usually, yes. We connect lead sources so every lead lands in one place.")],
  "Instant lead replies and follow-ups in your voice.")
industry("contractors.html", "Roofing & Contractors", "AI automation for roofers and contractors", "More estimates <span>signed.</span>",
  "Leads answered fast, inspections booked, and every estimate followed up until you get a yes or no.",
  ["Storm-season leads pile up faster than you can call", "Estimates sit without follow-up", "Job photos and notes scattered across phones", "Crews and customers out of sync on schedules"],
  ["Every lead answered and qualified quickly", "Estimate follow-ups on autopilot", "Job details organized in one place", "Automatic schedule updates to customers"],
  "A roof leak call to a booked inspection",
  ["Homeowner submits a leak request", "AI asks for photos and address", "Inspection booked on the calendar", "Estimate sent after the visit", "Follow-ups until they decide"],
  [CRM_Q, ("Can it handle storm-season volume?", "Yes. Automation answers every lead the same way whether you get five or five hundred."), ("Can customers get schedule updates?", "Yes. Customers can get automatic texts when crews are scheduled or running late.")],
  "Lead intake, inspections and estimate follow-up.")
industry("auto-repair.html", "Auto Repair Shops", "AI automation for auto repair shops", "Keep the bays <span>full.</span>",
  "Appointment requests handled automatically, customers updated on their car, and maintenance reminders that bring them back.",
  ["The front desk spends all day on the phone", "Customers call asking 'is my car ready?'", "Repair approvals wait on callbacks", "Customers forget their next service"],
  ["Online appointment requests and booking", "Automatic status texts while the car is in", "Quick repair approvals by text", "Maintenance reminders that bring cars back"],
  "A service request to a car back on the road",
  ["Customer requests an oil change online", "AI books a time", "Status text when the car is in the bay", "Approval request for extra work", "Pickup text when it's ready"],
  [CRM_Q, ("Can customers approve repairs by text?", "Yes. We can send the estimate by text and record their approval."), ("Do reminders really bring people back?", "Reminders make it easy for customers to book their next service instead of forgetting.")],
  "Booking, status texts and service reminders.")
industry("dental-medical.html", "Dental & Medical Offices", "AI automation for dental and medical offices", "Fewer calls. <span>Fuller schedules.</span>",
  "Appointment requests, reminders and common questions handled automatically, so your front desk can focus on patients.",
  ["Phones ring nonstop during patient check-in", "No-shows and late cancellations", "The same questions about hours, insurance and directions", "Recall reminders go out late or not at all"],
  ["Online appointment requests any time", "Automatic reminders and confirmations", "Instant answers to general questions", "Recall reminders on schedule"],
  "An appointment request to a confirmed visit",
  ["Patient requests an appointment online", "AI offers open times", "Visit confirmed and added to the schedule", "Reminder the day before", "Recall reminder months later"],
  [("What about patient privacy?", "We discuss your privacy and compliance requirements on the free call and design the system around them before anything is built."), CRM_Q, ("Does it give medical advice?", "No. It handles scheduling and general questions you approve. Clinical questions go to your team.")],
  "Scheduling, reminders and recall outreach.")
industry("law-firms.html", "Law Firms", "AI automation for law firms", "Faster intake. <span>Fewer lost leads.</span>",
  "Potential clients get a quick response, intake details are collected for you, and consultations get booked.",
  ["Potential clients call other firms when you don't pick up", "Intake details are collected over several calls", "Consultation scheduling takes back-and-forth", "Document requests get lost in email"],
  ["A fast response to every inquiry", "Structured intake questions collected automatically", "Consultations booked straight onto calendars", "Automatic document request reminders"],
  "A website inquiry to a booked consultation",
  ["Inquiry comes in after hours", "AI collects the intake details", "Conflict-check info passed to staff", "Consultation booked", "Document checklist sent"],
  [NOT_ADVICE("an attorney"), CRM_Q, ("Who reviews the intake?", "Your team does. The system collects and organizes the details so staff can review them quickly.")],
  "Client intake, scheduling and document requests.")
industry("accounting.html", "Accounting & Tax Firms", "AI automation for accounting and tax firms", "Tax season, <span>organized.</span>",
  "Documents collected and sorted automatically, clients reminded about deadlines, and fewer status emails.",
  ["Client documents arrive in every format", "Staff chase missing items for weeks", "Clients email asking for status updates", "Deadline reminders depend on someone remembering"],
  ["Documents read, labeled and filed automatically", "Missing items requested automatically", "Status updates sent without staff time", "Deadline reminders on schedule"],
  "A stack of PDFs to one clean file",
  ["Client emails a stack of PDFs", "AI reads and labels each one", "Numbers pulled into a spreadsheet", "Missing items requested automatically", "Accountant reviews one clean file"],
  [CRM_Q, NOT_ADVICE("your accountants"), ("Can it handle tax season volume?", "Yes. It processes documents the same way whether it's ten clients or a thousand.")],
  "Document collection, sorting and deadline reminders.")
industry("restaurants.html", "Restaurants", "AI automation for restaurants", "Answer every guest, <span>even mid-rush.</span>",
  "Reservations, catering inquiries and common questions handled automatically while your staff focus on the floor.",
  ["Phones ring during the dinner rush", "Catering and event inquiries slip through", "The same questions about hours, menu and parking", "Happy guests rarely leave reviews"],
  ["Reservations and waitlist handled automatically", "Every catering inquiry captured and followed up", "Instant answers to common questions", "Review requests after visits"],
  "A catering inquiry to a booked event",
  ["Guest asks about catering for 40", "AI collects the date, headcount and menu", "Manager gets a summary", "Quote sent and followed up", "Event confirmed"],
  [CRM_Q, ("Can it take reservations?", "Yes. It can work with your reservation system or a simple booking setup."), ("Will it answer menu questions?", "Yes, from the menu and info you approve.")],
  "Reservations, catering leads and guest questions.")
industry("fitness.html", "Gyms & Fitness Studios", "AI automation for gyms and fitness studios", "Turn interest into <span>members.</span>",
  "Trial sign-ups followed up instantly, classes booked automatically, and members nudged before they drift away.",
  ["Trial leads go cold before anyone follows up", "Class booking questions flood the front desk", "Members stop coming without anyone noticing", "Renewals depend on manual reminders"],
  ["Instant follow-up on every trial sign-up", "Class booking and reminders handled automatically", "Check-ins for members who stop showing up", "Renewal reminders on schedule"],
  "A free-trial sign-up to a new member",
  ["Visitor signs up for a free class", "AI confirms and sends a reminder", "Follow-up after the first class", "Membership offer sent", "Welcome sequence starts"],
  [CRM_Q, ("Can it spot members who stop coming?", "Yes. Based on check-in data, it can send a friendly nudge to members who haven't been in for a while."), ("Can it book classes?", "Yes. It connects to your scheduling software or sets up booking.")],
  "Trial follow-up, class booking and member check-ins.")
industry("cleaning.html", "Cleaning Services", "AI automation for cleaning companies", "Quotes out <span>in minutes.</span>",
  "Instant quote requests, recurring bookings handled automatically, and reminders that keep customers on schedule.",
  ["Quote requests wait until evening", "Recurring schedules managed by hand", "Last-minute changes cause confusion", "Customers drift after one clean"],
  ["Instant quote replies with the right questions", "Recurring bookings managed automatically", "Change requests handled by text", "Rebooking reminders after every clean"],
  "A quote request to a recurring customer",
  ["Customer requests a quote", "AI asks size, rooms and frequency", "Quote sent and booked", "Reminder before each visit", "Rebooking offer after the clean"],
  [CRM_Q, ("Can it handle recurring bookings?", "Yes. Weekly, biweekly and monthly schedules can run automatically with reminders."), ("Can customers reschedule by text?", "Yes, within the rules you set.")],
  "Instant quotes, recurring bookings and reminders.")
industry("property-management.html", "Property Management", "AI automation for property managers", "Requests handled. <span>Tenants informed.</span>",
  "Maintenance requests collected and routed, tenant questions answered, and leasing inquiries followed up.",
  ["Maintenance requests come by call, text and email", "Tenants call asking for status updates", "Leasing inquiries wait for a callback", "Renewals and notices tracked by hand"],
  ["Maintenance requests collected with photos and routed", "Automatic status updates to tenants", "Instant replies to leasing inquiries", "Renewal and notice reminders on schedule"],
  "A maintenance request to a closed work order",
  ["Tenant reports a leak by text", "AI asks for photos and details", "Work order sent to the right vendor", "Tenant gets status updates", "Request closed and logged"],
  [CRM_Q, ("Can it route requests to vendors?", "Yes. Requests can be routed by type, property or urgency."), ("Can it handle leasing inquiries?", "Yes. It answers common questions and books showings.")],
  "Maintenance requests, tenant updates and leasing.")
industry("retail.html", "Retail & E-commerce", "AI automation for retail and e-commerce", "Answers in seconds. <span>Orders on track.</span>",
  "Customer questions answered instantly, order updates sent automatically, and repeat customers brought back.",
  ["The same order-status questions all day", "Product questions go unanswered after hours", "Returns and exchanges handled by email", "One-time buyers never come back"],
  ["Instant answers about orders and products", "Automatic order and shipping updates", "Simple return and exchange flows", "Follow-ups that bring customers back"],
  "A customer question to a repeat purchase",
  ["Customer asks where their order is", "AI looks up the status and replies", "Delivery confirmation sent", "Review request after delivery", "Personal offer for the next order"],
  [CRM_Q, ("Does it work with my online store?", "Usually, yes. We connect to common store platforms and order systems."), ("Can it handle returns?", "Yes. It can walk customers through returns using the rules you set.")],
  "Order updates, product answers and repeat sales.")

IND_CAT = {"insurance-agencies.html": "pro", "mortgage-brokers.html": "pro", "real-estate.html": "pro", "law-firms.html": "pro", "accounting.html": "pro", "dental-medical.html": "pro",
  "home-services.html": "home", "contractors.html": "home", "auto-repair.html": "home", "cleaning.html": "home", "property-management.html": "home",
  "local-businesses.html": "local", "restaurants.html": "local", "fitness.html": "local", "retail.html": "local"}
CAT_NAMES = [("all", "All"), ("pro", "Professional & health"), ("home", "Home & trades"), ("local", "Local & retail")]

def industries_section():
    counts = {k: sum(1 for v in IND_CAT.values() if v == k) for k, _ in CAT_NAMES}; counts["all"] = len(INDUSTRIES)
    tabs = "".join(f'<button type="button" class="ftab" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n} <small>{counts[k]}</small></button>' for k, n in CAT_NAMES)
    cards = "".join(f'<a class="ind" data-cat="{IND_CAT.get(slug, "pro")}" href="{slug}" style="--i:{i}"><span class="mono" style="color:var(--ink-2)">{i + 1:02d}</span><h3>{crumb}</h3><p>{blurb}</p><span class="go">See how <span class="arr">→</span></span></a>' for i, (slug, crumb, blurb) in enumerate(INDUSTRIES))
    return f"""  <section id="industries">
    <div class="wrap">
      <div class="head rv"><span class="label">Industries</span><h2>Built for how your industry works.</h2><p>Fifteen industries we build for. Pick a group, then yours.</p></div>
      <div class="ftabs rv" role="group" aria-label="Filter industries">{tabs}</div>
      <div class="inds stg rv" id="ind-grid">{cards}</div>
    </div>
  </section>"""

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


# ---------- Build-your-system tool ----------
SB_IN = [("form", "Web form", "your web form"), ("phone", "Phone calls", "phone"), ("email", "Email", "email"), ("text", "Text messages", "text"), ("chat", "Website chat", "website chat"), ("social", "Social DMs", "social media messages")]
SB_AI = [("qualify", "Qualify leads", "qualifies the lead"), ("answer", "Answer questions", "answers questions"), ("collect", "Collect details", "collects the missing details"), ("docs", "Read documents", "reads the documents")]
SB_OUT = [("crm", "Update CRM", "updates your CRM"), ("book", "Book meeting", "books a meeting"), ("alert", "Alert team", "alerts your team"), ("follow", "Send follow-up", "sends a follow-up"), ("report", "Daily report", "adds it to a daily report"), ("review", "Ask for review", "asks for a review")]

def chips(group, items):
    return "".join(f'<button type="button" class="sb-chip" data-g="{group}" data-k="{k}" data-say="{say}" aria-pressed="false">{label}</button>' for k, label, say in items)

def builder_html(preset, title="Design your system in 10 seconds.", intro="Pick where work comes in and what should happen next. Watch the system wire itself up, then get a free plan for building it.", form_extra=""):
    import json as _j
    return f"""  <section id="build-yours" class="sb-sec">
    <div class="wrap">
      <div class="head rv"><span class="label">Build your system</span><h2>{title}</h2><p>{intro}</p></div>
      <div class="sb rv" data-preset='{_j.dumps(preset)}'>
        <div class="sb-stage">
          <svg class="sb-wires" aria-hidden="true"></svg>
          <div class="sb-col in"><h3>Work comes in by</h3>{chips("in", SB_IN)}</div>
          <div class="sb-core"><b><i aria-hidden="true"></i>AI agent</b>{chips("ai", SB_AI)}</div>
          <div class="sb-col out"><h3>Then it</h3>{chips("out", SB_OUT)}</div>
        </div>
        <div class="sb-out">
          <div class="sb-summary-box" aria-live="polite"><span class="mono" style="color:var(--night-dim)">Your system</span><p class="sb-summary"></p></div>
          <form class="sb-form" name="system-plan" method="POST" data-netlify="true" netlify-honeypot="sb-website" novalidate>
            <input type="hidden" name="form-name" value="system-plan">
            <p hidden><label>Leave this empty <input name="sb-website"></label></p>
            <input type="hidden" name="system"><input type="hidden" name="inputs"><input type="hidden" name="ai_tasks"><input type="hidden" name="outcomes">{form_extra}
            <label for="sb-email-{id(preset)}" style="font-weight:600">Get a free plan for this system</label>
            <div class="r"><input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name"><input id="sb-email-{id(preset)}" name="email" type="email" placeholder="you@company.com" autocomplete="email" required></div>
            <button type="submit">Send me this plan</button>
            <p class="sb-err" hidden></p>
          </form>
          <div class="sb-sent" hidden><strong class="mono">Plan requested</strong><p>Thanks. Tristan will email you a plan for this system.</p></div>
        </div>
      </div>
    </div>
  </section>"""

# ---------- Founder block (photo/video appear when files are added) ----------
def founder_html():
    assets = OUT / "assets"
    photo = next((f for f in ("tristan.jpg", "tristan.jpeg", "tristan.png", "tristan.webp") if (assets / f).exists()), None)
    video = "tristan.mp4" if (assets / "tristan.mp4").exists() else None
    av = f'<img class="fphoto" src="assets/{photo}" alt="Tristan Karim, founder of Konnect AI" width="96" height="96">' if photo else '<span class="av">TK</span>'
    vid = f'<video class="fvideo" controls playsinline preload="metadata"{f" poster=assets/{photo}" if photo else ""}><source src="assets/{video}" type="video/mp4"></video>' if video else ""
    return f"""<div class="founder rv{" has-video" if video else ""}">{av}<div><b>Tristan Karim, founder</b><p>Every Konnect AI project starts with a conversation with me. Book a call, tell me what's taking your team's time, and I'll show you how we'd automate it.</p></div>{vid}</div>"""

# ---------- City pages ----------
CITIES = [
 ("troy", "Troy", "From the offices along Big Beaver Road to family-run shops, Troy businesses run on fast responses. We build AI systems and websites that answer leads, book appointments and keep follow-ups on schedule.", ["insurance-agencies.html", "mortgage-brokers.html", "accounting.html", "dental-medical.html"]),
 ("detroit", "Detroit", "Detroit's small businesses and contractors are busy doing the work. We build systems that answer calls you miss, follow up on every estimate and keep your calendar full.", ["home-services.html", "contractors.html", "restaurants.html", "property-management.html"]),
 ("ann-arbor", "Ann Arbor", "Ann Arbor's professional firms, clinics and local shops serve customers who expect quick answers. We build AI assistants and automations that respond right away and keep everything organized.", ["dental-medical.html", "law-firms.html", "fitness.html", "retail.html"]),
 ("southfield", "Southfield", "Southfield is full of offices and service firms juggling calls, documents and follow-ups. We build automation that collects documents, routes requests and keeps clients updated.", ["insurance-agencies.html", "law-firms.html", "accounting.html", "mortgage-brokers.html"]),
 ("royal-oak", "Royal Oak", "Royal Oak's restaurants, salons and shops get questions at all hours. We build assistants that answer, take bookings and bring customers back.", ["local-businesses.html", "restaurants.html", "fitness.html", "retail.html"]),
 ("farmington-hills", "Farmington Hills", "Farmington Hills service businesses and professional offices lose time to phone tag and manual data entry. We build systems that answer, schedule and file the details for you.", ["home-services.html", "dental-medical.html", "real-estate.html", "cleaning.html"]),
 ("sterling-heights", "Sterling Heights", "Sterling Heights contractors, auto shops and home service companies are on the job all day. We build systems that catch every lead and keep customers updated.", ["auto-repair.html", "contractors.html", "home-services.html", "cleaning.html"]),
 ("novi", "Novi", "Novi businesses, from retail to real estate and medical offices, need follow-up that never slips. We build automations that respond fast and keep your pipeline organized.", ["real-estate.html", "retail.html", "dental-medical.html", "mortgage-brokers.html"]),
]
def area_links(): return " · ".join(f'<a href="ai-automation-{slug}-mi.html">{name}</a>' for slug, name, *_ in CITIES)

def city_pages():
    names = {s: c for s, c, _ in INDUSTRIES}
    for slug, name, intro, inds in CITIES:
        cards = "".join(f'<a class="ind rv d{(i % 3) + 1}" href="{u}"><h3>{names.get(u, u)}</h3><span class="go">See how →</span></a>' for i, u in enumerate(inds))
        PAGES[f"ai-automation-{slug}-mi.html"] = (f"AI Automation & Websites in {name}, MI | Konnect AI", f"Custom AI automation systems and websites for {name}, Michigan businesses. Lead follow-up, AI chat and voice agents, booking and more.", f"""
  {hero(f"{name}, MI", f"Serving {name}, Michigan", f"AI automation in <span>{name}.</span>", intro)}
  <section><div class="wrap">
    <div class="head rv"><span class="label">What we build</span><h2>Systems for {name} businesses.</h2></div>
    <div class="promise">
      <div class="pr rv"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 5h16v10H8l-4 4z"/></svg><h3>AI chat &amp; voice agents</h3><p>Answer customers day and night in your business's voice.</p></div>
      <div class="pr rv d1"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M3 19c.8-3.2 3.2-5 6-5s5.2 1.8 6 5"/></svg><h3>Lead follow-up</h3><p>Every new lead gets a fast reply and lands in your CRM.</p></div>
      <div class="pr rv d2"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M7 3h7l4 4v14H7z"/></svg><h3>Document processing</h3><p>Forms, PDFs and emails read and filed automatically.</p></div>
      <div class="pr rv d3"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3"/></svg><h3>Websites</h3><p>Mobile-first sites with tap-to-call, booking and lead forms.</p></div>
    </div>
  </div></section>
  <section class="rule"><div class="wrap">
    <div class="head rv"><span class="label">Popular in {name}</span><h2>Industries we build for.</h2></div>
    <div class="inds">{cards}</div>
    <p class="ex-note mono"><a href="index.html#industries">See all 15 industries →</a></p>
  </div></section>
  {reviews_strip()}
  {CTA}""")

# ---------- Prospect pages (konnectai.org/for/<slug>/) ----------
PROSPECT_DIR = pathlib.Path(__file__).resolve().parent / "prospects"
def calc_html(hours, people, rate):
    return f"""  <section id="calculator" class="calc-sec"><div class="wrap">
      <div class="head rv"><span class="label">Cost calculator</span><h2>What manual work costs you today.</h2><p>We filled this in with a typical estimate. Move the sliders to match your team.</p></div>
      <div class="calc">
        <div class="inputs rv d1">
          <div class="rng"><div class="row"><label for="c-hours">Hours per week on the task</label><output id="o-hours">{hours}</output></div><input id="c-hours" type="range" min="1" max="60" value="{hours}"></div>
          <div class="rng"><div class="row"><label for="c-people">People doing it</label><output id="o-people">{people}</output></div><input id="c-people" type="range" min="1" max="20" value="{people}"></div>
          <div class="rng"><div class="row"><label for="c-rate">Cost per hour (pay + overhead)</label><output id="o-rate">${rate}</output></div><input id="c-rate" type="range" min="15" max="150" step="5" value="{rate}"></div>
        </div>
        <div class="result rv d2" aria-live="polite"><span class="mono" style="color:var(--night-dim)">Yearly cost of doing it by hand</span><span class="big" id="r-cost">$0</span><div class="meter"><i id="r-meter"></i></div><span class="hours" id="r-hours"></span><span class="fine">An estimate based on the inputs above and 52 working weeks.</span></div>
      </div>
    </div></section>"""

def prospect_pages():
    import json
    built = []
    if not PROSPECT_DIR.exists(): return built
    for f in sorted(PROSPECT_DIR.glob("*.json")):
        if f.name.startswith("_"): continue
        d = json.loads(f.read_text()); slug = f.stem
        first, biz = d["first_name"], d["business"]
        ind = next((x for x in INDUSTRIES if x[0] == d.get("industry")), None)
        note = d.get("note", "")
        body = f"""
  <section class="page-hero"><div class="wrap">
    <span class="label rv">Prepared for {biz}</span>
    <h1 class="rv d1">Hi {first}. Here's what we'd build for <span>{biz}.</span></h1>
    <p class="rv d1">{note or "A quick look at how a Konnect AI system could take repetitive work off your team's plate. Nothing here is set in stone; it's a starting point for a conversation."}</p>
    <div class="ctas rv d2"><a class="btn btn-primary btn-hero" href="{BOOK}" target="_blank" rel="noopener">Book a 20-minute call <svg aria-hidden="true"><use href="#arrow"/></svg></a><a class="btn btn-ghost" href="#" data-open-chat>Ask our AI a question</a></div>
  </div></section>
{builder_html(d.get("system", {}), title=f"Your system, {first}.", intro="We picked a starting setup based on businesses like yours. Tap anything to change it.", form_extra=f'<input type="hidden" name="prospect" value="{biz}">')}
{calc_html(d.get("hours", 10), d.get("people", 2), d.get("rate", 35))}
  {f'<section class="rule"><div class="wrap"><div class="head rv"><span class="label">For {ind[1].lower()}</span><h2>More on how this works in your industry.</h2></div><a class="btn btn-ghost rv" href="{ind[0]}">See how it works for {ind[1].lower()} <svg aria-hidden="true"><use href="#arrow"/></svg></a></div></section>' if ind else ""}
{reviews_strip()}
  {CTA}"""
        title = f"For {biz} | Konnect AI"
        html = head(title, f"What Konnect AI would build for {biz}.", "index.html").replace('<meta name="theme-color"', '<base href="/">\n<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color"', 1)
        out = OUT / "for" / slug; out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(html + header("") + '\n<main id="top">' + body + '\n</main>\n\n' + FOOTER.replace("AREA_LINKS", area_links()))
        built.append(slug)
    return built

def build():
    city_pages()
    footer = FOOTER.replace("AREA_LINKS", area_links())
    for name, (title, desc, body) in PAGES.items():
        (OUT / name).write_text(head(title, desc, name) + header(name) + '\n<main id="top">' + body + '\n</main>\n\n' + footer)
        print("built", name)
    # sync shared header/footer into the hand-built homepage
    idx = (OUT / "index.html").read_text()
    a = idx.find('<div class="intro-ov"'); a = a if a > -1 else idx.index('<header class="top"')
    b = idx.index('</nav>', idx.index('<nav class="menu"')) + 6
    ab = idx.find('<div class="actionbar"', b)
    if ab > -1 and ab - b < 10: b = idx.index('</div>', idx.index('</button>', ab)) + 6
    idx = idx[:a] + header("index.html").rstrip() + idx[b:]
    a = idx.index('<footer>'); b = idx.index('</html>') + 7
    idx = idx[:a] + footer.rstrip() + "\n"
    (OUT / "index.html").write_text(idx)
    for tag, html in (("INDUSTRIES", industries_section()), ("REVIEWS", reviews_strip()), ("BUILDER", builder_html({"in": ["form", "phone"], "ai": ["qualify"], "out": ["crm", "book"]})), ("FOUNDER", founder_html())):
        a = idx.index(f"<!--{tag}-->") + len(f"<!--{tag}-->"); b = idx.index(f"<!--/{tag}-->")
        idx = idx[:a] + "\n" + html + "\n  " + idx[b:]
    (OUT / "index.html").write_text(idx)
    (OUT / "_redirects").write_text("/websites.html  /reviews.html  301\n/websites  /reviews.html  301\n")
    print("synced index.html, wrote _redirects")
    urls = ["", *PAGES.keys()]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")
    print("prospect pages:", ", ".join(prospect_pages()) or "none")

if __name__ == "__main__":
    build()
