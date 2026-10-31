# Va Va Voom preference model (v0.1, 31 Oct 2026)

The idea: help each person drift towards the things that are for them, and away from the things that aren't, while we learn
what people actually want. It starts with Kev on the hidden **My picks** page (`tryout.html`), and is built so a future cohort can use it too.

## 1. What every event is described by

Every event carries tags in four "what it is" groups and four "does it fit my life" groups.

| Group | Tags | Notes |
|---|---|---|
| **Theme** (what it's about) | Moving, Growing, Making, Homes and energy, Talking, Nature, Food and drink, Music art and words | The site's six themes plus two the outside events needed. |
| **Experience** (how it feels) | Playful, Meeting people, Inspiring | The site's three "feels". One per event. |
| **Flavour** (the vibe) | Slow and gentle, Deep and meaningful, Lively and social, Hands-on, Learn something | Where the quieter, deeper side lives. Several allowed. |
| **Setting** | Outdoors, Indoors | |
| **Time of day** | Daytime, Evenings | From the start time: 5pm or later is evening. |
| **Day** | Weekends, Weekdays | From the next date. |
| **Cost** | Free, Under £20, £20 and up | From the price. Unknown price: no tag. |
| **Distance** | Close to home (<3 miles), A short drive (3 to 8), Further afield (8+) | From your home place or your phone's location. |

The first four are tagged by hand when an event goes on (in `tryout.html`, the `TRY` list). The last four are worked out.

## 2. What a person tells us

On each card:

- **For me** (+1), **Maybe** (+0.3), **Not for me** (-1).
- An optional **why**: quick chips (Too far, Wrong time, Too pricey, Not my thing, Love this kind of thing, Would go with a friend, Something new for me) and a free-text line.
- **I'm in** is separate: it means "I'd actually go", not just "I like the look of it".
- Filters they choose (when, time of day, how far, free only) are recorded too: they show needs, not just tastes.

## 3. How it learns

For each tag: `weight = (sum of scores on events with that tag) / (number of those events + 1)`.

- The +1 keeps a single score from deciding everything.
- A reason nudges its practical tag a bit more: "Too far" takes another 0.5 off that event's distance tag, "Wrong time" off its time-of-day tag, "Too pricey" off its cost tag. So a "not for me" because of price doesn't count against the theme as hard.
- An event's **match** = the sum of its tags' weights. "Best for me" sorts by match once there are 3 scores (before that, by date).
- Each card says why: "Because you like: Slow and gentle, Nature", or "Maybe not: £20 and up".
- The "What we're learning about you" box shows the strongest **More of** and **Less of** tags, in plain words, so the person can see (and argue with) the model.

This is deliberately simple and readable. No black box: anyone can see why something is near the top.

## 4. Who it belongs to (the "login")

- No password, no email. "Start my picks" gives this phone a random code (`k` + 12 letters and numbers) and a secret name made from it, like *Curious Otter 23*.
- It's kept separate from the front page's "help us learn" yes, so starting picks doesn't switch on anything else.
- Another phone: type the code there. Scores so far stay on the first phone (and in our sheet copy).
- Home place and "use where I am now" stay on the phone. Only the distance band (near, mid, far) is sent.
- "Forget me on this phone" wipes the code and scores.

## 5. What we capture (Signals tab of the responses sheet)

Every row carries the code (Visitor code column), release and team flag.

| Event | Detail |
|---|---|
| `picks started` | new, or code from another phone |
| `pick` | JSON: event id, title, score, reasons, why text, tags, distance band, filters at the time. Sent on scoring and again on "Done" (use the latest per code and event). |
| `picks filter` | which filter changed, e.g. `time=evening` |
| `tryout in` | event id (I'm in) |
| `tryout link` | event id (opened their booking page) |
| `tryout added` | JSON of an event someone added |
| `tryout verdict` | team only: push or no, and event id |

## 6. How we'll use it

- **Now (Kev):** score the list, add things, see the ranking shift. Push the good ones to the main page.
- **Next:** read the `pick` rows to see which tags predict a yes, and which reasons come up most (if "Too far" dominates, local beats exciting).
- **Future cohort:** the same tags on the main page's events; a "for you" order for people who opt in; group patterns (what a Tongham couple likes vs a Godalming retiree) to decide what to put on next.

## 7. Known limits

- Distances are rough, as the crow flies, from the centre of the home place.
- Trinkfluss times aren't on their listing, so those events have no time-of-day tag.
- Burrow events without exact dates drop out of the "when" filters.
- Scores don't sync between phones yet; the sheet has the record.
- Tags are hand-picked by us, which is itself a bias. Kev's "why" text is how we'll find tags we're missing.
