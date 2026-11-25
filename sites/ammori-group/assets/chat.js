// Ammori Group AI chat widget: talks to /api/chat (Netlify Function).
(function () {
  var EMAIL = 'info@ammorigroup.com';
  var history = [], busy = false;
  var root = document.createElement('div');
  root.className = 'ac';
  root.innerHTML =
    '<button class="ac-open" type="button" aria-expanded="false" aria-controls="ac-panel"><span class="dot" aria-hidden="true"></span><span class="lbl">Ask about our spaces</span><span class="lbl-s">Ask AI</span><span class="sr">Open chat</span></button>' +
    '<section class="ac-panel" id="ac-panel" role="dialog" aria-label="Chat with Ammori Group" hidden>' +
      '<header class="ac-head"><img class="logo" src="assets/mark-sm.png" alt="" width="56" height="30"><div><b>Ammori Group assistant</b><small>AI-powered · may make mistakes</small></div><button class="ac-x" type="button" aria-label="Close chat">✕</button></header>' +
      '<div class="ac-log" aria-live="polite"></div>' +
      '<div class="ac-chips"></div>' +
      '<form class="ac-form"><label class="sr" for="ac-in">Message</label><input id="ac-in" autocomplete="off" maxlength="1500" placeholder="Ask about space, sizes, locations…"><button type="submit" aria-label="Send">↑</button></form>' +
    '</section>';
  document.body.appendChild(root);
  var openBtn = root.querySelector('.ac-open'), panel = root.querySelector('.ac-panel'), log = root.querySelector('.ac-log'),
      form = root.querySelector('.ac-form'), input = root.querySelector('#ac-in'), chips = root.querySelector('.ac-chips'), sendBtn = form.querySelector('button');

  function linkify(text) {
    var frag = document.createDocumentFragment();
    text.split(/(https?:\/\/[^\s)]+|[\w.+-]+@[\w-]+\.[\w.]+)/g).forEach(function (part, i) {
      if (i % 2) {
        var a = document.createElement('a'), clean = part.replace(/[.,]$/, ''), tail = part.slice(clean.length);
        if (clean.indexOf('@') > -1 && clean.indexOf('http') !== 0) { a.href = 'mailto:' + clean; a.textContent = clean; }
        else { a.href = clean; a.textContent = /#contact$/.test(clean) ? 'the inquiry form' : clean.replace(/^https?:\/\//, ''); if (/#contact$/.test(clean)) a.addEventListener('click', function (e) { var c = document.getElementById('contact'); if (c) { e.preventDefault(); close(); c.scrollIntoView({ behavior: 'smooth' }); } }); }
        frag.appendChild(a); if (tail) frag.appendChild(document.createTextNode(tail));
      } else frag.appendChild(document.createTextNode(part));
    });
    return frag;
  }
  function add(role, text) { var m = document.createElement('div'); m.className = 'ac-msg ' + role; m.appendChild(linkify(text)); log.appendChild(m); log.scrollTop = log.scrollHeight; }
  function typing(on) {
    var t = log.querySelector('.ac-wait');
    if (on && !t) { t = document.createElement('div'); t.className = 'ac-msg bot ac-wait'; t.innerHTML = '<span class="ac-typing"><i></i><i></i><i></i></span>'; log.appendChild(t); log.scrollTop = log.scrollHeight; }
    if (!on && t) t.remove();
  }
  function send(text) {
    text = text.trim(); if (!text || busy) return;
    chips.hidden = true; add('me', text); history.push({ role: 'user', content: text });
    busy = true; sendBtn.disabled = true; typing(true);
    fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ messages: history }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        typing(false);
        if (res.ok && res.j.reply) { add('bot', res.j.reply); history.push({ role: 'assistant', content: res.j.reply }); }
        else { history.pop(); add('bot', (res.j && res.j.error ? res.j.error + ' ' : '') + 'You can also reach our team at ' + EMAIL + ' or through the inquiry form.'); }
      })
      .catch(function () { typing(false); history.pop(); add('bot', "I couldn't connect just now. Please email " + EMAIL + ' or use the inquiry form.'); })
      .then(function () { busy = false; sendBtn.disabled = false; input.focus(); });
  }
  function open() { panel.hidden = false; openBtn.setAttribute('aria-expanded', 'true'); if (!log.children.length) start(); setTimeout(function () { input.focus(); }, 50); }
  function close() { panel.hidden = true; openBtn.setAttribute('aria-expanded', 'false'); openBtn.focus(); }
  function start() {
    add('bot', "Hi! I can help you find office, medical or retail space in our buildings, or answer questions about selling a property to Ammori Group. What are you looking for?");
    ['What spaces are available?', 'Do you have medical office space?', 'I need about 4,000 SF', 'I want to sell a building'].forEach(function (q) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = q; b.addEventListener('click', function () { send(q); }); chips.appendChild(b);
    });
  }
  openBtn.addEventListener('click', function () { panel.hidden ? open() : close(); });
  root.querySelector('.ac-x').addEventListener('click', close);
  panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); var v = input.value; input.value = ''; send(v); });
})();
