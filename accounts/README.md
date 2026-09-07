# Accounts

Yeunshik Park (yspark624@gmail.com) trades across four accounts on three time
horizons. Every screen in this repo (`stage2-momentum-screener` skill) frames
its verdicts in these terms — never a generic "buy/sell".

| Tier | Broker | Account | Role |
|---|---|---|---|
| 단기 스윙 (short-term swing) | Webull | — | Fresh Stage 2 / VCP breakouts, tightest stops, smallest size |
| 중기 (mid-term) | Vanguard | Roth IRA #59087753 | Established Stage 2, strong RS, core holds through normal pullbacks |
| 중기 (mid-term) | Vanguard | Roth IRA (2nd account) | Same tier rules as above |
| 장기 (long-term) | Principal | 401(k) | Fundamentals-first, low-volatility compounders / fund menu |
| 장기 (long-term) | Ascensus | 401(k) | Fundamentals-first, low-volatility compounders / fund menu |

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
