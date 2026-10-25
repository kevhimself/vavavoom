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
first = log[-1][0][:10] if log else ''
version = re.search(r"VERSION = window.VVV_VERSION = '([^']+)'", (ROOT / 'gate.js').read_text()).group(1)
hours = sum(s['hours'] for s in P['sittings'])
days = len({s['date'] for s in P['sittings']})
pv = P['page_versions']
pp = P['people']
today = datetime.date.today().isoformat()

def d(s):
    return datetime.date.fromisoformat(s).strftime('%-d %B')

stats = [
    (f'{hours:g}', 'hours of Kev\'s time'),
    (str((datetime.date.today()-datetime.date.fromisoformat(first)).days+1), 'days since it started'),
    (str(releases), 'releases'),
    (str(len(pv)), 'versions of the page'),
    (str(pp['let_in']), 'people let in so far'),
    (str(pp['in_person_tests']), 'in-person user test'),
]

rows = ''.join(f'<tr><td>{E(d(s["date"]))}</td><td>{s["hours"]:g}h</td><td>{E(s["what"])}</td></tr>' for s in P['sittings'])
vers = ''.join(f'<li><a href="{E(f)}">{E(n)}</a> <span>{E(d(dt))}</span></li>' for f, n, dt in pv)
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
footer{{padding:30px 0 80px}}
</style>
</head>
<body>
<script src="gate.js"></script>
<main class="wrap">
<p class="small" style="margin-top:24px"><a href="./">← Va Va Voom</a></p>
<h1>How we built this</h1>
<p class="lede">Va Va Voom was made by a few Godalming people and Claude, in spare evenings and early mornings. It's a test of what citizens can build for themselves with the tools we have today.</p>
<p class="pen">Started {E(d(first))}. Now on version {E(version.split(" ")[0])}.</p>
<div class="stats">{''.join(f'<div class="stat"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in stats)}</div>
<p class="small">People let in counts unique emails through the gate. Also {pp['personas']} test personas (not real visitors), {pp['signups']} sign-ups, {pp['board_posts']} board post and {pp['feedback_forms']} feedback forms so far. As of {E(d(pp['as_of']))}.</p>

<h2>Who's on the team</h2>
<p>{E(', '.join(P['team']))}.</p>

<h2>Where the hours went</h2>
<p class="small">Kev's time is measured from when he was actually in the chat, plus ten minutes a sitting. Claude does the building in between, so the making took longer than this.</p><table>{rows}</table>

<h2>Every version of the page</h2>
<ul class="v">{vers}</ul>

<h2>Latest releases</h2>
<ul class="r">{rel}</ul>
<p class="small">The full history is on <a href="https://github.com/kevhimself/vavavoom/commits/main" target="_blank" rel="noopener">GitHub</a>.</p>
</main>
<footer class="wrap small">Updated {E(d(today))} · version {E(version)}</footer>
</body>
</html>
'''
(ROOT / 'built.html').write_text(page, encoding='utf-8')
print(f'built.html: {hours:g}h, {days} days, {releases} releases, {len(pv)} versions, {pp["let_in"]} people, {version}')
