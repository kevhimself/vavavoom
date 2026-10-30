#!/usr/bin/env python3
"""Writes pulse.json (counts only, no names) for pulse.html from CSV copies of the responses sheet.

    python3 tools/build_pulse.py DATA_DIR [--visitors N]

DATA_DIR holds the tabs saved as CSV with their header row: signals.csv, signups.csv,
access.csv, board.csv, held.csv (any missing file counts as empty), plus team.txt:
one team email or first name per line. team.txt never goes in the repo.
--visitors is PostHog's unique devices since the start date (optional).

How it counts
- A "visit": rows with an experiment code (vid.js) are grouped by that code. Rows without one
  (older rows) fall back to a run of taps with no gap over 20 minutes.
- A bubble's number is how many visits touched it (picked the thread, tapped interest,
  opened the event, tapped "I'm in"), so toggling a button ten times still counts once.
- Team visits are dropped: rows marked Who = team, and any visit that contains a team
  Access, Sign-up or Held back row (Kev, Tim, Carl).
- Nothing personal leaves this script: no names, emails, phones or free text.
"""
import csv, json, sys, pathlib, datetime, argparse, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = json.loads((ROOT / 'tools' / 'pulse_map.json').read_text())
TEAM_EMAILS, TEAM_NAMES = set(), set()  # filled from DATA_DIR/team.txt, kept out of the repo (no emails in public files)
GAP = datetime.timedelta(minutes=20)        # no code: a visit is taps with no 20-minute break
KEPT_GAP = datetime.timedelta(minutes=30)   # kept code: a new visit after 30 minutes away
PAGE_GAP = datetime.timedelta(hours=12)     # page code: one page view is one visit
PAD = datetime.timedelta(minutes=2)

# Code names, worked out exactly as vid.js does on the phone (keep the two lists in step).
ADJ = ['Brave','Sunny','Curious','Merry','Nimble','Gentle','Bold','Cheery','Swift','Jolly','Plucky','Kind','Dapper','Breezy','Spry','Mellow']
ANIMAL = ['Badger','Otter','Kingfisher','Hedgehog','Owl','Heron','Fox','Hare','Wren','Robin','Dormouse','Newt','Swift','Vole','Kestrel','Mole']

def code_name(code):
    try:
        h = int(code[1:9], 16)
    except ValueError:
        h = 0
    adj, an = ADJ[h % 16], ANIMAL[(h >> 4) % 16]
    if adj == an:
        adj = 'Merry'
    return adj, an, (h >> 8) % 98 + 2

