# Refreshing the Pulse

`pulse.html` is the hidden page that shows what neighbours are tapping on. It reads `pulse.json`, and
`pulse.json` is the only thing that changes when you refresh. It holds counts only: no names, emails,
phones or anything people typed. Never put any of that in it.

The Watcher refreshes it every morning. To refresh it on demand (say, before or during an event), tell
Claude "refresh the pulse", or run the "Refresh the Pulse" scheduled task from the Claude app.

## Steps (for Claude)

1. `git pull --rebase` in the repo.
2. Read these tabs of the responses sheet (1Gvy7ZzehWgtZVw_0lSr6uoZxs4K_cF2Tc5p16wySc7o) with the
   Google Sheets connector, then save each as CSV with its header row in a scratch folder (not in the repo):
   - `Signals!A1:F` → `signals.csv`
   - `Sign-ups!A1:Q` → `signups.csv`
   - `Access!A1:E` → `access.csv`
   - `Board!A1:K` → `board.csv`
   - `'Held back'!A1:D` → `held.csv`
   Copy the cells exactly; quote any cell with a comma or quote mark (standard CSV).
   Also write `team.txt` in the same folder: the team's emails and first names, one per line, taken
   from the Watcher's instructions or from Kev. Never commit it.
3. Optional: unique devices from PostHog (project 319273, EU), read-only:
   `SELECT count(DISTINCT person_id) FROM events WHERE event = '$pageview' AND timestamp > '2026-10-28'`
4. `python3 tools/build_pulse.py <scratch folder> --visitors <number>` (leave out `--visitors` if PostHog
   isn't reachable; the page then shows "?").
5. Check that `pulse.json` has no `@`, no phone numbers and no free text, then commit only `pulse.json`
   with the message "Pulse refresh" and push to main. GitHub Pages updates in a minute or two.
6. Reply with one line: visits, "I'm in" taps and the top three threads.

## When hello.html gets a new card

Add it to `tools/pulse_map.json` (id, kind, thread, title). Use the card's title only, never a person's name.
