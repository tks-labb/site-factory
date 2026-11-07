#!/usr/bin/env node
// Site factory: turns clients/<slug>/site.json into sites/<slug>/index.html.
// Usage:  node build.mjs <slug>      build one client
//         node build.mjs --all       build every client (folders not starting with "_")
//         node build.mjs _example    build the example
// No dependencies. Requires Node 18+.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));

// ---------- helpers ----------
const esc = (v) =>
  String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const telHref = (p) => "tel:+" + (p.replace(/\D/g, "").length === 10 ? "1" : "") + p.replace(/\D/g, "");
const has = (a) => Array.isArray(a) && a.length > 0;

function hexToRgb(hex) {
  const h = hex.replace("#", "");
  const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function luminance(hex) {
  const [r, g, b] = hexToRgb(hex).map((v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
const onColor = (hex) => (luminance(hex) > 0.4 ? "#111111" : "#FFFFFF");

const FONTS = {
  modern: { display: "Sora", body: "DM Sans", url: "family=Sora:wght@600;700;800&family=DM+Sans:wght@400;500;700" },
  classic: { display: "Fraunces", body: "Source Sans 3", url: "family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;600;700" },
  friendly: { display: "Nunito", body: "Nunito Sans", url: "family=Nunito:wght@700;800;900&family=Nunito+Sans:wght@400;600;700" },
  bold: { display: "Archivo", body: "Archivo", url: "family=Archivo:wght@400;500;700;800;900" },
};

// Simple stroke icons (24x24). Pick by name in site.json.
const ICONS = {
  wrench: '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
  drop: '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/>',
  bolt: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
  home: '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
  leaf: '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  snow: '<path d="M12 2v20M4 6l16 12M20 6 4 18"/>',
  hammer: '<path d="M14 4h6v4l-2 1-3-3z"/><path d="m15 7-11 11 2 2 11-11"/>',
  paint: '<rect x="3" y="3" width="14" height="6" rx="1"/><path d="M17 6h3v5h-8v3"/><rect x="10" y="14" width="4" height="7" rx="1"/>',
  car: '<path d="M5 16V11l2-5h10l2 5v5"/><path d="M3 16h18v3H3z"/><circle cx="7.5" cy="13" r="1"/><circle cx="16.5" cy="13" r="1"/>',
  tooth: '<path d="M7 3c-2 0-4 2-4 5 0 4 2 5 2.5 9 .3 2 1 4 2.2 4 1.6 0 1.3-6 4.3-6s2.7 6 4.3 6c1.2 0 1.9-2 2.2-4 .5-4 2.5-5 2.5-9 0-3-2-5-4-5-2 0-3 1-5 1S9 3 7 3z"/>',
  scissors: '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 7.5 20 18M8.5 16.5 20 6"/>',
  paw: '<circle cx="5" cy="10" r="2"/><circle cx="9" cy="5" r="2"/><circle cx="15" cy="5" r="2"/><circle cx="19" cy="10" r="2"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5-2 3-4 3-4 0-4-3z"/>',
  heart: '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>',
  shield: '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
  chat: '<path d="M4 5h16v11H9l-5 4z"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  truck: '<path d="M2 6h11v10H2zM13 10h4l4 3v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
  dollar: '<path d="M12 2v20M17 6.5C16 5 14.3 4.5 12 4.5c-3 0-4.5 1.5-4.5 3.3 0 4.4 9.5 2.2 9.5 7 0 2-1.8 3.7-5 3.7-2.6 0-4.3-.8-5.3-2.5"/>',
  spark: '<path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l3.5 3.5M15.5 15.5 19 19M5 19l3.5-3.5M15.5 8.5 19 5"/>',
  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  phone: '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
  pin: '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
};
const icon = (name, cls = "ic") =>
  `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ICONS.check}</svg>`;

// ---------- page ----------
function render(c) {
  const b = c.business;
  const brand = c.brand || {};
  const primary = brand.primary || "#1F5FD6";
  const accent = brand.accent || primary;
  const font = FONTS[brand.font] || FONTS.modern;
  const hero = c.hero || {};
  const seo = c.seo || {};
  const title = seo.title || `${b.name}${b.city ? " | " + b.city : ""}`;
  const desc = seo.description || b.description || "";
  const quoteLabel = hero.secondaryCta || "Get a free quote";
  const logo = brand.logo
    ? `<img src="assets/${esc(brand.logo)}" alt="" class="logo-img">`
    : `<span class="logo-mark" aria-hidden="true">${esc(b.name.trim()[0])}</span>`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": c.schemaType || "LocalBusiness",
    name: b.name,
    description: desc,
    telephone: b.phone,
    email: b.email,
    url: c.domain ? `https://${c.domain}` : undefined,
    address: b.address
      ? { "@type": "PostalAddress", streetAddress: b.address.street, addressLocality: b.address.city, addressRegion: b.address.state, postalCode: b.address.zip, addressCountry: "US" }
      : undefined,
    areaServed: b.serviceArea,
    aggregateRating: c.rating ? { "@type": "AggregateRating", ratingValue: c.rating.value, reviewCount: c.rating.count } : undefined,
  };

  const navLinks = [
    has(c.services) && ["#services", "Services"],
    has(c.why) && ["#why", "Why us"],
    has(c.reviews) && ["#reviews", "Reviews"],
    has(c.faq) && ["#faq", "FAQ"],
    ["#contact", "Contact"],
  ].filter(Boolean);

  const heroImage = c.hero?.image
    ? `<img class="hero-photo" src="assets/${esc(c.hero.image)}" alt="${esc(c.hero.imageAlt || b.name)}">`
    : `<div class="hero-card" aria-label="${esc(b.name)} at a glance">
        ${c.rating ? `<div class="hc-rating"><span class="stars" aria-hidden="true">${icon("star", "st")}${icon("star", "st")}${icon("star", "st")}${icon("star", "st")}${icon("star", "st")}</span><strong>${esc(c.rating.value)}</strong><span>${esc(c.rating.count)} reviews on ${esc(c.rating.source || "Google")}</span></div>` : ""}
        ${has(b.hours) ? `<div class="hc-block"><span class="hc-label">${icon("clock")}Hours</span><ul class="hours">${b.hours.map(([d, t]) => `<li><span>${esc(d)}</span><span>${esc(t)}</span></li>`).join("")}</ul></div>` : ""}
        <a class="hc-call" href="${telHref(b.phone)}">${icon("phone")}<span><small>${esc(c.callLabel || "Call us")}</small>${esc(b.phone)}</span></a>
      </div>`;

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
${c.demo ? `<meta name="robots" content="noindex, nofollow">` : c.domain ? `<link rel="canonical" href="https://${esc(c.domain)}/">` : ""}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?${font.url}&display=swap">
<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>
<style>
:root {
  --primary: ${primary};
  --on-primary: ${onColor(primary)};
  --accent: ${accent};
  --bg: #FAFAF8;
  --surface: #FFFFFF;
  --tint: color-mix(in srgb, var(--primary) 7%, #FAFAF8);
  --ink: #15171A;
  --ink-2: #555B63;
  --line: #E3E4E0;
  --link: color-mix(in srgb, var(--primary) 85%, black);
  --f-display: "${font.display}", Georgia, system-ui, sans-serif;
  --f-body: "${font.body}", system-ui, -apple-system, "Segoe UI", sans-serif;
  --r: 14px;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101214; --surface: #171A1D; --tint: color-mix(in srgb, var(--primary) 14%, #101214);
    --ink: #EEF0F2; --ink-2: #A3A9B1; --line: #2A2F35;
    --link: color-mix(in srgb, var(--primary) 55%, white);
    color-scheme: dark;
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 17px/1.6 var(--f-body); -webkit-font-smoothing: antialiased; }
img { max-width: 100%; display: block; }
a { color: var(--link); }
[hidden] { display: none !important; }
:focus-visible { outline: 3px solid var(--primary); outline-offset: 3px; border-radius: 6px; }
h1, h2, h3 { font-family: var(--f-display); line-height: 1.1; margin: 0; text-wrap: balance; letter-spacing: -0.01em; }
p { margin: 0; }
.wrap { max-width: 1140px; margin: 0 auto; padding-left: max(18px, env(safe-area-inset-left)); padding-right: max(18px, env(safe-area-inset-right)); }
.ic { width: 22px; height: 22px; flex-shrink: 0; }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: 50px; padding: 0 24px; border-radius: 999px; font: 700 16px/1 var(--f-body); text-decoration: none; cursor: pointer; border: 2px solid transparent; transition: transform .15s ease, box-shadow .15s ease; }
.btn:hover { transform: translateY(-1px); box-shadow: 0 6px 18px -8px color-mix(in srgb, var(--primary) 70%, transparent); }
.btn-primary { background: var(--primary); color: var(--on-primary); }
.btn-outline { border-color: currentColor; color: var(--ink); background: transparent; }
.eyebrow { font-weight: 700; font-size: 14px; letter-spacing: .08em; text-transform: uppercase; color: var(--link); }

/* header */
.top { position: sticky; top: 0; z-index: 20; background: color-mix(in srgb, var(--bg) 90%, transparent); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }
.top .wrap { display: flex; align-items: center; gap: 20px; min-height: 70px; }
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink); font: 800 19px/1.1 var(--f-display); margin-right: auto; }
.logo-img { height: 40px; width: auto; }
.logo-mark { width: 38px; height: 38px; border-radius: 10px; background: var(--primary); color: var(--on-primary); display: grid; place-items: center; font-size: 20px; }
.nav { display: flex; gap: 24px; }
.nav a { color: var(--ink-2); text-decoration: none; font-weight: 600; font-size: 15px; }
.nav a:hover { color: var(--ink); }
.top .btn { min-height: 44px; padding: 0 18px; font-size: 15px; }
@media (max-width: 880px) { .nav { display: none; } }
@media (max-width: 420px) { .top .btn .lbl { display: none; } .top .btn { padding: 0 14px; } }

/* hero */
.hero { background: var(--tint); padding-block: 64px; }
.hero .wrap { display: grid; grid-template-columns: 1.15fr .85fr; gap: 48px; align-items: center; }
.hero .wrap > * { min-width: 0; }
.hero h1 { font-size: clamp(36px, 5.4vw, 64px); margin-top: 14px; }
.hero .sub { font-size: 20px; color: var(--ink-2); margin-top: 18px; max-width: 36ch; }
.ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
.trust { list-style: none; padding: 0; margin: 28px 0 0; display: flex; flex-wrap: wrap; gap: 10px 22px; }
.trust li { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: 15px; }
.trust .ic { color: var(--link); width: 20px; height: 20px; }
.hero-photo { border-radius: 20px; aspect-ratio: 4 / 5; object-fit: cover; width: 100%; max-width: 100%; }
.hero-card { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 26px; display: grid; gap: 22px; box-shadow: 0 20px 50px -30px rgba(0,0,0,.35); }
.hc-rating { display: grid; gap: 4px; }
.hc-rating strong { font: 800 40px/1 var(--f-display); }
.hc-rating span:last-child { color: var(--ink-2); font-size: 15px; }
.stars { display: flex; gap: 2px; color: #E8A317; }
.stars .st { width: 20px; height: 20px; fill: currentColor; stroke: none; }
.hc-label { display: flex; align-items: center; gap: 8px; font-weight: 700; margin-bottom: 8px; }
.hc-label .ic { width: 18px; height: 18px; color: var(--link); }
.hours { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; font-variant-numeric: tabular-nums; }
.hours li { display: flex; justify-content: space-between; gap: 16px; border-bottom: 1px dashed var(--line); padding-bottom: 6px; color: var(--ink-2); }
.hours li span:first-child { color: var(--ink); font-weight: 600; }
.hc-call { display: flex; align-items: center; gap: 14px; text-decoration: none; background: var(--primary); color: var(--on-primary); border-radius: 14px; padding: 16px 18px; font: 800 22px/1.1 var(--f-display); }
.hc-call small { display: block; font: 600 13px/1.3 var(--f-body); opacity: .85; }
@media (max-width: 900px) { .hero .wrap { grid-template-columns: 1fr; } .hero { padding-block: 44px; } .hero-photo { aspect-ratio: 16 / 10; } }

/* sections */
section { padding-block: 80px; }
.head { max-width: 680px; display: grid; gap: 12px; margin-bottom: 40px; }
.head h2 { font-size: clamp(30px, 3.8vw, 44px); }
.head p { color: var(--ink-2); font-size: 18px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 18px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 26px; display: grid; gap: 12px; align-content: start; min-width: 0; }
.card .ic-wrap { width: 48px; height: 48px; border-radius: 12px; background: var(--tint); color: var(--link); display: grid; place-items: center; }
.card h3 { font-size: 20px; }
.card p { color: var(--ink-2); }
.card .price { font-weight: 700; color: var(--ink); }
.why { background: var(--surface); border-block: 1px solid var(--line); }
.why-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 28px 40px; list-style: none; padding: 0; margin: 0; }
.why-list li { display: grid; grid-template-columns: 40px 1fr; gap: 4px 14px; }
.why-list .ic { grid-row: span 2; width: 40px; height: 40px; padding: 8px; border-radius: 50%; background: var(--primary); color: var(--on-primary); }
.why-list h3 { font-size: 19px; }
.why-list p { color: var(--ink-2); }
.reviews { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }
blockquote { margin: 0; background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 26px; display: grid; gap: 16px; align-content: start; }
blockquote p { font-size: 17px; }
blockquote footer { color: var(--ink-2); font-size: 15px; }
blockquote footer strong { color: var(--ink); }
.area { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: start; }
.area > * { min-width: 0; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; padding: 0; margin: 0; }
.chips li { padding: 8px 14px; border-radius: 999px; background: var(--tint); font-weight: 600; font-size: 15px; }
.info { display: grid; gap: 14px; }
.info a, .info div { display: flex; gap: 12px; align-items: flex-start; color: var(--ink); text-decoration: none; overflow-wrap: anywhere; }
.info .ic { color: var(--link); margin-top: 2px; }
@media (max-width: 760px) { .area { grid-template-columns: 1fr; } }
.faq { max-width: 820px; border-top: 1px solid var(--line); }
details { border-bottom: 1px solid var(--line); }
summary { cursor: pointer; list-style: none; padding: 20px 0; font-weight: 700; font-size: 18px; display: flex; justify-content: space-between; gap: 16px; }
summary::-webkit-details-marker { display: none; }
summary::after { content: "+"; font-size: 24px; line-height: 1; color: var(--link); transition: transform .2s; }
details[open] summary::after { transform: rotate(45deg); }
details p { padding-bottom: 20px; color: var(--ink-2); max-width: 65ch; }

/* contact */
.contact { background: var(--tint); }
.contact-box { display: grid; grid-template-columns: .9fr 1.1fr; gap: 40px; background: var(--surface); border: 1px solid var(--line); border-radius: 22px; padding: clamp(22px, 4vw, 48px); }
.contact-box > * { min-width: 0; }
.contact h2 { font-size: clamp(30px, 3.8vw, 44px); }
.contact-copy { display: grid; gap: 18px; align-content: start; }
.contact-copy > p { color: var(--ink-2); font-size: 18px; }
form { display: grid; gap: 14px; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 560px) { .row { grid-template-columns: 1fr; } }
.field { display: grid; gap: 6px; min-width: 0; }
label { font-weight: 700; font-size: 15px; }
input, select, textarea { font: inherit; font-size: 16px; color: var(--ink); background: var(--bg); border: 1.5px solid var(--line); border-radius: 10px; padding: 12px 14px; min-height: 50px; width: 100%; }
input:focus, select:focus, textarea:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 25%, transparent); }
textarea { min-height: 110px; resize: vertical; }
.err { color: #C0362C; font-size: 14px; }
@media (prefers-color-scheme: dark) { .err { color: #FF8A7E; } }
.sent { border: 2px solid var(--primary); border-radius: 14px; padding: 22px; display: grid; gap: 8px; }
@media (max-width: 860px) { .contact-box { grid-template-columns: 1fr; } }
.foot { padding-block: 32px; border-top: 1px solid var(--line); color: var(--ink-2); font-size: 15px; }
.foot .wrap { display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; }
.callbar { display: none; }
@media (max-width: 640px) {
  .callbar { display: flex; position: fixed; left: 0; right: 0; bottom: 0; z-index: 30; gap: 10px; padding: 10px max(12px, env(safe-area-inset-right)) calc(10px + env(safe-area-inset-bottom)) max(12px, env(safe-area-inset-left)); background: var(--surface); border-top: 1px solid var(--line); }
  .callbar .btn { flex: 1; min-height: 48px; padding: 0 12px; }
  body { padding-bottom: 76px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } html { scroll-behavior: auto; } }
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="#top">${logo}<span>${esc(b.name)}</span></a>
    <nav class="nav" aria-label="Main">${navLinks.map(([h, l]) => `<a href="${h}">${l}</a>`).join("")}</nav>
    <a class="btn btn-primary" href="${telHref(b.phone)}">${icon("phone")}<span class="lbl">${esc(b.phone)}</span></a>
  </div>
</header>

<main id="top">
  <section class="hero">
    <div class="wrap">
      <div>
        ${b.city ? `<span class="eyebrow">${esc(hero.eyebrow || `Serving ${b.city}${b.serviceArea && b.serviceArea.length > 1 ? " and nearby" : ""}`)}</span>` : ""}
        <h1>${esc(hero.headline || b.tagline || b.name)}</h1>
        ${hero.subheadline ? `<p class="sub">${esc(hero.subheadline)}</p>` : ""}
        <div class="ctas">
          <a class="btn btn-primary" href="${b.bookingUrl ? esc(b.bookingUrl) : "#contact"}"${b.bookingUrl ? ' target="_blank" rel="noopener"' : ""}>${esc(hero.primaryCta || (b.bookingUrl ? "Book online" : quoteLabel))}</a>
          <a class="btn btn-outline" href="${telHref(b.phone)}">${icon("phone")}Call ${esc(b.phone)}</a>
        </div>
        ${has(c.trust) ? `<ul class="trust">${c.trust.map((t) => `<li>${icon("check")}${esc(t)}</li>`).join("")}</ul>` : ""}
      </div>
      <div>${heroImage}</div>
    </div>
  </section>

  ${has(c.services) ? `<section id="services">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Services</span><h2>${esc(c.servicesTitle || "What we do")}</h2>${c.servicesIntro ? `<p>${esc(c.servicesIntro)}</p>` : ""}</div>
      <div class="grid">${c.services.map((s) => `
        <article class="card"><span class="ic-wrap">${icon(s.icon || "check")}</span><h3>${esc(s.name)}</h3><p>${esc(s.description)}</p>${s.price ? `<p class="price">${esc(s.price)}</p>` : ""}</article>`).join("")}
      </div>
    </div>
  </section>` : ""}

  ${has(c.why) ? `<section id="why" class="why">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Why ${esc(b.name)}</span><h2>${esc(c.whyTitle || "Why customers choose us")}</h2></div>
      <ul class="why-list">${c.why.map((w) => `<li>${icon(w.icon || "check")}<h3>${esc(w.title)}</h3><p>${esc(w.text)}</p></li>`).join("")}</ul>
    </div>
  </section>` : ""}

  ${has(c.reviews) ? `<section id="reviews">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Reviews</span><h2>${esc(c.reviewsTitle || "What customers say")}</h2></div>
      <div class="reviews">${c.reviews.map((r) => `
        <blockquote><span class="stars" aria-label="5 stars">${icon("star", "st").repeat(5)}</span><p>“${esc(r.quote)}”</p><footer><strong>${esc(r.name)}</strong>${r.source ? ` · ${esc(r.source)}` : ""}</footer></blockquote>`).join("")}
      </div>
    </div>
  </section>` : ""}

  <section id="area" class="${has(c.reviews) ? "why" : ""}">
    <div class="wrap area">
      <div class="head" style="margin:0">
        <span class="eyebrow">Where we work</span>
        <h2>${esc(c.areaTitle || (b.city ? `Proudly serving ${b.city}` : "Service area"))}</h2>
        ${has(b.serviceArea) ? `<ul class="chips">${b.serviceArea.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>` : ""}
      </div>
      <div class="info">
        <a href="${telHref(b.phone)}">${icon("phone")}<span>${esc(b.phone)}</span></a>
        ${b.email ? `<a href="mailto:${esc(b.email)}">${icon("mail")}<span>${esc(b.email)}</span></a>` : ""}
        ${b.address ? `<a href="${esc(b.mapsUrl || "https://maps.google.com/?q=" + encodeURIComponent([b.address.street, b.address.city, b.address.state].join(" ")))}" target="_blank" rel="noopener">${icon("pin")}<span>${esc(b.address.street)}, ${esc(b.address.city)}, ${esc(b.address.state)} ${esc(b.address.zip || "")}</span></a>` : ""}
        ${has(b.hours) ? `<div>${icon("clock")}<ul class="hours" style="flex:1">${b.hours.map(([d, t]) => `<li><span>${esc(d)}</span><span>${esc(t)}</span></li>`).join("")}</ul></div>` : ""}
      </div>
    </div>
  </section>

  ${has(c.faq) ? `<section id="faq">
    <div class="wrap">
      <div class="head"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
      <div class="faq">${c.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join("")}</div>
    </div>
  </section>` : ""}

  <section id="contact" class="contact">
    <div class="wrap">
      <div class="contact-box">
        <div class="contact-copy">
          <h2>${esc(c.contactTitle || quoteLabel)}</h2>
          <p>${esc(c.contactIntro || "Tell us what you need and we'll get back to you quickly.")}</p>
          ${b.bookingUrl ? `<a class="btn btn-primary" style="justify-self:start" href="${esc(b.bookingUrl)}" target="_blank" rel="noopener">${icon("calendar")}Book a time online</a>` : ""}
          <a class="btn btn-outline" style="justify-self:start" href="${telHref(b.phone)}">${icon("phone")}${esc(b.phone)}</a>
        </div>
        <div>
          <form id="lead" name="contact" method="POST" data-netlify="true" netlify-honeypot="website" novalidate>
            <input type="hidden" name="form-name" value="contact">
            <p hidden><label>Leave this empty <input name="website"></label></p>
            <div class="row">
              <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
              <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required><span class="err" id="e-phone" hidden>Enter a phone number with at least 10 digits.</span></div>
            </div>
            <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err" id="e-email" hidden>Enter an email like name@example.com.</span></div>
            ${has(c.services) ? `<div class="field"><label for="f-service">What do you need?</label><select id="f-service" name="service">${c.services.map((s) => `<option>${esc(s.name)}</option>`).join("")}<option>Something else</option></select></div>` : ""}
            <div class="field"><label for="f-msg">Details</label><textarea id="f-msg" name="message" required></textarea></div>
            <button class="btn btn-primary" type="submit" style="justify-self:start">Send request</button>
            <p class="err" id="e-send" hidden>Your request didn't send. Please call ${esc(b.phone)} or try again.</p>
          </form>
          <div class="sent" id="sent" hidden><strong>Request sent</strong><p>Thanks! ${esc(b.name)} will be in touch soon. Need help now? Call <a href="${telHref(b.phone)}">${esc(b.phone)}</a>.</p></div>
        </div>
      </div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap">
    <span>© ${new Date().getFullYear()} ${esc(b.name)}${b.license ? ` · ${esc(b.license)}` : ""}</span>
    <span>${esc(b.phone)}${b.email ? ` · ${esc(b.email)}` : ""}</span>
  </div>
</footer>

<div class="callbar">
  <a class="btn btn-primary" href="${telHref(b.phone)}">${icon("phone")}Call</a>
  <a class="btn btn-outline" href="#contact">${esc(c.mobileQuoteLabel || "Get a quote")}</a>
</div>

<script>
(function () {
  var form = document.getElementById('lead'), sent = document.getElementById('sent');
  function check(id, ok) { var el = document.getElementById(id); if (el) el.hidden = ok; return ok; }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = form.email.value.trim(), phone = form.phone.value.replace(/\\D/g, '');
    var ok = check('e-phone', phone.length >= 10) & check('e-email', /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email));
    var empty = Array.prototype.find.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (!ok) { (phone.length < 10 ? form.phone : form.email).focus(); return; }
    if (empty) { empty.focus(); return; }
    var btn = form.querySelector('button[type=submit]'); btn.disabled = true; btn.textContent = 'Sending…';
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
      .then(function (r) { if (!r.ok) throw 0; form.hidden = true; sent.hidden = false; })
      .catch(function () { btn.disabled = false; btn.textContent = 'Send request'; check('e-send', false); });
  });
})();
</script>
</body>
</html>
`;
}

// ---------- build ----------
function build(slug) {
  const dir = path.join(ROOT, "clients", slug);
  const cfgPath = path.join(dir, "site.json");
  if (!fs.existsSync(cfgPath)) throw new Error(`No clients/${slug}/site.json`);
  const cfg = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
  for (const k of ["name", "phone"]) if (!cfg.business?.[k]) throw new Error(`${slug}: business.${k} is required`);
  const out = path.join(ROOT, "sites", slug);
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, "index.html"), render(cfg));
  const assets = path.join(dir, "assets");
  if (fs.existsSync(assets)) fs.cpSync(assets, path.join(out, "assets"), { recursive: true });
  console.log(`built sites/${slug}/index.html`);
}

const arg = process.argv[2];
if (!arg) {
  console.error("Usage: node build.mjs <slug> | --all");
  process.exit(1);
}
const slugs = arg === "--all"
  ? fs.readdirSync(path.join(ROOT, "clients")).filter((d) => !d.startsWith("_") && fs.existsSync(path.join(ROOT, "clients", d, "site.json")))
  : [arg];
slugs.forEach(build);
