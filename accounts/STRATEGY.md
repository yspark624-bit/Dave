# Trend-Following Strategy (shared across accounts)

Applies to every account tracked under `accounts/` — Webull swing, both
Vanguard Roth IRA mid-term accounts, and the Principal/Ascensus 401(k)
long-term accounts. Screening itself is done by the
`stage2-momentum-screener` skill (William O'Neil CANSLIM + Mark Minervini
Trend Template); this file adds the position-management rules — hold,
trim, and pyramid (add to a winning position) — that the daily/morning
checks apply on top of a Stage classification.

## Investor profile and position policy

Read [`position_policy.json`](position_policy.json) **before** classifying
anything. It holds the investor profile and the per-position policy, and it
lives outside `holdings/latest.json` deliberately — the nightly snapshot is
overwritten from the pasted dashboard and would wipe it.

- **Risk posture: moderately aggressive.** Earlier entries are preferred
  over waiting for full confirmation, deeper drawdowns and higher
  volatility are tolerated, and concentration is acceptable — do not
  propose trimming a position for diversification alone. This widens the
  tolerance band; it does not suspend stop discipline on trend-managed
  positions.
- **Two position policies.** `trend` (the default) is fully governed by
  the rules below. **`sitting` is a long-term core hold the user has
  explicitly exempted from the sell rules** — report how it is doing, but
  never raise it as a trim, sell, or replace action item and never count
  it as a rule violation. QQQM in account 33171515 is `sitting`: a
  long-held position the user is deliberately holding through a loss of
  the 50-day line.

A judgement the user has already made and declined is not re-raised each
morning. Repeating a rejected recommendation daily is noise, not analysis.

## Stage2 hold/trim baseline

- **Stage 2 confirmed** (Trend Template 7-8/8, RS ≥ 70, price within 25% of
  52-week high) → hold, core position stays on.

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
- **Criteria 1, 2, or 4 failing (50/150/200-SMA order inverted)** → check
  **where price sits and which way the 50-SMA is moving** before calling it
  Stage 3/4:
  - price **below** a **falling** 50-SMA → genuine breakdown. Trim or exit.
  - price **above** a **rising** 50-SMA, with the 50-SMA merely still under
    the 150-SMA → the average is *lagging a recovery*, not rolling over.
    A sharp earlier drop dragged the 50-SMA down; the rally has outrun it
    and the crossover simply has not happened yet. That is a base breakout,
    and it is a hold — potentially an early Stage 2 entry.

> Learned the hard way (2026-09-07): OIH failed criterion 4 (SMA50 394.48 <
> SMA150 402.34) and was flagged "trim watch". But price sat **+8.38% above**
> the 50-SMA, which had turned up (**+2.05 over the last month after −24.62
> the month before**), it was +79.4% off its 52-week low and only −6.91% off
> its high. IBD had added it to **Leaders as a half position on Aug 31**.
> The criterion failed; the conclusion drawn from it did not follow.

**The recurring mistake, three times over.** Criteria 2 and 6 (XLF),
criterion 4 (OIH) — each time a criterion was read as a verdict instead of
as a symptom whose cause needed diagnosing. The Trend Template confirms an
**already-established** uptrend; a stock emerging from a long base fails
parts of it *because it has not advanced yet*, which is the opposite of
weakness. **Always ask why a criterion failed before acting on it.**

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

**The proxy is not directionally reliable. Do not use it for anything.**
All 14 holdings measured against their real IBD ratings:

| Holding | Proxy | Actual IBD RS | Error |
|---|---|---|---|
| SMH | 81 | 66 | **−15** |
| ERO | 86 | 82 | **−4** |
| RVMD 97 / XLK 67 | | 98 / 68 | +1 |
| MRX 93 / MPC 92 / GH 89 | | 98 / 98 / 95 | +5 … +6 |
| HNGE 90 / NVDA 66 | | 97 / 73 | +7 |
| CF | 77 | 89 | +12 |
| QQQM | 42 | 60 | +18 |
| XBI | 79 | 99 | +20 |
| VOO | 41 | 80 | **+39** |
| XLF | 39 | 90 | **+51** |

Errors run **−15 to +51 with no consistent direction**, so there is no
correction factor and no safe half of the range.

> An earlier version of this file claimed "the bias was low every single
> time, so a proxy that says a holding is strong is safe." That was written
> on five data points and **falsified on the next two** — SMH proxied 81
> against an actual 66, ERO 86 against 82. Both were overstatements, and
> SMH is a holding the overstatement would have kept.
>
> The lesson is about method, not about RS: **do not turn a small sample
> into a rule, and do not build an operating shortcut on top of a
> measurement already known to be unreliable.** When the real number is
> obtainable, get the real number.

So: **ask for the IBD rating.** If it is genuinely unavailable, say the RS
criterion is unscored — an honest gap beats a fabricated percentile.

### ROE and the other CANSLIM ratios are ANNUAL figures

Webull's `get_financial_indicators` returns **quarterly** `roe`, `roa` and
margins. O'Neil's thresholds (ROE ≥ 17%) are **annual**. Reading one as the
other understates every company by roughly 3-4×.

> Learned the hard way (2026-09-07): CF was written up as "ROE 8.5%, low"
> and ERO as "ROE 7.7%" — both used to mark the holdings down. Their real
> IBD **Annual ROE** figures are **39.19%** and **30.56%**: both comfortably
> above O'Neil's bar, and the criticism was withdrawn.

Do not fix this by multiplying the quarterly figure by four — that happened
to land near CF and ERO but was far off for MPC (83.6% computed vs 47.88%
actual), MRX and HNGE. Use IBD's **Annual ROE**, **SMR Rating** and
**EPS Rating** for the fundamental side, and use Webull's quarterly series
only for the *trend* (accelerating or decelerating), which is what it is
actually good for.

**A skewed universe also corrupts the market read, not just the names.**
The same basket made SPY look mid-pack and produced the conclusion
"leadership is narrow, favour individual leaders over index sleeves". The
real IBD ratings said the opposite — XLF 90 > VOO 80 > NVDA 73 > XLK 68 >
QQQM 60, i.e. financials and the broad market *leading* mega-cap tech,
which is broadening, not narrowing. Before drawing any breadth or rotation
conclusion, check it against ratings you did not compute yourself.

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

   **Classify the day, don't just compare the close.** Three different
   outcomes get three different readings:
   - intraday high *and* close above the pivot → breakout;
   - intraday high above the pivot but the close back below it → a
     **failed breakout attempt**, and if it closes near the day's low on
     unremarkable volume that is a warning, not an entry;
   - intraday high never reached the pivot → still under resistance.

   Prefer a base whose successive pullbacks are **contracting** (a real VCP,
   e.g. 12% → 8% → 6% → 4%). But before calling a *widening* sequence a
   late-stage warning, **check when the deepest leg formed and whether
   price has recovered from it**: a deep leg that formed months ago and has
   since been repaired is the **cup of a base**, not deterioration. Only a
   deep leg that is recent and still unrecovered is an actual expansion
   warning.

   > Learned the hard way (2026-09-07): NVDA's contraction sequence read
   > 13% → 5% → 10% → 19.7% and was called "volatility expanding, late
   > stage". The 19.7% leg ran 5/14→6/29 and was fully repaired — IBD
   > identified the same structure as a cup with two handles, and the
   > pivot it produced (230.47) matched ours to the cent. ERO's 16.3% leg,
   > by contrast, ran 8/26→9/3 and had not recovered — there the warning
   > was real. Same number, opposite meaning; the timestamp is what
   > separates them.
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
