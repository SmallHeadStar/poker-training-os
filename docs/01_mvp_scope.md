# MVP Scope

## V0.1 In Scope

- 5-10 sanitized GG PokerCraft fixture hands.
- Raw hand split.
- Canonical expected JSON.
- Deterministic parsing into base facts.
- Explicit `decision_nodes` supporting multiple decisions per hand.
- Decision-time tags needed for the first candidate matcher.
- DominatedBroadway candidate matcher.
- Markdown Chinese review report.
- Tests for the full vertical slice.

## Later Scope

- More parser fixtures.
- OOP River Bluffcatch candidate matcher.
- Range Alarm candidate matcher.
- Human review labels.
- Basic leak ranking.
- Training cycles.
- Cycle comparison.
- Streamlit UI.
- AI Chinese summaries grounded in computed facts.

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
- Streamlit UI in V0.1.
- AI features in V0.1.
- Training cycles in V0.1.
- Complete baseline stats dashboard in V0.1.

## Planned Leak Themes

V0.1 only implements the first vertical candidate matcher for `DominatedBroadway3betCall`.

Planned themes:

1. `DominatedBroadway3betCall`
   Hero calls 3bets with hands like KQo, KJo, AJo, QJs, hits top pair, and continues.

2. `RangeAlarmIgnored`
   Hero recognizes or should recognize a value-heavy node, but continues with strong non-nut hands.

3. `OopRiverBluffcatchOvercall`
   Hero plays OOP, arrives on river with a weak bluffcatcher, faces large pressure, and calls.

## V0.1 Acceptance

V0.1 is useful when fixture data can produce:

- Parsed base tables.
- Multiple decision nodes per hand.
- DominatedBroadway candidate matches independent of final result.
- Outcome evidence attached separately from matching.
- A Markdown report with representative hands.
- Passing tests for the slice.
