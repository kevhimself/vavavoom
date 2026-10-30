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

## Git
Another session may edit this folder: `git pull --rebase` first, commit only your files.
Claude sessions commit as `Claude <noreply@anthropic.com>` (signed, so GitHub shows Verified), never under Kev's name.
Never rewrite or force-push main to fix old "Unverified" badges: they only mean a commit wasn't signed.
