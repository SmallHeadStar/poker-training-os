# MVP Scope

## In Scope

- Manual import of GG PokerCraft hand history files.
- Import batches, raw hand storage, duplicate detection, parse logs.
- Deterministic parsing into base facts.
- Node tagging for the first leak scenarios.
- Core metrics for Z10 review.
- First three leak detectors.
- Markdown Chinese review report.
- Minimal UI only after parser, tags, stats, and detectors are stable.

## Out of Scope

- Real-time HUD or overlay.
- Live hand advice.
- GG client automation.
- Screen scraping.
- Shared opponent database.
- Data mining hands not played by the user.
- Full GTO solver.
- Full Hand2Note replacement.
- Broad commercial multi-user product.

## First Three Leak Themes

1. `RangeAlarmIgnored`
   Hero recognizes or should recognize a value-heavy node, but continues with strong non-nut hands.

2. `DominatedBroadway3betCall`
   Hero calls 3bets with hands like KQo, KJo, AJo, QJs, hits top pair, and pays off better ranges.

3. `OopRiverBluffcatchOvercall`
   Hero plays OOP, arrives on river with a weak bluffcatcher, faces large pressure, and overcalls.

## MVP Acceptance

The MVP is useful when one import can produce:

- Total hands and import summary.
- Actual bb/100 and EV bb/100 when available.
- Leak Ranking Top 5.
- Representative hand IDs for each leak.
- A Chinese review report.
- A next-cycle training plan.
