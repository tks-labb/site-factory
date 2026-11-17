// Konnect AI chat widget: talks to /api/chat (Netlify Function).
(function () {
  var BOOK = 'https://calendar.app.google/ZGPwJmMpcz3yWbkt5';
  var history = [], busy = false;
  var root = document.createElement('div');
  root.className = 'kc';
  root.innerHTML =
    '<button class="kc-open" type="button" aria-expanded="false" aria-controls="kc-panel"><span class="kc-dot" aria-hidden="true"></span><span>Ask our AI</span></button>' +
    '<section class="kc-panel" id="kc-panel" role="dialog" aria-label="Chat with Konnect AI" hidden>' +
      '<header class="kc-head"><div><b>Konnect AI assistant</b><small>AI-powered · may make mistakes</small></div><button class="kc-x" type="button" aria-label="Close chat">✕</button></header>' +
      '<div class="kc-log" aria-live="polite"></div>' +
      '<div class="kc-chips"></div>' +
      '<form class="kc-form"><label class="kc-sr" for="kc-in">Message</label><input id="kc-in" autocomplete="off" maxlength="1500" placeholder="Ask about automation or websites…"><button type="submit" aria-label="Send">↑</button></form>' +
    '</section>';
  document.body.appendChild(root);
  var openBtn = root.querySelector('.kc-open'), panel = root.querySelector('.kc-panel'), log = root.querySelector('.kc-log'),
      form = root.querySelector('.kc-form'), input = root.querySelector('#kc-in'), chips = root.querySelector('.kc-chips');

  function linkify(text) {
    var frag = document.createDocumentFragment();
    text.split(/(https?:\/\/[^\s)]+)/g).forEach(function (part, i) {
      if (i % 2) { var a = document.createElement('a'); a.href = part; a.target = '_blank'; a.rel = 'noopener'; a.textContent = part.indexOf('calendar') > -1 ? 'Book a call →' : part; frag.appendChild(a); }
      else frag.appendChild(document.createTextNode(part));
    });
    return frag;
  }
  function add(role, text) {
    var m = document.createElement('div'); m.className = 'kc-msg ' + role;
    m.appendChild(linkify(text)); log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
  }
  function typing(on) {
    var t = log.querySelector('.kc-typing');
    if (on && !t) { t = document.createElement('div'); t.className = 'kc-msg bot kc-typing'; t.innerHTML = '<i></i><i></i><i></i>'; log.appendChild(t); log.scrollTop = log.scrollHeight; }
    if (!on && t) t.remove();
  }
  function send(text) {
    text = text.trim(); if (!text || busy) return;
    chips.hidden = true; add('me', text); history.push({ role: 'user', content: text });
    busy = true; typing(true); input.value = '';
    fetch('/api/chat', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ messages: history.slice(-12) }) })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        typing(false);
        if (res.ok && res.d.reply) { add('bot', res.d.reply); history.push({ role: 'assistant', content: res.d.reply }); }
        else { history.pop(); add('bot', (res.d && res.d.error ? res.d.error + ' ' : '') + 'You can also email tristan@getkonnectai.com or book a call: ' + BOOK); }
      })
      .catch(function () { typing(false); history.pop(); add('bot', "I couldn't connect. Email tristan@getkonnectai.com or book a call: " + BOOK); })
      .then(function () { busy = false; input.focus(); });
  }
  function setOpen(o) {
    panel.hidden = !o; openBtn.setAttribute('aria-expanded', o ? 'true' : 'false'); root.classList.toggle('on', o);
    if (o) {
      if (!log.children.length) {
        add('bot', "Hi! I'm Konnect AI's assistant. Tell me about a task that eats up your team's time, or ask about our websites.");
        ['What can you automate?', 'Do you build websites?', 'How does it work?'].forEach(function (q) {
          var c = document.createElement('button'); c.type = 'button'; c.textContent = q; c.addEventListener('click', function () { send(q); }); chips.appendChild(c);
        });
      }
      setTimeout(function () { input.focus(); }, 50);
    } else openBtn.focus();
  }
  openBtn.addEventListener('click', function () { setOpen(panel.hidden); });
  root.querySelector('.kc-x').addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) setOpen(false); });
  form.addEventListener('submit', function (e) { e.preventDefault(); send(input.value); });
  document.querySelectorAll('[data-open-chat]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); setOpen(true); }); });
})();
