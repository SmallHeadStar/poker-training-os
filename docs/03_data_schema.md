# Data Schema Draft

Status: this schema describes the native parser fallback / later route. Current V0.1 uses the H2N4 Bridge contracts in `docs/h2n_export_contract.md` and `docs/output_layer.md`.

Do not implement these parser-native tables for V0.1 unless the Product Orchestrator explicitly switches back to the native parser route.

This is the initial physical contract for data modeling. Types use SQL-like names. Monetary and chip fields must be Decimal-compatible, not binary float.

Conventions:

- Primary keys use internal surrogate keys ending in `_pk`.
- External hand identifiers are stored separately and constrained per site.
- Source timestamps are normalized to UTC while preserving source timezone.
- Player identifiers are hand-scoped in V0.1.
- Parser, tagger, stats, and detector outputs must carry version fields.
- Nullable means explicitly allowed to be missing; otherwise fields are required.

## RAW

### import_batches

```text
batch_pk UUID PRIMARY KEY NOT NULL
source_site TEXT NOT NULL
stake TEXT NULL
game_type TEXT NULL
imported_at_utc TIMESTAMP NOT NULL
source_timezone TEXT NULL
file_count INTEGER NOT NULL
hand_count INTEGER NOT NULL
parser_version TEXT NOT NULL
notes TEXT NULL
```

### import_files

```text
file_pk UUID PRIMARY KEY NOT NULL
batch_pk UUID NOT NULL REFERENCES import_batches(batch_pk)
source_path TEXT NULL
file_name TEXT NOT NULL
file_hash TEXT NOT NULL
file_size_bytes INTEGER NOT NULL
imported_at_utc TIMESTAMP NOT NULL
UNIQUE(file_hash)
```

### raw_hands

```text
raw_hand_pk UUID PRIMARY KEY NOT NULL
batch_pk UUID NOT NULL REFERENCES import_batches(batch_pk)
file_pk UUID NULL REFERENCES import_files(file_pk)
raw_text TEXT NOT NULL
raw_hand_hash TEXT NOT NULL
site_hand_id TEXT NULL
parse_status TEXT NOT NULL CHECK parse_status IN ('pending','parsed','failed','skipped_duplicate')
parse_error TEXT NULL
created_at_utc TIMESTAMP NOT NULL
UNIQUE(raw_hand_hash)
```

## BASE

### hands

```text
hand_pk UUID PRIMARY KEY NOT NULL
raw_hand_pk UUID NOT NULL REFERENCES raw_hands(raw_hand_pk)
batch_pk UUID NOT NULL REFERENCES import_batches(batch_pk)
site TEXT NOT NULL
site_hand_id TEXT NOT NULL
game_type TEXT NOT NULL
stake TEXT NULL
table_type TEXT NULL
max_players INTEGER NOT NULL
button_seat INTEGER NULL
hero_hand_player_key TEXT NOT NULL
small_blind_amount DECIMAL(18,6) NOT NULL
big_blind_amount DECIMAL(18,6) NOT NULL
started_at_utc TIMESTAMP NULL
source_timezone TEXT NULL
parser_version TEXT NOT NULL
UNIQUE(site, site_hand_id)
```

### players

```text
player_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
hand_player_key TEXT NOT NULL
seat_no INTEGER NULL
display_name TEXT NULL
is_hero BOOLEAN NOT NULL
starting_stack_amount DECIMAL(18,6) NULL
starting_stack_bb DECIMAL(18,6) NULL
position TEXT NULL
UNIQUE(hand_pk, hand_player_key)
```

### actions

```text
action_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
street TEXT NOT NULL CHECK street IN ('preflop','flop','turn','river','showdown','summary')
action_order INTEGER NOT NULL
player_pk UUID NULL REFERENCES players(player_pk)
position TEXT NULL
action_type TEXT NOT NULL
amount_put_in_bb DECIMAL(18,6) NULL
raise_to_bb DECIMAL(18,6) NULL
amount_to_call_before_bb DECIMAL(18,6) NULL
pot_before_action_bb DECIMAL(18,6) NULL
pot_after_action_bb DECIMAL(18,6) NULL
is_all_in BOOLEAN NOT NULL DEFAULT false
is_forced_post BOOLEAN NOT NULL DEFAULT false
raw_line TEXT NOT NULL
UNIQUE(hand_pk, street, action_order)
```

Action type values:

```text
post_sb
post_bb
post_ante
fold
check
call
bet
raise
return_uncalled
collect
show
muck
```

Amount semantics:

