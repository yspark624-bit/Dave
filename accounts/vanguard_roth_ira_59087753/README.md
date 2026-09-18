# Vanguard Roth IRA — 59087753 (mid-term account)

Second mid-term account (Yeunshik Park). Set up the same way as the
[33171515 account](../vanguard_roth_ira_33171515) — auto-trading linkage
source for a daily morning Stage2 check, buy-and-hold on Stage 2
trend-following names. See the `stage2-momentum-screener` skill for the
screening rules and [`../STRATEGY.md`](../STRATEGY.md) for the shared
hold/trim/pyramid rules the morning check applies to current positions.

## Files

- `holdings/latest.json` — current snapshot (balances + positions). This is
  what the morning Routine reads.
- `holdings/history/<YYYY-MM-DD>.json` — end-of-day archive, one file per
  evening update.

## Update process

Same as the 33171515 account: every evening, paste the Vanguard dashboard
(account balances + holdings table) into the chat. Claude:

1. Copies the current `holdings/latest.json` to
   `holdings/history/<as_of date>.json`.
2. Overwrites `holdings/latest.json` with the newly pasted snapshot.
3. Commits both changes.

## Morning check

A scheduled Routine ("Vanguard Roth IRA (59087753) Morning Stage2 Check",
cron `10 12 * * 1-5` = 8:10 AM ET weekdays, currently EDT — shift to
7:10 AM ET once EST resumes in November) runs on weekday mornings before
market open. It reads `holdings/latest.json` and, for every position with
quantity > 0, runs the Stage2/CANSLIM screen:

- **Stage 2 confirmed** → hold; check the pyramiding conditions in
  [`../STRATEGY.md`](../STRATEGY.md) to see if it's also an add-to-position
  candidate.
- **Stage 3/4 or trend template failing** → flag for review (possible trim).
- Notes Fundamental (earnings/sales growth, ROE, RS rating) and Technical
  (trend template, moving averages, volume) read for each name.
- Calls out if `as_of` in the snapshot is more than one trading day old.
