#!/usr/bin/env python3
"""Builds the style branches of the Va Va Voom page from one set of words.

    python3 tools/build_v.py

Writes v-buzz.html, v-pink.html, v-grounded.html and tongham.html in the site root.
Edit the words in GODALMING / TONGHAM below, then run it again.
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VVV_URL = 'https://script.google.com/macros/s/AKfycbyRAgr3130xITAA6iyjVouv8fAEkjJDU-hABex8n5-UtUJEpENeIrRMFek_PGe7re7o/exec'
E = html.escape

# ---------------------------------------------------------------- line drawings
ICON = {
 'home': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 'food': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21V11"/><path d="M12 13c0-4 3-6 7-6 0 4-3 6-7 6Z"/><path d="M12 15c0-3-2-5-6-5 0 3 2 5 6 5Z"/></svg>',
 'land': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21v-5"/><path d="M12 3 6 13h12Z"/><path d="M3 21h18"/></svg>',
 'well': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10Z"/></svg>',
 'money': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.7 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6.5V8m0 8v1.5"/></svg>',
 'love': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M3 20c0-3 2.5-5 5-5s5 2 5 5"/><path d="M11 20c0-3 2.5-5 5-5s5 2 5 5"/></svg>',
 'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M4.5 9.5c3 1 5 3.5 5.5 10M19.5 9.5c-3 1-5 3.5-5.5 10M8 4.8c1.5 2 6.5 2 8 0"/></svg>',
}

def threads(place='Godalming'):
    t = GOD_T if place == 'Godalming' else TONG_T
    return [dict(x, icon=ICON[x['i']]) for x in t]

GOD_T = [
 {'n': 'Home & around', 'i': 'home', 'c': '#df8350', 'line': 'Warm homes, cheaper energy, getting around without the car.', 'tags': ['energy & solar', 'warm homes', 'water & floods', 'getting around']},
 {'n': 'Food', 'i': 'food', 'c': '#f2c75a', 'line': 'Growing it, cooking it, sharing it, knowing where it came from.', 'tags': ['growing', 'cooking together', 'local supply', 'cider & preserving']},
 {'n': 'Land & nature', 'i': 'land', 'c': '#6fa84e', 'line': 'The Lammas Lands, the heaths, the rivers, and the scruffy corners.', 'tags': ['Lammas Lands', 'heathlands', 'rivers', 'guerrilla gardening']},
 {'n': 'Being well', 'i': 'well', 'c': '#5aa9e6', 'line': 'Moving, resting, getting outside, feeling properly alive.', 'tags': ['sauna & cold water', 'walks', 'outdoors', 'rest']},
 {'n': 'Work & money', 'i': 'money', 'c': '#3d5a8c', 'ink': '#fbf8f1', 'line': 'Making a living, saving, and spending it where it keeps the town going.', 'tags': ['Money Moves', 'local economy', 'skills swap', 'AI & jobs']},
 {'n': 'Love & connection', 'i': 'love', 'c': '#ee8fa4', 'line': 'Neighbours, belonging, looking after each other.', 'tags': ['meeting neighbours', 'care', 'belonging', 'life off the feed']},
 {'n': 'Play & sport', 'i': 'play', 'c': '#6b4fa0', 'ink': '#fbf8f1', 'line': 'Making, music, and sport for the fun of it, not the league table.', 'q': 'What kind of play gets you out of the house?', 'tags': ['ceilidh', 'ultimate frisbee', 'social trail running', 'beer bike', 'making & music']},
]
TONG_T = [
 {'n': 'Home & around', 'i': 'home', 'c': '#df8350', 'line': 'New homes and old ones, cheaper energy, getting around.', 'tags': ['new estates', 'energy & solar', 'getting around', 'water & floods']},
 {'n': 'Food', 'i': 'food', 'c': '#f2c75a', 'line': 'Hops on the hill, the café-bar, and growing your own.', 'tags': ['growing on the estate', 'hops & brewing', 'cooking together', 'local supply']},
 {'n': 'Land & nature', 'i': 'land', 'c': '#6fa84e', 'line': 'Tice\'s Meadow, the Hog\'s Back, the Blackwater Valley, the forgotten corners.', 'tags': ['Tice\'s Meadow', 'chalk downland', 'Blackwater Valley', 'guerrilla gardening']},
 {'n': 'Being well', 'i': 'well', 'c': '#5aa9e6', 'line': 'A sauna in the woods, a walk up the ridge, a proper rest.', 'tags': ['sauna & cold showers', 'walks', 'outdoors', 'rest']},
 {'n': 'Work & money', 'i': 'money', 'c': '#3d5a8c', 'ink': '#fbf8f1', 'line': 'Working from home, spending local, swapping skills.', 'tags': ['local economy', 'skills swap', 'working from home', 'AI & jobs']},
 {'n': 'Love & connection', 'i': 'love', 'c': '#ee8fa4', 'line': 'Finding out what\'s on without the feed. Knowing your neighbours.', 'tags': ['meeting neighbours', 'life off the feed', 'new here', 'been here forever']},
 {'n': 'Play & sport', 'i': 'play', 'c': '#6b4fa0', 'ink': '#fbf8f1', 'line': 'Sport for the fun of it, music, making.', 'q': 'What kind of play gets you out of the house? Not the league, the fun kind.', 'tags': ['ceilidh', 'ultimate frisbee on the Rec', 'social running', 'beer bike', 'making & music']},
]

SAUNA = {
 'title': 'Treat yourself this winter: the Waggon Sauna',
 'by': 'Hosted by Elenid Coleman at the Hampton Estate, Seale. A wood-fired sauna in a waggon, on a woodland walk, with bucket and woodland showers to cool off.',
 'tips': [
   '<b>Open:</b> Thursday 4 to 8pm, Friday 7 to 11am (the early commuter dip), Saturday 4 to 8pm, Sunday 8am to noon. Check the booking page, as times change with the seasons.',
   '<b>Top tip:</b> get the Trailblazer pass. It works out at about £16 a session instead of £20.',
   '<b>Go with:</b> a friend or three. Take the corner seat if you like it hot.',
 ],
 'credit': 'Good news from Jules, after a Sunday morning visit.',
 'url': 'https://www.thewaggonsauna.co.uk/',
}

FIVE = ['Come as you are.', 'Talk less, do more.', "We're all leaders here. It's our space, and we all look after it.", 'Deep chats and silliness, in equal measure.', "If it's alive, we follow it."]
NOT_FOR = ["You're here to make speeches.", "You'd rather talk about it than do it.", 'You want the mic all to yourself.', 'You want somewhere to moan.', 'You want to look green more than do green.']
WAYS = [
 ('Come and do', 'Turn up, get your hands dirty, make something. Learn a skill from a neighbour.'),
 ('See the numbers', 'What the solar actually saved. How much rain a roof catches. What the town taps on most.'),
 ('Read the stories', 'Good news from round here, long and short. The people, the places, the why.'),
]

GODALMING = {
 'slug': 'Godalming', 'place': 'Godalming',
 'eyebrow': 'Godalming · psst, pass it on',
 'primary': "Let's make Godalming awesome. Together, for real.",
 'secondary': 'Godalming people getting unstuck. We learn things, with our hands and with good tech, make things, and do small brave things together. With a lot of laughs.',
 'serious': 'Playful, yes. But we mean it: real projects, real people, change you can see from your front door.',
 'next': {'label': 'Next up', 'title': "People's Emergency Briefing", 'when': 'Saturday 31 October, 10.30am · Shackleford',
          'what': 'Tim and Sue explain plainly where things have got to and what we can do here. Then a wander round Norney Farm.',
          'proof': '40-odd of us are going. Room for about 100.', 'url': 'https://www.tickettailor.com/events/jseverest/2441375', 'cta': 'Get tickets →'},
 'then': ('Then', 'The Human Bit', 'Thursday 12 November, 7 to 9pm · the studio on the hill · free', 'A circle on being analogue humans in a digital world. Real stories about AI: where it helps, where it takes over, where we stay human. Hosted by Kev.', 'happening.html#human-bit', 'people/kev.jpg'),
 'easy': ('Or start easy:', 'a walk and a pint.', "I'd come for a walk →", 'A walk and a pint', 'Where would you walk? Any day or time that suits you?'),
 'projects': [
   ('Home & around', 'Choosing solar', 'Tim', 'Norney', 'How Tim chose his solar, battery and rain tanks, what they really save, and what he\'d do differently.'),
   ('Being well', 'Micro homes, off-grid loos and a community sauna', 'Carl', 'Green Spaces', 'Small, clever buildings, loos that need no mains, and a sauna to share. Learn by building.'),
   ('Land & nature', 'Bug houses and vertical gardens', 'Rieks', 'Milford', 'Homes for the small wild things, and how to grow up a wall when you have no room to grow out.'),
 ],
 'more_url': 'happening.html',
 'good': [
   ('Norney Farm', 'Tim gave Claude a floor plan and got back a 3D model of the bungalow that works out how much rain each roof catches. Numbers people, this one\'s for you.'),
   ('The briefing', 'Forty-odd tickets gone for 31 October. Not bad for a Saturday morning about the state of the world.'),
 ],
 'odd': ['See things a bit differently from everyone else?', 'Quietly the odd one out at the dinner party?', 'Maybe this is your place.'],
 'faces': {'Kev': 'people/kev.jpg', 'Tim': 'people/tim.jpg', 'Carl': 'people/carl.jpg', 'Rieks': 'people/reiks.jpg', 'Ruth': 'people/ruth.jpg'},
 'people': [('Kev', 'Started it. Runs his home on sunshine and small computers.'), ('Tim', 'Norney Farm. Solar, rain, cider, 3D models.'), ('Sue', 'Hosts the briefings. Has the time and the questions.'),
            ('Carl', 'Builds small, clever things. Will tell you if it\'s too silly.'), ('Rieks', 'Milford. Bug houses and walls that grow.'), ('Ruth', 'Coaching for when life shifts under your feet.')],
 'places': [('Norney Farm', 'Land, fire, muddy boots. Where things get made.', 'roots.html'), ('The studio on the hill', 'Circles, quiet thinking, the occasional loud idea.', 'circle.html'), ('Trinkfluss', 'The clubhouse. Bastian pours, we plot.', 'nest.html')],
}

TONGHAM = {
 'slug': 'Tongham', 'place': 'Tongham',
 'eyebrow': 'Tongham · under the Hog\'s Back · psst, pass it on',
 'primary': "Let's make Tongham awesome. Together, for real.",
 'secondary': 'New here or been here forever, off the feed or on it: this is where you find out what\'s on, meet the neighbours, and do something worthwhile together, even if you won\'t be here forever.',
 'serious': 'Not another village hall evening. Real things, nearby, with people you\'ll want to see again.',
 'next': {'label': 'Next up · an idea, not a date yet', 'title': 'A walk up the ridge and a pint', 'when': 'A weekend afternoon in November, if enough of you fancy it',
          'what': 'Up the Hampton Estate\'s permissive path to the viewpoint over the Surrey Hills (about 2km there and back), then down to the Hogs Back Brewery for a pint.',
          'proof': 'Ten "I\'d come"s and we pick a date.', 'url': '', 'cta': ''},
 'easy': ('Or tell us:', 'what would get you out of the house?', 'Suggest something →', 'Ideas for Tongham', 'What would you love to do round here? A ceilidh, a run, a garden, a fix-it café?'),
 'projects': [
   ('Land & nature', 'A garden on a forgotten corner', 'a neighbour', 'one of the new estates', 'Someone\'s quietly started growing on a scrap of the estate nobody uses. Want to help it spread, even if you\'re only here a couple of years?'),
   ('Land & nature', 'Volunteer days on the chalk downland', 'the Hampton Estate', 'Seale', 'Hedge planting and scrub clearing on the Hog\'s Back slopes, usually in winter. Good company, fresh air, cake if you\'re lucky.'),
   ('Play & sport', 'Sport for the fun of it', 'you?', 'the Rec', 'Ultimate frisbee on the Rec, a social run on the Blackwater Valley Path, a ceilidh in a barn. Tell us which and we\'ll find a host.'),
 ],
 'more_url': '',
 'good': [
   ('Hogs Back Brewery', 'Surrey\'s biggest independent brewer is right here, brewing with hops grown at Hampton in Seale. Tours run Fridays to Sundays, £23 with tastings.'),
   ('Tice\'s Meadow', 'An old quarry between Tongham and Badshot Lea turned into a nature reserve. Bring binoculars.'),
   ('The Rec', 'A free tennis court (no booking), a basketball court and an outdoor gym, behind the Community Centre.'),
 ],
 'odd': ['New in Tongham and can\'t work out what\'s going on?', 'Off Instagram and missing the gossip?', 'Maybe this is your place.'],
 'people': [],
 'places': [],
}

TONG_PLACES = [
 {'n': 'Hogs Back Brewery', 'k': 'business', 'll': [51.2289, -0.7319], 'd': 'Manor Farm, The Street. Shop, tap room and tours (Fri to Sun).'},
 {'n': 'St Paul\'s Church', 'k': 'place', 'll': [51.2318, -0.7314], 'd': 'Built 1865, and the only church in Surrey with a separate belfry.'},
 {'n': 'The Rec and Community Centre', 'k': 'place', 'll': [51.2343, -0.7385], 'd': 'Free tennis court, basketball, outdoor gym. Ultimate frisbee, anyone?'},
 {'n': 'Tice\'s Meadow', 'k': 'place', 'll': [51.2282, -0.7505], 'd': 'Old quarry, now a nature reserve.'},
 {'n': 'Blackwater Valley Path', 'k': 'place', 'll': [51.2380, -0.7480], 'd': 'A long path along the river valley. A social run?'},
 {'n': 'Hampton Estate', 'k': 'business', 'll': [51.2185, -0.7020], 'd': 'Farm, woods and chalk downland. Volunteer days, a viewpoint path, the hops for the brewery.'},
 {'n': 'The Waggon Sauna', 'k': 'business', 'll': [51.2215, -0.6950], 'd': 'Wood-fired sauna in the woods at Hampton. Hosted by Elenid.'},
 {'n': 'A garden on a forgotten corner', 'k': 'people', 'll': [51.2360, -0.7350], 'd': 'Somewhere on a new estate (pin is a guess). Neighbours growing on a scrap nobody used.'},
 {'n': 'Idea: a barn ceilidh', 'k': 'idea', 'll': [51.2300, -0.7270], 'd': 'Where? Tell us.'},
]
TONG_WEB = {
 'nodes': [
  {'id': 'you', 'k': 'centre', 'n': 'Tongham people', 's': 'Us', 'd': 'New and old, on the feed and off it. Everything else connects through people.'},
  {'id': 'brew', 'k': 'business', 'n': 'Hogs Back Brewery', 's': 'Brewery', 'd': 'Brews with Hampton\'s hops. Tours, a tap room, and a volunteers group, the Hogs Back Hoppers.'},
  {'id': 'hamp', 'k': 'business', 'n': 'Hampton Estate', 's': 'Hampton', 'd': 'Grows the hops, grew the sauna\'s timber, runs volunteer days on the downland.'},
  {'id': 'sauna', 'k': 'business', 'n': 'The Waggon Sauna', 's': 'Sauna', 'd': 'Built by Surrey Wood Products from Hampton timber. Hosted by Elenid.'},
  {'id': 'rec', 'k': 'place', 'n': 'The Rec', 's': 'The Rec', 'd': 'Free courts and an outdoor gym. Home of Tongham FC at Poyle Road.'},
  {'id': 'tice', 'k': 'place', 'n': 'Tice\'s Meadow', 's': 'Tice\'s', 'd': 'Quarry turned nature reserve.'},
  {'id': 'church', 'k': 'place', 'n': 'St Paul\'s', 's': 'St Paul\'s', 'd': 'The church with the separate belfry, and its hall.'},
  {'id': 'cafe', 'k': 'business', 'n': 'The café-bar and bakery', 's': 'Café-bar', 'd': 'Coffee shop by day, bar and restaurant by night. The place everyone actually goes.'},
  {'id': 'garden', 'k': 'people', 'n': 'The estate garden', 's': 'Garden', 'd': 'Neighbours growing on a forgotten corner of a new estate.'},
  {'id': 'vols', 'k': 'people', 'n': 'Downland volunteers', 's': 'Volunteers', 'd': 'Hedge planting and scrub clearing with Hampton.'},
  {'id': 'frisbee', 'k': 'idea', 'n': 'Idea: frisbee on the Rec', 's': 'Frisbee?', 'd': 'Sport for the fun of it. Would you come?'},
  {'id': 'ceilidh', 'k': 'idea', 'n': 'Idea: a barn ceilidh', 's': 'Ceilidh?', 'd': 'Music, dancing badly, a pint from up the road.'},
  {'id': 'walk', 'k': 'idea', 'n': 'Idea: ridge walk and a pint', 's': 'Walk?', 'd': 'Up the viewpoint path, down to the brewery.'},
 ],
 'links': [['you', x] for x in ['brew', 'hamp', 'sauna', 'rec', 'tice', 'church', 'cafe', 'garden', 'vols', 'frisbee', 'ceilidh', 'walk']] + [
   ['hamp', 'brew'], ['hamp', 'sauna'], ['hamp', 'vols'], ['walk', 'hamp'], ['walk', 'brew'], ['frisbee', 'rec'], ['ceilidh', 'brew'], ['garden', 'vols'], ['tice', 'vols'], ['cafe', 'ceilidh']],
}

# ---------------------------------------------------------------- logos
RABBIT = '<path d="M22 30 C14 18 12 6 17 4 C22 2 27 14 28 26" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5" stroke-linejoin="round"/><path d="M19 9 C21 14 23 19 24 24" stroke="#ee8fa4" stroke-width="3.5" stroke-linecap="round" fill="none"/><path d="M34 26 C36 12 42 2 47 5 C52 8 46 20 39 30" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5" stroke-linejoin="round"/><path d="M44 9 C42 14 39 20 37 25" stroke="#ee8fa4" stroke-width="3.5" stroke-linecap="round" fill="none"/><ellipse cx="31" cy="40" rx="17" ry="15" fill="#fbf8f1" stroke="#221e19" stroke-width="3.5"/><circle cx="25" cy="38" r="2.6" fill="#221e19"/><circle cx="37" cy="38" r="2.6" fill="#221e19"/><path d="M29 45 l2 2 l2 -2" stroke="#221e19" stroke-width="2.5" fill="#e8337f" stroke-linejoin="round"/>'
TUNNEL = '<svg class="rings" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="96" stroke="#e8337f"/><circle cx="102" cy="98" r="80" stroke="#c9f24a" stroke-dasharray="6 6"/><circle cx="99" cy="101" r="64" stroke="#ee8fa4"/><circle cx="101" cy="99" r="49" stroke="#f2c75a" stroke-dasharray="4 5"/><circle cx="100" cy="100" r="35" stroke="#5aa9e6"/><circle cx="100" cy="100" r="22" stroke="#e8337f" stroke-dasharray="3 4"/></svg>'

def logo(theme, place):
    if theme == 'buzz':
        return ('<div class="logo"><div class="tun">' + TUNNEL + '<svg class="rab" viewBox="0 0 64 64" aria-hidden="true">' + RABBIT + '</svg></div>'
                '<div class="wm"><span>VA VA</span><span class="hl">VOOM</span><small>' + place.upper() + '</small></div></div>')
    if theme == 'pink':
        return '<div class="logo"><span>VA VA</span><span class="l">VOOM</span><small>' + ' '.join(place.upper()) + '</small></div>'
    # grounded / tongham: line drawing of the sun over a ridge
    return ('<div class="logo"><svg class="ridge" viewBox="0 0 120 60" aria-hidden="true"><circle cx="78" cy="24" r="11" class="sun"/>'
            '<path d="M4 50 C22 34 34 30 48 38 S78 30 92 36 S110 44 116 50"/><path d="M4 56h112"/>'
            '<path d="M78 7v-4M93 12l3-3M63 12l-3-3M97 24h4M55 24h4"/></svg>'
            '<div class="wm">Va Va Voom<small>' + place + '</small></div></div>')

EMBLEM = ('<svg class="emblem" viewBox="0 0 200 200" role="img" aria-label="A Tongham emblem: a hop cone and a belfry under the Hog\'s Back ridge">'
 '<defs><path id="ring" d="M100 100 m-78 0 a78 78 0 1 1 156 0 a78 78 0 1 1 -156 0"/></defs>'
 '<circle cx="100" cy="100" r="94" class="e-o"/><circle cx="100" cy="100" r="64" class="e-i"/>'
 '<text class="e-t"><textPath href="#ring" startOffset="2%">TONGHAM · UNDER THE HOG\'S BACK · TOGETHER ·</textPath></text>'
 '<path class="e-l" d="M40 118 C58 100 74 96 90 104 S120 96 136 102 S154 110 160 118"/>'
 '<g class="e-l"><path d="M62 118v-26l8-8 8 8v26"/><path d="M66 92h8"/><path d="M70 84v-8"/></g>'
 '<g class="e-hop"><path d="M128 66c-10 6-14 18-10 30 8 10 22 10 28 0 4-12 0-24-10-30"/><path d="M118 80c6 3 14 3 20 0M117 90c7 4 16 4 23 0"/><path d="M132 66c0-6 4-10 10-12"/></g>'
 '<circle cx="100" cy="146" r="4" class="e-dot"/></svg>')

# ---------------------------------------------------------------- CSS
BASE = '''
*{box-sizing:border-box}
html{scroll-padding-top:70px}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.55;overflow-x:hidden}
.wrap{max-width:880px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
section{padding-block:52px}
h1,h2,h3{font-family:var(--head);font-weight:400;margin:0}
h2{font-size:clamp(28px,5.6vw,46px);line-height:1.05;margin-bottom:18px;text-wrap:balance}
h3{font-size:20px;line-height:1.15}
p{margin:0 0 12px;max-width:60ch}
a{color:inherit}
:focus-visible{outline:3px dashed var(--spark);outline-offset:3px}
.eyebrow{font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:22px 0 10px}
.big{font-size:clamp(32px,7vw,58px);line-height:1.04;max-width:16ch;text-wrap:balance;margin:6px 0 16px}
.sub{font-size:clamp(17px,2.3vw,20px)}
.serious{font-weight:700;border-left:4px solid var(--spark);padding-left:12px;margin:18px 0 24px}
.btn{display:inline-block;font-family:var(--head);font-size:17px;text-decoration:none;border:var(--bw) solid var(--line);background:var(--a);color:var(--a-ink);padding:12px 18px;box-shadow:var(--shadow);border-radius:var(--r);cursor:pointer;min-height:44px}
.btn.q{background:transparent;color:var(--ink)}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.card{background:var(--card);border:var(--bw) solid var(--line);border-radius:var(--r);padding:18px}
.nextcard{margin:8px 0 18px}
.nextcard .lbl{display:inline-block;font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;background:var(--spark);color:var(--spark-ink);padding:2px 8px;border-radius:var(--r);margin-bottom:10px}
.nextcard h3{font-size:clamp(22px,4vw,30px);margin-bottom:6px}
.nextcard .when{font-weight:700;margin-bottom:8px}
.nextcard .proof{font-weight:700;color:var(--muted)}
.thencard{display:flex;gap:14px;align-items:flex-start;text-decoration:none;color:inherit;margin:0 0 18px}
.thencard img{width:56px;height:56px;border-radius:50%;object-fit:cover;flex:none;border:var(--bw) solid var(--line)}
.thencard .lbl{display:inline-block;font-weight:700;font-size:11px;letter-spacing:.14em;text-transform:uppercase;background:var(--spark);color:var(--spark-ink);padding:1px 7px;border-radius:var(--r);margin-bottom:4px}
.thencard b{display:block;font-family:var(--head);font-weight:400;font-size:21px;line-height:1.1}
.thencard .tw{display:block;font-weight:700;font-size:14px;margin:4px 0}.thencard .td{display:block;font-size:15px}.thencard .tm{display:block;font-weight:700;margin-top:6px;text-decoration:underline;text-underline-offset:3px}
.pp{display:flex;gap:12px;align-items:flex-start}.pp img,.pp .ph{width:52px;height:52px;border-radius:50%;object-fit:cover;flex:none;border:var(--bw) solid var(--line)}
.pp .ph{display:grid;place-items:center;font-style:normal;font-family:var(--head);font-size:22px;background:var(--card)}
.easy{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:10px}
.easy b{font-family:var(--head);font-weight:400;font-size:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.pj .th{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.pj h3{margin:6px 0 4px}
.pj .lead{font-weight:700;font-size:15px;margin-bottom:8px}
.pj p{font-size:15px}
.more{display:inline-block;margin-top:16px;font-weight:700}
.feature{margin-top:18px}
.feature ul{margin:10px 0 12px;padding-left:20px}
.feature li{margin:6px 0;max-width:62ch}
.credit{font-size:14px;color:var(--muted)}
.odd p{font-family:var(--head);font-size:clamp(20px,3.6vw,28px);line-height:1.2;margin:0 0 6px}
.ways{margin:26px 0}
.ways h3{margin-bottom:6px}
.five{list-style:none;padding:0;margin:20px 0;display:grid;gap:8px}
.five li{font-family:var(--head);font-size:clamp(18px,3vw,24px);line-height:1.2}
details.nf{margin-top:12px}
details.nf summary{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 16px}
.chip{display:inline-flex;align-items:center;gap:8px;font:inherit;font-weight:700;font-size:16px;border:var(--bw) solid var(--line);background:var(--card);color:var(--ink);padding:9px 14px;border-radius:var(--r);cursor:pointer;min-height:44px}
.chip svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.chip[aria-pressed="true"]{background:var(--c);color:var(--ci,#221e19)}
.tags{border-left:6px solid var(--c);padding:6px 0 6px 16px}
.tags .tline{font-size:18px}
.tags .tq{font-weight:700}
.tlist{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 14px}
.tag{font:inherit;font-weight:700;font-size:15px;border:var(--bw) solid var(--line);background:transparent;color:var(--ink);padding:7px 12px;border-radius:var(--r);cursor:pointer;min-height:40px}
.tag:hover{background:var(--c);color:var(--ci,#221e19)}
.tadd{font:inherit;font-weight:700;background:none;border:0;color:var(--ink);text-decoration:underline;text-underline-offset:4px;cursor:pointer;padding:6px 0;min-height:44px}
.people{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px 18px;margin:8px 0 26px}
.people b{font-family:var(--head);font-weight:400;font-size:20px;display:block}
.people span{font-size:15px}
.places .card{position:relative}
.places a.door{display:inline-block;margin-top:8px;font-weight:700}
footer{padding:36px 0 90px;font-size:14px;color:var(--muted)}
.vf{position:fixed;inset:0;z-index:70;background:rgba(20,18,15,.6);display:grid;place-items:center;padding:16px}
.vf[hidden]{display:none!important}
.vf-card{width:min(460px,100%);max-height:100%;overflow:auto;background:var(--card-solid);color:var(--card-ink);border:var(--bw) solid var(--line);border-radius:var(--r);padding:22px;position:relative;box-shadow:var(--shadow)}
.vf-card h2{font-size:26px;margin:0 0 6px}
.vf-card label{display:grid;gap:4px;font-weight:700;font-size:14px;margin-bottom:10px}
.vf-card label span{font-weight:400;opacity:.75}
.vf-card input,.vf-card textarea{font:inherit;font-size:16px;padding:10px 11px;border:var(--bw) solid var(--card-ink);background:#fff;color:#221e19;border-radius:var(--r);width:100%}
.vf-card textarea{min-height:90px;resize:vertical}
.vf-x{position:absolute;right:8px;top:6px;border:0;background:none;font-size:28px;cursor:pointer;color:inherit;padding:4px 10px}
.vf-err{min-height:1.3em;font-weight:700;color:#b8285f;margin:0 0 8px}
.vf-hp{position:absolute;left:-9999px}
.vf-row{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap}
.vf-ghost{font:inherit;font-weight:700;background:none;border:0;text-decoration:underline;cursor:pointer;color:inherit}
.vf-note{font-size:13px;opacity:.75;margin-top:10px}
.share h2{font-size:clamp(24px,4.6vw,36px)}
.asks{margin:6px 0 18px;padding-left:20px}.asks li{margin:4px 0}
.vf-card select{font:inherit;font-size:16px;padding:10px 11px;border:var(--bw) solid var(--card-ink);background:#fff;color:#221e19;border-radius:var(--r);width:100%}
.vp-who{border:0;padding:0;margin:0 0 10px}.vp-who legend{font-weight:700;font-size:14px;margin-bottom:6px}
.vp-who label{display:flex;gap:8px;align-items:center;font-weight:400;margin:4px 0}.vp-who input{width:auto}
.vp-step{font-family:var(--head);font-size:17px;margin:16px 0 8px;padding-top:12px;border-top:1px dashed currentColor}
.vf-card label.chk{display:flex;gap:10px;align-items:flex-start;font-weight:400}.vf-card label.chk input{width:auto;margin-top:4px}
'''

THEME = {
'buzz': '''
:root{--bg:#221e19;--ink:#f3eee2;--muted:#cfc6b6;--card:#2e2822;--card-solid:#fbf8f1;--card-ink:#221e19;--line:#f3eee2;--a:#e8337f;--a-ink:#221e19;--spark:#c9f24a;--spark-ink:#221e19;
--head:'Bowlby One SC',Impact,'Arial Black',sans-serif;--body:'Courier Prime','Courier New',monospace;--r:0px;--shadow:5px 5px 0 #c9f24a;--bw:2px;color-scheme:dark}
.logo{display:flex;align-items:center;gap:16px;margin-top:20px}
.tun{position:relative;width:min(150px,38vw);flex:none}
.tun .rings{width:100%;height:auto;display:block}.tun .rings circle{fill:none;stroke-width:2}
.tun .rab{position:absolute;left:50%;top:50%;width:46%;transform:translate(-50%,-58%)}
@media (prefers-reduced-motion:no-preference){.tun .rings{animation:spin 26s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}}
.wm{display:flex;flex-direction:column;font-family:var(--head);font-size:clamp(34px,9vw,60px);line-height:.95}
.wm .hl{background:#ee8fa4;color:#221e19;padding:0 8px;transform:rotate(-2deg);display:inline-block;width:max-content}
.wm small{font-family:var(--body);font-weight:700;font-size:13px;letter-spacing:.3em;color:#c9f24a;margin-top:8px}
h2 span,.big span{background:#ee8fa4;color:#221e19;padding:0 8px;display:inline-block;transform:rotate(-1.5deg)}
.eyebrow{color:#c9f24a}
.card{box-shadow:4px 4px 0 rgba(201,242,74,.35)}
.pj:nth-child(2){transform:rotate(.6deg)}.pj:nth-child(1){transform:rotate(-.5deg)}
.btn.q{border-color:#f3eee2}
section+section{border-top:2px dashed #4a4238}
.serious{border-color:#e8337f}
.vn{background:rgba(34,30,25,.94)!important;border-bottom-color:#c9f24a!important}
.vn-logo{color:#f3eee2!important}.vn-logo i{background:#e8337f!important;color:#221e19}
.vn-burger{background:#2e2822!important;border-color:#f3eee2!important}.vn-burger span,.vn-burger span::before,.vn-burger span::after{background:#f3eee2!important}
.vn-burger[aria-expanded="true"] span{background:transparent!important}
.vn-menu{background:#2e2822!important;border-top-color:#c9f24a!important}.vn-menu a,.vn-menu button{color:#f3eee2!important;border-bottom-color:#4a4238!important}
body::before{background:#221e19!important}
''',
'pink': '''
:root{--bg:#f3eee2;--ink:#221e19;--muted:#3d5a8c;--card:#fbf8f1;--card-solid:#fbf8f1;--card-ink:#221e19;--line:#221e19;--a:#ee8fa4;--a-ink:#221e19;--spark:#e8337f;--spark-ink:#fbf8f1;
--head:'Bowlby One SC',Impact,'Arial Black',sans-serif;--body:'Courier Prime','Courier New',monospace;--r:0px;--shadow:4px 4px 0 #221e19;--bw:2px;color-scheme:light}
.logo{display:inline-flex;flex-direction:column;align-items:flex-start;gap:4px;background:#ee8fa4;padding:22px 26px 18px;margin-top:22px;transform:rotate(-1deg);box-shadow:4px 4px 0 rgba(38,34,28,.55)}
.logo span{font-family:'Bungee',Impact,sans-serif;font-size:clamp(46px,12vw,92px);line-height:.9}
.logo span.l{background:#f2c75a;padding:4px 12px}
.logo small{font-weight:700;font-size:14px;letter-spacing:.32em;margin-top:8px}
.nextcard .lbl{background:#c9f24a;color:#221e19}
h2::after{content:"";display:inline-block;width:.42em;height:.42em;margin-left:.22em;vertical-align:.5em;background:#e8337f;clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%)}
.pj:nth-child(1){transform:rotate(-.6deg)}.pj:nth-child(3){transform:rotate(.5deg)}
.odd p,.five li{font-family:'Permanent Marker',cursive}
.serious{border-color:#e8337f}
.credit{color:#b8285f}
#goodnews{background:#ece3cf}
''',
'grounded': '''
:root{--bg:#faf8f3;--ink:#23211d;--muted:#5b5a55;--card:#ffffff;--card-solid:#ffffff;--card-ink:#23211d;--line:#d9d4c7;--a:#23211d;--a-ink:#faf8f3;--spark:#e8806a;--spark-ink:#23211d;
--head:'Fraunces',Georgia,serif;--body:'Atkinson Hyperlegible',Verdana,sans-serif;--r:12px;--shadow:none;--bw:1px;color-scheme:light}
h1,h2,h3,.btn,.wm{font-weight:600}
.big{font-weight:700;letter-spacing:-.01em}
.logo{display:flex;align-items:flex-end;gap:12px;margin-top:22px}
.ridge{width:110px;height:auto;fill:none;stroke:#23211d;stroke-width:1.6;stroke-linecap:round}
.ridge .sun{fill:#f2c75a;stroke:#23211d}
.wm{font-family:var(--head);font-size:30px;line-height:1;font-style:italic}
.wm small{display:block;font-style:normal;font-family:var(--body);font-weight:700;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);margin-top:6px}
h2::before{content:"";display:inline-block;width:12px;height:12px;border-radius:50%;background:var(--dot,#e8337f);margin-right:12px;vertical-align:.2em}
#happening{--dot:#6fa84e}#goodnews{--dot:#f2c75a}#you{--dot:#5a9bd6}#threads{--dot:#e8806a}#who,#map-s{--dot:#6b4fa0}#in{--dot:#e8337f}
.btn{font-family:var(--body);font-weight:700}
.btn.q{border:1px solid #23211d}
.chip,.tag{border-radius:999px}
.card{box-shadow:0 1px 0 rgba(35,33,29,.04)}
.nextcard{border-left:6px solid #e8806a}
.pj{border-top:4px solid var(--c,#6fa84e)}
.odd p,.five li{font-weight:600}
section+section{border-top:1px solid #e8e3d6}
.serious{border-color:#6fa84e;font-weight:400;font-style:italic}
.vn{background:rgba(250,248,243,.95)!important;border-bottom:1px solid #d9d4c7!important}
.vn-logo{font-family:'Fraunces',Georgia,serif!important;font-style:italic;font-size:21px!important;font-weight:600}
.vn-logo i{background:none!important;color:#e8806a;padding:0!important}
.vn-burger{border:1px solid #23211d!important;border-radius:12px;background:#fff!important}
.vn-menu{background:#fff!important;border-top:1px solid #d9d4c7!important}.vn-menu a,.vn-menu button{font-family:'Fraunces',Georgia,serif!important;font-weight:600;border-bottom:1px solid #eee8db!important}
body::before{background:#faf8f3!important}
.emblem{width:min(150px,34vw);height:auto;display:block;flex:none}
.e-o{fill:#fff;stroke:#23211d;stroke-width:2}.e-i{fill:#faf8f3;stroke:#23211d;stroke-width:1.2}
.e-t{font-family:'Atkinson Hyperlegible',sans-serif;font-weight:700;font-size:12.5px;letter-spacing:2px;fill:#23211d}
.e-l,.e-l path{fill:none;stroke:#23211d;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.e-hop path{fill:none;stroke:#3f7a2e;stroke-width:2;stroke-linecap:round}.e-hop path:first-child{fill:#cfe5b0}
.e-dot{fill:#e8806a}
.door-top{display:flex;align-items:center;justify-content:space-between;gap:12px}.door-top .ridge{width:84px}.door-top .wm{font-size:26px}
#map{height:360px;border-radius:12px;border:1px solid #d9d4c7;margin:12px 0}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:14px;margin:6px 0 4px}.legend i{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:1.5px solid #23211d}
#web svg{width:100%;max-width:520px;height:auto;display:block;margin:6px auto}
.wl{stroke:#cfc8b8;stroke-width:1.2}.wl.on{stroke:#23211d;stroke-width:2}
.wn{cursor:pointer;outline:none}.wn circle{stroke:#23211d;stroke-width:1.5}.wn.on circle{stroke-width:3}
.wt{font-family:'Atkinson Hyperlegible',sans-serif;font-size:13px;font-weight:700;fill:#23211d}.wt.wc{fill:#faf8f3;font-size:12px}
.wn:focus-visible{outline:none}.wn:focus-visible circle{stroke:#e8337f;stroke-width:3}
#web-note{min-height:3em;text-align:center;max-width:46ch;margin:4px auto 0}
''',
}

FONTS = {
 'buzz': 'family=Bowlby+One+SC&family=Courier+Prime:wght@400;700',
 'pink': 'family=Bowlby+One+SC&family=Bungee&family=Courier+Prime:wght@400;700&family=Permanent+Marker',
 'grounded': 'family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,600&family=Atkinson+Hyperlegible:wght@400;700',
}

def h2(text, theme, hl=None):
    if theme == 'buzz' and hl:
        text = text.replace(hl, '<span>' + hl + '</span>')
    return text

def build(theme, D, fname, title, tongham=False):
    T = threads(D['place'])
    n = D['next']
    css_theme = THEME['grounded' if tongham else theme]
    fonts = FONTS['grounded' if tongham else theme]
    look = 'grounded' if tongham else theme
    nav = [['Next up', '#door'], ["What's happening", '#happening'], ['Share a project', '#share'], ['Good news', '#goodnews'], ['Is this you?', '#you'], ['Find your thread', '#threads']]
    nav += [['The map', '#map-s']] if tongham else [['Who we are', '#who']]
    nav += [['Want in?', '#in'], ['How we built this', 'built.html']]
    out = []
    w = out.append
    w('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex,nofollow">')
    w('<title>' + E(title) + '</title>\n<link rel="icon" href="favicon.svg" type="image/svg+xml">')
    w('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?' + fonts + '&display=swap">')
    if tongham:
        w('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">')
    w('<script>window.VVV_URL=' + json.dumps(VVV_URL) + ';window.VVV_PLACE=' + json.dumps(D['place']) + ';window.VVV_NAV=' + json.dumps(nav) + ';</script>')
    if look == 'grounded':
        w('<script>window.VVV_NAV_LOGO="Va Va <i>Voom</i>";</script>')
    w('<style>' + BASE + css_theme + '</style>\n</head>\n<body class="t-' + look + '">')
    w('<script src="gate.js"></script>\n<script src="nav.js"></script>')
    w('<!-- Built by tools/build_v.py. Edit the words there, not here. -->\n<main>')

    # front door
    w('<section id="door"><div class="wrap">')
    if tongham:
        w('<div class="door-top">' + logo('grounded', D['place']) + EMBLEM + '</div>')
    else:
        w(logo(theme, D['place']))
    w('<p class="eyebrow">' + E(D['eyebrow']) + '</p>')
    big = E(D['primary'])
    if theme == 'buzz': big = big.replace('awesome', '<span>awesome</span>')
    w('<h1 class="big">' + big + '</h1>')
    w('<p class="sub">' + E(D['secondary']) + '</p>')
    w('<p class="serious">' + E(D['serious']) + '</p>')
    w('<div class="card nextcard"><span class="lbl">' + E(n['label']) + '</span><h3>' + E(n['title']) + '</h3><p class="when">' + E(n['when']) + '</p><p>' + E(n['what']) + '</p><p class="proof">' + E(n['proof']) + '</p><div class="row">')
    if n['url']:
        w('<a class="btn" href="' + n['url'] + '" target="_blank" rel="noopener" data-sig="tickets">' + E(n['cta']) + '</a>')
        w('<button type="button" class="btn q" data-act="quick" data-thread="Tell me about the next one" data-title="Tell me about the next one" data-prompt="No feeds, no spam. Just a nudge when something good is on.">Tell me about the next one</button>')
    else:
        w('<button type="button" class="btn" data-act="board" data-thread="Meet-ups" data-tag="' + E(n['title']) + '" data-title="' + E(n['title']) + '" data-prompt="Which weekend works? Anyone you\'d bring?" data-label="When could you come?">I\'d come →</button>')
        w('<button type="button" class="btn q" data-act="quick" data-thread="Tell me about the next one" data-title="Tell me what\'s on" data-prompt="No feeds, no spam. Just a nudge when something good is on nearby.">Tell me what\'s on</button>')
    w('</div></div>')
    if D.get('then'):
        tl, tt, tw, td, tu, ti = D['then']
        w('<a class="card thencard" href="' + tu + '" data-sig="then event"><img src="' + ti + '" alt="" width="56" height="56" loading="lazy"><span><span class="lbl">' + E(tl) + '</span><b>' + E(tt) + '</b><span class="tw">' + E(tw) + '</span><span class="td">' + E(td) + '</span><span class="tm">More and I\'m interested →</span></span></a>')
    e = D['easy']
    w('<div class="easy"><b>' + E(e[0]) + '</b><span>' + E(e[1]) + '</span><button type="button" class="btn q" data-act="board" data-thread="Meet-ups" data-tag="' + E(e[3]) + '" data-title="' + E(e[3]) + '" data-prompt="' + E(e[4]) + '">' + E(e[2]) + '</button></div>')
    w('</div></section>')

    # what's happening
    w('<section id="happening"><div class="wrap"><h2>' + h2("What's happening", theme, 'happening') + '</h2>')
    w('<p>' + ('Real projects, led by real people round here. Say you\'re in and it helps them happen.' if not tongham else 'Some of it is already happening. Some of it needs you. Say you\'re in and it helps it happen.') + '</p><div class="grid">')
    col = {t['n']: t['c'] for t in T}
    for th, t, lead, where, d in D['projects']:
        w('<article class="card pj" style="--c:' + col.get(th, '#6fa84e') + '"><div class="th">' + E(th) + '</div><h3>' + E(t) + '</h3><div class="lead">with ' + E(lead) + ' · ' + E(where) + '</div><p>' + E(d) + '</p>'
          '<button type="button" class="btn q" data-act="board" data-thread="Projects" data-tag="' + E(t) + '" data-title="' + E(t) + '" data-prompt="What draws you to this? Even a line helps." data-label="What draws you to it?">I\'m in →</button></article>')
    w('</div>')
    if D['more_url']:
        w('<a class="more" href="' + D['more_url'] + '" data-sig="all projects">All six projects →</a>')
    w('</div></section>')

    # share a project
    w('<section id="share"><div class="wrap"><div class="card share"><h2>' + h2('Know a project we should all know about?', theme, 'project') + '</h2>')
    w('<p>Something brilliant happening near ' + E(D['place']) + '? Yours, a friend\'s, or one you just love. Tell us who\'s behind it, what you love about it, and the little secrets for getting the best from it. We check it, ask the person if they\'re happy, then add it here.</p>')
    w('<ul class="asks"><li>What it is, and who\'s doing it</li><li>What you love about it</li><li>Tips and little secrets</li><li>How to get involved, key dates, a link</li></ul>')
    w('<button type="button" class="btn" id="vp-open">Share a project →</button></div></div></section>')

    # good news
    w('<section id="goodnews"><div class="wrap"><h2>' + h2('Good news from round here', theme, 'Good news') + '</h2>')
    w('<p>' + ('Small wins, out loud. This is what it looks like when things move.' if not tongham else 'Things worth knowing about, right on the doorstep.') + '</p><div class="grid">')
    for t, d in D['good']:
        w('<article class="card"><h3>' + E(t) + '</h3><p style="margin-top:6px">' + E(d) + '</p></article>')
    w('</div>')
    s = SAUNA
    w('<article class="card feature"><h3>' + E(s['title']) + '</h3><p style="margin-top:8px">' + E(s['by']) + '</p><ul>' + ''.join('<li>' + x + '</li>' for x in s['tips']) + '</ul>'
      '<div class="row"><a class="btn" href="' + s['url'] + '" target="_blank" rel="noopener" data-sig="waggon sauna">Book the Waggon →</a>'
      '<button type="button" class="btn q" data-act="board" data-thread="Being well" data-tag="Sauna buddies" data-title="Sauna buddies" data-prompt="Fancy sharing a Trailblazer pass, or going together? Which day suits?">Find a sauna buddy</button></div>'
      '<p class="credit" style="margin-top:12px">' + E(s['credit']) + '</p></article>')
    w('</div></section>')

    # is this you
    w('<section id="you"><div class="wrap"><h2>' + h2('Is this you?', theme, 'you?') + '</h2><div class="odd">' + ''.join('<p>' + E(x) + '</p>' for x in D['odd']) + '</div>')
    w('<div class="ways grid">' + ''.join('<div class="card"><h3>' + E(a) + '</h3><p style="margin-top:6px">' + E(b) + '</p></div>' for a, b in WAYS) + '</div>')
    w('<h3>How we show up</h3><ul class="five">' + ''.join('<li>' + E(x) + '</li>' for x in FIVE) + '</ul>')
    w('<details class="nf"><summary>Not for everyone +</summary><p>This isn\'t for you if…</p><ul>' + ''.join('<li>' + E(x) + '</li>' for x in NOT_FOR) + '</ul><p><b>Still reading? Good sign.</b></p></details>')
    w('</div></section>')

    # threads
    w('<section id="threads"><div class="wrap"><h2>' + h2('Find your thread', theme, 'thread') + '</h2><p>Which one is speaking to you right now? Tap it. Pick one, not seven.</p>')
    w('<div class="chips" id="chips" role="group" aria-label="Threads"></div><div class="tags" id="tags" hidden aria-live="polite"></div></div></section>')

    if tongham:
        w('<section id="map-s"><div class="wrap"><h2>Tongham, mapped</h2><p>The people, places and businesses that could make this place hum. Tap a pin.</p>')
        w('<div class="legend"><span><i style="background:#3f7a2e"></i>Places</span><span><i style="background:#d9822b"></i>Businesses</span><span><i style="background:#e8337f"></i>People doing things</span><span><i style="background:#5a7fd6"></i>Ideas</span></div>')
        w('<div id="map" role="region" aria-label="Map of Tongham"></div><p class="credit">Pins are roughly placed. Missing something? Tell us.</p>')
        w('<h3 style="margin-top:28px">The web</h3><p>After the Transition Towns idea of a local web: who and what is here, and how it all connects. Tap a circle.</p>')
        w('<div id="web"></div><p id="web-note">Tap a circle to see what it connects to.</p>')
        w('<div class="row" style="justify-content:center;margin-top:10px"><button type="button" class="btn q" data-act="board" data-thread="The web" data-title="Add to the web" data-prompt="A person, a business, a place or a group we\'ve missed? Tell us what they do.">Add someone to the web →</button></div>')
        w('</div></section>')
    else:
        w('<section id="who"><div class="wrap"><h2>' + h2('Who we are', theme, 'we are') + '</h2><p>A few Godalming people who got tired of talking about it.</p><div class="people">')
        F = D.get('faces', {})
        w(''.join('<div class="pp">' + ('<img src="' + F[a] + '" alt="" width="52" height="52" loading="lazy">' if a in F else '<i class="ph">' + E(a[0]) + '</i>') + '<div><b>' + E(a) + '</b><span>' + E(b) + '</span></div></div>' for a, b in D['people']) + '</div>')
        w('<h3 style="margin-bottom:12px">Where you\'ll find us</h3><div class="grid places">' + ''.join('<div class="card"><h3>' + E(a) + '</h3><p style="margin-top:6px">' + E(b) + '</p><a class="door" href="' + u + '" data-sig="portal ' + E(a) + '">Peek inside →</a></div>' for a, b, u in D['places']) + '</div>')
        w('</div></section>')

    # want in
    w('<section id="in"><div class="wrap"><h2>' + h2('Want in?', theme, 'in?') + '</h2>')
    if tongham:
        w('<p>Leave a name and a number or email. We\'ll tell you when the first thing in Tongham is happening, and ask what you\'d like to host.</p><div class="row">'
          '<button type="button" class="btn" data-act="quick" data-thread="Tongham: count me in" data-title="Count me in" data-prompt="We\'ll tell you when something\'s happening in Tongham. No spam.">Count me in →</button></div>')
    else:
        w('<p>Two ways. Quick: leave a name and a number and we\'ll tell you when something\'s on. Or take five minutes with a few questions, one at a time, to see if this is really for you.</p><div class="row">'
          '<button type="button" class="btn" data-act="quick" data-thread="Want in: quick" data-title="Count me in" data-prompt="We\'ll tell you when something good is on. No spam.">Count me in →</button>'
          '<a class="btn q" href="index.html#join" data-sig="full questions">The five-minute questions</a></div>')
    w('</div></section>\n</main>')
    w('<footer><div class="wrap">Va Va Voom ' + E(D['place']) + ' · made by neighbours, not committees · a prototype, version <span id="ver"></span>. We count which bits get tapped so we know what to grow next. <a href="built.html">How we built this</a></div></footer>')

    # form
    w('''<div class="vf" id="vf" hidden role="dialog" aria-modal="true" aria-labelledby="vf-h"><div class="vf-card"><button type="button" class="vf-x" data-close aria-label="Close">×</button>
<div class="vf-body"><h2 id="vf-h">Add a thought</h2><p id="vf-p"></p><form novalidate>
<label><span id="vf-bigl" style="opacity:1;font-weight:700">Your idea, thought or feeling</span><textarea id="vf-big" name="post"></textarea></label>
<label hidden>Phone or email<input id="vf-contact" name="contact" type="text" autocomplete="tel"></label>
<label>Your first name<input id="vf-name" name="name" type="text" autocomplete="given-name"></label>
<label>Email <span>(optional, only if you'd like to hear back)</span><input name="email" type="email" autocomplete="email"></label>
<label class="vf-hp" aria-hidden="true">Leave this empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
<p class="vf-err" role="alert"></p><div class="vf-row"><button type="button" class="vf-ghost" data-close>Not now</button><button type="submit" class="btn">Send it →</button></div></form>
<p class="vf-note">Read by a human before anything goes anywhere. Be kind, keep it real.</p></div>
<div class="vf-done" hidden><h2>Lovely. Got it.</h2><p>We'll be in touch if it's alive. Fancy another?</p><button type="button" class="btn" data-close>Back to the page</button></div></div></div>''')
    w('''<div class="vf" id="vp" hidden role="dialog" aria-modal="true" aria-labelledby="vp-h"><div class="vf-card"><button type="button" class="vf-x" data-pclose aria-label="Close">×</button>
<div class="vf-body"><h2 id="vp-h">Share a project</h2><p>A few lines each is plenty. Only the first two are a must.</p><form novalidate>
<label>What's the project called? *<input name="title" type="text"></label>
<label>What is it? *<span>What happens, where, who it's for</span><textarea name="what"></textarea></label>
<fieldset class="vp-who"><legend>Is it yours?</legend><label><input type="radio" name="rel" value="I run it"> I run it</label><label><input type="radio" name="rel" value="I'm part of it"> I'm part of it</label><label><input type="radio" name="rel" value="I just love it" checked> I just love it</label></fieldset>
<p class="vp-step">The person behind it</p>
<label>Who's doing it?<input name="lead" type="text"></label>
<label>A little about them<span>What they're like, why they started it</span><textarea name="about"></textarea></label>
<p class="vp-step">Why it's good</p>
<label>What do you love about it?<textarea name="love"></textarea></label>
<label>Tips and little secrets<span>How to get the best from it. The corner seat, the cheaper pass, the day to go.</span><textarea name="tips"></textarea></label>
<p class="vp-step">Getting involved</p>
<label>How best to get involved<textarea name="engage"></textarea></label>
<label>Key dates or times<input name="dates" type="text"></label>
<label>A link<span>Website, booking page or Instagram</span><input name="url" type="url" inputmode="url" placeholder="https://"></label>
<label>Which thread is it closest to?<select name="thread"><option value="">Not sure</option>''' + ''.join('<option>' + E(t['n']) + '</option>' for t in T) + '''</select></label>
<label>Where is it?<input name="where" type="text"></label>
<p class="vp-step">You</p>
<label>Your first name *<input name="name" type="text" autocomplete="given-name"></label>
<label>Email <span>(optional, so we can check details with you)</span><input name="email" type="email" autocomplete="email"></label>
<label class="chk"><input type="checkbox" name="ok"> If it's not yours, I think they'd be happy to be on here. (We'll ask them before it goes up.)</label>
<label class="vf-hp" aria-hidden="true">Leave this empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
<p class="vf-err" role="alert"></p><div class="vf-row"><button type="button" class="vf-ghost" data-pclose>Not now</button><button type="submit" class="btn">Send it →</button></div></form>
<p class="vf-note">Read by a human, and checked with the person behind it, before anything goes on the site.</p></div>
<div class="vf-done" hidden><h2>Brilliant, thank you.</h2><p>We'll take a look, check with the person behind it, and add it when it's ready. Know another?</p><button type="button" class="btn" data-pclose>Back to the page</button></div></div></div>''')
    w('<script>window.VVV_THREADS=' + json.dumps(T) + ';</script>')
    if tongham:
        w('<script>window.VVV_PLACES=' + json.dumps(TONG_PLACES) + ';window.VVV_CENTRE=[51.2285,-0.7240];window.VVV_WEB=' + json.dumps(TONG_WEB) + ';</script>')
        w('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')
    w('<script src="v.js"></script>\n<script>document.getElementById("ver").textContent=(window.VVV_VERSION||"").split(" ")[0];</script>\n</body>\n</html>\n')
    (ROOT / fname).write_text('\n'.join(out), encoding='utf-8')
    print('wrote', fname)

if __name__ == '__main__':
    build('buzz', GODALMING, 'v-buzz.html', 'Va Va Voom · Buzzy')
    build('pink', GODALMING, 'v-pink.html', 'Va Va Voom · Pink')
    build('grounded', GODALMING, 'v-grounded.html', 'Va Va Voom · Grounded')
    build('grounded', TONGHAM, 'tongham.html', 'Va Va Voom Tongham', tongham=True)
