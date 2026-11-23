// "Build your system": visitors pick inputs and outcomes, the diagram rewires live,
// and they can request a plan (Netlify form "system-plan").
// Markup: <div class="sb" data-preset='{"in":["form"],"ai":["qualify"],"out":["crm"]}'> ... see index.html
(function () {
  document.querySelectorAll('.sb').forEach(init);

  function init(root) {
    var svg = root.querySelector('.sb-wires'), stage = root.querySelector('.sb-stage'), core = root.querySelector('.sb-core');
    var summary = root.querySelector('.sb-summary');
    var preset = {}; try { preset = JSON.parse(root.dataset.preset || '{}'); } catch (e) {}
    ['in', 'ai', 'out'].forEach(function (g) {
      (preset[g] || []).forEach(function (k) { var b = root.querySelector('[data-g="' + g + '"][data-k="' + k + '"]'); if (b) b.setAttribute('aria-pressed', 'true'); });
    });
    root.querySelectorAll('.sb-chip').forEach(function (b) {
      b.addEventListener('click', function () { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); draw(); describe(); });
    });

    function picked(g) { return Array.prototype.filter.call(root.querySelectorAll('[data-g="' + g + '"]'), function (b) { return b.getAttribute('aria-pressed') === 'true'; }); }
    function labels(list) { return list.map(function (b) { return b.dataset.say || b.textContent.trim().toLowerCase(); }); }
    function join(a) { return a.length < 2 ? (a[0] || '') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]; }

    function describe() {
      var i = labels(picked('in')), a = labels(picked('ai')), o = labels(picked('out'));
      var text;
      if (!i.length && !o.length) text = 'Pick where work comes in and what should happen next.';
      else text = (i.length ? 'When something comes in by ' + join(i) + ', ' : 'When something comes in, ') +
        'the AI agent ' + (a.length ? join(a) : 'handles it') + (o.length ? ', then ' + join(o) + '.' : '.');
      summary.textContent = text;
      var hidden = root.querySelector('input[name="system"]'); if (hidden) hidden.value = text;
      var hi = root.querySelector('input[name="inputs"]'), ha = root.querySelector('input[name="ai_tasks"]'), ho = root.querySelector('input[name="outcomes"]');
      if (hi) hi.value = i.join(', '); if (ha) ha.value = a.join(', '); if (ho) ho.value = o.join(', ');
    }

    function draw() {
      var box = stage.getBoundingClientRect(); svg.setAttribute('viewBox', '0 0 ' + box.width + ' ' + box.height);
      svg.innerHTML = '';
      var c = core.getBoundingClientRect(), vertical = window.innerWidth <= 760;
      var cx = c.left - box.left + c.width / 2, cy = c.top - box.top + c.height / 2;
      function wire(b, side, i) {
        var r = b.getBoundingClientRect(), x, y, x2, y2, d;
        if (!vertical) {
          if (side === 'in') { x = r.right - box.left; y = r.top - box.top + r.height / 2; x2 = c.left - box.left; y2 = cy; }
          else { x = c.right - box.left; y = cy; x2 = r.left - box.left; y2 = r.top - box.top + r.height / 2; }
          var mx = (x + x2) / 2; d = 'M' + x + ' ' + y + ' C ' + mx + ' ' + y + ', ' + mx + ' ' + y2 + ', ' + x2 + ' ' + y2;
        } else {
          if (side === 'in') { x = r.left - box.left + r.width / 2; y = r.bottom - box.top; x2 = cx; y2 = c.top - box.top; }
          else { x = cx; y = c.bottom - box.top; x2 = r.left - box.left + r.width / 2; y2 = r.top - box.top; }
          var my = (y + y2) / 2; d = 'M' + x + ' ' + y + ' C ' + x + ' ' + my + ', ' + x2 + ' ' + my + ', ' + x2 + ' ' + y2;
        }
        var base = document.createElementNS('http://www.w3.org/2000/svg', 'path'); base.setAttribute('d', d); base.setAttribute('class', 'sb-w'); svg.appendChild(base);
        var p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); p.setAttribute('class', 'sb-p ' + side);
        p.style.animationDelay = (i * 0.35 + (side === 'out' ? 0.9 : 0)) + 's'; svg.appendChild(p);
      }
      picked('in').forEach(function (b, i) { wire(b, 'in', i); });
      picked('out').forEach(function (b, i) { wire(b, 'out', i); });
      core.classList.toggle('live', picked('in').length > 0 && picked('out').length > 0);
    }

    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(draw, 80); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
    draw(); describe();

    // request a plan
    var form = root.querySelector('.sb-form'), sent = root.querySelector('.sb-sent');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault(); describe();
      var err = root.querySelector('.sb-err');
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim());
      if (!picked('in').length && !picked('out').length) { err.textContent = 'Pick at least one input and one outcome first.'; err.hidden = false; return; }
      if (!ok) { err.textContent = 'Enter an email address like name@company.com.'; err.hidden = false; form.email.focus(); return; }
      err.hidden = true;
      var b = form.querySelector('button'); b.disabled = true; b.textContent = 'Sending…';
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(form)).toString() })
        .then(function (r) { if (!r.ok) throw 0; form.hidden = true; sent.hidden = false; if (window.fbq) fbq('track', 'Lead'); })
        .catch(function () { b.disabled = false; b.textContent = 'Send me this plan'; err.textContent = "That didn't send. Please try again."; err.hidden = false; });
    });
  }
})();
