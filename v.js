/* Va Va Voom: shared behaviour for the style branches (v-buzz, v-pink, v-grounded, tongham).
   Forms post to the same catcher as the main page (window.VVV_URL). */
(function () {
  var URL = window.VVV_URL || '';
  var PAGE = location.pathname;
  function send(data) {
    data.page = PAGE; data.when = new Date().toISOString(); data.version = window.VVV_VERSION || '';
    if (URL) { try { fetch(URL, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}); } catch (e) {} }
    else { try { var a = JSON.parse(localStorage.getItem('vvv-local') || '[]'); a.push(data); localStorage.setItem('vvv-local', JSON.stringify(a)); } catch (e) {} }
  }
  function signal(ev, detail) { send({ type: 'signal', event: ev, detail: detail || '' }); }
  window.vvvSignal = signal;

  /* ---------- the one form ---------- */
  var m = document.getElementById('vf');
  if (m) {
    var form = m.querySelector('form'), h = m.querySelector('#vf-h'), p = m.querySelector('#vf-p'),
      big = m.querySelector('#vf-big'), bigL = m.querySelector('#vf-bigl'), contact = m.querySelector('#vf-contact'),
      err = m.querySelector('.vf-err'), done = m.querySelector('.vf-done'), body = m.querySelector('.vf-body');
    var ctx = {}, opened = 0, last = null;
    window.vvvOpenForm = function (o) {
      ctx = o; opened = Date.now(); last = document.activeElement;
      form.reset(); err.textContent = ''; body.hidden = false; done.hidden = true;
      h.textContent = o.title || 'Add a thought';
      p.textContent = o.prompt || '';
      var quick = o.kind === 'quick';
      big.parentNode.hidden = quick; contact.parentNode.hidden = !quick;
      bigL.textContent = o.label || 'Your idea, thought or feeling';
      m.hidden = false; document.body.style.overflow = 'hidden';
      setTimeout(function () { (quick ? m.querySelector('#vf-name') : big).focus(); }, 40);
      signal('form opened', (o.thread || '') + (o.tag ? ' / ' + o.tag : '') + (quick ? ' quick' : ''));
    };
    function close() { m.hidden = true; document.body.style.overflow = ''; if (last) try { last.focus(); } catch (e) {} }
    m.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', close); });
    m.addEventListener('click', function (e) { if (e.target === m) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !m.hidden) close(); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.name.value.trim(), email = form.email.value.trim();
      if (!name) { err.textContent = 'Pop your first name in, so we know who to thank.'; form.name.focus(); return; }
      var bot = form.website.value || (Date.now() - opened < 2500);
      if (ctx.kind === 'quick') {
        var c = form.contact.value.trim();
        if (!c && !email) { err.textContent = 'A phone number or an email, so we can tell you.'; form.contact.focus(); return; }
        var isMail = c.indexOf('@') > -1;
        if (!bot) send({ type: 'signup', name: name, phone: isMail ? '' : c, email: isMail ? c : email, fit: 'in', thread: ctx.thread || 'Tell me about the next one', where: window.VVV_PLACE || '' });
      } else {
        var post = form.post.value.trim();
        if (!post) { err.textContent = 'A line is plenty.'; form.post.focus(); return; }
        if (!bot) send({ type: 'board', level: ctx.tag ? 'Tag' : 'Thread', thread: ctx.thread || '', tag: ctx.tag || '', post: post, name: name, email: email });
      }
      body.hidden = true; done.hidden = false; done.querySelector('button').focus();
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-act]');
    if (!b || !window.vvvOpenForm) return;
    window.vvvOpenForm({ kind: b.dataset.act, thread: b.dataset.thread, tag: b.dataset.tag, title: b.dataset.title, prompt: b.dataset.prompt, label: b.dataset.label });
  });

  /* ---------- threads ---------- */
  var T = window.VVV_THREADS || [];
  var chips = document.getElementById('chips'), tags = document.getElementById('tags');
  if (chips && tags) {
    T.forEach(function (t, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.style.setProperty('--c', t.c); b.style.setProperty('--ci', t.ink || '#221e19'); b.setAttribute('aria-pressed', 'false');
      b.innerHTML = (t.icon || '') + '<span>' + t.n + '</span>';
      b.addEventListener('click', function () { show(i); });
      chips.appendChild(b);
    });
    function show(i) {
      var t = T[i];
      chips.querySelectorAll('.chip').forEach(function (c, j) { c.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      tags.style.setProperty('--c', t.c); tags.style.setProperty('--ci', t.ink || '#221e19');
      tags.innerHTML = '<p class="tline">' + t.line + '</p>' + (t.q ? '<p class="tq">' + t.q + '</p>' : '') + '<div class="tlist">' +
        t.tags.map(function (g) { return '<button type="button" class="tag" data-act="board" data-thread="' + t.n + '" data-tag="' + g + '" data-title="' + g + '" data-prompt="What would you love to do with this, round here?">' + g + '</button>'; }).join('') +
        '</div><button type="button" class="tadd" data-act="board" data-thread="' + t.n + '" data-title="' + t.n + '" data-prompt="' + (t.q || 'What\'s stirring for you here? An idea, a thought, a feeling.') + '">Add a thought about ' + t.n.toLowerCase() + ' →</button>';
      tags.hidden = false;
      signal('thread tapped', t.n);
    }
  }

  /* ---------- map (Leaflet + OpenStreetMap) ---------- */
  var mapEl = document.getElementById('map');
  if (mapEl && window.L && window.VVV_PLACES) {
    var P = window.VVV_PLACES;
    var map = L.map(mapEl, { scrollWheelZoom: false }).setView(window.VVV_CENTRE || [51.2289, -0.7319], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
    var COL = { place: '#3f7a2e', business: '#d9822b', people: '#e8337f', idea: '#5a7fd6' };
    P.forEach(function (pl) {
      var mk = L.circleMarker(pl.ll, { radius: 9, color: '#23211d', weight: 2, fillColor: COL[pl.k] || '#555', fillOpacity: 0.95 }).addTo(map);
      mk.bindPopup('<b>' + pl.n + '</b><br>' + pl.d);
      mk.on('click', function () { signal('map pin', pl.n); });
    });
  }

  /* ---------- the web (people, places, businesses, ideas) ---------- */
  var web = document.getElementById('web');
  if (web && window.VVV_WEB) {
    var W = window.VVV_WEB, NS = 'http://www.w3.org/2000/svg', cx = 200, cy = 200;
    var COLW = { place: '#3f7a2e', business: '#d9822b', people: '#e8337f', idea: '#5a7fd6', centre: '#23211d' };
    var pos = {};
    W.nodes.forEach(function (n, i) {
      if (n.k === 'centre') { pos[n.id] = [cx, cy]; return; }
      var ring = W.nodes.filter(function (x) { return x.k !== 'centre'; });
      var idx = ring.indexOf(n), a = (idx / ring.length) * Math.PI * 2 - Math.PI / 2, r = idx % 2 ? 150 : 118;
      pos[n.id] = [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
    });
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('viewBox', '0 0 400 400'); svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'How Tongham\'s people, places, businesses and ideas connect');
    W.links.forEach(function (l) {
      var a = pos[l[0]], b = pos[l[1]]; if (!a || !b) return;
      var ln = document.createElementNS(NS, 'line');
      ln.setAttribute('x1', a[0]); ln.setAttribute('y1', a[1]); ln.setAttribute('x2', b[0]); ln.setAttribute('y2', b[1]);
      ln.setAttribute('class', 'wl'); ln.dataset.a = l[0]; ln.dataset.b = l[1]; svg.appendChild(ln);
    });
    var note = document.getElementById('web-note');
    W.nodes.forEach(function (n) {
      var g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'wn'); g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button');
      g.setAttribute('aria-label', n.n);
      var c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', pos[n.id][0]); c.setAttribute('cy', pos[n.id][1]);
      c.setAttribute('r', n.k === 'centre' ? 26 : 9); c.setAttribute('fill', COLW[n.k]); g.appendChild(c);
      var t = document.createElementNS(NS, 'text'); t.setAttribute('x', pos[n.id][0]); t.setAttribute('y', pos[n.id][1] + (n.k === 'centre' ? 4 : (pos[n.id][1] < cy ? -14 : 22)));
      t.setAttribute('text-anchor', 'middle'); t.setAttribute('class', n.k === 'centre' ? 'wt wc' : 'wt'); t.textContent = n.s || n.n; g.appendChild(t);
      function pick() {
        svg.querySelectorAll('.wl').forEach(function (l) { l.classList.toggle('on', l.dataset.a === n.id || l.dataset.b === n.id); });
        svg.querySelectorAll('.wn').forEach(function (x) { x.classList.toggle('on', x === g); });
        if (note) note.innerHTML = '<b>' + n.n + '</b> ' + n.d;
        signal('web node', n.n);
      }
      g.addEventListener('click', pick);
      g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
      svg.appendChild(g);
    });
    web.appendChild(svg);
  }

  /* anonymous section signals */
  document.querySelectorAll('a[data-sig]').forEach(function (a) { a.addEventListener('click', function () { signal('link', a.dataset.sig); }); });
})();
