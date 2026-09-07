# Trend-Following Strategy (shared across accounts)

Applies to every account tracked under `accounts/` — Webull swing, both
Vanguard Roth IRA mid-term accounts, and the Principal/Ascensus 401(k)
long-term accounts. Screening itself is done by the
`stage2-momentum-screener` skill (William O'Neil CANSLIM + Mark Minervini
Trend Template); this file adds the position-management rules — hold,
trim, and pyramid (add to a winning position) — that the daily/morning
checks apply on top of a Stage classification.

## Stage2 hold/trim baseline

- **Stage 2 confirmed** (Trend Template 7-8/8, RS ≥ 70, price within 25% of
  52-week high) → hold, core position stays on.
- **Trend Template slipping to 5-6/8** → Stage 1↔2 transition, needs a
  chart read (base + breakout on volume) before trusting it.
- **Criteria 1, 2, or 4 failing (50/150/200-SMA order inverted)** → Stage
  3/4. Not a hold. Trim or exit.

## Pyramiding conditions (adding to an existing winner)

Only ever pyramid a position that is **already a confirmed Stage 2 holding**
(not a fresh idea) and only on strength, never to average down.

1. **Trend intact.** Trend Template still 7-8/8 at the time of the add —
   if any of criteria 1/2/4 have slipped, do not add (that's a trim signal,
   not a pyramid signal).
2. **Add trigger, not just "it's up."** Only add on:
   - a new pivot breakout (price clears a prior high / VCP pivot on volume
     ≥ 40-50% above the 50-day average volume), or
   - a low-volume pullback to and hold of the rising 50-day SMA followed by
     a resumption of the uptrend.
3. **Don't chase.** Skip the add if price is already more than ~5-10%
   above the breakout pivot, or more than ~10% above the 50-day SMA, with
   no fresh base — that's extended, not a clean add point.
4. **Size down each add** (classic 50/30/20 scaling): initial position =
   full base size; first add ≤ 50% of the base size; second add ≤ 25-30%
   of the base size. No more than two pyramid adds on a single name.
5. **Stops trail up with each add.** After the first add, move the stop on
   the combined position to breakeven or better; after the second add,
   the stop should protect the accumulated open profit — never let a
   pyramided position round-trip into a loss on the whole position.
6. **Stop adding the moment Stage 3/4 signs show up**: SMA order breaking
   down, a high-volume reversal day, or classic climax-top action
   (parabolic move + huge volume spike). That's an exit/trim signal, not a
   "wait it out."

## Account-tier framing

- **Webull (단기 스윙):** tightest stops (7-8% below VCP pivot), smallest
  initial size, first add on the earliest follow-through.
- **Vanguard Roth IRA (중기):** wider stop, core position; pyramids are
  the main way size grows in this tier — apply the rules above directly.
- **Principal / Ascensus 401(k) (장기):** fundamentals-first; pyramiding
  is generally not applicable given fund-menu restrictions — flag instead
  whether the current fund allocation still fits the CANSLIM/Stage2 read.
