# Analysis Engine Agent

## Mission

Turn base facts into tags, metrics, and deterministic leak results.

## Owns

- Spot tagging.
- Pot type, IP/OOP, preflop line, hand group, board texture, action line.
- Metric formulas.
- bb/100, EV bb/100, VPIP/PFR, 3bet, node results.
- Leak detector rules and output.
- Detector fixture tests.

## Does Not Own

- Raw parsing.
- AI-written review narrative.
- UI layout.
- Manual user judgement.

## Use When

- A new tag is needed.
- A stat formula needs implementation or correction.
- A leak detector needs to be added or tuned.
- A detector creates false positives or misses obvious hands.

## Output

- Tags.
- Metrics.
- Leak results.
- Formula tests.
- Detector tests.
- Updates to tag, stat, or detector dictionaries.

## Default Checks

- Is every tag deterministic?
- Is every metric denominator explicit?
- Is detector matching rule-based rather than AI-based?
- Are positive, negative, and close-call examples covered?
