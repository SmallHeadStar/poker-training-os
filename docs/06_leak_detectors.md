# Leak Detectors

Status: native decision-node leak detectors are deferred. Current V0.1 creates source-tagged issue cards from H2N4 exports and manual review inputs. Use this document when the native parser/detector route is explicitly revived, or when an issue-card rule needs detector-style decision-time safeguards.

Leak detectors must be deterministic, documented, and tested with positive and negative fixtures.

Detector matching must use only information available at the decision point. Final result, showdown, and hand net loss are outcome evidence, not match conditions.

Use three layers:

```text
Pattern Match
= decision-time candidate matching

Outcome Evidence
= result, showdown, incremental outcome, repeated count

Review Verdict
= user confirms mistake, reasonable play, cooler, solver-needed, or unknown
```

## Detector Match Contract

Each detector match returns:

```text
detector_name
detector_version
node_id
matched
match_strength
reason_codes
data_completeness
```

Outcome evidence is attached separately:

```text
hand_net_bb
decision_incremental_realized_bb
showdown_summary
outcome_notes
```

Human review verdict is stored separately:

```text
user_label
user_note
reviewed_at
review_priority
```

## DominatedBroadway3betCall

Purpose:

Detect dominated broadway calls against 3bets that become review candidates after top-pair continuation.

Initial trigger shape:

```text
Hero opens preflop
Villain 3bets
Hero calls
Hero hand is in dominated_broadway_watchlist
Hero flops or turns top pair / good-looking one pair
Hero continues on turn or river
```

Final loss or showdown domination may be outcome evidence, but must not decide the match.

Split by:

- Hero IP vs OOP.
- BTN vs SB/BB 3bet.
- CO vs BTN/SB/BB 3bet.
- Effective stack bucket.
- Suited vs offsuit.

## RangeAlarmIgnored

Purpose:

Detect hands where Hero faces a strong value-heavy node, has a strong but non-nut hand, and continues despite the range alarm.

Initial trigger shape:

```text
Hero has QQ/JJ/AK/AQs or similar strong non-nut hand
Hero faces 4bet, cold 4bet, or equivalent strong pressure
Node is value-heavy by position/action context
Hero continues
```

Postflop payment, final loss, and showdown value strength may increase review priority as outcome evidence, but must not decide the match.

## OopRiverBluffcatchOvercall

Purpose:

Detect river calls out of position where Hero holds weak showdown value and calls in a pressure node.

Initial trigger shape:

```text
Hero is OOP
Hero check-calls earlier street(s)
River bet size is large or pot_plus
Hero made-hand / pair / kicker tags indicate weak showdown value
Hero calls
```

The river call decision is the match. Whether Hero wins or loses is outcome evidence.

## Detector Development Rules

- Add fixture hands before or with each detector.
- Include at least one positive, one negative, and one close-call test.
- Detector matching must be deterministic.
- Do not use AI to decide whether a detector matches.
- Do not use final result, showdown, or hand net loss as match conditions.
- If a rule needs poker interpretation, write the interpretation here first.
