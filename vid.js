/* Va Va Voom: the experiment code.
   Say yes ("Yes, happy to help") on the "Help us learn?" bar and this phone keeps one random code (vvv-id), so we can
   tell one person's taps from another's without knowing who anyone is. It is not your name,
   it never sits next to your name in our records, and it is never sold.
   Say no (or nothing) and nothing is stored: each page view gets a throwaway code held in memory
   only, gone when the page closes. No IP addresses, ever.
   Used by hello.html, news.html and privacy.html. */
(function () {
  var KEY = 'vvv-id', CHOICE = 'vvv-ph';
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  function fresh() {
    var a = new Uint8Array(6);
    try { crypto.getRandomValues(a); } catch (e) { for (var i = 0; i < 6; i++) a[i] = Math.random() * 256; }
    return Array.prototype.map.call(a, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  }
  var pageCode = 'p' + fresh(); // this page view only, memory only

  window.VVV_ID = {
    // The code to send with each tap, and whether it is kept on this phone or just for this page.
    code: function () {
      if (get(CHOICE) === 'yes') {
        var k = get(KEY);
        if (!k) { k = 'k' + fresh(); set(KEY, k); }
        return { vid: k, vk: 'kept' };
      }
      return { vid: pageCode, vk: 'page' };
    },
    // Call on the yes/no choice. No wipes the code.
    chose: function (yes) {
      if (yes) { this.code(); try { if (window.posthog) window.posthog.register({ vvv_id: get(KEY) }); } catch (e) {} }
      else set(KEY, null);
    },
    // "Forget my code" on the privacy page: wipes the code and the yes, so the bar asks again.
    forget: function () {
      set(KEY, null); set(CHOICE, null);
      try { if (window.posthog) { window.posthog.unregister('vvv_id'); window.posthog.opt_out_capturing(); } } catch (e) {}
    },
    kept: function () { return get(CHOICE) === 'yes' ? get(KEY) : null; }
  };
  // Link PostHog replays to the same code, only for people who said yes.
  try { if (get(CHOICE) === 'yes' && window.posthog && get(KEY)) window.posthog.register({ vvv_id: get(KEY) }); } catch (e) {}
})();
