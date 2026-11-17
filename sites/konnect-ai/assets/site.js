(function () {
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; // soften motion, never remove it
  var $ = function (id) { return document.getElementById(id); };

  // hero headline word-in
  if ($('hero')) requestAnimationFrame(function () { setTimeout(function () { $('hero').classList.add('go'); }, 60); });

  // mobile menu
  var menuBtn = $('menu-btn'), menu = $('menu');
  function setMenu(open) { menu.hidden = !open; menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); document.body.classList.toggle('menu-open', open); }
  menuBtn.addEventListener('click', function () { setMenu(menu.hidden); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 900) setMenu(false); });

  // reveal on scroll + run example flows
  function runFlow(ol) {
    var items = ol.querySelectorAll('li'), i = 0;
    function step() {
      items.forEach(function (li, k) { li.classList.toggle('on', k <= i); });
      i++;
      if (i < items.length) setTimeout(step, reduce ? 500 : 650);
      else setTimeout(function () { i = 0; items.forEach(function (li) { li.classList.remove('on'); }); setTimeout(step, 600); }, 2600);
    }
    step();
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in'); io.unobserve(e.target);
      var flow = e.target.querySelector('.flow'); if (flow) runFlow(flow);
    });
  }, { threshold: 0.01, rootMargin: '0px 0px -8% 0px' }) : null;
  document.querySelectorAll('.rv').forEach(function (el) { if (io) io.observe(el); else { el.classList.add('in'); var f = el.querySelector('.flow'); if (f) runFlow(f); } });

  // process steps fill with scroll
  var stepsEl = $('steps'), bar = $('steps-bar'), steps = stepsEl ? stepsEl.querySelectorAll('li') : [];
  function stepProgress() {
    if (!stepsEl) return;
    var r = stepsEl.getBoundingClientRect(), vh = window.innerHeight;
    var p = Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
    if (window.innerWidth <= 860) { bar.style.height = 'calc((100% - 44px) * ' + p + ')'; bar.style.width = ''; }
    else { bar.style.width = 'calc((100% - 44px) * ' + p + ')'; bar.style.height = ''; }
    steps.forEach(function (s, i) { s.classList.toggle('on', p >= i / (steps.length - 1) - 0.02); });
  }
  window.addEventListener('scroll', stepProgress, { passive: true });
  window.addEventListener('resize', stepProgress);
  stepProgress();

  // example activity feed (clearly labelled demo)
  var feed = $('feed');
  if (feed) {
  var events = [
    ['New lead from web form', 'AI replied in 40 sec'],
    ['Missed call', 'AI voice agent answered'],
    ['Quote request', 'Missing details collected by text'],
    ['Invoice PDF received', 'Totals filed in spreadsheet'],
    ['Lead qualified', 'Meeting booked for 10:30'],
    ['Daily report', 'Sent to the team inbox'],
    ['New review request', 'Sent after completed job'],
    ['Website form', 'Lead added to CRM']
  ];
  var ei = 0, mins = 8 * 60 + 2;
  function clock() { var h = Math.floor(mins / 60) % 24, m = mins % 60, ap = h >= 12 ? 'pm' : 'am'; h = h % 12 || 12; return h + ':' + (m < 10 ? '0' : '') + m + ap; }
  function push() {
    var e = events[ei % events.length]; ei++; mins += 7 + Math.floor(Math.random() * 23);
    var li = document.createElement('li');
    li.innerHTML = '<time>' + clock() + '</time><span><b></b> → <span class="ok"></span></span>';
    li.querySelector('b').textContent = e[0]; li.querySelector('.ok').textContent = e[1];
    feed.insertBefore(li, feed.firstChild);
    while (feed.children.length > 6) feed.removeChild(feed.lastChild);
  }
  for (var k = 0; k < 3; k++) push();
  var feedTimer = setInterval(push, reduce ? 4200 : 2600);
  document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(feedTimer); else feedTimer = setInterval(push, reduce ? 4200 : 2600); });
  }

  // cost calculator with animated number
  var hrs = $('c-hours'), ppl = $('c-people'), rate = $('c-rate'), out = $('r-cost'), shown = 31200;
  if (hrs) {
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function calc() {
    $('o-hours').textContent = hrs.value; $('o-people').textContent = ppl.value; $('o-rate').textContent = '$' + rate.value;
    var hours = hrs.value * ppl.value * 52, cost = hours * rate.value;
    $('r-hours').textContent = hours.toLocaleString('en-US') + ' hours a year';
    $('r-meter').style.width = Math.min(100, cost / 2000) + '%';
    var from = shown, t0 = null, dur = 500;
    function tick(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3); out.textContent = money(from + (cost - from) * e); if (p < 1) requestAnimationFrame(tick); else shown = cost; }
    requestAnimationFrame(tick);
  }
  [hrs, ppl, rate].forEach(function (el) { el.addEventListener('input', calc); });
  calc();
  // email the estimate (Netlify form "estimate")
  var est = $('estimate');
  if (est) est.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(est.email.value.trim());
    $('e-est').hidden = ok; if (!ok) { est.email.focus(); return; }
    est.hours.value = hrs.value; est.people.value = ppl.value; est.rate.value = rate.value; est.yearly_cost.value = out.textContent;
    var b = est.querySelector('button'); b.disabled = true; b.textContent = 'Sending…';
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(est)).toString() })
      .then(function (r) { if (!r.ok) throw 0; est.hidden = true; $('est-sent').hidden = false; })
      .catch(function () { b.disabled = false; b.textContent = 'Send me the plan'; $('e-est').textContent = "That didn't send. Please try again."; $('e-est').hidden = false; });
  });
  }

  // copy buttons
  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var done = function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1600); };
      try { navigator.clipboard.writeText(btn.dataset.copy).then(done, function () {}); } catch (e) {}
    });
  });

  // contact form (Netlify)
  var form = $('lead'), sent = $('sent');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var okE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim()), okP = form.phone.value.replace(/\D/g, '').length >= 10;
    $('e-email').hidden = okE; $('e-phone').hidden = okP;
    if (!okP) { form.phone.focus(); return; }
    if (!okE) { form.email.focus(); return; }
    var empty = Array.prototype.find.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (empty) { empty.focus(); return; }
    var btn = form.querySelector('button[type=submit]'); btn.disabled = true; btn.firstChild.textContent = 'Sending… ';
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
      .then(function (r) { if (!r.ok) throw 0; form.hidden = true; sent.hidden = false; })
      .catch(function () { btn.disabled = false; btn.firstChild.textContent = 'Send my request '; $('e-send').hidden = false; });
  });
})();
