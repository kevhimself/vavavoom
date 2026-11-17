// Va Va Voom Godalming: catches sign-ups, board posts and tap signals from the website
// and writes them into this spreadsheet. Paste into Extensions > Apps Script, then
// Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).

const MAX_LEN = 2000;          // longest text we keep from any one field
const SIGNALS_PER_MINUTE = 300; // flood guard for tap counts

function doGet() {
  return ContentService.createTextOutput('Va Va Voom is listening.');
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const now = new Date();

    const why = reasonToHold(d);
    if (why) {
      ss.getSheetByName('Held back').appendRow([now, clean(d.type), why, clean(JSON.stringify(d))]);
      return ok();
    }

    if (d.type === 'signup') {
      ss.getSheetByName('Sign-ups').appendRow([
        now, clean(d.name), clean(d.phone), clean(d.email), clean(d.where),
        d.fit === 'in' ? "I'm in" : d.fit === 'out' ? 'Not for me' : clean(d.fit),
        clean(d.voom), clean(d.five_easy), clean(d.bring), clean(d.experiment),
        clean(d.five_grow), clean(d.cool), clean(d.thread), clean(d.page), '', clean(d.version), clean(d.who || '')
      ]);
      if (d.fit === 'booked') sendBookingEmail(ss, d, now);
    } else if (d.type === 'board') {
      ss.getSheetByName('Board').appendRow([
        now, clean(d.level), clean(d.thread), clean(d.tag), clean(d.post),
        clean(d.name), clean(d.email), clean(d.page), 'New', '', '', clean(d.version), clean(d.who || '')
      ]);
    } else if (d.type === 'signal') {
      // Signals: Received, Event, Detail, Page, Release, Who (team or visitor; Kev 29 Oct: ignore Kev, Tim and Carl when counting),
      // Visitor code, Code kept. The code is random (vid.js): 'kept' = said yes to helping the experiment, 'page' = one page view only.
      const vid = /^[kp][0-9a-f]{12}$/.test(String(d.vid || '')) ? String(d.vid) : '';
      const vk = d.vk === 'kept' || d.vk === 'page' ? d.vk : '';
      ss.getSheetByName('Signals').appendRow([now, clean(d.event), clean(d.detail), clean(d.page), clean(d.version), clean(d.who || 'visitor'), vid, vk]);
    } else if (d.type === 'access') {
      ss.getSheetByName('Access').appendRow([now, clean(d.email), clean(d.page), clean(d.version), clean(d.contact || 'No')]);
    } else if (d.type === 'project') {
      // Tab "Projects": Received, Project, What it is, Their link to it, Who's doing it, About them, What they love,
      // Tips and secrets, How to get involved, Key dates, Link, Thread, Where, Shared by, Email, Happy to be named, Page, Status
      ss.getSheetByName('Projects').appendRow([
        now, clean(d.title), clean(d.what), clean(d.rel), clean(d.lead), clean(d.about), clean(d.love), clean(d.tips),
        clean(d.engage), clean(d.dates), clean(d.url), clean(d.thread), clean(d.where), clean(d.name), clean(d.email),
        clean(d.ok), clean(d.page), 'New', clean(d.version), clean(d.who || '')
      ]);
    } else if (d.type === 'feedback') {
      ss.getSheetByName('Feedback').appendRow([
        now, clean(d.version), clean(d.felt), clean(d.drawn), clean(d.turnoff), clean(d.onething),
        clean(d.other), clean(d.name), clean(d.email), clean(d.page), clean(d.who || '')
      ]);
    }
  } catch (err) {
    console.error(err);
  } finally {
    lock.releaseLock();
  }
  return ok();
}

