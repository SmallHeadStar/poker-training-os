# Leak Detectors

Leak detectors must be deterministic, documented, and tested with positive and negative fixtures.

## Detector Output Contract

Each detector returns:

```text
detector_name
hand_id
spot_id
matched
confidence
loss_bb
matched_reason
review_priority
representative_tags
```

## RangeAlarmIgnored

Purpose:

Detect hands where Hero faces a strong value-heavy node, has a strong but non-nut hand, and continues despite the range alarm.

Initial trigger shape:

```text
Hero has QQ/JJ/AK/AQs or similar strong non-nut hand
Hero faces 4bet, cold 4bet, or equivalent strong pressure
Node is value-heavy by position/action context
Hero continues
Hero pays postflop or stacks off
Result is materially negative, or showdown confirms top-heavy villain value
```

Output should explain that the detector is not saying the fold is always mandatory. It flags hands for review where execution may have ignored a clear range warning.

## DominatedBroadway3betCall

Purpose:

Detect dominated broadway calls against 3bets that become expensive after top pair.

Initial trigger shape:

```text
Hero opens preflop
Villain 3bets
Hero calls
Hero hand is in dominated_broadway_watchlist
Hero flops or turns top pair / good-looking one pair
Hero continues on turn or river
Result is materially negative or showdown shows domination
```

Split by:

- Hero IP vs OOP.
- BTN vs SB/BB 3bet.
- CO vs BTN/SB/BB 3bet.
- Effective stack bucket.
- Suited vs offsuit.

## OopRiverBluffcatchOvercall

Purpose:

Detect river calls out of position where Hero holds weak showdown value and repeatedly pays value-heavy river ranges.

Initial trigger shape:

```text
Hero is OOP
Hero check-calls earlier street(s)
River bet size is large or pot_plus
Hero hand class is bluffcatcher, weak pair, second pair, or top pair weak kicker
Hero calls
Result is negative
```

Split by:

- Pot type.
- Bet size bucket.
- River card texture.
- Blocker presence once blocker tagging exists.
- Villain line.

## Detector Development Rules

- Add fixture hands before or with each detector.
- Include at least one positive, one negative, and one close-call test.
- Detector confidence must be explainable.
- Do not use AI to decide whether a detector matches.
- If a rule needs poker interpretation, write the interpretation here first.
