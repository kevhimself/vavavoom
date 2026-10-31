"""Make the QR codes for hello.html: one per event, one per theme, one for the page itself.
Writes qr/<id>.svg and qr.html (a print sheet). Run: python3 tools/build_qr.py
Edit the lists below to match EVENTS and THREADS in hello.html."""
import os, qrcode, qrcode.image.svg

BASE = 'https://vavavoom.town/hello.html'
CODES = [
    ('qr', 'Va Va Voom', 'The front page', ''),
    ('walk', 'A better walk', 'Event: opens straight to I\'m in', '#walk'),
    ('pub', 'Va Va Voom at the pub', 'Event: opens straight to I\'m in', '#pub'),
    ('feedback', 'Tell us what you think', 'Feedback', '#feedback'),
    ('t-grow', 'Grow and share food', 'Theme', '#t-grow'),
    ('t-make', 'Make, mend and share', 'Theme', '#t-make'),
    ('t-nature', 'Get out in nature', 'Theme', '#t-nature'),
    ('t-homes', 'Save energy & water', 'Theme', '#t-homes'),
    ('t-move', 'Move and play', 'Theme', '#t-move'),
    ('t-talk', 'Meet and belong', 'Theme', '#t-talk'),
]
root = os.path.join(os.path.dirname(__file__), '..')
os.makedirs(os.path.join(root, 'qr'), exist_ok=True)
cards = []
for cid, title, kind, frag in CODES:
    url = BASE + (frag or '#qr')
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    img.save(os.path.join(root, 'qr', cid + '.svg'))
    cards.append(f'<figure><img src="qr/{cid}.svg" alt=""><figcaption><b>{title}</b><span>{kind}</span></figcaption></figure>')

open(os.path.join(root, 'qr.html'), 'w').write('''<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Va Va Voom QR codes</title>
<style>body{font-family:system-ui,sans-serif;margin:24px;color:#1c1a2b;background:#fff}h1{margin:0 0 4px}p{margin:0 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:18px}
figure{margin:0;border:1px solid #ddd;border-radius:10px;padding:12px;text-align:center;break-inside:avoid}
img{width:100%;max-width:160px;height:auto}figcaption b{display:block}figcaption span{font-size:13px;color:#555}</style></head><body>
<h1>Va Va Voom QR codes</h1><p>Print this page. Each code opens hello.html in the right place and is counted (signal "arrived").</p>
<div class="grid">''' + '\n'.join(cards) + '</div></body></html>\n')
print(len(CODES), 'codes written')
