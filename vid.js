/* Va Va Voom: the experiment code.
   Say yes ("Yes, I'll help") on the "Fancy joining the experiment?" bar and this phone keeps one random code (vvv-id), so we can
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
  var offered = 'k' + fresh();  // the code we'd give you if you say yes (memory only until then)

  // A friendly secret name made from the code. Only the code is sent; the Pulse (tools/build_pulse.py)
  // works out the same name from it, so keep these two lists in step with build_pulse.py.
  var ADJ = ['Brave','Sunny','Curious','Merry','Nimble','Gentle','Bold','Cheery','Swift','Jolly','Plucky','Kind','Dapper','Breezy','Spry','Mellow'];
  var ANIMAL = ['Badger','Otter','Kingfisher','Hedgehog','Owl','Heron','Fox','Hare','Wren','Robin','Dormouse','Newt','Swift','Vole','Kestrel','Mole'];
  function nameFor(code) {
    if (!code) return '';
    var h = parseInt(code.slice(1, 9), 16) || 0;
    var adj = ADJ[h % 16], an = ANIMAL[(h >>> 4) % 16];
    if (adj === an) adj = 'Merry';
    return adj + ' ' + an + ' ' + (((h >>> 8) % 98) + 2);
  }

  // Animal badges, drawn in code so they look the same everywhere (Pulse crew, hello header).
  var ADJCOL={Brave:'#ffd9c2',Sunny:'#fbeec8',Curious:'#d8e7ff',Merry:'#ffd6e6',Nimble:'#e2f5c4',Gentle:'#ece5dc',Bold:'#ffc9c2',Cheery:'#fff1b8',Swift:'#cdeefa',Jolly:'#f3d6ff',Plucky:'#ffe0b3',Kind:'#d9f2e4',Dapper:'#e3e0f7',Breezy:'#d6f1f0',Spry:'#eaf7c8',Mellow:'#f5e6d3'};
  var FACE={Badger:'#f4f1ec',Otter:'#8a5a3b',Kingfisher:'#1f8fc2',Hedgehog:'#c79a6b',Owl:'#a67f52',Heron:'#c2ccd3',Fox:'#e0662b',Hare:'#b9966f',Wren:'#9a6b45',Robin:'#9a6b45',Dormouse:'#e0ae66',Newt:'#e9803a',Swift:'#4a4a58',Vole:'#86674f',Kestrel:'#bf6d33',Mole:'#3d3636'};
  var BIRDS={Kingfisher:1,Owl:1,Heron:1,Wren:1,Robin:1,Swift:1,Kestrel:1};
  function critter(an,adj){
    var f=FACE[an]||'#b9966f',bg=ADJCOL[adj]||'#ece5dc',ink='#1c1a2b',o='<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="31" fill="'+bg+'" stroke="'+ink+'" stroke-width="2"/>';
    if(an==='Hedgehog'){var sp='';for(var i=0;i<12;i++){var a=Math.PI*(1.05+i/11*0.9);sp+=(i?' L':'M')+(32+Math.cos(a)*25).toFixed(1)+' '+(36+Math.sin(a)*25).toFixed(1)+' L'+(32+Math.cos(a+0.13)*17).toFixed(1)+' '+(36+Math.sin(a+0.13)*17).toFixed(1)}o+='<path d="'+sp+'" fill="#6b4b30" stroke="'+ink+'" stroke-width="1.5" stroke-linejoin="round"/>'}
    else if(an==='Fox')o+='<path d="M15 26 L19 8 L28 20 Z M49 26 L45 8 L36 20 Z" fill="'+f+'" stroke="'+ink+'" stroke-width="2" stroke-linejoin="round"/>';
    else if(an==='Hare')o+='<ellipse cx="24" cy="13" rx="4.5" ry="12" fill="'+f+'" stroke="'+ink+'" stroke-width="2"/><ellipse cx="40" cy="13" rx="4.5" ry="12" fill="'+f+'" stroke="'+ink+'" stroke-width="2"/>';
    else if(an==='Owl')o+='<path d="M17 24 L18 13 L26 20 Z M47 24 L46 13 L38 20 Z" fill="'+f+'" stroke="'+ink+'" stroke-width="2" stroke-linejoin="round"/>';
    else if(!BIRDS[an]&&an!=='Newt'&&an!=='Mole')o+='<circle cx="19" cy="21" r="6.5" fill="'+f+'" stroke="'+ink+'" stroke-width="2"/><circle cx="45" cy="21" r="6.5" fill="'+f+'" stroke="'+ink+'" stroke-width="2"/>';
    o+='<circle cx="32" cy="36" r="18" fill="'+f+'" stroke="'+ink+'" stroke-width="2"/>';
    if(an==='Badger')o+='<path d="M23 22 Q25 34 27 44 L22 44 Q18 32 19 25 Z M41 22 Q39 34 37 44 L42 44 Q46 32 45 25 Z" fill="'+ink+'"/>';
    if(an==='Robin')o+='<path d="M20 44 Q32 56 44 44 Q32 50 20 44 Z" fill="#e2492f"/><path d="M19 42 Q32 52 45 42 L44 47 Q32 56 20 47 Z" fill="#e2492f"/>';
    if(an==='Kingfisher')o+='<path d="M18 42 Q32 55 46 42 L45 47 Q32 56 19 47 Z" fill="#ff8a2a"/>';
    if(an==='Kestrel'||an==='Newt'){o+='<circle cx="22" cy="42" r="1.6" fill="'+ink+'"/><circle cx="42" cy="44" r="1.6" fill="'+ink+'"/><circle cx="35" cy="48" r="1.3" fill="'+ink+'"/>'}
    if(an==='Owl')o+='<circle cx="25" cy="33" r="6" fill="#fff" stroke="'+ink+'" stroke-width="1.5"/><circle cx="39" cy="33" r="6" fill="#fff" stroke="'+ink+'" stroke-width="1.5"/><circle cx="25" cy="33" r="2.8" fill="'+ink+'"/><circle cx="39" cy="33" r="2.8" fill="'+ink+'"/>';
    else if(an==='Mole')o+='<circle cx="26" cy="33" r="1.4" fill="#fff"/><circle cx="38" cy="33" r="1.4" fill="#fff"/>';
    else o+='<circle cx="26" cy="33" r="2.6" fill="'+(an==='Badger'?'#fff':ink)+'"/><circle cx="38" cy="33" r="2.6" fill="'+(an==='Badger'?'#fff':ink)+'"/><circle cx="26.8" cy="32.2" r=".8" fill="#fff"/><circle cx="38.8" cy="32.2" r=".8" fill="#fff"/>';
    if(BIRDS[an])o+='<path d="M28 39 L36 39 L32 46 Z" fill="#f2c75a" stroke="'+ink+'" stroke-width="1.5" stroke-linejoin="round"/>';
    else if(an==='Newt')o+='<path d="M24 42 Q32 47 40 42" fill="none" stroke="'+ink+'" stroke-width="2" stroke-linecap="round"/>';
    else o+='<ellipse cx="32" cy="41" rx="3.4" ry="2.4" fill="'+(an==='Mole'?'#f19bb6':ink)+'"/><path d="M29 45 Q32 47 35 45" fill="none" stroke="'+(an==='Mole'?'#f4f1ec':ink)+'" stroke-width="1.5" stroke-linecap="round"/>';
    return o+'</svg>';
  }

  window.VVV_ID = {
    // The code to send with each tap, and whether it is kept on this phone or just for this page.
    code: function () {
      if (get(CHOICE) === 'yes') {
        var k = get(KEY);
        if (!k) { k = offered; set(KEY, k); }
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
      set(KEY, null); set(CHOICE, null); offered = 'k' + fresh();
      try { if (window.posthog) { window.posthog.unregister('vvv_id'); window.posthog.opt_out_capturing(); } } catch (e) {}
    },
    kept: function () { return get(CHOICE) === 'yes' ? get(KEY) : null; },
    // Your secret name if you've said yes, or the one waiting for you if you haven't.
    name: function () { return nameFor(this.kept() || offered); },
    // Your secret name as [adjective, animal, number], and your badge as an SVG.
    parts: function () { var n = this.name().split(' '); return [n[0], n[1], n[2]]; },
    badge: critter
  };
  // Link PostHog replays to the same code, only for people who said yes.
  try { if (get(CHOICE) === 'yes' && window.posthog && get(KEY)) window.posthog.register({ vvv_id: get(KEY) }); } catch (e) {}
})();
