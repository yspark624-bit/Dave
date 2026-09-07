# Accounts

Yeunshik Park (yspark624@gmail.com) trades across four accounts on three time
horizons. Every screen in this repo (`stage2-momentum-screener` skill) frames
its verdicts in these terms — never a generic "buy/sell".

| Tier | Broker | Account | Data source | Review cadence | Role |
|---|---|---|---|---|---|
| 단기 스윙 (short-term swing) | Webull | Margin #5JF28979 | live (Webull MCP) | **daily** | Fresh Stage 2 / VCP breakouts, tightest stops, smallest size |
| 중기 (mid-term) | Vanguard | Roth IRA #59087753 (V-7753) | manual snapshot | **daily** | Established Stage 2, strong RS, core holds through normal pullbacks |
| 중기 (mid-term) | Vanguard | Roth IRA #1515* (V-1515) | **pending data** | **daily** | Same tier rules as above |
| 장기 (long-term) | Principal | 401(k) | **pending data** | quarterly | Mutual funds rebalanced quarterly — fundamentals-first, excluded from the daily Routine |
| 장기 (long-term) | Ascensus | 401(k) | **pending data** | quarterly | Mutual funds rebalanced quarterly — fundamentals-first, excluded from the daily Routine |

The daily Stage2/CANSLIM Routine covers only the three daily-cadence rows
above (V-7753, V-1515, Webull) — the 401(k) accounts hold mutual funds on a
quarterly rebalance cycle and don't need a daily technical read.

Webull also has a second, currently-empty Individual Cash account
(#CUV86FB6) that isn't tracked here since it holds no positions.

## Layout

Each account gets its own directory: `accounts/<broker>-<account-type>-<id>/`.

- `holdings.json` — hand-captured snapshot of positions (no brokerage API is
  wired up in this repo, so update this file whenever a trade fills).
- `README.md` — account-specific notes (methodology reminders, restrictions
  such as a 401(k) fund menu).
- `reports/YYYY-MM-DD.md` — dated output from the daily Stage2/CANSLIM
  screen, so today's call and the reasoning behind it stay auditable and the
  agent can compare today's read against its own prior calls (closed-loop
  review, not just a fresh take every morning).

## Methodology

All screens use William O'Neil's CANSLIM + Mark Minervini's 8-point Trend
Template — see the `stage2-momentum-screener` skill for the full checklist,
the Weinstein 4-stage model, and position-management-by-stage guidance
(including pyramiding rules: add only near a valid low-risk trigger — a VCP
breakout on volume or a pullback to a rising 50-day SMA — never chase a name
already extended past its pivot).