- `amount_put_in_bb`: incremental chips put in by this action.
- `raise_to_bb`: total street contribution after a raise, when available.
- `amount_to_call_before_bb`: amount needed to call before this action.
- `pot_before_action_bb`: pot before this action.
- `pot_after_action_bb`: pot after this action.
- `is_all_in`: all-in is an attribute of bet/call/raise, not a separate action type.

### boards

```text
board_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
flop_cards TEXT NULL
turn_card TEXT NULL
river_card TEXT NULL
```

### showdowns

```text
showdown_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
player_pk UUID NOT NULL REFERENCES players(player_pk)
cards TEXT NULL
shown BOOLEAN NOT NULL
hand_description TEXT NULL
```

### results

```text
result_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
player_pk UUID NOT NULL REFERENCES players(player_pk)
net_amount DECIMAL(18,6) NOT NULL
net_bb DECIMAL(18,6) NOT NULL
all_in_ev_amount DECIMAL(18,6) NULL
all_in_ev_bb DECIMAL(18,6) NULL
rake_amount DECIMAL(18,6) NULL
```

## DERIVED

### decision_nodes

One hand may emit multiple decision nodes.

```text
node_pk UUID PRIMARY KEY NOT NULL
hand_pk UUID NOT NULL REFERENCES hands(hand_pk)
street TEXT NOT NULL
actor_player_pk UUID NOT NULL REFERENCES players(player_pk)
source_action_pk UUID NOT NULL REFERENCES actions(action_pk)
action_order INTEGER NOT NULL
facing_action_type TEXT NULL
pot_type TEXT NOT NULL
player_count_context TEXT NOT NULL
hero_position TEXT NULL
villain_position TEXT NULL
position_relation TEXT NULL
effective_stack_before_bb DECIMAL(18,6) NULL
pot_before_action_bb DECIMAL(18,6) NULL
amount_to_call_bb DECIMAL(18,6) NULL
bet_size_pot_fraction DECIMAL(18,6) NULL
action_taken TEXT NOT NULL
hand_strength_snapshot TEXT NULL
board_feature_snapshot JSON NULL
line_before_action TEXT NULL
tagger_version TEXT NOT NULL
UNIQUE(hand_pk, source_action_pk)
```

`line_before_action` is a display/debug field. The underlying facts remain `actions` plus `decision_nodes`.

## LEAK

### detector_matches

```text
match_pk UUID PRIMARY KEY NOT NULL
detector_name TEXT NOT NULL
detector_version TEXT NOT NULL
node_pk UUID NOT NULL REFERENCES decision_nodes(node_pk)
matched BOOLEAN NOT NULL
match_strength DECIMAL(5,4) NULL
reason_codes JSON NOT NULL
data_completeness DECIMAL(5,4) NULL
created_at_utc TIMESTAMP NOT NULL
UNIQUE(detector_name, detector_version, node_pk)
```

### outcome_evidence

```text
evidence_pk UUID PRIMARY KEY NOT NULL
match_pk UUID NOT NULL REFERENCES detector_matches(match_pk)
hand_net_bb DECIMAL(18,6) NULL
decision_incremental_realized_bb DECIMAL(18,6) NULL
showdown_summary TEXT NULL
outcome_notes TEXT NULL
```

### leak_aggregates

```text
aggregate_pk UUID PRIMARY KEY NOT NULL
detector_name TEXT NOT NULL
detector_version TEXT NOT NULL
filter_scope JSON NOT NULL
opportunity_count INTEGER NOT NULL
match_count INTEGER NOT NULL
total_hand_net_bb DECIMAL(18,6) NULL
decision_incremental_bb DECIMAL(18,6) NULL
max_5_loss_share DECIMAL(8,6) NULL
sample_reliability TEXT NOT NULL
stats_version TEXT NOT NULL
```

## REVIEW / TRAINING

### review_items

```text
review_item_pk UUID PRIMARY KEY NOT NULL
match_pk UUID NOT NULL REFERENCES detector_matches(match_pk)
user_label TEXT NULL
user_note TEXT NULL
reviewed_at_utc TIMESTAMP NULL
```

### training_cycles

Training cycles are later scope. `focus_leaks` and `target_metrics` must become child tables or JSON with an explicit schema before implementation.

```text
cycle_pk UUID PRIMARY KEY NOT NULL
start_batch_pk UUID NULL REFERENCES import_batches(batch_pk)
end_batch_pk UUID NULL REFERENCES import_batches(batch_pk)
status TEXT NOT NULL
summary TEXT NULL
```
