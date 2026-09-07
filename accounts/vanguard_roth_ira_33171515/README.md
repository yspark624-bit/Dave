# Vanguard Roth IRA — 33171515 (mid-term account)

Auto-trading linkage source for the daily morning Stage2 check. This account
is buy-and-hold on Stage 2 trend-following names (William O'Neil / Mark
Minervini methodology) — see the `stage2-momentum-screener` skill for the
screening rules applied to these holdings.

## Files

- `holdings/latest.json` — current snapshot (balances + positions). This is
  what the morning Routine reads.
- `holdings/history/<YYYY-MM-DD>.json` — end-of-day archive, one file per
  evening update.

## Update process

Every evening, Jooyoung pastes the Vanguard dashboard (account balances +
holdings table) into the chat. Claude:

1. Copies the current `holdings/latest.json` to
   `holdings/history/<as_of date>.json`.
2. Overwrites `holdings/latest.json` with the newly pasted snapshot.
3. Commits both changes.

## Morning check

A scheduled Routine ("Vanguard Roth IRA Morning Stage2 Check") runs on
weekday mornings before market open. It reads `holdings/latest.json` and,
for every position with quantity > 0, runs the Stage2/CANSLIM screen:

- **Stage 2 confirmed** → hold / consider adding.
- **Stage 3/4 or trend template failing** → flag for review (possible trim).
- Notes Fundamental (earnings/sales growth, ROE, RS rating) and Technical
  (trend template, moving averages, volume) read for each name.
- Calls out if `as_of` in the snapshot is more than one trading day old.
