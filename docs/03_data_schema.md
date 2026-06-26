# Data Schema Draft

This is the initial contract for data modeling. The exact physical schema may evolve, but the logical layers should remain stable.

## RAW

### import_batches

```text
batch_id
source_site
stake
game_type
import_time
file_count
hand_count
raw_file_hash
parser_version
notes
```

### raw_hands

```text
raw_hand_id
batch_id
raw_text
raw_hand_hash
parse_status
parse_error
created_at
```

## BASE

### hands

```text
hand_id
batch_id
site
stake
table_type
max_players
button_seat
hero_name
small_blind
big_blind
started_at
```

### players

```text
hand_id
seat_no
player_id
display_name
is_hero
starting_stack
position
```

### actions

```text
hand_id
street
action_order
player_id
position
action_type
amount
pot_before
raw_line
```

### boards

```text
hand_id
flop_cards
turn_card
river_card
```

### showdowns

```text
hand_id
player_id
cards
shown
hand_description
```

### results

```text
hand_id
player_id
net_amount
net_bb
all_in_ev_amount
all_in_ev_bb
rake_amount
```

## DERIVED

### derived_spots

```text
hand_id
spot_id
pot_type
hero_position
villain_position
position_relation
preflop_line
effective_stack_bb
hero_hand
hero_hand_group
flop_texture
flop_hand_class
turn_hand_class
river_hand_class
action_line
river_decision
```

## LEAK

### leak_results

```text
leak_result_id
hand_id
spot_id
detector_name
matched
confidence
loss_bb
matched_reason
review_priority
```

## REVIEW / TRAINING

### review_items

```text
review_item_id
hand_id
leak_result_id
user_label
user_note
reviewed_at
```

### training_cycles

```text
cycle_id
start_batch_id
end_batch_id
focus_leaks
target_metrics
status
summary
```
