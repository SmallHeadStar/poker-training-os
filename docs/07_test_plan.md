# Test Plan

## Test Pyramid

Priority order:

```text
1. Parser golden tests
2. Decision-node tests
3. Tagging tests
4. Candidate matcher tests
5. Markdown report tests
6. UI smoke tests, later
```

## V0.1 Gate

V0.1 requires one vertical slice, not full product coverage:

- 5-10 sanitized fixtures.
- Canonical parser golden tests.
- Decision-node tests.
- One candidate matcher: `DominatedBroadway3betCall`.
- Markdown report structure tests.
- Package import smoke test.

## Parser Golden Tests

Each sanitized raw hand should have an expected canonical JSON file.

Test requirements:

- Hand ID is correct.
- Players and positions are correct.
- Street actions are ordered correctly.
- Board cards are correct.
- Showdown and result are correct when present.
- Parse failures are explicit and inspectable.

## Decision-Node Tests

Test requirements:

- One hand can emit multiple decision nodes.
- Each decision node links back to a source action.
- Decision nodes use only information available at that decision point.
- Action amount fields are unambiguous.

## Tagging Tests

Test requirements:

- Pot type and player-count context are separate.
- IP/OOP relation is correct.
- Preflop line tags are correct.
- Hand groups can be multi-label.
- Board features are multi-feature, not one combined enum.

## Candidate Matcher Tests

For each candidate matcher:

- Positive fixture should match.
- Negative fixture should not match.
- Close-call fixture should document expected behavior.
- Matching must not inspect final result, showdown cards, or hand net result.

## Report Tests

Report tests should verify structure and grounding in computed facts.

The report must distinguish:

- candidate matches
- outcome evidence
- user review verdicts

## Later UI Gate

Before V0.3 UI work, the project should have:

- More parser fixtures.
- At least the planned first three candidate matchers tested.
- Basic review labels.
- Basic leak ranking.
- A Markdown report generated from fixture data.
