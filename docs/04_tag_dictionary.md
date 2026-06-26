# Tag Dictionary

Tags translate parsed facts into poker semantics. They must be deterministic and testable.

## Pot Type

Pot type is separate from player count.

```text
SRP = single-raised pot
3BP = 3bet pot
4BP = 4bet pot
5BP_PLUS = 5bet-or-larger pot
LIMPED = limped pot
```

## Player Count Context

```text
HEADS_UP
THREE_WAY
FOUR_PLUS
```

## Position Relation

```text
IP = Hero acts in position against the main villain postflop
OOP = Hero acts out of position against the main villain postflop
NA = no clear heads-up relation
```

## Preflop Line

Examples:

```text
hero_open
hero_open_call_3bet
hero_open_fold_to_3bet
hero_3bet
hero_call_open
hero_cold_call
hero_face_4bet_continue
hero_face_4bet_fold
```

## Hero Hand Groups

Hand groups are multi-label. A hand may belong to more than one group.

```text
premium_pair = AA, KK, QQ
medium_pair = JJ-77
small_pair = 66-22
suited_broadway = AKs, AQs, AJs, KQs, KJs, QJs
offsuit_broadway = AKo, AQo, AJo, KQo, KJo, QJo
dominated_broadway_watchlist = KQo, KJo, KJs, AJo, QJs, AQo
suited_connector = T9s-54s
suited_ace = A2s-A5s, A6s-ATs
```

## Made Hand Class

```text
HIGH_CARD
ONE_PAIR
TWO_PAIR
TRIPS
STRAIGHT
FLUSH
FULL_HOUSE
QUADS
STRAIGHT_FLUSH
```

## Pair Relation

```text
NONE
UNDERPAIR
SECOND_PAIR
TOP_PAIR
OVERPAIR
```

## Kicker Bucket

```text
NONE
WEAK
MEDIUM
STRONG
TOP
```

## Draw Class

```text
NONE
GUTSHOT
OESD
FLUSH_DRAW
COMBO_DRAW
```

## Strategic Role

Strategic roles such as `bluffcatcher` are deferred until range modeling is defined. Do not encode them as static made-hand classes.

```text
DEFERRED
```

## Board Features

Board texture is multi-feature, not a single enum.

```text
is_paired
is_monotone
is_two_tone
is_connected
flush_completed
straight_completed
is_dynamic
```

## Bet Size Bucket

Use half-open intervals. All-in is a separate boolean flag, not a bucket.

```text
tiny = [0, 0.25)
small = [0.25, 0.40)
half = [0.40, 0.60)
large = [0.60, 0.90)
pot_plus = [0.90, infinity)
is_all_in = boolean
```

## Action Line Display

Use compact line notation for reports only:

```text
x/c flop -> x/c turn -> call river
cbet flop -> check turn -> fold river
call 3bet -> call flop -> call turn -> call river
face 4bet -> call -> no fold postflop
```

Do not create new tag names ad hoc in code. Update this dictionary first.
