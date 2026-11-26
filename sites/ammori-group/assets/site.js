(function () {
  var $ = function (id) { return document.getElementById(id); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var d = document.documentElement;

  // Opening: drone video of 5600 Crooks Road (first visit in a session). Falls back to the
  // gold line drawing when motion is reduced, data saver is on, or the video can't start quickly.
  var pickSrc = function (v) {
    var src = window.innerWidth <= 700 ? v.dataset.srcSm : v.dataset.src;
    var mp4 = v.canPlayType('video/mp4; codecs="avc1.640028"'), webm = v.canPlayType('video/webm; codecs="vp9"');
    return (!mp4 && webm) ? src.replace(/\.mp4$/, '.webm') : src;
  };
  if (d.classList.contains('intro')) {
    var done = false, ev = ['click', 'keydown', 'wheel', 'touchmove'], t1, guard;
    var vid = document.querySelector('.ix-video'), conn = navigator.connection;
    var slow = conn && (conn.saveData || /(^|-)2g/.test(conn.effectiveType || ''));
    var out = function () {
      if (done) return; done = true; clearTimeout(t1); clearTimeout(guard);
      ev.forEach(function (n) { window.removeEventListener(n, out); });
      d.classList.add('intro-out');
      setTimeout(function () { d.classList.remove('intro', 'intro-out', 'ix-vid', 'ix-draw', 'ix-land'); if (vid) vid.pause(); }, reduce ? 450 : 1050);
    };
    var drawMode = function () {
      if (done || d.classList.contains('ix-draw')) return;
      clearTimeout(t1); clearTimeout(guard); if (vid) vid.pause();
      d.classList.remove('ix-vid'); d.classList.add('ix-draw');
      t1 = setTimeout(out, reduce ? 1200 : 3900);
    };
    if (vid && !reduce && !slow) {
      d.classList.add('ix-vid');
      var started = false;
      vid.addEventListener('playing', function () { started = true; clearTimeout(guard); });
      vid.addEventListener('timeupdate', function () { if (vid.currentTime > 6.3) d.classList.add('ix-land'); });
      vid.addEventListener('ended', function () { t1 = setTimeout(out, 1100); });
      vid.addEventListener('error', drawMode);
      vid.src = pickSrc(vid);
      var pr = vid.play(); if (pr && pr.catch) pr.catch(drawMode);
      guard = setTimeout(function () { if (!started) drawMode(); }, 3000);
      t1 = setTimeout(out, 13000);
    } else drawMode();
    setTimeout(function () { if (!done) ev.forEach(function (n) { window.addEventListener(n, out, { passive: true }); }); }, 300);
  }

  // Hero panel: the drone video loops quietly behind the stats (not with reduced motion or data saver)
  var hv = document.querySelector('.hero-video');
  if (hv && !reduce && !(navigator.connection && navigator.connection.saveData) && 'IntersectionObserver' in window) {
    var hio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { if (!hv.src) { hv.src = pickSrc(hv); hv.addEventListener('playing', function () { hv.classList.add('on'); }, { once: true }); } var p = hv.play(); if (p && p.catch) p.catch(function () {}); }
        else hv.pause();
      });
    }, { threshold: .2 });
    hio.observe(hv);
  }

  // Light / dark mode (remembers the visitor's choice; otherwise follows their device)
  var tbtn = $('theme-btn');
  function isDark() { var t = d.getAttribute('data-theme'); return t ? t === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches; }
  function label() { tbtn.setAttribute('aria-label', isDark() ? 'Switch to light mode' : 'Switch to dark mode'); }
  if (tbtn) { label(); tbtn.addEventListener('click', function () {
    var next = isDark() ? 'light' : 'dark'; d.setAttribute('data-theme', next);
    try { localStorage.setItem('am_theme', next); } catch (e) {}
    label();
  }); }

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' }) : null;
  document.querySelectorAll('.rv, .hero-art').forEach(function (el) { io ? io.observe(el) : el.classList.add('in'); });

  // Count-up on the hero stats (once)
  if (!reduce) document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = +el.dataset.count, t0 = null; if (!target) return;
    el.textContent = '0';
    setTimeout(function () {
      requestAnimationFrame(function step(t) {
        if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1400), v = Math.round(target * (1 - Math.pow(1 - k, 3)));
        el.textContent = v.toLocaleString('en-US'); if (k < 1) requestAnimationFrame(step);
      });
    }, 500);
  });

  // Header hairline once the page scrolls
  var bar = $('top-bar'); var onS = function () { bar.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onS, { passive: true }); onS();

  // Mobile menu
  var btn = $('menu-btn'), nav = $('nav');
  btn.addEventListener('click', function () { var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });

  // Highlight the section in view
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="index.html#"]'));
  if ('IntersectionObserver' in window && document.querySelector('#spaces')) {
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) links.forEach(function (l) { if (l.hash === '#' + e.target.id) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current'); }); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (l) { var s = document.querySelector(l.hash); if (s) nio.observe(s); });
  }

  // Property photo gallery: click a photo to see it larger
  var lb = $('lightbox'), tiles = Array.prototype.slice.call(document.querySelectorAll('.g-tile')), cur = 0;
  if (lb && lb.showModal && tiles.length) {
    var img = lb.querySelector('img');
    var show = function (n) { cur = (n + tiles.length) % tiles.length; img.src = tiles[cur].dataset.full; img.alt = tiles[cur].dataset.alt; };
    tiles.forEach(function (t, n) { t.addEventListener('click', function () { show(n); lb.showModal(); }); });
    lb.querySelector('.lb-x').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });
  }

  // Portfolio filter: all / with space available / fully leased
  var pgrid = $('prop-grid');
  document.querySelectorAll('.pchip').forEach(function (c) {
    c.addEventListener('click', function () {
      document.querySelectorAll('.pchip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      pgrid.querySelectorAll('.prop').forEach(function (p) { p.classList.toggle('out', c.dataset.p !== 'all' && p.dataset.avail !== c.dataset.p); });
    });
  });

  // "Inquire" buttons pre-fill the form
  var form = $('inquiry');
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-space], [data-topic]'); if (!a || !form) return;
    e.preventDefault();
    if (a.dataset.topic) form.topic.value = a.dataset.topic;
    if (a.dataset.space) { form.topic.value = 'Leasing space'; if (!form.message.value.trim() || /^I'm interested in /.test(form.message.value)) form.message.value = "I'm interested in " + a.dataset.space + '. '; }
    $('contact').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    setTimeout(function () { (form.name.value ? form.message : form.name).focus({ preventScroll: true }); }, reduce ? 0 : 600);
  });

  // Inquiry form: email to Ammori Group (FormSubmit) and a backup copy in Netlify Forms
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var okN = !!form.name.value.trim(), okE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim()), okM = !!form.message.value.trim();
    $('e-name').hidden = okN; $('e-email').hidden = okE; $('e-msg').hidden = okM;
    if (!okN) return form.name.focus(); if (!okE) return form.email.focus(); if (!okM) return form.message.focus();
    var b = form.querySelector('button[type=submit]'); b.disabled = true; b.textContent = 'Sending…'; $('e-send').hidden = true;
    var fd = new FormData(form);
    var emailIt = fetch('https://formsubmit.co/ajax/info@ammorigroup.com', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ _subject: 'New website inquiry: ' + fd.get('topic') + ' from ' + fd.get('name'), _template: 'table', _captcha: 'false', _replyto: fd.get('email'),
        Name: fd.get('name'), Email: fd.get('email'), Phone: fd.get('phone') || 'Not given', 'Interested in': fd.get('topic'), Message: fd.get('message'), 'Tour requested': fd.get('tour') ? 'Yes: ' + (fd.get('tour_date') || 'date open') + ', ' + (fd.get('tour_time') || '') : 'No', Page: location.href })
    }).then(function (r) { if (!r.ok) throw 0; });
    var saveIt = fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(fd).toString() })
      .then(function (r) { if (!r.ok) throw 0; });
    Promise.allSettled([emailIt, saveIt]).then(function (res) {
      if (res.some(function (x) { return x.status === 'fulfilled'; })) { form.hidden = true; var s = $('sent'); s.hidden = false; s.focus(); }
      else { b.disabled = false; b.textContent = 'Send message'; $('e-send').hidden = false; }
    });
  });
})();
