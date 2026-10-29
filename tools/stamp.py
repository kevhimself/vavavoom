#!/usr/bin/env python3
"""Writes release.js: the one place the release name and build time live.
Every page loads it, and everything people send carries it, so we always know which version someone tested.
    python3 tools/stamp.py            # keep the release name, new build time
    python3 tools/stamp.py Garden     # start a new named release (next local place, A to Z)
"""
import sys, re, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
f = ROOT / 'release.js'
name = sys.argv[1] if len(sys.argv) > 1 else re.search(r"VVV_RELEASE = '([^']+)'", f.read_text()).group(1)
now = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime('%-d %b %H:%M')
f.write_text(f"/* One source of truth for the release. Updated by tools/stamp.py on every release. */\nwindow.VVV_RELEASE = '{name}';\nwindow.VVV_BUILD = '{now}';\n")
print('release.js:', name, now)
