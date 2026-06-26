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

Preflop Raise.

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

## Node Metrics

### Node Result

```text
node_result_bb = sum(net_bb for hands matching node)
node_bb_per_100 = node_result_bb / node_hand_count * 100
```

### Review Priority

Initial heuristic:

```text
review_priority = loss_bb * confidence * repeat_factor
```

Where:

- `loss_bb` is the positive absolute value of negative result.
- `confidence` is detector confidence from 0 to 1.
- `repeat_factor` increases when the same node appears repeatedly.

The exact formula must be versioned once implemented.

## River Call Result

```text
river_call_result_bb = sum(net_bb for hands where hero called a river bet)
river_call_count = count(hands where hero called a river bet)
river_call_avg_bb = river_call_result_bb / river_call_count
```

Split river calls by IP/OOP, pot type, bet size bucket, and hand class whenever sample size allows.
