# Stats Dictionary

All formulas must be documented here before or alongside implementation.

## Basic Results

### bb

```text
bb = amount / big_blind_amount
```

### bb/100

```text
bb_per_100 = total_net_bb / hand_count * 100
```

### EV bb/100

```text
ev_bb_per_100 = total_all_in_ev_bb / hand_count * 100
```

Only calculate EV metrics when all-in EV data is available in the imported source.

## Preflop Stats

### VPIP

Voluntarily Put Money In Pot.

```text
VPIP = hands_where_hero_voluntarily_entered_pot / eligible_hands
```

Blinds posted automatically do not count as VPIP.

### PFR

```text
PFR = hands_where_hero_raised_preflop / eligible_hands
```

### 3bet

```text
3bet = hero_3bet_opportunities_taken / hero_3bet_opportunities
```

### Call 3bet

```text
call_3bet = hero_called_3bet / hero_faced_3bet
```

### Fold to 3bet

```text
fold_to_3bet = hero_folded_to_3bet / hero_faced_3bet
```

## Observed Node Metrics

### Observed Net Result For Occurrences

```text
observed_net_bb = sum(hand_net_bb for hands matching a node filter)
observed_net_bb_per_100_occurrences = observed_net_bb / occurrence_count * 100
```

This is an observed full-hand result for spots matching a filter. It is not decision EV and must not be presented as proof that a decision was correct or incorrect.

### Review Priority

Initial heuristic:

```text
review_priority = loss_or_cost_evidence * match_strength * repeat_factor
```

The exact formula must be versioned once implemented.

## River Call Metrics

Keep full-hand result separate from the river decision result.

### Hand Net Result

```text
hand_net_bb = final full-hand result for Hero
```

Use this for overall bankroll and graph-style reporting.

### River Call Incremental Realized Result

This estimates the realized increment of calling relative to folding at the river decision.

```text
river_call_incremental_realized_bb =
  if Hero loses at showdown: -call_amount_bb
  if Hero wins: amount_collected_after_call_bb - call_amount_bb
  if split: amount_returned_to_hero_after_call_bb - call_amount_bb
```

Also calculate:

```text
required_equity = call_amount_bb / (pot_before_call_bb + call_amount_bb)
showdown_win_share
river_call_count
river_call_incremental_total_bb
river_call_incremental_avg_bb
```

Do not call this EV. It is realized incremental outcome from observed hands.
