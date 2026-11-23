/* Va Va Voom: one set of checks for every sign-up form (Kev, 23 Nov 2026).
   Why: a booking came in as "…@gmail.cm", so the confirmation never arrived.
   How: include <script src="validate.js"></script> on any page with a form. It checks fields by id:
     …Name     first name: letters, spaces, hyphens, apostrophes; no numbers, emails or links
     …Contact  mobile or email: a real-looking email or phone number
     …Email    email only;  …Phone / …Tel  phone only
   Empty fields are left to each form's own rules (details are often optional).
   It runs before the form's own submit handler; if something's wrong it stops the submit,
   says what to fix in plain words, and offers a one-tap fix for likely typos ("Did you mean …?"). */
(function () {
  var DOMAIN_FIX = {
    'gmail.cm': 'gmail.com', 'gmail.co': 'gmail.com', 'gmail.con': 'gmail.com', 'gmail.om': 'gmail.com',
    'gmail.cmo': 'gmail.com', 'gmail.ocm': 'gmail.com', 'gmail.comm': 'gmail.com', 'gmail.vom': 'gmail.com',
    'gmail.cm.com': 'gmail.com', 'gmail.co.uk': 'gmail.com', 'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com',
    'gamil.com': 'gmail.com', 'gnail.com': 'gmail.com', 'gmaill.com': 'gmail.com', 'gmal.com': 'gmail.com',
    'googlemail.cm': 'googlemail.com',
    'hotmail.cm': 'hotmail.com', 'hotmail.con': 'hotmail.com', 'hotmial.com': 'hotmail.com', 'hotmal.com': 'hotmail.com',
    'hotmail.co': 'hotmail.co.uk', 'hotmail.couk': 'hotmail.co.uk', 'hotmail.co.uj': 'hotmail.co.uk',
    'outlook.cm': 'outlook.com', 'outlook.con': 'outlook.com', 'outlok.com': 'outlook.com', 'outloo.com': 'outlook.com',
    'yahoo.cm': 'yahoo.com', 'yahoo.con': 'yahoo.com', 'yaho.com': 'yahoo.com', 'yahoo.co': 'yahoo.co.uk',
    'yahoo.couk': 'yahoo.co.uk', 'yahoo.co.uj': 'yahoo.co.uk', 'yaho.co.uk': 'yahoo.co.uk',
    'icloud.cm': 'icloud.com', 'icloud.con': 'icloud.com', 'icoud.com': 'icloud.com', 'iclod.com': 'icloud.com',
    'live.cm': 'live.com', 'live.con': 'live.com', 'msn.cm': 'msn.com', 'msn.con': 'msn.com',
    'btinternet.cm': 'btinternet.com', 'btinternet.con': 'btinternet.com', 'btinternt.com': 'btinternet.com',
    'sky.cm': 'sky.com', 'aol.cm': 'aol.com', 'aol.con': 'aol.com'
  };
  var TLD_FIX = { con: 'com', cmo: 'com', ocm: 'com', vom: 'com', comm: 'com', couk: 'co.uk', 'co.uj': 'co.uk', 'co.ik': 'co.uk', 'og': 'org', 'ogr': 'org' };

  function checkName(v) {
    v = v.trim();
    if (!v) return { ok: true, empty: true };
    if (/@|https?:|www\./i.test(v)) return { ok: false, msg: 'That looks like an email or a link. Please put just your first name here.' };
    if (/\d/.test(v)) return { ok: false, msg: 'Names don\'t usually have numbers in. Please check your first name.' };
    if (!/^[\p{L}][\p{L}\p{M}' .-]*$/u.test(v)) return { ok: false, msg: 'Please use letters for your name (hyphens and apostrophes are fine).' };
    if (v.length > 40) return { ok: false, msg: 'That\'s a long one. Just your first name is perfect.' };
    return { ok: true, value: v.replace(/\s+/g, ' ') };
  }

  function checkEmail(v) {
    v = v.trim().replace(/\s+/g, '');
    if (!v) return { ok: true, empty: true };
    var m = /^([^@\s]+)@([^@\s]+)$/.exec(v);
    if (!m) return { ok: false, msg: 'That email doesn\'t look quite right. It should look like name@example.com.' };
    var local = m[1], domain = m[2].toLowerCase().replace(/\.+$/, '');
    if (/\.\./.test(domain) || !/^[a-z0-9.-]+\.[a-z]{2,}$/.test(domain)) return { ok: false, msg: 'Please check the part after the @. It should look like example.com.' };
    var fixed = DOMAIN_FIX[domain];
    if (!fixed) {
      var parts = domain.split('.'), last2 = parts.slice(-2).join('.'), last = parts[parts.length - 1];
      if (TLD_FIX[last2]) fixed = parts.slice(0, -2).join('.') + '.' + TLD_FIX[last2];
      else if (TLD_FIX[last]) fixed = parts.slice(0, -1).join('.') + '.' + TLD_FIX[last];
    }
    if (fixed && fixed !== domain) {
      var s = local + '@' + fixed;
      return { ok: false, suggest: s, msg: 'Did you mean ' + s + '? Typos here mean our emails never reach you.' };
    }
    return { ok: true, value: local + '@' + domain };
  }

  function checkPhone(v) {
    var raw = v.trim();
    if (!raw) return { ok: true, empty: true };
    if (/[a-z]/i.test(raw)) return { ok: false, msg: 'Please use numbers only for your phone number.' };
    var d = raw.replace(/[\s().-]/g, '');
    if (/^\+44/.test(d)) d = '0' + d.slice(3).replace(/^0/, '');
    if (/^0044/.test(d)) d = '0' + d.slice(4);
    if (/^\+\d{8,15}$/.test(d)) return { ok: true, value: raw };           // other countries
    if (/^7\d{9}$/.test(d)) return { ok: false, suggest: '0' + d, msg: 'Did you mean 0' + d + '? UK mobiles start with 07.' };
    if (!/^0\d+$/.test(d)) return { ok: false, msg: 'That number doesn\'t look quite right. UK numbers start with 0, or use +44.' };
    if (d.length < 11) return { ok: false, msg: 'That number looks a digit or two short. UK numbers have 11 digits, like 07700 900123.' };
    if (d.length > 11) return { ok: false, msg: 'That number looks a digit or two long. UK numbers have 11 digits, like 07700 900123.' };
    return { ok: true, value: raw };
  }

  function checkContact(v) {
    var t = v.trim();
    if (!t) return { ok: true, empty: true };
    if (t.indexOf('@') > -1) return checkEmail(t);
    if (/^[+\d][\d\s().-]*$/.test(t)) return checkPhone(t);
    return { ok: false, msg: 'Please add a mobile number or an email address.' };
  }

  function kind(el) {
    var id = el.id || '';
    if (/Contact$/.test(id)) return checkContact;
    if (/Email$/.test(id) || el.type === 'email') return checkEmail;
    if (/(Phone|Tel)$/.test(id) || el.type === 'tel') return checkPhone;
    if (/Name$/.test(id)) return checkName;
    return null;
  }

  function errBox(form) {
    var e = form.querySelector('.err');
    if (!e) { e = document.createElement('p'); e.className = 'err'; e.setAttribute('role', 'alert'); form.appendChild(e); }
    return e;
  }

  function show(form, el, res, noFocus) {
    var e = errBox(form);
    e.textContent = res.msg;
    el.setAttribute('aria-invalid', 'true');
    if (res.suggest) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'vvv-fix';
      b.textContent = 'Yes, use ' + res.suggest;
      b.style.cssText = 'display:inline-flex;align-items:center;min-height:44px;margin:6px 8px 0 0;padding:0 14px;border-radius:999px;border:2px solid currentColor;background:transparent;font:inherit;font-weight:700;cursor:pointer';
      b.onclick = function () { el.value = res.suggest; el.removeAttribute('aria-invalid'); e.textContent = ''; el.focus(); };
      var k = document.createElement('button');
      k.type = 'button'; k.className = 'vvv-fix';
      k.textContent = 'No, mine is right';
      k.style.cssText = b.style.cssText + ';border-color:transparent;text-decoration:underline';
      k.onclick = function () { el.dataset.vvvOk = el.value; el.removeAttribute('aria-invalid'); e.textContent = ''; el.focus(); };
      e.appendChild(document.createElement('br')); e.appendChild(b); e.appendChild(k);
    }
    if (!noFocus) el.focus();
  }

  // Runs in the capture phase, before each form's own submit handler.
  document.addEventListener('submit', function (ev) {
    var form = ev.target;
    if (!form || form.tagName !== 'FORM') return;
    var fields = form.querySelectorAll('input[id]');
    for (var i = 0; i < fields.length; i++) {
      var el = fields[i], fn = kind(el);
      if (!fn || el.type === 'checkbox' || el.type === 'hidden' || el.classList.contains('trap')) continue;
      if (el.dataset.vvvOk && el.dataset.vvvOk === el.value) continue;   // they said "mine is right"
      var res = fn(el.value);
      if (!res.ok) { ev.preventDefault(); ev.stopImmediatePropagation(); show(form, el, res); return; }
      if (res.value && res.value !== el.value) el.value = res.value;    // tidy spaces and case
      el.removeAttribute('aria-invalid');
    }
  }, true);

  // A gentle early nudge when someone leaves a field with a likely typo.
  document.addEventListener('focusout', function (ev) {
    var el = ev.target;
    if (!el || el.tagName !== 'INPUT' || !el.form) return;
    var fn = kind(el);
    if (!fn || !el.value.trim()) return;
    if (el.dataset.vvvOk && el.dataset.vvvOk === el.value) return;
    var res = fn(el.value);
    if (!res.ok && res.suggest) show(el.form, el, res, true);
  }, true);

  window.VVVCheck = { name: checkName, email: checkEmail, phone: checkPhone, contact: checkContact };
})();
