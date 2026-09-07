# Accounts

Tracks Jooyoung's brokerage/retirement accounts so Claude can run the
[Stage2 momentum screener](../.claude/skills/stage2-momentum-screener) against
real holdings and route recommendations to the right account by time horizon.
See [`STRATEGY.md`](STRATEGY.md) for the shared hold/trim/pyramid rules
applied on top of the Stage classification.

| Tier | Account | Role |
|---|---|---|
| Short-term swing | Webull | Fast in/out swing trades |
| Mid-term | Vanguard Roth IRA (x2) | Stage 2 trend-following core; buy & hold while in Stage 2 |
| Long-term | Principal 401(k), Ascensus 401(k) | Long-horizon retirement holdings |

Currently tracked here:

- [`vanguard_roth_ira_33171515/`](vanguard_roth_ira_33171515) — mid-term account (Jooyoung Park)
- [`vanguard_roth_ira_59087753/`](vanguard_roth_ira_59087753) — mid-term account (Yeunshik Park)

## How updates flow

1. **Evening (user):** Jooyoung pastes the current Vanguard dashboard
   (balances + holdings table) into the chat. Claude parses it and updates
   that account's `holdings/latest.json`, archiving the previous snapshot
   under `holdings/history/<date>.json`, then commits the change.
2. **Morning (automated):** A scheduled Routine reads the latest snapshot
   and runs the Stage2/CANSLIM screener on every current holding, flagging
   which are still Stage 2 (hold/add) vs. breaking down (Stage 3/4, review
   for trim), and reports the Fundamental + Technical read for each.

If an evening update is missed, the morning check uses the last available
snapshot and calls out how stale it is.
