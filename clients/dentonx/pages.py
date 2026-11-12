#!/usr/bin/env python3
"""Builds the DentonX demo pages in sites/dentonx/.
Shared head, header and footer live here; page bodies are below.
Run: python3 clients/dentonx/pages.py
"""
import re, pathlib
OUT = pathlib.Path(__file__).resolve().parents[2] / "sites" / "dentonx"
PHONE, PHONE_TEL = "+1 (925) 220-2187", "+19252202187"
BASE = "https://dentonx.konnectai.org"
EDGAR = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=0002093375&amp;owner=include"

NAV = [("platform.html", "Platform"), ("solutions.html", "Solutions"), ("index.html#market", "Market"), ("company.html", "Company"), ("investors.html", "Investors")]

def head(title, desc, page):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#121A2A">
<meta name="color-scheme" content="dark light">
<meta name="apple-mobile-web-app-title" content="DentonX">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DentonX">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}/{"" if page == "index.html" else page}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta name="twitter:image" content="{BASE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Unbounded:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"DentonX Inc.","description":"Data infrastructure, workflow automation and analytics for non-bank lending partners.","telephone":"+1-925-220-2187","address":{{"@type":"PostalAddress","streetAddress":"1999 Harrison Street, Suite 1800","addressLocality":"Oakland","addressRegion":"CA","postalCode":"94612","addressCountry":"US"}}}}</script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <symbol id="arr" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="ok" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m7.5 12.5 3 3 6-6.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="no" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
  <symbol id="doc" viewBox="0 0 24 24"><path d="M7 3h7l4 4v14H7z M14 3v4h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
</defs></svg>
'''

def header(page):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{l}</a>' for h, l in NAV)
    mlinks = "".join(f'<a href="{h}">{l}</a>' for h, l in [("index.html", "Home")] + NAV)
    return f'''<header class="top" id="top-bar">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="DentonX home">Denton<em>X</em></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn" href="contact.html">Get started</a>
    <button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu">
      <svg class="bars3" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
<nav class="menu" id="menu" hidden aria-label="Mobile">
  {mlinks}
  <a class="btn" href="contact.html">Get started</a>
  <div class="menu-meta"><a href="tel:{PHONE_TEL}">{PHONE}</a><span>Oakland · New York · Las Vegas</span></div>
</nav>
'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="fl"><a class="logo" href="index.html" style="color:var(--night-ink)">Denton<em>X</em></a>
      <nav class="fnav" aria-label="Footer"><a href="platform.html">Platform</a><a href="solutions.html">Solutions</a><a href="company.html">Company</a><a href="investors.html">Investors</a><a href="contact.html">Contact</a></nav></div>
    <div class="fl"><span>© 2026 DentonX Inc.</span><span>Oakland · New York · Las Vegas · <a href="tel:{PHONE_TEL}" style="color:inherit">{PHONE}</a></span></div>
    <p class="disc">DentonX Inc. is a technology company. It does not originate loans, extend credit, underwrite financial products, broker securities or provide consumer financial services. Regulated activities are carried out by licensed, independent entities. Nothing on this website is an offer to sell or a solicitation of an offer to buy any securities. Market statistics are from the third-party sources cited and are provided for general information.</p>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
