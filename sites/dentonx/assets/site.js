(function () {
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (id) { return document.getElementById(id); };

  // ----- header: solid on scroll, mobile menu -----
  var bar = $('top-bar'), menuBtn = $('menu-btn'), menu = $('menu');
  function setMenu(open) {
    if (!menu) return;
    menu.hidden = !open; menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('menu-open', open);
    if (bar) bar.classList.toggle('solid', open || window.scrollY > 40);
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(menu.hidden); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 960) setMenu(false); });
  }
  function onScroll() {
    if (bar) bar.classList.toggle('solid', window.scrollY > 40 || document.body.classList.contains('menu-open'));
    stepProgress();
  }

  // ----- reveal + chart triggers -----
  var C = 2 * Math.PI * 56;
  function fmt(n) { return Math.round(n).toLocaleString('en-US'); }
  function countUp(root) {
    root.querySelectorAll('[data-count]').forEach(function (el) {
      var end = +el.dataset.count, pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
      if (reduce) { el.textContent = pre + fmt(end) + suf; return; }
      var t0 = null, dur = 1600;
      function tick(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = pre + fmt(end * e) + suf; if (p < 1) requestAnimationFrame(tick); }
      el.textContent = pre + '0' + suf; requestAnimationFrame(tick);
    });
  }
  function drawChart(root) {
    root.querySelectorAll('.seg').forEach(function (s) {
      var len = C * (+s.dataset.pct / 100) - 2, off = C * (+s.dataset.off / 100);
      s.style.strokeDashoffset = -off; s.style.strokeDasharray = len + ' ' + (C - len);
    });
    root.querySelectorAll('.fill').forEach(function (f) { f.style.width = f.dataset.w + '%'; });
    var share = root.querySelector('.share');
    if (share) share.querySelectorAll('i').forEach(function (cell, i) { setTimeout(function () { if (i < +share.dataset.on) cell.classList.add('on'); }, reduce ? 0 : i * 18); });
  }
  document.querySelectorAll('.share').forEach(function (g) { for (var i = 0; i < 100; i++) g.appendChild(document.createElement('i')); });
  document.querySelectorAll('.seg').forEach(function (s) { s.style.strokeDasharray = '0 ' + C; });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in'); io.unobserve(e.target);
        if (e.target.querySelector('[data-count]') || e.target.hasAttribute('data-count')) countUp(e.target);
        if (e.target.classList.contains('chart')) drawChart(e.target);
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); countUp(el); if (el.classList.contains('chart')) drawChart(el); });
  }

  // ----- pipeline progress tied to scroll -----
  var stepsEl = $('steps'), sBar = $('steps-bar'), steps = stepsEl ? stepsEl.querySelectorAll('.step') : [];
  function stepProgress() {
    if (!stepsEl) return;
    var r = stepsEl.getBoundingClientRect(), vh = window.innerHeight;
    var p = Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
    if (window.innerWidth <= 900) { sBar.style.height = 'calc((100% - 56px) * ' + p + ')'; sBar.style.width = ''; }
    else { sBar.style.width = 'calc((100% - 56px) * ' + p + ')'; sBar.style.height = ''; }
    steps.forEach(function (s, i) { s.classList.toggle('on', p >= i / (steps.length - 1) - 0.02); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', stepProgress);
  onScroll();

  // ----- hero data-flow canvas -----
  var cv = $('flow');
  if (cv) {
    var ctx = cv.getContext('2d');
    var srcs = ['Bank statements', 'Credit data', 'Property records', 'Payments'];
    var outs = ['Lenders', 'Servicers', 'Investors', 'Compliance'];
    var W, H, parts = [], running = true;
    var size = function () {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    var geom = function () {
      var narrow = W < 640, pad = narrow ? 14 : Math.max(18, W * 0.06);
      var lx = pad + (narrow ? 0 : 70), rx = W - pad - (narrow ? 0 : 70), cx = W / 2, cy = H * 0.5;
      var ys = srcs.map(function (_, i) { return H * (0.16 + i * 0.23); });
      return { lx: lx, rx: rx, cx: cx, cy: cy, ys: ys, narrow: narrow, hub: narrow ? 34 : 46 };
    };
    var bez = function (p0, p1, p2, p3, t) { var u = 1 - t; return u*u*u*p0 + 3*u*u*t*p1 + 3*u*t*t*p2 + t*t*t*p3; };
    var spawn = function () {
      var side = Math.random() < 0.5 ? 0 : 1;
      parts.push({ side: side, k: Math.floor(Math.random() * 4), t: 0, sp: 0.004 + Math.random() * 0.004, c: side ? '#FFC03D' : '#3AA6E0' });
    };
    var draw = function (time) {
      var g = geom(), h = g.hub; ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1.2; ctx.strokeStyle = 'rgba(58,166,224,0.22)';
      g.ys.forEach(function (y) {
        ctx.beginPath(); ctx.moveTo(g.lx, y); ctx.bezierCurveTo(g.cx - (g.cx - g.lx) * 0.4, y, g.cx - (g.cx - g.lx) * 0.4, g.cy, g.cx - h, g.cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(g.cx + h, g.cy); ctx.bezierCurveTo(g.cx + (g.rx - g.cx) * 0.4, g.cy, g.cx + (g.rx - g.cx) * 0.4, y, g.rx, y); ctx.stroke();
      });
      parts.forEach(function (p) {
        var y = g.ys[p.k], x, yy;
        if (!p.side) { x = bez(g.lx, g.cx - (g.cx - g.lx) * 0.4, g.cx - (g.cx - g.lx) * 0.4, g.cx - h, p.t); yy = bez(y, y, g.cy, g.cy, p.t); }
        else { x = bez(g.cx + h, g.cx + (g.rx - g.cx) * 0.4, g.cx + (g.rx - g.cx) * 0.4, g.rx, p.t); yy = bez(g.cy, g.cy, y, y, p.t); }
        ctx.beginPath(); ctx.fillStyle = p.c; ctx.shadowColor = p.c; ctx.shadowBlur = 10; ctx.arc(x, yy, 2.6, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
        p.t += p.sp;
      });
      parts = parts.filter(function (p) { return p.t < 1; });
      var pulse = reduce ? 0 : (Math.sin(time / 600) + 1) / 2;
      ctx.beginPath(); ctx.fillStyle = 'rgba(58,166,224,' + (0.10 + pulse * 0.12) + ')'; ctx.arc(g.cx, g.cy, h + 16 + pulse * 10, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.fillStyle = '#1A2438'; ctx.strokeStyle = '#3AA6E0'; ctx.lineWidth = 2; ctx.arc(g.cx, g.cy, h, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#E8EDF5'; ctx.font = (g.narrow ? '600 11px' : '600 15px') + ' Unbounded, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('DentonX', g.cx, g.cy);
      ctx.font = (g.narrow ? '500 11px' : '500 13px') + ' "IBM Plex Mono", monospace';
      g.ys.forEach(function (y, i) {
        [[g.lx, srcs[i], 0, '#3AA6E0'], [g.rx, outs[i], 1, '#FFC03D']].forEach(function (n) {
          ctx.beginPath(); ctx.fillStyle = '#121A2A'; ctx.strokeStyle = n[3]; ctx.lineWidth = 2; ctx.arc(n[0], y, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
          ctx.fillStyle = '#8B97AB';
          if (g.narrow) { ctx.textAlign = n[2] ? 'right' : 'left'; ctx.fillText(n[1], n[0] + (n[2] ? 8 : -8), y - 15); }
          else { ctx.textAlign = n[2] ? 'left' : 'right'; ctx.fillText(n[1], n[0] + (n[2] ? 14 : -14), y); }
        });
      });
      if (!reduce && running) { if (Math.random() < 0.35) spawn(); requestAnimationFrame(draw); }
    };
    size();
    if (reduce) { for (var j = 0; j < 30; j++) { spawn(); parts[j].t = Math.random(); } draw(0); }
    else requestAnimationFrame(draw);
    window.addEventListener('resize', function () { size(); if (reduce) draw(0); });
    // pause when off screen to save battery on phones
    if ('IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(function (e) { var vis = e[0].isIntersecting; if (vis && !running) { running = true; requestAnimationFrame(draw); } running = vis; }).observe(cv);
    }
  }

  // ----- contact form (Netlify) -----
  var form = $('lead'), sent = $('sent');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim());
      $('e-email').hidden = ok;
      if (!ok) { form.email.focus(); return; }
      var empty = Array.prototype.find.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
      if (empty) { empty.focus(); return; }
      var btn = form.querySelector('button[type=submit]'), label = btn.firstChild.textContent;
      btn.disabled = true; btn.firstChild.textContent = 'Sending… ';
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
        .then(function (r) { if (!r.ok) throw 0; form.hidden = true; sent.hidden = false; })
        .catch(function () { btn.disabled = false; btn.firstChild.textContent = label; $('e-send').hidden = false; });
    });
  }
})();
