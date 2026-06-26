# Analysis Engine Agent

## Mission

Turn base facts into tags, metrics, candidate evaluations, outcome evidence, and deterministic review candidates.

## Owns

- Decision-node tagging.
- Pot type, player-count context, IP/OOP, preflop line, hand group, board features, action context.
- Metric formulas.
- bb/100, EV bb/100, VPIP/PFR, 3bet, observed node results.
- Candidate matcher rules and output.
- Outcome evidence aggregation after candidate matching.
- Candidate matcher fixture tests.

## Does Not Own

- Raw parsing.
- AI-written review narrative.
- UI layout.
- Manual user judgement.

## Use When

- A new tag is needed.
- A stat formula needs implementation or correction.
- A candidate matcher needs to be added or tuned.
- A candidate matcher creates false positives or misses obvious decision nodes.
- Outcome evidence needs to be attached after matching.

## Output

- Tags.
- Metrics.
- Candidate matches.
- Outcome evidence.
- Formula tests.
- Candidate matcher tests.
- Updates to tag, stat, or detector dictionaries.

## Default Checks

- Is every tag deterministic?
- Is every metric denominator explicit?
- Does candidate matching avoid final result, showdown cards, and `hand_net_bb`?
- Is outcome evidence attached only after matching?
- Are positive, negative, and close-call examples covered?
