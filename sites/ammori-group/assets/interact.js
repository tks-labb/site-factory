// Ammori Group interactions: portfolio map, property maps, space finder, space calculator,
// shortlist, tour request fields and "notify me" alerts.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var d = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var data = { props: [] };
  try { data = JSON.parse($('am-data').textContent); } catch (e) {}
  var fmt = function (n) { return Number(n).toLocaleString('en-US'); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var store = {
    get: function (k, f) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : f; } catch (e) { return f; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  // ---------- Maps (Leaflet, loaded only when a map scrolls into view) ----------
  var LCSS = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';
  var LJS = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';
  var queue = null, maps = [];
  function loadLeaflet(cb, fail) {
    if (window.L) return cb();
    if (queue) { queue.push([cb, fail]); return; }
    queue = [[cb, fail]];
    var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = LCSS; document.head.appendChild(css);
    var js = document.createElement('script'); js.src = LJS; js.async = true;
    js.onload = function () { queue.forEach(function (q) { q[0](); }); queue = []; };
    js.onerror = function () { queue.forEach(function (q) { if (q[1]) q[1](); }); queue = null; };
    document.head.appendChild(js);
  }
  function isDark() { var t = d.getAttribute('data-theme'); return t ? t === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches; }
  // OpenStreetMap tiles (no API key). The site's colors come from CSS filters on .am-tiles,
  // which also follow light and dark mode automatically.
  function addTiles(map) {
    var layer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, className: 'am-tiles', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
    maps.push(layer);
  }
  function pinIcon(avail) { return L.divIcon({ className: 'am-pin ' + (avail ? 'av' : 'full'), html: '<span></span>', iconSize: [24, 24], iconAnchor: [12, 12], popupAnchor: [0, -14] }); }
  function whenVisible(el, fn) {
    if (!('IntersectionObserver' in window)) return fn();
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); fn(); } }, { rootMargin: '300px 0px' });
    io.observe(el);
  }
  function mapFailed(el) { el.innerHTML = '<p class="map-fallback">The map couldn\'t load. Check your connection and refresh.</p>'; }

  // Portfolio map on the homepage
  var pm = $('pmap');
  if (pm && data.props.length) whenVisible(pm, function () {
    loadLeaflet(function () {
      pm.innerHTML = '';
      var map = L.map(pm, { scrollWheelZoom: false, zoomControl: true, attributionControl: true });
      addTiles(map);
      var markers = {}, bounds = [];
      data.props.forEach(function (p) {
        if (!p.ll) return;
        var status = p.avail ? '<span class="pp-av">' + p.avail + ' space' + (p.avail > 1 ? 's' : '') + ' available' + (p.sf ? ' · ' + fmt(p.sf) + ' SF' : '') + '</span>'
          : '<span class="pp-full">Fully leased' + (p.tenants.length ? ' · ' + esc(p.tenants.join(', ')) : '') + '</span>';
        var html = '<a class="pp" href="' + p.slug + '.html">' + (p.photo ? '<img src="' + p.photo + '" alt="" width="240" height="135">' : '') +
          '<span class="pp-b"><b>' + esc(p.name) + '</b><span class="pp-c">' + esc(p.kind) + ' · ' + esc(p.city) + '</span>' + status + '<span class="pp-go">View property →</span></span></a>';
        var m = L.marker(p.ll, { icon: pinIcon(p.avail), title: p.name, riseOnHover: true, keyboard: true }).addTo(map).bindPopup(html, { maxWidth: 260, minWidth: 240, className: 'am-pop' });
        markers[p.slug] = { m: m, avail: p.avail };
        bounds.push(p.ll);
      });
      map.fitBounds(bounds, { padding: [28, 28] });
      if (map.getZoom() < 9) map.setZoom(9);
      map.once('focus click', function () { map.scrollWheelZoom.enable(); });
      // keep the map in step with the "Space available / Fully leased" filter
      document.querySelectorAll('.pchip').forEach(function (c) {
        c.addEventListener('click', function () {
          var f = c.dataset.p;
          Object.keys(markers).forEach(function (k) {
            var o = markers[k], show = f === 'all' || (f === 'yes') === !!o.avail;
            if (show && !map.hasLayer(o.m)) o.m.addTo(map); if (!show && map.hasLayer(o.m)) map.removeLayer(o.m);
          });
        });
      });
      // hovering a property card highlights its pin
      document.querySelectorAll('#prop-grid .prop').forEach(function (card) {
        var o = markers[card.dataset.slug]; if (!o) return;
        card.addEventListener('mouseenter', function () { var el = o.m.getElement(); if (el) el.classList.add('hot'); });
        card.addEventListener('mouseleave', function () { var el = o.m.getElement(); if (el) el.classList.remove('hot'); });
      });
    }, function () { mapFailed(pm); });
  });

  // Small map on each property page
  var mm = $('mini-map');
  if (mm) whenVisible(mm, function () {
    loadLeaflet(function () {
      mm.innerHTML = '';
      var ll = mm.dataset.ll.split(',').map(Number);
      var map = L.map(mm, { scrollWheelZoom: false }).setView(ll, 15);
      addTiles(map);
      var avail = !!document.querySelector('#avail .space');
      L.marker(ll, { icon: pinIcon(avail), title: mm.dataset.name }).addTo(map).bindPopup('<b>' + esc(mm.dataset.name) + '</b>', { className: 'am-pop' });
      map.once('focus click', function () { map.scrollWheelZoom.enable(); });
    }, function () { mapFailed(mm); });
  });

  // ---------- Space finder: search, city, size range, type, sort ----------
  var grid = $('space-grid');
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.space'));
    cards.forEach(function (c, i) { c.dataset.i = i; });
    var q = $('q'), city = $('f-city'), sMin = $('s-min'), sMax = $('s-max'), sort = $('f-sort'), out = $('size-out'), count = $('f-count'), reset = $('f-reset');
    var MAX = +sMax.max, type = 'all';
    var cities = data.props.map(function (p) { return p.city.toLowerCase(); }).filter(function (v, i, a) { return a.indexOf(v) === i; });
    var TYPES = { office: 'Office', offices: 'Office', medical: 'Medical', dental: 'Medical', clinic: 'Medical', retail: 'Retail', store: 'Retail', shop: 'Retail', showroom: 'Retail', restaurant: 'Restaurant', cafe: 'Restaurant', café: 'Restaurant', food: 'Restaurant', storage: 'Storage', land: 'Land', lot: 'Land', acres: 'Land', acre: 'Land', parcel: 'Land', commercial: 'Commercial' };
    var STOP = 'a an and about around approx approximately roughly of in at near for the to i we need want looking sf sq ft feet foot square space spaces something some with or me my our'.split(' ');

    function parse(text) {
      var r = { lo: 0, hi: Infinity, type: null, city: null, words: [] };
      var t = (text || '').toLowerCase().replace(/(\d),(\d)/g, '$1$2');
      var m = t.match(/(\d+(?:\.\d+)?)\s*(k\b|thousand)?/);
      if (m) {
        var n = parseFloat(m[1]) * (m[2] ? 1000 : 1);
        if (n >= 100) {
          if (/(under|less than|below|max|up to|no more than)\s*\d/.test(t)) r.hi = n;
          else if (/(over|more than|at least|min|minimum|above|\+)\s*\d|\d\s*\+/.test(t)) r.lo = n;
          else { r.lo = n * 0.65; r.hi = n * 1.35; }
        }
        t = t.replace(m[0], ' ');
      }
      cities.forEach(function (c) { if (t.indexOf(c) > -1) { r.city = c; t = t.replace(c, ' '); } });
      t.split(/[^a-zé0-9]+/).forEach(function (w) {
        if (!w || STOP.indexOf(w) > -1 || /^\d+$/.test(w)) return;
        if (TYPES[w] && !r.type) { r.type = TYPES[w]; return; }
        r.words.push(w);
      });
      return r;
    }
    function sizeLabel() {
      var a = +sMin.value, b = +sMax.value;
      out.textContent = (a === 0 && b === MAX) ? 'Any size' : (a === 0 ? 'Up to ' + fmt(b) + ' SF' : b === MAX ? fmt(a) + '+ SF' : fmt(a) + ' – ' + fmt(b) + ' SF');
      sMin.parentNode.style.setProperty('--a', (a / MAX * 100) + '%'); sMin.parentNode.style.setProperty('--b', (b / MAX * 100) + '%');
    }
    function apply() {
      var p = parse(q.value), a = +sMin.value, b = +sMax.value, sizeOn = a > 0 || b < MAX || p.lo > 0 || p.hi < Infinity;
      var c = city.value.toLowerCase() || p.city, t = type !== 'all' ? type : p.type, shown = 0;
      cards.forEach(function (el) {
        var sf = +el.dataset.sf, ok = true;
        if (t && el.dataset.type !== t) ok = false;
        if (ok && c && el.dataset.city.toLowerCase() !== c) ok = false;
        if (ok && sizeOn) ok = sf > 0 && sf >= a && sf <= b && sf >= p.lo && sf <= p.hi;
        if (ok && p.words.length) ok = p.words.every(function (w) { return el.dataset.text.indexOf(w) > -1; });
        el.classList.toggle('out', !ok); if (ok) shown++;
      });
      var order = cards.slice();
      if (sort.value) order.sort(function (x, y) {
        var sx = +x.dataset.sf || (sort.value === 'asc' ? 1e9 : -1), sy = +y.dataset.sf || (sort.value === 'asc' ? 1e9 : -1);
        return sort.value === 'asc' ? sx - sy : sy - sx;
      }); else order.sort(function (x, y) { return x.dataset.i - y.dataset.i; });
      order.forEach(function (el) { grid.appendChild(el); });
      count.textContent = 'Showing ' + shown + ' of ' + cards.length + ' spaces';
      $('empty').hidden = shown > 0;
      reset.hidden = !(q.value || city.value || a > 0 || b < MAX || sort.value || type !== 'all');
      sizeLabel();
    }
    var timer; q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(apply, 150); });
    [city, sort].forEach(function (el) { el.addEventListener('change', apply); });
    sMin.addEventListener('input', function () { if (+sMin.value > +sMax.value) sMin.value = sMax.value; apply(); });
    sMax.addEventListener('input', function () { if (+sMax.value < +sMin.value) sMax.value = sMin.value; apply(); });
    document.querySelectorAll('#spaces .chip').forEach(function (ch) {
      ch.addEventListener('click', function () {
        type = ch.dataset.f;
        document.querySelectorAll('#spaces .chip').forEach(function (x) { x.setAttribute('aria-pressed', x === ch ? 'true' : 'false'); });
        apply();
      });
    });
    function setType(tp) {
      var ch = document.querySelector('#spaces .chip[data-f="' + tp + '"]') || document.querySelector('#spaces .chip[data-f="all"]');
      type = ch.dataset.f; document.querySelectorAll('#spaces .chip').forEach(function (x) { x.setAttribute('aria-pressed', x === ch ? 'true' : 'false'); });
    }
    reset.addEventListener('click', function () { q.value = ''; city.value = ''; sMin.value = 0; sMax.value = MAX; sort.value = ''; setType('all'); apply(); q.focus(); });
    apply();

    // ---------- Space calculator ----------
    var ct = $('calc-toggle'), calc = $('calc'), people = $('c-people'), kind = $('c-type'), cOut = $('c-out');
    function est() {
      var n = Math.max(1, Math.min(2000, +people.value || 1)), r = +kind.selectedOptions[0].dataset.r;
      var lo = Math.round(n * r * 0.85 / 100) * 100, hi = Math.round(n * r * 1.15 / 100) * 100;
      cOut.textContent = fmt(lo) + ' – ' + fmt(hi) + ' SF'; return [lo, hi];
    }
    ct.addEventListener('click', function () { var open = calc.hidden; calc.hidden = !open; ct.setAttribute('aria-expanded', open); if (open) { est(); people.focus(); } });
    people.addEventListener('input', est); kind.addEventListener('change', est);
    $('c-go').addEventListener('click', function () {
      var r = est(), step = 500;
      sMin.value = Math.max(0, Math.floor(r[0] * 0.8 / step) * step);
      sMax.value = Math.min(MAX, Math.ceil(r[1] * 1.3 / step) * step);
      q.value = ''; city.value = ''; setType(kind.selectedOptions[0].dataset.t); apply();
      if (!grid.querySelector('.space:not(.out)')) { setType('all'); apply(); }
      grid.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  }

  // ---------- Shortlist (saved in this browser) ----------
  var KEY = 'am_shortlist', list = store.get(KEY, []);
  var pill = document.createElement('div'); pill.className = 'sl';
  pill.innerHTML = '<button class="sl-pill" type="button" aria-expanded="false" aria-controls="sl-panel" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 8 3.4 4.5 7 4.5c2 0 3.5 1.1 5 3 1.5-1.9 3-3 5-3 3.6 0 5.6 3.5 4.3 6.8-1.8 4.6-9.3 9.2-9.3 9.2z"/></svg><span>My shortlist (<b>0</b>)</span></button>' +
    '<section class="sl-panel" id="sl-panel" role="dialog" aria-label="Your shortlist" hidden><header><b>Your shortlist</b><button class="sl-x" type="button" aria-label="Close shortlist">✕</button></header><ul class="sl-list"></ul>' +
    '<div class="sl-actions"><button class="btn btn-gold sl-send" type="button">Send one inquiry for all</button><button class="link-btn sl-clear" type="button">Clear list</button></div></section>';
  document.body.appendChild(pill);
  var pBtn = pill.querySelector('.sl-pill'), panel = pill.querySelector('.sl-panel'), ul = pill.querySelector('.sl-list');
  function save() { store.set(KEY, list); render(); }
  function has(id) { return list.some(function (x) { return x.id === id; }); }
  function render() {
    pBtn.hidden = !list.length; pBtn.querySelector('b').textContent = list.length;
    if (!list.length) panel.hidden = true;
    ul.innerHTML = list.map(function (x, i) { return '<li><a href="' + esc(x.url) + '">' + esc(x.label) + '</a><span>' + esc(x.size) + '</span><button type="button" data-i="' + i + '" aria-label="Remove ' + esc(x.label) + '">✕</button></li>'; }).join('');
    document.querySelectorAll('.space .save').forEach(function (b) { b.setAttribute('aria-pressed', has(b.closest('.space').dataset.id) ? 'true' : 'false'); });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.space .save'); if (!b) return;
    var c = b.closest('.space'), id = c.dataset.id;
    if (has(id)) list = list.filter(function (x) { return x.id !== id; });
    else list.push({ id: id, label: c.dataset.label, url: c.dataset.url, size: c.dataset.size });
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
    pBtn.classList.remove('pop'); void pBtn.offsetWidth; pBtn.classList.add('pop');
    save();
  });
  pBtn.addEventListener('click', function () { panel.hidden = !panel.hidden; pBtn.setAttribute('aria-expanded', !panel.hidden); });
  pill.querySelector('.sl-x').addEventListener('click', function () { panel.hidden = true; pBtn.setAttribute('aria-expanded', 'false'); pBtn.focus(); });
  ul.addEventListener('click', function (e) { var b = e.target.closest('button[data-i]'); if (b) { list.splice(+b.dataset.i, 1); save(); } });
  pill.querySelector('.sl-clear').addEventListener('click', function () { list = []; save(); });
  pill.querySelector('.sl-send').addEventListener('click', function () {
    var form = $('inquiry'); if (!form) return;
    form.topic.value = 'Leasing space';
    form.message.value = "I'm interested in these spaces:\n" + list.map(function (x) { return '- ' + x.label + ' (' + x.size + ')'; }).join('\n') + '\n\n';
    panel.hidden = true;
    $('contact').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    setTimeout(function () { (form.name.value ? form.message : form.name).focus({ preventScroll: true }); }, reduce ? 0 : 600);
  });
  render();

  // ---------- Tour request fields ----------
  var tour = $('f-tour'), tf = $('tour-fields'), td = $('f-tdate');
  if (tour && tf) {
    var now = new Date(); now.setMinutes(now.getMinutes() - now.getTimezoneOffset()); if (td) td.min = now.toISOString().slice(0, 10);
    tour.addEventListener('change', function () { tf.hidden = !tour.checked; if (tour.checked && td) td.focus(); });
  }

  // ---------- "Notify me when space opens" ----------
  document.querySelectorAll('.alert-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value.trim()); f.querySelector('.al-err').hidden = ok;
      if (!ok) return f.email.focus();
      var b = f.querySelector('button'); b.disabled = true; b.textContent = 'Saving…';
      var fd = new FormData(f);
      var keep = fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(fd).toString() }).then(function (r) { if (!r.ok) throw 0; });
      keep.then(function () { f.hidden = true; var s = f.parentNode.querySelector('.al-sent'); s.hidden = false; s.focus(); })
        .catch(function () { b.disabled = false; b.textContent = 'Notify me'; var er = f.querySelector('.al-err'); er.textContent = "That didn't go through. Please try again or email info@ammorigroup.com."; er.hidden = false; });
    });
  });
})();
