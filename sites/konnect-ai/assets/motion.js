// Konnect AI motion layer: logo intro, staggering, filters, rubber banding,
// prefetching, follow-through and success moments.
(function () {
  var d = document.documentElement, reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fire() { window.__introDone = true; window.dispatchEvent(new Event('introdone')); }

  // ---------- Logo intro (first visit, refresh, or logo click) ----------
  document.querySelectorAll('[data-intro-link]').forEach(function (a) {
    a.addEventListener('click', function () { try { sessionStorage.setItem('k_logo', '1'); } catch (e) {} });
  });
  var ov = document.querySelector('.intro-ov');
  if (d.classList.contains('intro') && ov) {
    var finished = false;
    var finish = function () {
      if (finished) return; finished = true;
      var stage = ov.querySelector('.intro-stage'), big = ov.querySelector('.intro-logo').getBoundingClientRect(), sr = stage.getBoundingClientRect();
      var small = document.querySelector('.top .brand .logo'), tr = small ? small.getBoundingClientRect() : null;
      if (tr && tr.width) {
        var s = tr.width / big.width, scx = sr.left + sr.width / 2, scy = sr.top + sr.height / 2;
        var lcx = big.left + big.width / 2, lcy = big.top + big.height / 2;
        stage.style.setProperty('--ts', s.toFixed(3));
        stage.style.setProperty('--tx', (tr.left + tr.width / 2 - scx - s * (lcx - scx)).toFixed(1) + 'px');
        stage.style.setProperty('--ty', (tr.top + tr.height / 2 - scy - s * (lcy - scy)).toFixed(1) + 'px');
      }
      d.classList.add('intro-out');
      setTimeout(function () { d.classList.remove('intro', 'intro-out'); d.classList.add('intro-done'); fire(); }, 650);
      setTimeout(fire, 250); // let the page start moving while the logo flies home
    };
    var elapsed = performance.now();
    var t = setTimeout(finish, Math.max(150, (reduce ? 900 : 1750) - elapsed));
    var skip = function () { clearTimeout(t); finish(); };
    ov.addEventListener('click', skip);
    window.addEventListener('keydown', skip, { once: true });
    window.addEventListener('wheel', skip, { once: true, passive: true });
    window.addEventListener('touchmove', skip, { once: true, passive: true });
  } else { fire(); }

  // ---------- Staggered entrances ----------
  ['.builds', '.promise', '.rgrid', '.webs', '.tracks', '.outs', '.roles'].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (box) {
      box.classList.add('stg');
      Array.prototype.forEach.call(box.children, function (c, i) { c.classList.remove('rv', 'd1', 'd2', 'd3'); c.style.setProperty('--i', i); });
    });
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.stg').forEach(function (el) { io.observe(el); });
  } else document.querySelectorAll('.stg').forEach(function (el) { el.classList.add('in'); });

  // ---------- Follow-through: toggles pop, the AI core reacts (secondary action) ----------
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.sb-chip, .ftab'); if (!b) return;
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
    var core = b.closest('.sb') && b.closest('.sb').querySelector('.sb-core');
    if (core) { core.classList.remove('bump'); void core.offsetWidth; core.classList.add('bump'); }
  });
  document.addEventListener('animationend', function (e) { e.target.classList && e.target.classList.remove('pop', 'bump', 'enter'); });

  // ---------- Industry filter (Hick's law) ----------
  var grid = document.getElementById('ind-grid');
  document.querySelectorAll('.ftab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.ftab').forEach(function (t) { t.setAttribute('aria-pressed', t === tab ? 'true' : 'false'); });
      var f = tab.dataset.f, n = 0;
      grid.querySelectorAll('.ind').forEach(function (c) {
        var show = f === 'all' || c.dataset.cat === f;
        c.classList.toggle('out', !show);
        if (show) { c.style.setProperty('--n', n++); c.classList.remove('enter'); void c.offsetWidth; c.classList.add('enter'); }
      });
    });
  });

  // ---------- Rubber banding on the reviews strip ----------
  document.querySelectorAll('.rmarquee').forEach(function (m) {
    var track = m.querySelector('.rtrack'); if (!track) return;
    var wrap = document.createElement('div'); wrap.className = 'rtrack-wrap';
    track.parentNode.insertBefore(wrap, track); wrap.appendChild(track);
    var x0 = null, moved = false;
    m.addEventListener('pointerdown', function (e) { x0 = e.clientX; moved = false; m.classList.add('dragging'); track.style.animationPlayState = 'paused'; m.setPointerCapture(e.pointerId); });
    m.addEventListener('pointermove', function (e) {
      if (x0 === null) return; var dx = e.clientX - x0; if (Math.abs(dx) > 4) moved = true;
      var band = dx / (1 + Math.abs(dx) / 260);           // resistance grows the further you pull
      wrap.style.transform = 'translateX(' + band.toFixed(1) + 'px)';
    });
    function release() { if (x0 === null) return; x0 = null; m.classList.remove('dragging'); wrap.style.transform = ''; track.style.animationPlayState = ''; }
    m.addEventListener('pointerup', release); m.addEventListener('pointercancel', release);
    m.addEventListener('click', function (e) { if (moved) e.preventDefault(); }, true);
  });

  // ---------- Doherty threshold: prefetch pages before the click lands ----------
  var done = {};
  function prefetch(a) {
    var href = a.getAttribute('href'); if (!href || !/\.html(#.*)?$/.test(href) || a.target === '_blank') return;
    var url = new URL(href, location.href); url.hash = '';
    if (url.origin !== location.origin || done[url.href] || url.pathname === location.pathname) return;
    done[url.href] = 1; var l = document.createElement('link'); l.rel = 'prefetch'; l.href = url.href; document.head.appendChild(l);
  }
  document.addEventListener('pointerover', function (e) { var a = e.target.closest && e.target.closest('a[href]'); if (a) prefetch(a); }, { passive: true });
  document.addEventListener('touchstart', function (e) { var a = e.target.closest && e.target.closest('a[href]'); if (a) prefetch(a); }, { passive: true });

  // ---------- Thumb-zone action bar ----------
  var bar = document.getElementById('actionbar');
  if (bar) {
    var onScroll = function () { bar.classList.toggle('show', window.scrollY > 420); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }


  // ---------- Rotating outcome line under the headline ----------
  var rot = document.getElementById('rot');
  if (rot) {
    var words = rot.querySelectorAll('b'), wi = 0;
    var spin = function () {
      var cur = words[wi]; wi = (wi + 1) % words.length; var nxt = words[wi];
      cur.classList.remove('on'); cur.classList.add('off');
      nxt.classList.remove('off'); void nxt.offsetWidth; nxt.classList.add('on');
      setTimeout(function () { cur.classList.remove('off'); }, 500);
    };
    var rotTimer = setInterval(spin, reduce ? 5000 : 2800);
    document.addEventListener('visibilitychange', function () { clearInterval(rotTimer); if (!document.hidden) rotTimer = setInterval(spin, reduce ? 5000 : 2800); });
  }

  // ---------- Outcome pillars animate when they scroll in ----------
  var outs = document.querySelectorAll('.out');
  if (outs.length && 'IntersectionObserver' in window) {
    var oio = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('in', e.isIntersecting); }); }, { threshold: 0.25 });
    outs.forEach(function (o) { oio.observe(o); });
  } else outs.forEach(function (o) { o.classList.add('in'); });


  // ---------- Careers: role buttons pre-select the form, form submits with the resume ----------
  document.querySelectorAll('[data-role]').forEach(function (a) {
    a.addEventListener('click', function () { var sel = document.getElementById('a-role'), card = a.closest('.role'); if (sel && card) sel.value = card.querySelector('h3').textContent; });
  });
  var apply = document.getElementById('apply-form');
  if (apply) apply.addEventListener('submit', function (e) {
    e.preventDefault();
    var $$ = function (id) { return document.getElementById(id); };
    var okE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(apply.email.value.trim()); $$('a-e-email').hidden = okE;
    var f = apply.resume.files[0], okF = !f || f.size <= 8 * 1024 * 1024; $$('a-e-cv').hidden = okF;
    if (!okE) { apply.email.focus(); return; } if (!okF) { apply.resume.focus(); return; }
    var empty = Array.prototype.find.call(apply.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (empty) { empty.focus(); return; }
    var btn = apply.querySelector('button[type=submit]'), label = btn.firstChild.textContent; btn.disabled = true; btn.firstChild.textContent = 'Sending… ';
    fetch('/', { method: 'POST', body: new FormData(apply) })   /* multipart, so the resume file is included */
      .then(function (r) { if (!r.ok) throw 0; apply.hidden = true; $$('apply-sent').hidden = false; if (window.fbq) fbq('track', 'SubmitApplication'); })
      .catch(function () { btn.disabled = false; btn.firstChild.textContent = label; $$('a-e-send').hidden = false; });
  });

  // ---------- Peak-end: celebrate every successful submission ----------
  var colors = ['var(--accent)', 'var(--red)', 'var(--live)', '#FFB020'];
  function celebrate(el) {
    if (el.dataset.celebrated) return; el.dataset.celebrated = '1'; el.classList.add('celebrate');
    var ok = '<svg class="okmark" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="19" pathLength="1"/><path d="M13 22.5l6 6 12-13" pathLength="1"/></svg>';
    var burst = '<span class="burst" aria-hidden="true">' + Array.apply(null, Array(10)).map(function (_, i) {
      var a = (i / 10) * Math.PI * 2, r = 46 + (i % 3) * 14;
      return '<i style="--x:' + Math.round(Math.cos(a) * r) + 'px;--y:' + Math.round(Math.sin(a) * r) + 'px;--c:' + colors[i % 4] + '"></i>';
    }).join('') + '</span>';
    el.insertAdjacentHTML('afterbegin', ok + (reduce ? '' : burst));
  }
  var targets = document.querySelectorAll('.sent, .sb-sent, #est-sent, #apply-sent');
  if ('MutationObserver' in window) targets.forEach(function (el) {
    new MutationObserver(function () { if (!el.hidden) celebrate(el); }).observe(el, { attributes: true, attributeFilter: ['hidden'] });
  });
})();
