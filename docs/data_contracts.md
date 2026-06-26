# Data Contracts

## Principle

Raw hand-history text is an input format, not an analysis model. The parser must emit canonical JSON before any reporting, filtering, or decision analysis runs.

## Canonical hand JSON

Required top-level fields:

| Field | Type | Description |
| --- | --- | --- |
| `schema_version` | string | Version of this canonical contract. |
| `source` | object | Import metadata and source file reference. |
| `hand_id` | string | Unique hand identifier from the hand history. |
| `played_at` | string | ISO-8601 timestamp when available. |
| `game` | object | Game family, stake, currency, table type, and max seats. |
| `hero` | object | Hero player identity and seat or position if known. `hero.player` is the canonical screen name used by reports and spot analysis. |
| `players` | array | Seats, names, stacks, positions, and hero flag. |
| `hero_hole_cards` | array | Hero private cards when present. |
| `actions` | array | Ordered actions by street. |
| `board` | object | Flop, turn, and river cards. |
| `showdown` | array | Revealed hands and outcomes when available. |
| `results` | array | Per-player net results and pot collection details. |
| `parser_warnings` | array | Non-fatal parsing uncertainty. |

Hero identity rules:

- If an exact Hero screen name is supplied during import, it is used as `hero.player`.
- Otherwise, the parser infers `hero.player` from the private-card line shaped like `Dealt to <player> [Ah Kh]`.
- If neither path is available, the hand remains parseable but receives a parser warning and downstream Hero-centric reports should treat the hand as provisional or incomplete.

## Action object

Required fields:

| Field | Type | Description |
| --- | --- | --- |
| `street` | string | `preflop`, `flop`, `turn`, `river`, or `showdown`. |
| `order` | integer | Stable order within the hand. |
| `player` | string | Acting player. |
| `action_type` | string | Normalized action such as `fold`, `call`, `bet`, `raise`, `check`, `post_blind`, `ante`. |
| `amount` | number or null | Amount in table currency when available. |
| `amount_bb` | number or null | Amount converted to big blinds when reliable. |
| `facing_amount_bb` | number or null | Current bet faced before the action when reliable. |
| `pot_before_bb` | number or null | Pot before action when reliable. |
| `raw_text` | string | Source line for traceability. |

## Decision node

Decision nodes are derived records, not parser output.

Required fields:

- `hand_id`
- `node_id`
- `street`
- `hero_position`
- `villain_position`
- `pot_type`
- `preflop_line`
- `action_line_before`
- `facing_bet_size_bucket`
- `hero_decision`
- `hand_net_bb`
- `observed_result`
- `decision_incremental_bb`
- `attribution_warning`

## Storage policy

- DuckDB stores base tables and derived analysis tables.
- Polars performs core dataframe transformations.
- pandas is only allowed for compatibility with libraries that require it.
