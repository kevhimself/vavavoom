#!/usr/bin/env python3
"""Writes built.html, the 'How we built this' page, from tools/project.json and the git history.

    python3 tools/build_stats.py

Run it on every release (after bumping VERSION in gate.js and adding a sitting to project.json).
"""
import json, re, subprocess, pathlib, html, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
P = json.loads((ROOT / 'tools' / 'project.json').read_text())

log = subprocess.run(['git', '-C', str(ROOT), 'log', '--format=%ad|%s', '--date=format:%Y-%m-%d %H:%M'], capture_output=True, text=True).stdout.strip().splitlines()
log = [l.split('|', 1) for l in log if '|' in l]
releases = len(log) + 1  # this release is about to be committed
first = min([s['date'] for s in P['sittings']] + ([log[-1][0][:10]] if log else []))  # the project started before the repo
version = re.search(r"VERSION = window.VVV_VERSION = '([^']+)'", (ROOT / 'gate.js').read_text()).group(1)
hours = sum(s['hours'] for s in P['sittings'])
days = len({s['date'] for s in P['sittings']})
pv = P['page_versions']
pp = P['people']
release = re.search(r"VVV_RELEASE = '([^']+)'", (ROOT / 'release.js').read_text()).group(1)
team = ''.join(f'<li><b>{E(n)}</b> {E(r)}{" <span class=ai>AI</span>" if ai else ""}</li>' for n, r, ai in P['team'])
looks = ''.join(f'<a class="look" href="{E(h)}"><img src="img/looks/{E(i)}.jpg" alt="" loading="lazy"><b>{E(t)}</b><span>{E(s)}</span></a>' for i, h, t, s in P.get('looks', []))
votes = ''.join(f'<li><span class="vt">{E(t)}</span><button type="button" class="vote" data-vote="{E(i)}">I\'d use this</button></li>' for i, t in P.get('vote', []))
today = datetime.date.today().isoformat()

def d(s):
    return datetime.date.fromisoformat(s).strftime('%-d %B')

rel_hours = {}
for s in P['sittings']:
    if s.get('release'): rel_hours[s['release']] = rel_hours.get(s['release'], 0) + s['hours']
this_rel = round(rel_hours.get(release, 0), 1)
stats = [
    (f'{round(hours,1):g}', 'hours of Kev\'s time'),
    (str((datetime.date.today()-datetime.date.fromisoformat(first)).days+1), 'days since it started'),
    (f'{this_rel:g}', f'hours on this release ({release})'),
    ('£' + format(sum(c[1] for c in P.get('costs', [])), '.0f'), 'a year to run (just the web address)'),
    (str(len(P.get('releases',[]))), 'named releases'),
    (str(len(pv)), 'versions of the page'),
    (str(pp['let_in']), 'people let in so far'),
    (str(pp['in_person_tests']), 'real user tests' if pp['in_person_tests']!=1 else 'real user test'),
]

rows = ''.join(f'<tr><td>{E(d(s["date"]))}</td><td>{s["hours"]:g}h</td><td>{E(s["what"])}</td></tr>' for s in P['sittings'])
vers = ''.join(f'<li><a href="{E(f)}">{E(n)}</a> <span>{E(d(dt))}</span></li>' for f, n, dt in pv)
rels = ''.join(f'<li><span>{E(dt)}</span> <b>{E(n)}</b>{(" · " + format(round(rel_hours[n],1), "g") + "h") if n in rel_hours else ""}: {E(w)}</li>' for n, dt, w in reversed(P.get('releases', [])))
rel = ''.join(f'<li><span>{E(t)}</span> {E(m)}</li>' for t, m in log[:15])

