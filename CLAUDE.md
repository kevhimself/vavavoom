# Va Va Voom: rules for anyone building this site

Check every new screen, card or story against these before you commit.
Full version: Notion "Va Va Voom: design patterns (safe, accessible, consensual)"
https://app.notion.com/p/40893f7bf11a8182bc6dcf1ef52242ea

## Consensual
- Nobody is featured (name, photo, story, link) without their own yes. Public online is not a yes.
- Before publishing a person, check the Consent tab of the responses sheet
  (1Gvy7ZzehWgtZVw_0lSr6uoZxs4K_cF2Tc5p16wySc7o). If they're not "Yes", use an initials card and tell Kev.
- A new use of someone (new photo, page or story) is a new ask. People named in passing count too.
- Bios in the person's own words. Never point at someone's home: invite openly.

## Personas are private (fundamental control, Kev 31 Oct 2026)
- Personas and persona panels are for Kev only. Never put a persona's name, quote, score or story in this repo,
  the site, commit messages, artifacts or anything shared. This repo is public.
- Public pages may say "we test with pretend personas", nothing more. Share findings without who said them.
- Persona work lives only in Kev's private Notion page "Va Va Voom: personas and panels (Kev only)".
- Before every release: `grep -rniE "persona|panel 0" --include=*.{html,js,json,md} .` and check no persona is named.

## Safe
- No emails, phone numbers or addresses in public files. Only the PostHog key and catcher URL are public.
- "I'm in" counts first; details are always optional. Every form says who sees details and links privacy.html.
- Paid things: price on the card, ticket/booking link before "I'm in".
- Don't make things up: prices, dates and quotes need a source. No crisis or activist framing.
- Past events fade at once, come down a week later.

## Accessible
- Short screens, one job each, ending in a real-world next step. Plain UK English, no em dashes, no insider names.
- Colour never carries meaning alone (tags are border-only with words). Strong contrast.
- "I'm in" is the only pink button, right-aligned; everything else is a quiet text link. Tap targets 44px+.
- Test at 390px and 430px wide. Empty inputs get a clear, kind message.

## Honest
- Release name visible on every page (release.js); every submission tagged with it.
- Team (Kev, Tim, Carl) excluded from usage numbers via ?team.

## Check with Kev before anything goes live (Kev, 31 Oct 2026)
- Ask Kev before pushing a visible change to main: "live now, or preview for the team first?"
- Preview route: commit to a branch (e.g. preview-<topic>), copy the changed pages into preview/ with `<base href="../">`,
  noindex and a yellow "Preview for the team" strip, and send Kev the preview/ link. Merge the branch only after the team approves.
- Fixes to something already broken, and hidden pages Kev asked for directly, can still go straight live if he says so.

## Before every release
- `python3 tools/check_links.py` must pass: every link on a live page goes to a current page and every #anchor exists.
  Old looks (v-*.html, simple*.html, happening.html...) are only linked from built.html's gallery.
  New live page? Add it to CURRENT in the script.
- Changed a dated event in EVENTS? Run `node tools/build_cal.js` so its calendar file (cal/<id>.ics) matches.

## Git
Another session may edit this folder: `git pull --rebase` first, commit only your files.
Claude sessions commit as `Claude <noreply@anthropic.com>` (signed, so GitHub shows Verified), never under Kev's name.
Never rewrite or force-push main to fix old "Unverified" badges: they only mean a commit wasn't signed.
