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
    <nav aria-label="Footer"><a href="index.html#services">Services</a><a href="reviews.html">Reviews</a><a href="index.html#industries">Industries</a><a href="index.html#contact">Contact</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></nav>
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

def industries_section():
    cards = "".join(f'<a class="ind rv d{(i % 3) + 1}" href="{slug}"><span class="mono" style="color:var(--ink-2)">{i + 1:02d}</span><h3>{crumb}</h3><p>{blurb}</p><span class="go">See how →</span></a>' for i, (slug, crumb, blurb) in enumerate(INDUSTRIES))
    return f"""  <section id="industries">
    <div class="wrap">
      <div class="head rv"><span class="label">Industries</span><h2>Built for how your industry works.</h2><p>Fifteen industries we build for. Pick yours to see what a Konnect system looks like.</p></div>
      <div class="inds">{cards}</div>
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
    for tag, html in (("INDUSTRIES", industries_section()), ("REVIEWS", reviews_strip())):
        a = idx.index(f"<!--{tag}-->") + len(f"<!--{tag}-->"); b = idx.index(f"<!--/{tag}-->")
        idx = idx[:a] + "\n" + html + "\n  " + idx[b:]
    (OUT / "index.html").write_text(idx)
    (OUT / "_redirects").write_text("/websites.html  /reviews.html  301\n/websites  /reviews.html  301\n")
    print("synced index.html, wrote _redirects")
    urls = ["", *PAGES.keys()]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    build()
