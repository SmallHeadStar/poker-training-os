# Tag Dictionary

Tags translate parsed facts into poker semantics. They must be deterministic and testable.

## Pot Type

```text
SRP = single-raised pot
3BP = 3bet pot
4BP = 4bet pot
LIMP = limped pot
MULTIWAY = multiway pot
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

## Street Hand Class

```text
air
draw
combo_draw
weak_pair
second_pair
top_pair_weak_kicker
top_pair_good_kicker
overpair
two_pair_plus
nut_advantage_hand
bluffcatcher
```

## Board Texture

```text
dry
two_tone
monotone
paired
connected
high_card
low_card
dynamic
static
```

## Bet Size Bucket

```text
tiny = less than 25% pot
small = 25%-40% pot
half = 40%-60% pot
large = 60%-90% pot
pot_plus = 90% pot or more
all_in = all-in
```

## Action Line

Use compact line notation:

```text
x/c flop -> x/c turn -> call river
cbet flop -> check turn -> fold river
call 3bet -> call flop -> call turn -> call river
face 4bet -> call -> no fold postflop
```

Do not create new tag names ad hoc in code. Update this dictionary first.
