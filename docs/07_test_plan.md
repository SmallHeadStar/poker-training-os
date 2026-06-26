# Test Plan

## Test Pyramid

Priority order:

```text
1. Parser golden tests
2. Tagging tests
3. Stat formula tests
4. Leak detector tests
5. Report snapshot tests
6. UI smoke tests
```

## Parser Golden Tests

Each sanitized raw hand should have an expected JSON file.

Test requirements:

- Hand ID is correct.
- Players and positions are correct.
- Street actions are ordered correctly.
- Board cards are correct.
- Showdown and result are correct when present.
- Parse failures are explicit and inspectable.

## Tagging Tests

Test requirements:

- Pot type tags are correct.
- IP/OOP relation is correct.
- Preflop line tags are correct.
- Hand group tags are correct.
- Action line tags are stable.

## Stat Tests

Test requirements:

- Formula examples are small and hand-checkable.
- Each stat test should name the denominator.
- EV stats are skipped or marked unavailable when source EV data is absent.

## Detector Tests

For each detector:

- Positive fixture should match.
- Negative fixture should not match.
- Close-call fixture should document expected behavior.
- Matched reason should include enough detail for review.

## Acceptance Before UI Work

Do not build the UI until:

- Parser has at least 10 hand fixtures.
- Tagging covers the first three detector shapes.
- The first three detectors have tests.
- A Markdown report can be generated from fixture data.
