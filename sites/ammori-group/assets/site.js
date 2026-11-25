(function () {
  var $ = function (id) { return document.getElementById(id); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  // Filter available spaces by type
  var grid = $('space-grid');
  document.querySelectorAll('.chip').forEach(function (c) {
    c.addEventListener('click', function () {
      document.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      var f = c.dataset.f, shown = 0;
      grid.querySelectorAll('.space').forEach(function (s) { var ok = f === 'all' || s.dataset.type === f; s.classList.toggle('out', !ok); if (ok) shown++; });
      $('empty').hidden = shown > 0;
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
        Name: fd.get('name'), Email: fd.get('email'), Phone: fd.get('phone') || 'Not given', 'Interested in': fd.get('topic'), Message: fd.get('message'), Page: location.href })
    }).then(function (r) { if (!r.ok) throw 0; });
    var saveIt = fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(fd).toString() })
      .then(function (r) { if (!r.ok) throw 0; });
    Promise.allSettled([emailIt, saveIt]).then(function (res) {
      if (res.some(function (x) { return x.status === 'fulfilled'; })) { form.hidden = true; var s = $('sent'); s.hidden = false; s.focus(); }
      else { b.disabled = false; b.textContent = 'Send message'; $('e-send').hidden = false; }
    });
  });
})();
