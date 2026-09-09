# Accounts

Tracks the household's brokerage/retirement accounts so Claude can run the
`stage2-momentum-screener` skill (O'Neil CANSLIM + Minervini Trend Template)
against real holdings and route recommendations to the right account by time
horizon. See [`STRATEGY.md`](STRATEGY.md) for the shared hold/trim/pyramid
rules and [`position_policy.json`](position_policy.json) for the investor
profile and per-position exemptions — **read both before classifying
anything**.

| Tier | Broker | Account | Data source | Review cadence |
|---|---|---|---|---|
| 단기 스윙 (short-term swing) | Webull | Margin #5JF28979 | live (Webull MCP) | daily |
| 중기 (mid-term) | Vanguard | Roth IRA #59087753 — Yeunshik Park | manual snapshot | daily |
| 중기 (mid-term) | Vanguard | Roth IRA #33171515 — Jooyoung Park | manual snapshot | daily |
| 장기 (long-term) | Principal | 401(k) | pending data | quarterly |
| 장기 (long-term) | Ascensus | 401(k) | pending data | quarterly |

The 401(k) accounts hold mutual funds rebalanced quarterly, so they are
**excluded from the daily Routine** — they get reviewed on their own cadence.
Webull also has a second, currently-empty Individual Cash account (#CUV86FB6)
that isn't tracked here since it holds no positions.

## Layout

Each account directory holds:

- `holdings/latest.json` — current snapshot (pasted dashboard for Vanguard,
  live `get_account_positions` for Webull).
- `holdings/history/<date>.json` — the prior snapshot, archived on each update.
- `README.md` — account-specific notes and restrictions.
- `reports/<date>.md` / `.pdf` — dated Stage2/CANSLIM screens, so each call and
  its reasoning stay auditable and today's read can be compared against prior
  ones (closed-loop review, not a fresh take every morning).

## How updates flow

1. **Evening (user):** the current Vanguard dashboard is pasted into chat.
   Claude parses it, updates that account's `holdings/latest.json`, archives the
   previous snapshot under `holdings/history/<date>.json`, and commits.
   The Webull account needs no paste — it is pulled live via MCP.
2. **Morning (automated):** a scheduled Routine reads the latest snapshot plus
   `STRATEGY.md` / `position_policy.json`, runs the Stage2/CANSLIM screen on
   every holding, and reports hold / trim / pyramid per position.

If an evening update is missed, the morning check uses the last available
snapshot and calls out how stale it is.

## Rendering reports

`scripts/md_to_pdf.py` renders a dated report to PDF with full Hangul support
(Noto Sans CJK KR) — see `scripts/README.md`.
