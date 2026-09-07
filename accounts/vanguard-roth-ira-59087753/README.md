# Vanguard Roth IRA #59087753 (중기 / mid-term)

Owner: Yeunshik Park. Settlement fund: Vanguard Federal Money Market Fund
(VMFXX).

This account holds **established Stage 2** names with strong relative
strength — core positions meant to be held through normal pullbacks, not
swing-traded like the Webull account. See `../README.md` for the shared
methodology and `reports/` for the dated daily screens.

`holdings.json` is captured by hand from the Vanguard statement (no broker
API here) — keep it current after every trade so the daily routine sizes
pyramid adds off the right base.

## Daily routine

A scheduled Routine re-runs the Stage2/CANSLIM screen on this account's
holdings every weekday morning before the US market open, checks each
position's pyramiding condition (add-on trigger, position size, stop-loss),
flags any name that has broken down out of Stage 2, and writes a dated
report into `reports/`.