'''

def page_hero(crumb, tag, h1, lede):
    return f'''<section class="page-hero">
    <div class="grid-bg" aria-hidden="true"></div>
    <div class="wrap">
      <span class="crumbs rv"><a href="index.html">Home</a> / {crumb}</span>
      <span class="tag rv">{tag}</span>
      <h1 class="rv d1">{h1}</h1>
      <p class="rv d2">{lede}</p>
    </div>
  </section>'''

CTA = '''<section class="contact" style="padding-block:88px">
    <div class="wrap" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:center">
      <div class="rv" style="display:grid;gap:12px;max-width:640px"><span class="tag">Partner with us</span><h2 style="font:600 clamp(28px,3.8vw,46px)/1.08 var(--f-display);letter-spacing:-0.03em">Start building smarter credit infrastructure.</h2></div>
      <a class="btn btn-primary rv d1" href="contact.html">Get started <svg aria-hidden="true"><use href="#arr"/></svg></a>
    </div>
  </section>'''

def li(items, icon="ok"):
    return "".join(f'<li><svg aria-hidden="true"><use href="#{icon}"/></svg><span>{i}</span></li>' for i in items)

# ---------------- pages ----------------
PAGES = {}

PAGES["platform.html"] = ("Platform | DentonX", "Data infrastructure, an AI-powered automation engine, partner connectivity and scalable cloud infrastructure for non-bank lending.", f'''
  {page_hero("Platform", "The DentonX platform", 'One connected layer for <span class="grad">lending data and decisions.</span>', "Four modules that work together: data comes in clean, decisions run automatically, every partner stays connected, and the system scales with volume.")}
  <section>
    <div class="wrap">
      <div class="mods">
        <article class="mod rv"><span class="num">01</span><div><h3>Data infrastructure</h3><p>Real-time ingestion and normalization of complex financial data, so every partner works from the same clean records.</p></div><ul><li>Real-time ingestion from partner systems</li><li>Normalization into one standard format</li><li>Bank statement, credit, property and payment data</li><li>Secure data exchange between partners</li></ul></article>
        <article class="mod rv"><span class="num">02</span><div><h3>Automation engine</h3><p>End-to-end workflow orchestration powered by AI. Business rules and event triggers move each file forward without manual hand-offs.</p></div><ul><li>Approval workflows</li><li>Reconciliation and settlement triggers</li><li>Decision automation by partner rules</li><li>Compliance steps built into the flow</li></ul></article>
        <article class="mod rv"><span class="num">03</span><div><h3>Connectivity</h3><p>Lenders, platforms, servicers and investors share one technology layer instead of emailing files back and forth.</p></div><ul><li>API connectivity for partners and developers</li><li>Shared records across the lending chain</li><li>Operational visibility for every party</li><li>Complete audit trails</li></ul></article>
        <article class="mod rv"><span class="num">04</span><div><h3>Scalability</h3><p>Scalable cloud infrastructure and automated data pipelines that keep servicing and analytics simple as portfolios grow.</p></div><ul><li>Scalable cloud infrastructure</li><li>Automated data pipelines</li><li>Servicing and portfolio analytics</li><li>Modular, add what you need</li></ul></article>
      </div>
    </div>
  </section>
  <section class="market">
    <div class="wrap">
      <div class="head rv"><span class="tag">Architecture</span><h2>How the layers fit together.</h2><p>A modular automation system built on distributed-ledger technology, designed for secure process automation and digital record-keeping.</p></div>
      <div class="stack">
        <div class="layer rv"><b>Partners</b><span>Lenders, platforms, servicers, investors, developers</span></div>
        <div class="layer rv d1"><b>API &amp; connectivity</b><span>Secure data exchange and integrations</span></div>
        <div class="layer rv d1"><b>Data layer</b><span>Ingestion, normalization and validation</span></div>
        <div class="layer core rv d2"><b>Automation engine</b><span>Workflows, decision rules and smart-contract modules</span></div>
        <div class="layer rv d2"><b>Ledger &amp; records</b><span>Tamper-evident, distributed record-keeping</span></div>
        <div class="layer rv d3"><b>Analytics</b><span>Dashboards, audit trails and reporting pipelines</span></div>
      </div>
    </div>
  </section>
  <section>
    <div class="wrap">
      <div class="head rv"><span class="tag">Design principles</span><h2>Built for regulated partners.</h2></div>
      <div class="princ">
        <div class="pr rv d1"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg><h3>Auditable by default</h3><p>Every action is recorded, so partners and their compliance teams can trace any decision.</p></div>
        <div class="pr rv d2"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 14h4"/></svg><h3>Partner-controlled rules</h3><p>Licensed partners set their own credit and compliance rules. DentonX automates them.</p></div>
        <div class="pr rv d3"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 7h16M4 12h10M4 17h7"/><circle cx="18" cy="16" r="3"/></svg><h3>Modular</h3><p>Start with the module you need and add more as your operation grows.</p></div>
      </div>
    </div>
  </section>
  {CTA}''')

SOL = [
 ("01", "Non-bank lenders", "Run non-QM mortgage and SME credit operations on data-driven infrastructure, without building it yourself.",
  ["Borrower data arrives in different formats from different sources", "Manual reviews and hand-offs slow every file", "Compliance evidence is scattered across systems"],
  ["Clean, standardized borrower data in real time", "Automated workflows for your own credit rules", "A complete audit trail for every file"]),
 ("02", "Financial platforms & marketplaces", "Connect lenders, borrowers and capital on one layer with seamless data exchange and decision automation.",
  ["Every partner integration is custom work", "Data quality varies by partner", "Hard to show partners where a deal stands"],
  ["One integration layer for every partner", "Decision automation and compliance across partners", "Shared, real-time status for all parties"]),
 ("03", "Credit servicers & asset managers", "Get portfolio visibility, audit trails and automated data pipelines that simplify servicing and analytics.",
  ["Loan-level data arrives late or incomplete", "Reporting is assembled by hand", "Limited visibility into portfolio performance"],
  ["Automated loan-level data pipelines", "Operational dashboards and reporting", "Audit trails for investors and auditors"]),
 ("04", "Developers & integrators", "Build fintech products on API connectivity and scalable cloud infrastructure.",
  ["Lending data is hard to access and normalize", "Infrastructure has to scale with volume", "Compliance requirements add complexity"],
  ["API access to normalized financial data", "Scalable cloud infrastructure", "Workflow and record-keeping modules to build on"]),
]
sol_html = "".join(f'''<div class="sol rv"><div class="l"><span class="k">{k}</span><h3>{t}</h3><p>{d}</p></div><div><div class="pain" style="display:grid;gap:10px"><h4>The challenge</h4><ul>{li(p, "no")}</ul></div><div style="display:grid;gap:10px;margin-top:8px"><h4>With DentonX</h4><ul>{li(w)}</ul></div></div></div>''' for k, t, d, p, w in SOL)

PAGES["solutions.html"] = ("Solutions | DentonX", "DentonX solutions for non-bank lenders, financial platforms, credit servicers, asset managers and developers.", f'''
  {page_hero("Solutions", "Solutions", 'Built for everyone in the <span class="grad">lending chain.</span>', "From the lender making the decision to the investor reading the report, DentonX gives every party the same clean data and a clear record.")}
  <section><div class="wrap">{sol_html}</div></section>
  <section class="market">
    <div class="wrap">
      <div class="head rv"><span class="tag">Markets</span><h2>Where the platform focuses.</h2><p>Two lending markets where borrowers often fall outside traditional bank criteria.</p></div>
      <div class="mkts">
        <div class="mkt rv d1"><h3>Non-QM mortgage</h3><p>Loans outside the Qualified Mortgage standard, often for self-employed borrowers and real estate investors. About 10% of U.S. mortgage dollar volume in 2025.</p><ul class="chips"><li>Bank statement loans</li><li>Investor / DSCR loans</li><li>Asset-based loans</li><li>Self-employed borrowers</li></ul></div>
        <div class="mkt rv d2"><h3>SME lending</h3><p>Credit for small and mid-sized businesses. The share of small-business applicants seeking financing at online lenders rose from 17% to 29% between the 2020 and 2025 Federal Reserve surveys.</p><ul class="chips"><li>Term loans</li><li>Lines of credit</li><li>Equipment financing</li><li>Online and alternative lenders</li></ul></div>
      </div>
      <p class="note" style="color:var(--night-dim)">Sources: Polygon Research (non-QM, 2025 HMDA data); Federal Reserve Small Business Credit Survey.</p>
    </div>
  </section>
  {CTA}''')

PAGES["company.html"] = ("Company | DentonX", "DentonX's mission, vision, values, leadership and offices.", f'''
  {page_hero("Company", "Company", 'Enabling <span class="grad">connected financial ecosystems.</span>', "DentonX builds data infrastructure and automation for the lenders, platforms and investors working beyond traditional banking.")}
  <section>
    <div class="wrap co">
      <div class="mission rv">
        <span class="tag">Mission &amp; vision</span>
        <blockquote>Our mission is to enable <span>connected financial ecosystems</span> through data infrastructure and automation.</blockquote>
        <p style="color:var(--ink-2)">Our vision is a shared technology layer for lending and investing, where every partner works from the same data and every decision leaves a clear record.</p>
      </div>
      <div class="rv d2" style="display:grid;gap:18px;align-content:start">
        <span class="tag">Our story</span>
        <p style="color:var(--ink-2)">DentonX was founded in California in 2025 to bring modern infrastructure to non-bank lending, a fast-growing part of finance that still runs on spreadsheets, email and one-off integrations.</p>
        <p style="color:var(--ink-2)">We're a technology company, not a lender. Licensed, independent partners make the lending decisions. We build the systems that connect their data, automate their workflows and keep the records.</p>
      </div>
    </div>
  </section>
  <section class="company">
    <div class="wrap">
      <div class="head rv"><span class="tag">Milestones</span><h2>The story so far.</h2></div>
      <ol class="tl">
        <li class="rv"><span class="when">September 2025</span><b>DentonX Inc. incorporated</b><p>Founded with a focus on infrastructure for non-QM mortgage and SME lending.</p></li>
        <li class="rv d1"><span class="when">2026</span><b>Registration statement filed with the SEC</b><p>DentonX filed a registration statement on Form S-1 with the U.S. Securities and Exchange Commission.</p></li>
        <li class="rv d2"><span class="when">2026</span><b>Quarterly reporting</b><p>DentonX files quarterly reports on Form 10-Q. See the <a href="investors.html">Investors</a> page.</p></li>
      </ol>
    </div>
  </section>
  <section>
    <div class="wrap">
      <div class="head rv"><span class="tag">Core values</span><h2>What we hold ourselves to.</h2></div>
      <div class="values">
        <div class="value rv d1"><span class="k">01</span><h3>Integrity</h3><p>Clear records, honest data and systems partners can audit.</p></div>
        <div class="value rv d2"><span class="k">02</span><h3>Innovation</h3><p>Modern infrastructure for an industry still run on spreadsheets and email.</p></div>
        <div class="value rv d3"><span class="k">03</span><h3>Accessibility</h3><p>Technology that helps more borrowers reach responsible credit.</p></div>
        <div class="value rv d4"><span class="k">04</span><h3>Growth</h3><p>A platform that scales with every partner that joins.</p></div>
      </div>
    </div>
  </section>
  <section class="company">
    <div class="wrap co">
      <div class="people rv">
        <span class="tag">Leadership</span>
        <div class="person"><span class="av">LP</span><div><b>Lionel Pinuer</b><span>Chief Executive Officer &amp; Chief Financial Officer</span></div></div>
        <div class="person"><span class="av">LU</span><div><b>Luis Carlos Ung</b><span>Director, President &amp; Secretary</span></div></div>
      </div>
      <div class="rv d2" style="display:grid;gap:14px;align-content:start">
        <span class="tag">Offices</span>
        <ul class="offices" style="grid-template-columns:1fr">
          <li><b>Oakland, CA</b><span>Headquarters · 1999 Harrison Street, Suite 1800, Oakland, CA 94612</span></li>
          <li><b>New York, NY</b><span>Office</span></li>
          <li><b>Las Vegas, NV</b><span>Office</span></li>
        </ul>
      </div>
    </div>
  </section>
  {CTA}''')

FILINGS = [
 ("S-1/A", "Amended registration statement", "Filed May 1, 2026", "https://www.sec.gov/Archives/edgar/data/2093375/000209337526000006/dtnx_s1a.htm"),
 ("10-Q", "Quarterly report, period ended June 30, 2026", "Q2 2026", "https://www.sec.gov/Archives/edgar/data/2093375/000209337526000016/dtnx-20260630_10q.htm"),
 ("10-Q", "Quarterly report, period ended March 31, 2026", "Q1 2026", "https://www.sec.gov/Archives/edgar/data/2093375/000209337526000014/dtnx-20260331_10q.htm"),
 ("S-1", "Registration statement", "Initial filing, 2026", "https://www.sec.gov/Archives/edgar/data/2093375/000209337526000002/dtnx_s1.htm"),
]
fil_html = "".join(f'<a class="filing" href="{u}" target="_blank" rel="noopener"><span class="form">{f}</span><span><b>{t}</b><span>{d}</span></span><svg aria-hidden="true"><use href="#arr"/></svg></a>' for f, t, d, u in FILINGS)

PAGES["investors.html"] = ("Investors | DentonX", "SEC filings and investor contact information for DentonX Inc.", f'''
  {page_hero("Investors", "Investors", 'SEC filings.', "DentonX Inc. files reports with the U.S. Securities and Exchange Commission. Selected filings are listed below, and the complete record is on the SEC's EDGAR system.")}
  <section>
    <div class="wrap">
      <div class="head rv" style="margin-bottom:28px"><span class="tag">Filings</span><h2>Recent filings.</h2></div>
      <div class="filings rv">{fil_html}</div>
      <div style="margin-top:24px" class="rv"><a class="btn btn-ghost" href="{EDGAR}" target="_blank" rel="noopener">All filings on EDGAR <svg aria-hidden="true"><use href="#arr"/></svg></a></div>
      <p class="note">Links open documents on sec.gov. This page lists filings for reference only. Nothing on this website is an offer to sell or a solicitation of an offer to buy any securities.</p>
    </div>
  </section>
  <section class="company">
    <div class="wrap co">
      <div class="rv" style="display:grid;gap:14px"><span class="tag">Company information</span>
        <ul class="offices" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
          <li><b>Legal name</b><span>DentonX Inc.</span></li>
          <li><b>Incorporated</b><span>Wyoming, September 2025</span></li>
          <li><b>Headquarters</b><span>Oakland, California</span></li>
          <li><b>SEC CIK</b><span>0002093375</span></li>
        </ul></div>
      <div class="rv d2" style="display:grid;gap:14px;align-content:start"><span class="tag">Investor contact</span>
        <p style="color:var(--ink-2)">For investor questions, call <a href="tel:{PHONE_TEL}">{PHONE}</a> or use the <a href="contact.html">contact form</a>.</p></div>
    </div>
  </section>''')

PAGES["contact.html"] = ("Contact | DentonX", "Contact DentonX about partnerships for lenders, platforms, servicers and developers.", f'''
  <section id="contact" class="contact" style="padding-top:calc(150px + env(safe-area-inset-top))">
    <div class="wrap ct">
      <div class="copy rv">
        <span class="crumbs"><a href="index.html">Home</a> / Contact</span>
        <span class="tag">Get started</span>
        <h2>Let's build your credit infrastructure.</h2>
        <p>Lenders, platforms, servicers, capital partners and developers: tell us what you're working on and the DentonX team will be in touch.</p>
        <div class="info"><a href="tel:{PHONE_TEL}">{PHONE}</a><div>1999 Harrison Street, Suite 1800<br>Oakland, CA 94612</div></div>
      </div>
      <div class="rv d2">
        <form id="lead" name="partner" method="POST" data-netlify="true" netlify-honeypot="website" novalidate>
          <input type="hidden" name="form-name" value="partner">
          <p hidden><label>Leave this empty <input name="website"></label></p>
          <div class="frow">
            <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="f-co">Company</label><input id="f-co" name="company" autocomplete="organization" required></div>
          </div>
          <div class="frow">
            <div class="field"><label for="f-email">Work email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err" id="e-email" hidden>Enter an email like name@company.com.</span></div>
            <div class="field"><label for="f-type">I'm a</label><select id="f-type" name="partner_type"><option>Lender</option><option>Financial platform or marketplace</option><option>Servicer or asset manager</option><option>Developer or integrator</option><option>Capital partner</option><option>Other</option></select></div>
          </div>
          <div class="field"><label for="f-msg">How can we help?</label><textarea id="f-msg" name="message" required></textarea></div>
          <button class="btn btn-primary" type="submit">Send message <svg aria-hidden="true"><use href="#arr"/></svg></button>
          <p class="err" id="e-send" hidden>Your message didn't send. Please call {PHONE} or try again.</p>
        </form>
        <div class="sent" id="sent" hidden><strong>Message sent</strong><p>Thanks for reaching out. The DentonX team will be in touch.</p></div>
      </div>
    </div>
    <div class="wrap" style="margin-top:56px">
      <span class="tag rv">Offices</span>
      <div class="office-grid rv">
        <div class="office"><b>Oakland, CA</b><span>Headquarters</span><span>1999 Harrison Street, Suite 1800</span></div>
        <div class="office"><b>New York, NY</b><span>Office</span></div>
        <div class="office"><b>Las Vegas, NV</b><span>Office</span></div>
      </div>
    </div>
  </section>''')

def build():
    for name, (title, desc, body) in PAGES.items():
        (OUT / name).write_text(head(title, desc, name) + header(name) + '\n<main id="top">' + body + '\n</main>\n\n' + FOOTER)
        print("built", name)
    # home: keep its body, swap in shared head/header/footer
    idx = (OUT / "index.html").read_text()
    body = idx[idx.index('<main id="top">'):idx.index('</main>') + 7]
    body = body.replace('href="#contact">Partner with us', 'href="contact.html">Partner with us').replace('href="#platform">Explore the platform', 'href="platform.html">Explore the platform')
    title = "DentonX | Infrastructure for Non-Bank Lending"
    desc = "DentonX builds data infrastructure, workflow automation and analytics for non-QM mortgage and SME lending partners."
    (OUT / "index.html").write_text(head(title, desc, "index.html") + header("index.html") + "\n" + body + "\n\n" + FOOTER)
    print("built index.html")

if __name__ == "__main__":
    build()
