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
        clean(d.five_grow), clean(d.cool), clean(d.thread), clean(d.page), ''
      ]);
    } else if (d.type === 'board') {
      ss.getSheetByName('Board').appendRow([
        now, clean(d.level), clean(d.thread), clean(d.tag), clean(d.post),
        clean(d.name), clean(d.email), clean(d.page), 'New', '', ''
      ]);
    } else if (d.type === 'signal') {
      ss.getSheetByName('Signals').appendRow([now, clean(d.event), clean(d.detail), clean(d.page)]);
    }
  } catch (err) {
    console.error(err);
  } finally {
    lock.releaseLock();
  }
  return ok();
}

// The first line of defence. The Watcher does the thoughtful checking later.
function reasonToHold(d) {
  if (!d || ['signup', 'board', 'signal'].indexOf(d.type) === -1) return 'Not a Va Va Voom form';
  if (d.website) return 'Hidden trap field was filled in (likely a bot)';

  const cache = CacheService.getScriptCache();
  if (d.type === 'signal') {
    const key = 'sig' + Math.floor(Date.now() / 60000);
    const n = Number(cache.get(key) || 0) + 1;
    cache.put(key, String(n), 120);
    if (n > SIGNALS_PER_MINUTE) return 'Too many taps in a minute';
    return '';
  }

  const text = [d.post, d.voom, d.bring, d.experiment, d.cool, d.name].join(' ');
  if (/https?:\/\/|www\./i.test(text)) return 'Contains a web link';
  if (/[Ѐ-ӿ]/.test(text)) return 'Cyrillic text';
  if (!String(d.name || '').trim()) return 'No name given';

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