def rows(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    with p.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def when(s):
    s = (s or '').strip()
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.datetime.strptime(s[:19], fmt)
        except ValueError:
            pass
    return None

def is_team(name='', email='', who=''):
    return (who or '').strip().lower() == 'team' or (email or '').strip().lower() in TEAM_EMAILS \
        or (name or '').strip().lower() in TEAM_NAMES

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data')
    ap.add_argument('--visitors', type=int, default=None)
    ap.add_argument('--out', default=str(ROOT / 'pulse.json'))
    a = ap.parse_args()
    D = pathlib.Path(a.data)
    tf = D / 'team.txt'  # one team email or first name per line
    if tf.exists():
        for line in tf.read_text().split():
            (TEAM_EMAILS if '@' in line else TEAM_NAMES).add(line.strip().lower())
    else:
        print('warning: no team.txt, so team visits are only dropped where Who = team')
    since = datetime.datetime.fromisoformat(MAP['since'])

    threads = {t: n for t, n in MAP['threads']}
    items = {i: dict(kind=k, thread=t, title=n) for i, k, t, n in MAP['items']}
    by_title = {v['title'].lower(): k for k, v in items.items()}

    # Team markers: moments we know a team member was on the site
    marks = []
    for r in rows(D / 'access.csv'):
        if is_team(email=r.get('Email')): marks.append(when(r.get('Received')))
    signups = rows(D / 'signups.csv')
    for r in signups:
        if is_team(r.get('Name'), r.get('Email'), r.get('Who')): marks.append(when(r.get('Received')))
    for r in rows(D / 'held.csv'):
        raw = r.get('Raw') or ''
        m_e = re.search(r'"email":"([^"]*)"', raw); m_n = re.search(r'"name":"([^"]*)"', raw)
        if is_team(m_n.group(1) if m_n else '', m_e.group(1) if m_e else ''): marks.append(when(r.get('Received')))
    marks = [m for m in marks if m]

    # Each tap row: (time, event, detail, code, kept?). The code comes from vid.js (since 30 Oct):
    # 'kept' codes belong to people who said yes to helping the experiment and last across visits;
    # 'page' codes last one page view. Older rows have no code and fall back to the 20-minute rule.
    sig = []
    for r in rows(D / 'signals.csv'):
        t = when(r.get('Received'))
        if not t or t < since or (r.get('Who') or '').strip().lower() == 'team':
            continue
        sig.append((t, (r.get('Event') or '').strip(), (r.get('Detail') or '').strip(),
                    (r.get('Visitor code') or '').strip(), (r.get('Code kept') or '').strip() == 'kept'))
    sig.sort()

    def runs(rs, gap):
        out, cur = [], []
        for s in rs:
            if cur and s[0] - cur[-1][0] > gap:
                out.append(cur); cur = []
            cur.append(s)
        if cur: out.append(cur)
        return out

    by_code = {}
    for s in sig:
        if s[3]: by_code.setdefault(s[3], []).append(s)
    visits = runs([s for s in sig if not s[3]], GAP)          # no code: guess from timing
    for code, rs in by_code.items():                           # with a code: we know it's one person
        visits += runs(rs, KEPT_GAP if rs[0][4] else PAGE_GAP)
    visits.sort(key=lambda v: v[0][0])

    def touches_team(v):
        return any(v[0][0] - PAD <= m <= v[-1][0] + PAD for m in marks)
    team_codes = {v[0][3] for v in visits if v[0][3] and v[0][4] and touches_team(v)}
    kept = [v for v in visits if not touches_team(v) and v[0][3] not in team_codes]
    helpers = {v[0][3] for v in kept if v[0][3] and v[0][4]}
    days = {}
    for v in kept:
        if v[0][3] in helpers: days.setdefault(v[0][3], set()).add(v[0][0].date())
    coded = sum(1 for v in kept if v[0][3])

    tscore = {t: 0 for t in threads}
    iscore = {i: 0 for i in items}
    iin = {i: 0 for i in items}
    stories = 0
    im_in = 0
    crew = {}
    for v in kept:
        ts, its, read = set(), set(), False
        for _, ev, det, *_ in v:
            key = det.split('|')[0].strip()
            if ev == 'thread' and key in threads:
                ts.add(key)
            elif ev in ('interest', 'tickets', 'event opened', 'outbound') and key in items:
                its.add(key)
            elif ev == 'in':
                k = key.replace('event:', '').strip()
                if k in items:
                    its.add(k); iin[k] += 1
                im_in += 1
            elif ev == 'form opened' and '/' in det:
                k = by_title.get(det.split('/', 1)[1].strip().lower())
                if k: its.add(k)
            elif ev == 'stories opened':
                read = True
        for t in ts: tscore[t] += 1
        c = v[0][3]
        if c in helpers:
            crew.setdefault(c, {'visits': 0, 'threads': {}})
            crew[c]['visits'] += 1
            for t in ts: crew[c]['threads'][t] = crew[c]['threads'].get(t, 0) + 1
        for i in its: iscore[i] += 1
        stories += read

    su = [r for r in signups if (when(r.get('Received')) or since) >= since and not is_team(r.get('Name'), r.get('Email'), r.get('Who'))]
    gate = {(r.get('Email') or '').strip().lower() for r in rows(D / 'access.csv')
            if (r.get('Email') or '').strip() and not is_team(email=r.get('Email'))}
    posts = [r for r in rows(D / 'board.csv') if (r.get('Watcher') or '').strip() == 'Green']

    def top(d, labels, n=3):
        best = sorted(((c, k) for k, c in d.items() if c > 0), key=lambda x: (-x[0], labels[x[1]]))[:n]
        return [dict(id=k, title=labels[k], n=c) for c, k in best]

    # The crew: one entry per code name. Only the name, how often they came and the threads they
    # picked. Never the code, never events or times (that would say where someone will be).
    pluckies = []
    for c, d in crew.items():
        adj, an, num = code_name(c)
        pluckies.append(dict(name=f'{adj} {an} {num}', adj=adj, animal=an, visits=d['visits'],
                             back=len(days.get(c, ())) > 1,
                             threads=[t for t, _ in sorted(d['threads'].items(), key=lambda x: -x[1])][:3]))
    pluckies.sort(key=lambda p: (-p['visits'], p['name']))

    out = dict(
        updated=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),
        since=MAP['since'],
        counts=dict(visitors=a.visitors, visits=len(kept), im_in=im_in,
                    signups=len(su), signups_in=sum(1 for r in su if "I'm in" in (r.get('Is it for them?') or '')),
                    neighbours_gate=len(gate), posts=len(posts), story_visits=stories,
                    helpers=len(helpers), returning=sum(1 for c in helpers if len(days.get(c, ())) > 1),
                    visits_known=coded),
        threads=[dict(id=t, title=n, n=tscore[t],
                      items=[dict(id=i, kind=v['kind'], title=v['title'], n=iscore[i], im_in=iin[i])
                             for i, v in items.items() if v['thread'] == t])
                 for t, n in MAP['threads']],
        top_threads=top(tscore, threads),
        top_items=top(iscore, {k: v['title'] for k, v in items.items()}),
        crew=pluckies,
    )
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print(f"pulse.json: {coded} visits known by code, {len(helpers)} helpers; {len(kept)} visits kept of {len(visits)} ({len(visits)-len(kept)} team), "
          f"{im_in} I'm in, {len(su)} sign-ups, top: {', '.join(t['title'] for t in out['top_threads'])}")

if __name__ == '__main__':
    main()
