# Va Va Voom Godalming

One-page invitation site. Served with GitHub Pages from the main branch.

- `index.html` — the page
- `logos/` — logo files (SVG and PNG)

## Analytics (PostHog)

- `gate.js` loads PostHog (EU cloud) on every page that uses the gate. It is off until `PH_KEY` in `gate.js` holds the project key (starts `phc_`).
- Visits are counted without cookies until a visitor says yes on the "Can we record?" bar; session replay only runs after a yes. All inputs are masked. No email or name is sent to PostHog.
- Events: `gate passed`, `feedback sent`, plus automatic page views and clicks.
- PostHog project settings to switch on: Discard client IP data, Cookieless server hash mode (Web analytics), Session replay with Mask all inputs.

## On every release

1. Bump `VERSION` in `gate.js`.
2. If the branch pages changed, run `python3 tools/build_v.py`.
3. Add the sitting to `tools/project.json` (date, Kev's hours, what changed) and refresh `people` from the Access, Sign-ups, Board and Feedback tabs.
4. Run `python3 tools/build_stats.py` to update `built.html` (How we built this: hours, days, releases, page versions, people).
5. Commit and push to `main`. Note the change in the Notion spec page.
