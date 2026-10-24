/* Va Va Voom: the rabbit-hole gate, the "early prototype" note, and the feedback button.
   A soft gate for an invite-only prototype. It keeps casual visitors out; it is not real security. */
(function () {
  var KEY = 'vvv-in';
  var WORD = '1tk61rf'; // hash of the secret word, "rabbit hole" (lower case, letters only)
  var VERSION = window.VVV_VERSION = '0.4.5 (24 October 2026)'; // bump this whenever the site changes
  // PostHog (EU cloud). Paste the project key from PostHog > Settings > Project (it starts phc_).
  // Left blank, PostHog stays off and the consent bar never shows.
  var PH_KEY = 'phc_yxqNiM5WwH3EQD8sZSGEB8HDqHn6awwwuvgar5ZmdyQ6';
  var PH_CHOICE = 'vvv-ph'; // remembers yes or no to recording
  function hash(s) { var x = 2166136261; for (var i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619) >>> 0; } return x.toString(36); }
  function send(data) {
    data.page = location.pathname; data.when = new Date().toISOString(); data.version = VERSION;
    if (!window.VVV_URL) return;
    try { fetch(window.VVV_URL, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }); } catch (e) {}
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // ---- PostHog: visits are counted without cookies until someone says yes; replay only after a yes.
  // Every input (email, secret word, feedback) is masked in replays. No email or name is sent to PostHog.
  function track(name, props) { try { if (PH_KEY && window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }
  if (PH_KEY) {
    /* official PostHog loader */
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once unregister identify reset get_distinct_id set_config startSessionRecording stopSessionRecording opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing get_explicit_consent_status debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    window.posthog.init(PH_KEY, {
      api_host: 'https://eu.i.posthog.com',
      defaults: '2025-05-24',
      cookieless_mode: 'on_reject',
      person_profiles: 'identified_only',
      respect_dnt: true,
      session_recording: { maskAllInputs: true }
    });
    window.posthog.register({ site_version: VERSION });
  }

  var css = '\
.vg-wrap{position:fixed;inset:0;z-index:100;display:grid;place-items:center;overflow:auto;background:#221e19;color:#f3eee2;padding:max(16px,env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) max(16px,env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));font-family:"Courier Prime","Courier New",monospace}\
.vg-wrap[hidden],.vg-note[hidden],.vg-fb[hidden]{display:none!important}\
.vg-box{width:min(440px,100%);text-align:center;padding-block:24px}\
.vg-tunnel{position:relative;width:min(240px,62vw);margin:0 auto 6px}\
.vg-tunnel svg.r{width:100%;height:auto;display:block}\
.vg-tunnel svg.r circle{fill:none;stroke-width:2}\
.vg-rab{position:absolute;left:50%;top:50%;width:76px;height:76px;transform:translate(-50%,-58%)}\
@media (prefers-reduced-motion:no-preference){.vg-tunnel svg.r{animation:vgspin 26s linear infinite}@keyframes vgspin{to{transform:rotate(360deg)}}}\
.vg-box h1{font-family:"Bowlby One SC",Impact,"Arial Black",sans-serif;font-weight:400;font-size:clamp(30px,8vw,46px);line-height:1;margin:10px 0 8px;color:#f3eee2}\
.vg-box h1 span{background:#ee8fa4;color:#221e19;padding:0 8px;display:inline-block;transform:rotate(-2deg)}\
.vg-box p{margin:0 0 18px;color:#e6dfd1;font-size:16px;line-height:1.5}\
.vg-box form{display:grid;gap:12px;text-align:left}\
.vg-box label{display:grid;gap:4px;font-weight:700;font-size:14px;color:#c9f24a}\
.vg-box input{font:inherit;font-size:16px;padding:11px 12px;border:2px solid #f3eee2;background:#2e2822;color:#f3eee2;border-radius:0}\
.vg-box input:focus-visible{outline:3px dashed #e8337f;outline-offset:2px}\
.vg-btn{font-family:"Bowlby One SC",Impact,"Arial Black",sans-serif;font-size:18px;border:3px solid #f3eee2;background:#e8337f;color:#221e19;padding:12px 18px;cursor:pointer;box-shadow:5px 5px 0 #c9f24a;margin-top:4px}\
.vg-err{min-height:1.4em;color:#ee8fa4;font-weight:700;font-size:14px;margin:0}\
.vg-small{font-size:13px!important;color:#b8b0a2!important;margin-top:14px!important}\
.vg-note{position:fixed;inset:0;z-index:101;display:grid;place-items:center;background:rgba(34,30,25,.6);padding:16px;font-family:"Courier Prime","Courier New",monospace}\
.vg-card{width:min(460px,100%);background:#fbf8f1;color:#221e19;border:3px solid #221e19;box-shadow:8px 8px 0 #221e19;padding:22px 22px 18px;transform:rotate(-.6deg);position:relative}\
.vg-card::before{content:"";position:absolute;top:-13px;left:24px;width:110px;height:26px;background:rgba(201,242,74,.8);transform:rotate(-4deg);border:1px solid rgba(34,30,25,.2)}\
.vg-card h2{font-family:"Bowlby One SC",Impact,"Arial Black",sans-serif;font-weight:400;font-size:24px;margin:4px 0 10px;line-height:1.1}\
.vg-card p{margin:0 0 10px;font-size:16px;line-height:1.5}\
.vg-link{color:#221e19;font-weight:700;text-decoration:none;border-bottom:3px solid #e8337f}\
.vg-link:hover{color:#b8285f}\
.vg-card .vg-pen{font-family:"Permanent Marker","Comic Sans MS",cursive;font-size:20px;color:#b8285f}\
.vg-card .vg-btn{box-shadow:4px 4px 0 #221e19;border-color:#221e19;margin-top:8px}\
.vg-fbbtn{position:fixed;right:max(14px,env(safe-area-inset-right,0px));bottom:max(14px,env(safe-area-inset-bottom,0px));z-index:40;font-family:"Bowlby One SC",Impact,"Arial Black",sans-serif;font-size:15px;background:#c9f24a;color:#221e19;border:3px solid #221e19;padding:9px 14px;box-shadow:4px 4px 0 #221e19;cursor:pointer;transform:rotate(-2deg)}\
.vg-fbbtn:hover{transform:rotate(0)}\
.vg-fb{position:fixed;inset:0;z-index:60;display:grid;place-items:center;background:rgba(34,30,25,.55);padding:16px;font-family:"Courier Prime","Courier New",monospace}\
.vg-fb .vg-card{max-height:100%;overflow:auto}\
.vg-fb label{display:grid;gap:4px;font-weight:700;font-size:14px;margin-bottom:10px}\
.vg-fb label span{font-weight:400;color:#3d5a8c}\
.vg-fb textarea,.vg-fb input{font:inherit;font-size:16px;padding:9px 11px;border:2px solid #221e19;background:#fff;color:#221e19;border-radius:0;width:100%}\
.vg-fb textarea{min-height:72px;resize:vertical}\
.vg-x{position:absolute;right:8px;top:6px;border:0;background:none;font-size:26px;cursor:pointer;color:#221e19;padding:4px 8px}\
.vg-row{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center}\
.vg-ghost{font:inherit;font-weight:700;background:none;border:0;text-decoration:underline;cursor:pointer;color:#221e19}\
.vg-ok{position:fixed;left:max(14px,env(safe-area-inset-left,0px));bottom:max(14px,env(safe-area-inset-bottom,0px));z-index:45;width:min(380px,calc(100% - 28px));background:#fbf8f1;color:#221e19;border:3px solid #221e19;box-shadow:5px 5px 0 #221e19;padding:14px 16px;font-family:"Courier Prime","Courier New",monospace;font-size:14px;line-height:1.45}\
.vg-ok[hidden]{display:none!important}\
@media (max-width:560px){.vg-ok{bottom:calc(max(14px,env(safe-area-inset-bottom,0px)) + 62px)}}\
.vg-ok p{margin:0 0 10px}\
.vg-ok .vg-btn{font-size:15px;padding:8px 14px;box-shadow:3px 3px 0 #221e19;border-color:#221e19;margin:0}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var RABBIT = '<path d="M22 30 C14 18 12 6 17 4 C22 2 27 14 28 26" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5" stroke-linejoin="round"/><path d="M19 9 C21 14 23 19 24 24" stroke="#ee8fa4" stroke-width="3.5" stroke-linecap="round" fill="none"/><path d="M34 26 C36 12 42 2 47 5 C52 8 46 20 39 30" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5" stroke-linejoin="round"/><path d="M44 9 C42 14 39 20 37 25" stroke="#ee8fa4" stroke-width="3.5" stroke-linecap="round" fill="none"/><ellipse cx="31" cy="40" rx="17" ry="15" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5"/><circle cx="25" cy="38" r="2.6" fill="#221e19"/><circle cx="37" cy="38" r="2.6" fill="#221e19"/><path d="M29 45 l2 2 l2 -2" stroke="#221e19" stroke-width="2.5" fill="#e8337f" stroke-linejoin="round"/>';

  function el(html) { var d = document.createElement('div'); d.innerHTML = html.trim(); return d.firstChild; }

  // ---- the feedback button and card (shown once someone is in)
  var fbBtn = el('<button type="button" class="vg-fbbtn" hidden>Feedback</button>');
  var fb = el('<div class="vg-fb" hidden role="dialog" aria-modal="true" aria-labelledby="vg-fbh"><div class="vg-card">' +
    '<button type="button" class="vg-x" aria-label="Close">×</button>' +
    '<div class="vg-fbform"><h2 id="vg-fbh">Tell us how it feels</h2><p>Early days, so honest is gold. Answer any you like, a line is plenty.</p>' +
    '<form novalidate><label for="vg-f1">When you first opened it, how did it make you feel?<textarea id="vg-f1" name="felt"></textarea></label>' +
    '<label for="vg-f2">What did you want to tap, read or play with?<textarea id="vg-f2" name="drawn"></textarea></label>' +
    '<label for="vg-f3">Did anything turn you off, or confuse you?<textarea id="vg-f3" name="turnoff"></textarea></label>' +
    '<label for="vg-f4">What one thing would you love to see on here?<textarea id="vg-f4" name="onething"></textarea></label>' +
    '<label for="vg-o">Anything else?<textarea id="vg-o" name="other"></textarea></label>' +
    '<label for="vg-fn">Your name <span>(optional)</span><input id="vg-fn" name="name" type="text" autocomplete="name"></label>' +
    '<label for="vg-fe">Email <span>(optional, if you\'re happy for us to reply)</span><input id="vg-fe" name="email" type="email" autocomplete="email"></label>' +
    '<p class="vg-err" role="alert"></p><div class="vg-row"><button type="button" class="vg-ghost">Not now</button><button type="submit" class="vg-btn">Send it →</button></div></form></div>' +
    '<div class="vg-fbdone" hidden><h2>Thank you</h2><p class="vg-pen">That genuinely helps. Back to poking around.</p><button type="button" class="vg-btn">Close</button></div>' +
    '</div></div>');
  function openFb() { fb.hidden = false; fb.querySelector('.vg-fbform').hidden = false; fb.querySelector('.vg-fbdone').hidden = true; fb.querySelector('form').reset(); fb.querySelector('.vg-err').textContent = ''; setTimeout(function () { fb.querySelector('#vg-f1').focus(); }, 30); }
  function closeFb() { fb.hidden = true; fbBtn.focus(); }
  fbBtn.addEventListener('click', openFb);
  fb.querySelector('.vg-x').addEventListener('click', closeFb);
  fb.querySelector('.vg-ghost').addEventListener('click', closeFb);
  fb.querySelector('.vg-fbdone .vg-btn').addEventListener('click', closeFb);
  fb.addEventListener('click', function (e) { if (e.target === fb) closeFb(); });
  fb.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    var f = e.target.elements;
    var d = { type: 'feedback', felt: f.felt.value.trim(), drawn: f.drawn.value.trim(), turnoff: f.turnoff.value.trim(), onething: f.onething.value.trim(), other: f.other.value.trim(), name: f.name.value.trim(), email: f.email.value.trim() };
    if (!(d.felt || d.drawn || d.turnoff || d.onething || d.other)) { fb.querySelector('.vg-err').textContent = 'Pop a word or two in one of the boxes first.'; return; }
    send(d);
    track('feedback sent');
    fb.querySelector('.vg-fbform').hidden = true; fb.querySelector('.vg-fbdone').hidden = false;
  });

  // ---- the "early prototype" note
  var note = el('<div class="vg-note" hidden role="dialog" aria-modal="true" aria-labelledby="vg-nh"><div class="vg-card">' +
    '<h2 id="vg-nh">A very early prototype</h2>' +
    '<p>This is about two and a half hours\' work, made after a People\'s Emergency Briefing action session, as an experiment in getting people into action. It\'s also a nudge to show what we can build ourselves, as citizens, with the tools we have today.</p>' +
    '<p>We\'re letting you in early. Nothing in here has been reviewed in detail yet, so please view it with those eyes.</p>' +
    '<p>Any feedback, or any poking, tapping and posting, would be lovely. The Feedback button sits in the corner whenever you want it.</p>' +
    '<p><a class="vg-link" href="https://sky-wave-139.notion.site/Va-Va-Voom-Godalming-about-this-prototype-40293f7bf11a81739a98c6cbfceb97e3" target="_blank" rel="noopener">A bit more about the project →</a></p>' +
    '<p class="vg-pen">Thanks for being one of the first.</p>' +
    '<button type="button" class="vg-btn">Got it, let me in →</button></div></div>');
  note.querySelector('.vg-btn').addEventListener('click', function () { note.hidden = true; fbBtn.hidden = false; askOk(); });

  // ---- the "OK to record?" bar (only when PostHog is switched on)
  var ok = el('<div class="vg-ok" hidden role="region" aria-label="Recording your visit">' +
    '<p>Can we record how you use the site? It shows us where things confuse people. Anything you type is hidden, and the data stays in the EU (PostHog).</p>' +
    '<div class="vg-row"><button type="button" class="vg-ghost">No thanks</button><button type="button" class="vg-btn">Yes, fine</button></div></div>');
  function choose(yes) {
    store(PH_CHOICE, yes ? 'yes' : 'no'); ok.hidden = true;
    try { if (yes) window.posthog.opt_in_capturing(); else window.posthog.opt_out_capturing(); } catch (e) {}
  }
  ok.querySelector('.vg-btn').addEventListener('click', function () { choose(true); });
  ok.querySelector('.vg-ghost').addEventListener('click', function () { choose(false); });
  function askOk() {
    if (!PH_KEY) return;
    var c = store(PH_CHOICE);
    if (c === 'yes' || c === 'no') { choose(c === 'yes'); return; }
    ok.hidden = false;
  }

  // ---- the gate
  var gate = el('<div class="vg-wrap" role="dialog" aria-modal="true" aria-labelledby="vg-gh"><div class="vg-box">' +
    '<div class="vg-tunnel" aria-hidden="true"><svg class="r" viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" stroke="#e8337f"/><circle cx="102" cy="98" r="80" stroke="#c9f24a" stroke-dasharray="6 6"/><circle cx="99" cy="101" r="64" stroke="#ee8fa4"/><circle cx="101" cy="99" r="49" stroke="#f2c75a" stroke-dasharray="4 5"/><circle cx="100" cy="100" r="35" stroke="#5aa9e6"/><circle cx="100" cy="100" r="22" stroke="#e8337f" stroke-dasharray="3 4"/></svg>' +
    '<svg class="vg-rab" viewBox="0 0 64 64">' + RABBIT + '</svg></div>' +
    '<h1 id="vg-gh">Down the <span>rabbit hole</span></h1>' +
    '<p>This corner of Godalming is invite-only for now. Got the secret word? Pop it in with your email, and down you go.</p>' +
    '<form novalidate>' +
    '<label for="vg-e">Your email<input id="vg-e" name="email" type="email" autocomplete="email" required></label>' +
    '<label for="vg-p">The secret word<input id="vg-p" name="word" type="password" autocomplete="off" required></label>' +
    '<p class="vg-err" role="alert"></p>' +
    '<button type="submit" class="vg-btn">Jump in ↓</button></form>' +
    '<p class="vg-small">No word? Whoever handed you the card will know it.</p>' +
    '</div></div>');
  gate.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    var f = e.target.elements, err = gate.querySelector('.vg-err');
    var email = f.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = 'That email doesn\'t look quite right.'; f.email.focus(); return; }
    if (hash(f.word.value.toLowerCase().replace(/[^a-z]/g, '')) !== WORD) { err.textContent = 'Not quite. Whoever gave you the card knows the word.'; f.word.focus(); return; }
    send({ type: 'access', email: email });
    track('gate passed');
    store(KEY, '1');
    gate.hidden = true; document.documentElement.style.overflow = '';
    note.hidden = false; note.querySelector('.vg-btn').focus();
  });

  function start() {
    document.body.appendChild(fbBtn); document.body.appendChild(fb); document.body.appendChild(note); document.body.appendChild(ok);
    if (store(KEY) === '1') { fbBtn.hidden = false; askOk(); return; }
    document.body.appendChild(gate); document.documentElement.style.overflow = 'hidden';
    setTimeout(function () { var i = gate.querySelector('#vg-e'); if (i) i.focus(); }, 50);
  }
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !fb.hidden) closeFb(); });
})();