// Kev 16 Nov: when someone books an event with an email address, send a simple "You're booked" email.
// The words live in the private "Booking emails" tab (Event id, Subject, Body with {name}, Send? Yes/No, Notes, Reply-to),
// so no address sits in this public file. One email per person per event, at most 40 a day. Logged in Comms.
const BOOKING_EMAILS_PER_DAY = 40;
function sendBookingEmail(ss, d, now) {
  try {
    const to = String(d.email || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(to)) return;
    const id = String(d.thread || '').replace(/^event:\s*/, '').trim();
    const tab = ss.getSheetByName('Booking emails');
    if (!id || !tab) return;
    const tpl = tab.getDataRange().getValues().slice(1)
      .filter(function (r) { return String(r[0]).trim() === id && /^yes$/i.test(String(r[3]).trim()); })[0];
    if (!tpl) return;
    const comms = ss.getSheetByName('Comms');
    const already = comms.getDataRange().getValues().some(function (r) {
      return String(r[2]).trim().toLowerCase() === to.toLowerCase() && String(r[4]) === 'booked: ' + id;
    });
    if (already) return;
    const cache = CacheService.getScriptCache(), dayKey = 'mail' + Utilities.formatDate(now, 'Europe/London', 'yyyyMMdd');
    const n = Number(cache.get(dayKey) || 0) + 1;
    cache.put(dayKey, String(n), 21600);
    if (n > BOOKING_EMAILS_PER_DAY) return;
    const name = clean(d.name).replace(/^'/, '').split(/\s+/)[0] || 'there';
    const subject = String(tpl[1]);
    const text = String(tpl[2]).replace(/\{name\}/g, name);
    // **words** in the sheet become bold in the email; the plain-text copy just drops the stars.
    const msg = { to: to, subject: subject, body: text.replace(/\*\*/g, ''), htmlBody: toHtml(text), name: 'Va Va Voom' };
    const replyTo = String(tpl[5] || '').trim(); // column F: replies go to the shared inbox, not the script owner's own
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(replyTo)) msg.replyTo = replyTo;
    MailApp.sendEmail(msg);
    comms.appendRow([now, name, to, 'Booking confirmation', 'booked: ' + id, 'Va Va Voom (automatic)', 'Email', subject, 'Sent', 'Website', 'Sent automatically when they booked']);
  } catch (err) {
    console.error(err);
  }
}

// Plain text from the sheet to simple, safe email HTML: bold, links and line breaks only.
function toHtml(t) {
  const esc = String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#1c1a2b">' +
    esc.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
       .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" style="color:#c41f66">$1</a>')
       .replace(/\n/g, '<br>') + '</div>';
}

// Run this once from the editor (select it, then Run) to send the email to anyone who booked before it was switched on.
function sendMissedBookingEmails() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName('Sign-ups').getDataRange().getValues().slice(1).forEach(function (r) {
    if (String(r[5]) === 'booked') sendBookingEmail(ss, { name: r[1], email: r[3], thread: r[12] }, new Date());
  });
}

// The first line of defence. The Watcher does the thoughtful checking later.
function reasonToHold(d) {
  if (!d || ['signup', 'board', 'signal', 'access', 'feedback', 'project'].indexOf(d.type) === -1) return 'Not a Va Va Voom form';
  if (d.website) return 'Hidden trap field was filled in (likely a bot)';

  const cache = CacheService.getScriptCache();
  if (d.type === 'signal') {
    const key = 'sig' + Math.floor(Date.now() / 60000);
    const n = Number(cache.get(key) || 0) + 1;
    cache.put(key, String(n), 120);
    if (n > SIGNALS_PER_MINUTE) return 'Too many taps in a minute';
    return '';
  }

  if (d.type === 'access') {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || '').trim())) return 'Email does not look right';
  }
  const text = [d.post, d.voom, d.bring, d.experiment, d.cool, d.name, d.felt, d.drawn, d.turnoff, d.onething, d.other, d.email,
                d.title, d.what, d.lead, d.about, d.love, d.tips, d.engage, d.dates].join(' ');
  // Links are only allowed in a project's own link field (d.url), which is not part of text.
  if (d.type !== 'access' && /https?:\/\/|www\./i.test(text)) return 'Contains a web link';
  if (d.type === 'project' && (!String(d.title || '').trim() || !String(d.what || '').trim())) return 'Project without a name or description';
  if (/[\u0400-\u04FF]/.test(text)) return 'Cyrillic text';
  if ((d.type === 'signup' || d.type === 'board' || d.type === 'project') && !String(d.name || '').trim()) return 'No name given';
  if (d.type === 'feedback' && !String([d.felt, d.drawn, d.turnoff, d.onething, d.other].join('')).trim()) return 'Empty feedback';

  const digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, d.type + '|' + text);
  const dupKey = 'dup' + Utilities.base64EncodeWebSafe(digest);
  if (cache.get(dupKey)) return 'Same message sent twice within 10 minutes';
  cache.put(dupKey, '1', 600);
  return '';
}

// Trim, cap the length, and stop anything that looks like a spreadsheet formula.
function clean(v) {
  let s = String(v == null ? '' : v).trim().slice(0, MAX_LEN);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function ok() {
  return ContentService.createTextOutput('ok');
}
