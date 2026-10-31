#!/usr/bin/env python3
"""Release check: every link on the live pages goes to a current page, and every #anchor exists.
Run from the repo root: python3 tools/check_links.py   (exit 1 if anything is wrong)
Old looks (v-*.html, simple*.html, happening.html...) may only be linked from built.html's gallery."""
import re, sys, os
CURRENT = ['hello.html','news.html','experiment.html','built.html','privacy.html','pulse.html','tryout.html','index.html']
GALLERY_OK = {'built.html'}          # the "looks we tried" gallery may link old versions
EXTRA_OK = {'circle.html'}           # the Rabbit Hole, a deliberate easter egg from the Pulse
JS_HASHES = {'hello.html': {'what','feedback','qr'}}  # opened by script, not by an id
def ids(f):
    s=open(f).read()
    found=set(re.findall(r'id=["\']([^"\']+)["\']', s)) | set(re.findall(r"\bid:\s*'([^']+)'", s))
    return found | JS_HASHES.get(f,set())
bad=[]
for page in CURRENT:
    s=open(page).read()
    for m in re.finditer(r'''(?:href|src)=["']([^"']+)["']|["']([a-z0-9_-]+\.html(?:[?#][^"']*)?)["']''', s):
        url=m.group(1) or m.group(2)
        if re.match(r'(https?:|mailto:|tel:|data:|javascript:)',url) or url.startswith('//'): continue
        path,_,frag=url.partition('#'); path=path.split('?')[0] or page
        if not path.endswith('.html'):
            if not os.path.exists(path): bad.append(f'{page}: missing file {url}')
            continue
        if not os.path.exists(path): bad.append(f'{page}: missing page {url}'); continue
        if path not in CURRENT and path not in EXTRA_OK and page not in GALLERY_OK:
            bad.append(f'{page}: links to an old page {url}')
        if frag and path in CURRENT and frag not in ids(path) and not frag.startswith('t-'):
            bad.append(f'{page}: no #{frag} on {path}')
print('\n'.join(sorted(set(bad))) or 'All links go to current pages, all anchors exist.')
sys.exit(1 if bad else 0)