page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>How we built this · Va Va Voom</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bowlby+One+SC&family=Courier+Prime:wght@400;700&family=Permanent+Marker&display=swap">
<style>
:root{{--paper:#f3eee2;--char:#221e19;--card:#fbf8f1;--clay:#3d5a8c;--zap:#e8337f;--volt:#c9f24a;color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--char);font-family:'Courier Prime','Courier New',monospace;font-size:16px;line-height:1.55}}
.wrap{{max-width:820px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left,0px))}}
h1,h2{{font-family:'Bowlby One SC',Impact,sans-serif;font-weight:400;line-height:1.05}}
h1{{font-size:clamp(32px,7vw,54px);margin:30px 0 8px}}
h2{{font-size:clamp(22px,4.4vw,30px);margin:36px 0 12px}}
.lede{{font-size:18px;max-width:58ch}}
.pen{{font-family:'Permanent Marker',cursive;color:#b8285f;font-size:20px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:20px 0}}
.stat{{background:var(--card);border:2px solid var(--char);box-shadow:4px 4px 0 var(--char);padding:14px}}
.stat b{{display:block;font-family:'Bowlby One SC',Impact,sans-serif;font-weight:400;font-size:36px;line-height:1}}
.stat span{{font-size:14px}}
table{{width:100%;border-collapse:collapse;font-size:14px}}td{{border-top:1px dashed #c9c0ae;padding:8px 6px;vertical-align:top}}td:first-child{{white-space:nowrap;font-weight:700}}
ul.v,ul.r{{list-style:none;padding:0;margin:0}}ul.v li,ul.r li{{padding:6px 0;border-top:1px dashed #c9c0ae}}ul.v span,ul.r span{{color:var(--clay);font-size:13px;margin-right:8px}}
a{{color:inherit;text-decoration-color:var(--zap);text-underline-offset:3px}}
.small{{font-size:13px;color:var(--clay)}}
.team{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}}
.team li{{background:var(--card);border:2px solid var(--char);padding:4px 10px;font-size:14px}}
.ai{{display:inline-block;background:var(--volt);color:var(--char);font-weight:700;font-size:11px;padding:0 6px;margin-left:4px;border:1px solid var(--char)}}
.looks{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}}
.look{{display:block;text-decoration:none;background:var(--card);border:2px solid var(--char);box-shadow:4px 4px 0 var(--char);padding:8px}}
.look img{{width:100%;height:220px;object-fit:cover;object-position:top;display:block;border:1px solid #c9c0ae}}
.look b{{display:block;margin-top:6px}} .look span{{font-size:13px}}
ul.vl{{list-style:none;padding:0;margin:0}} ul.vl li{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 0;border-top:1px dashed #c9c0ae}}
.vote{{font:inherit;font-weight:700;font-size:14px;background:var(--card);color:var(--char);border:2px solid var(--char);border-radius:999px;padding:6px 12px;cursor:pointer;white-space:nowrap}}
.vote.on{{background:var(--zap);color:#fff;border-color:var(--zap)}}
footer{{padding:30px 0 80px}}
</style>
</head>
<body>
<script src="release.js"></script>
<script src="gate.js"></script>
<main class="wrap">
<p class="small" style="margin-top:24px"><a href="hello.html">← Va Va Voom</a> · <a href="experiment.html">About this experiment</a></p>
<h1>How we built this</h1>
<p class="lede">Va Va Voom was made by a few Godalming people and Claude, in spare evenings and early mornings. It's a test of what citizens can build for themselves with the tools we have today.</p>
<p class="pen">Started {E(d(first))}. Now on Release {E(release)}.</p>
<div class="stats">{''.join(f'<div class="stat"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in stats)}</div>
<p class="small">Real user tests: {E(pp.get('in_person_note',''))}. We also test with pretend personas: a guide, not evidence. As of {E(d(pp['as_of']))}.</p>

<h2>Five looks we tried</h2>
<p>Same idea, five different coats of paint. Tap one to see it.</p>
<div class="looks">{looks}</div>

<h2 id="vote">What should we build next?</h2>
<p>This is our feature backlog, opened up. Tap <b>I'd use this</b> on anything you'd actually use, and we'll build the most wanted first. Something missing? <a href="hello.html#feedback">Tell us</a>.</p>
<ul class="vl">{votes}</ul>
<p class="small">Votes go to our private sheet with the release you saw. No name needed.</p>

<h2>Who's on the team</h2>
<ul class="team">{team}</ul>
<p class="small">AI = one of Kev's AI team, played by Claude. The people are real.</p>

<h2>Where the hours went</h2>
<p class="small">Kev's time is measured from when he was actually in the chat, plus ten minutes a sitting. Claude does the building in between, so the making took longer than this.</p><table>{rows}</table>

<h2>Every version of the page</h2>
<ul class="v">{vers}</ul>

<h2>Releases</h2>
<p>Each release is named after a local place, A to Z.</p>
<ul class="r">{rels}</ul>
<p class="small">Every small change is on <a href="https://github.com/kevhimself/vavavoom/commits/main" target="_blank" rel="noopener">GitHub</a>, for the curious.</p>
</main>
<script>
(function(){{
  var CATCHER='https://script.google.com/macros/s/AKfycbyRAgr3130xITAA6iyjVouv8fAEkjJDU-hABex8n5-UtUJEpENeIrRMFek_PGe7re7o/exec';
  var key='vvv-votes', mine={{}}; try{{mine=JSON.parse(localStorage.getItem(key))||{{}}}}catch(e){{}}
  function save(){{ try{{localStorage.setItem(key,JSON.stringify(mine))}}catch(e){{}} }}
  function paint(b){{ var on=!!mine[b.getAttribute('data-vote')]; b.classList.toggle('on',on); b.textContent=on?'Voted ✓':"I'd use this"; b.setAttribute('aria-pressed',on); }}
  document.querySelectorAll('[data-vote]').forEach(function(b){{ paint(b); b.addEventListener('click',function(){{
    var id=b.getAttribute('data-vote'), on=!mine[id]; if(on) mine[id]=Date.now(); else delete mine[id]; save(); paint(b);
    try{{ fetch(CATCHER,{{method:'POST',mode:'no-cors',headers:{{'Content-Type':'text/plain'}},body:JSON.stringify({{type:'signal',event:on?'vote':'vote removed',detail:(localStorage.getItem('vvv-team')==='1'?'[team] ':'')+id,who:(localStorage.getItem('vvv-team')==='1'?'team':'visitor'),page:location.pathname,when:new Date().toISOString(),version:(window.VVV_RELEASE||'{E(release)}')+(window.VVV_BUILD?' · '+window.VVV_BUILD:'')}})}}).catch(function(){{}}) }}catch(e){{}}
  }}); }});
}})();
</script>
<footer class="wrap small">Updated {E(d(today))} · Release {E(release)} · site version {E(version)}</footer>
</body>
</html>
'''
(ROOT / 'built.html').write_text(page, encoding='utf-8')
print(f'built.html: {hours:g}h, {days} days, {releases} releases, {len(pv)} versions, {pp["let_in"]} people, {version}')
