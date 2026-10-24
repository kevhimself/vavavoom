/* Va Va Voom: floating header with a hamburger menu. Shared by every main page. */
(function () {
  var onHome = /\/(index\.html)?$/.test(location.pathname) || /vavavoom\/?$/.test(location.pathname);
  var home = onHome ? '' : './';
  var LINKS = [
    ['Next up', home + '#top'],
    ['What it is', home + '#h-what'],
    ['Have a poke around', home + '#compass'],
    ['Go deeper', home + '#h-deeper'],
    ['Where you\'ll find us', home + '#h-net'],
    ['How we show up', home + '#h-five'],
    ['Want in?', home + '#join'],
    ['What\'s happening', 'happening.html']
  ];
  var css = '\
html{scroll-padding-top:70px}\
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:41;background:#f3eee2}\
.vn{position:sticky;top:env(safe-area-inset-top,0px);z-index:40;background:rgba(243,238,226,.94);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-bottom:2px solid #221e19}\
.vn-in{max-width:860px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:8px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}\
.vn-logo{display:inline-flex;gap:5px;align-items:center;text-decoration:none;font-family:"Bungee",Impact,"Arial Black",sans-serif;font-size:18px;line-height:1;color:#221e19}\
.vn-logo b{font-weight:400;background:#f2c75a;padding:2px 6px}\
.vn-logo i{font-style:normal;background:#ee8fa4;padding:2px 6px}\
.vn-burger{width:44px;height:44px;display:grid;place-items:center;border:2px solid #221e19;background:#fbf8f1;cursor:pointer;padding:0}\
.vn-burger span,.vn-burger span::before,.vn-burger span::after{display:block;width:20px;height:2.5px;background:#221e19;position:relative;transition:transform .2s,background .2s}\
.vn-burger span::before,.vn-burger span::after{content:"";position:absolute;left:0}\
.vn-burger span::before{top:-6px}.vn-burger span::after{top:6px}\
.vn-burger[aria-expanded="true"] span{background:transparent}\
.vn-burger[aria-expanded="true"] span::before{transform:translateY(6px) rotate(45deg)}\
.vn-burger[aria-expanded="true"] span::after{transform:translateY(-6px) rotate(-45deg)}\
.vn-burger:focus-visible,.vn-menu a:focus-visible,.vn-menu button:focus-visible{outline:3px dashed #e8337f;outline-offset:2px}\
.vn-menu{border-top:2px solid #221e19;background:#fbf8f1}\
.vn-menu[hidden]{display:none!important}\
.vn-menu ul{list-style:none;margin:0 auto;max-width:860px;padding:10px max(16px,env(safe-area-inset-right,0px)) 16px max(16px,env(safe-area-inset-left,0px));display:grid;gap:2px}\
.vn-menu a,.vn-menu button{display:block;width:100%;text-align:left;font-family:"Bowlby One SC",Impact,"Arial Black",sans-serif;font-size:19px;color:#221e19;text-decoration:none;padding:10px 4px;background:none;border:0;border-bottom:1px dashed #c9c0ae;cursor:pointer;min-height:44px}\
.vn-menu a:hover,.vn-menu button:hover{color:#b8285f}\
.vn-menu .vn-fb{color:#3d5a8c}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var hdr = document.createElement('header');
  hdr.className = 'vn';
  hdr.innerHTML = '<div class="vn-in"><a class="vn-logo" href="' + (home || '#top') + '" aria-label="Va Va Voom, back to the top">VA VA <i>VOOM</i></a>' +
    '<button type="button" class="vn-burger" aria-expanded="false" aria-controls="vn-menu" aria-label="Menu"><span></span></button></div>' +
    '<nav class="vn-menu" id="vn-menu" hidden aria-label="Site"><ul>' +
    LINKS.map(function (l) { return '<li><a href="' + l[1] + '">' + l[0] + '</a></li>'; }).join('') +
    '<li><button type="button" class="vn-fb">Give feedback</button></li></ul></nav>';
  var btn = hdr.querySelector('.vn-burger'), menu = hdr.querySelector('.vn-menu');
  function setOpen(o) { menu.hidden = !o; btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
  btn.addEventListener('click', function () { setOpen(menu.hidden); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  hdr.querySelector('.vn-fb').addEventListener('click', function () { setOpen(false); if (window.vvvOpenFeedback) window.vvvOpenFeedback(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { setOpen(false); btn.focus(); } });
  document.addEventListener('click', function (e) { if (!menu.hidden && !hdr.contains(e.target)) setOpen(false); });

  var anchor = document.createElement('div'); anchor.id = 'top';
  function mount() { document.body.insertBefore(anchor, document.body.firstChild); document.body.insertBefore(hdr, anchor.nextSibling); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
