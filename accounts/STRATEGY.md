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

### RS Rating — use IBD's number, and never fake it

The "RS ≥ 70" threshold is defined against **IBD's full ~6,000-name
universe**. A percentile computed against any other universe is on a
different scale and **must not be compared to that threshold.**

1. **The user is an IBD member. IBD's published RS Rating is authoritative
   — ask for it or use the one supplied, and prefer it over any computed
   proxy.**
2. Only if no IBD rating is available, compute a proxy: percentile rank of
   the IBD-style weighted return (40% × 3-month + 20% each × 6/9/12-month).
   When you do, you must:
   - rank against a **breadth-representative** universe (small and mid caps
     included), never a hand-picked large-cap basket;
   - **sanity-check the scale with SPY.** If SPY lands near the middle of
     your universe, the universe is stacked with winners and every
     percentile from it is depressed — a real market has most stocks below
     the index in a narrow-leadership tape;
   - label the number as a proxy and **state its universe**, and do not
     apply the ≥70 pass/fail to it.

> Learned the hard way (2026-09-07): XLF was scored RS 39 against a 96-name
> large-cap basket whose median 12-month return (+24.9%) beat SPY's (+20.0%),
> and was then failed against the ≥70 line and called the portfolio's weakest
> holding. Its actual IBD RS Rating was **90**. SPY scored 40 on that same
> scale — the tell that the scale, not the holding, was wrong.

Never overrule a live IBD/market fact the user supplies with a home-grown
proxy. If the two disagree, the proxy is what needs explaining.
- **Trend Template slipping to 5-6/8** → Stage 1↔2 transition, needs a
  chart read (base + breakout on volume) before trusting it. Check *which*
  criteria failed before calling it weak: **criterion 2 (150-SMA above
  200-SMA) and criterion 6 (25% above the 52-week low) fail mechanically
  for a stock that has just broken out of a long base**, because it has not
  advanced far enough yet — that is the signature of an early Stage 2
  entry, not of a laggard. A near-miss on criterion 2 (the two averages
  within a fraction of a percent, i.e. an imminent golden cross) with price
  above the 50-SMA and near its 52-week high is a *young* base breakout.
  Size it as such (IBD's own convention: half-size starter) rather than
  flagging it for replacement.
- **Criteria 1, 2, or 4 failing (50/150/200-SMA order inverted)** → Stage
  3/4. Not a hold. Trim or exit.

## Pyramiding conditions (adding to an existing winner)

Only ever pyramid a position that is **already a confirmed Stage 2 holding**
(not a fresh idea) and only on strength, never to average down.

1. **Trend intact.** Trend Template still 7-8/8 at the time of the add —
   if any of criteria 1/2/4 have slipped, do not add (that's a trim signal,
   not a pyramid signal).
2. **Add trigger, not just "it's up."** Only add on:
   - a new pivot breakout — price clears the **highest intraday high** of
     the base (not the highest close) on volume ≥ 40-50% above the 50-day
     average volume, measured **on the breakout day itself**, or
   - a low-volume pullback to and hold of the rising 50-day SMA followed by
     a resumption of the uptrend.

   Prefer a base whose successive pullbacks are **contracting** (a real VCP,
   e.g. 12% → 8% → 6% → 4%). Contractions that are *widening* (e.g.
   5% → 6% → 16%) mean volatility is expanding — that is late-stage
   behaviour, not a base, and disqualifies the add.
3. **Don't chase — measure extension against the pivot and in ATR.** Skip
   the add if either:
   - price is more than ~5% above the breakout pivot — for a breakout
     entry the **pivot** is the reference point, not the 50-day SMA; or
   - price is more than **4 × ATR(14) above the 50-day SMA**.

   Use the ATR test, not a raw "% above the 50-day SMA" cap: a fixed
   percentage wrongly rejects high-volatility leaders breaking out of a
   sound base, and wrongly waves through low-volatility names that are
   genuinely stretched. **5+ ATR above the 50-day SMA is climax
   territory** — not an add, and a reason to consider taking partial
   profits.
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
