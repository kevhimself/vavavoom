#!/usr/bin/env python3
"""Writes pulse.json (counts only, no names) for pulse.html from CSV copies of the responses sheet.

    python3 tools/build_pulse.py DATA_DIR [--visitors N]

DATA_DIR holds the tabs saved as CSV with their header row: signals.csv, signups.csv,
access.csv, board.csv, held.csv (any missing file counts as empty), plus team.txt:
one team email or first name per line. team.txt never goes in the repo.
--visitors is PostHog's unique devices since the start date (optional).

How it counts
- A "visit" is a run of Signals rows with no gap over 20 minutes (Signals has no visitor ID).
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
GAP = datetime.timedelta(minutes=20)
PAD = datetime.timedelta(minutes=2)

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

    sig = []
    for r in rows(D / 'signals.csv'):
        t = when(r.get('Received'))
        if not t or t < since or (r.get('Who') or '').strip().lower() == 'team':
            continue
        sig.append((t, (r.get('Event') or '').strip(), (r.get('Detail') or '').strip()))
    sig.sort()

    visits, cur = [], []
    for s in sig:
        if cur and s[0] - cur[-1][0] > GAP:
            visits.append(cur); cur = []
        cur.append(s)
    if cur: visits.append(cur)
    kept = [v for v in visits if not any(v[0][0] - PAD <= m <= v[-1][0] + PAD for m in marks)]

    tscore = {t: 0 for t in threads}
    iscore = {i: 0 for i in items}
    iin = {i: 0 for i in items}
    stories = 0
    im_in = 0
    for v in kept:
        ts, its, read = set(), set(), False
        for _, ev, det in v:
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
        for i in its: iscore[i] += 1
        stories += read

    su = [r for r in signups if (when(r.get('Received')) or since) >= since and not is_team(r.get('Name'), r.get('Email'), r.get('Who'))]
    gate = {(r.get('Email') or '').strip().lower() for r in rows(D / 'access.csv')
            if (r.get('Email') or '').strip() and not is_team(email=r.get('Email'))}
    posts = [r for r in rows(D / 'board.csv') if (r.get('Watcher') or '').strip() == 'Green']

    def top(d, labels, n=3):
        best = sorted(((c, k) for k, c in d.items() if c > 0), key=lambda x: (-x[0], labels[x[1]]))[:n]
        return [dict(id=k, title=labels[k], n=c) for c, k in best]

    out = dict(
        updated=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),
        since=MAP['since'],
        counts=dict(visitors=a.visitors, visits=len(kept), im_in=im_in,
                    signups=len(su), signups_in=sum(1 for r in su if "I'm in" in (r.get('Is it for them?') or '')),
                    neighbours_gate=len(gate), posts=len(posts), story_visits=stories),
        threads=[dict(id=t, title=n, n=tscore[t],
                      items=[dict(id=i, kind=v['kind'], title=v['title'], n=iscore[i], im_in=iin[i])
                             for i, v in items.items() if v['thread'] == t])
                 for t, n in MAP['threads']],
        top_threads=top(tscore, threads),
        top_items=top(iscore, {k: v['title'] for k, v in items.items()}),
    )
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print(f"pulse.json: {len(kept)} visits kept of {len(visits)} ({len(visits)-len(kept)} team), "
          f"{im_in} I'm in, {len(su)} sign-ups, top: {', '.join(t['title'] for t in out['top_threads'])}")

if __name__ == '__main__':
    main()
