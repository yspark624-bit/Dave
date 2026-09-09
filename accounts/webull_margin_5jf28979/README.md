# Webull Individual Margin #5JF28979 (단기 스윙)

Owner: Yeunshik Park. This is the active short-term swing account (a second
Webull account, Individual Cash #CUV86FB6, is currently empty/unused and is
not tracked here).

Unlike the Vanguard accounts, this account has a **live MCP connection**
(`mcp__https_api_webull_com_mcp__*`) — `get_account_positions` and
`get_account_balance` pull real-time positions instead of a hand-maintained
snapshot. `holdings/latest.json` is a point-in-time cache; the daily routine should
re-pull live data rather than trust the file if the two disagree.

## Tier rules (short-term swing)

Per `../README.md`: fresh Stage 2 / VCP breakouts only, tightest stops
(7-8% below the breakout pivot, per Minervini's swing risk rule), smallest
initial size, add only on confirmed follow-through — never on a stock still
in Stage 1 chop (SMA150 below SMA200 or the 200-day SMA still falling).

## Daily routine

Covered by the same scheduled Routine as the Vanguard Roth IRA account —
see `reports/` for dated Stage2/CANSLIM screens and pyramiding conditions.
