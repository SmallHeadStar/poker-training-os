# Storage Contract v0.1

## Purpose

Canonical hands are stored in DuckDB base tables before derived reports, spot features, or action-result analysis run.

## Tables

### `hands`

One row per canonical hand.

| Column | Type | Meaning |
| --- | --- | --- |
| `hand_id` | text | Canonical hand id. |
| `played_at` | timestamp/text | Parsed hand timestamp. |
| `table_type` | text | `cash`, `rush_and_cash`, `tournament`, or `unknown`. |
| `stake` | text | Human stake string. |
| `small_blind` | double | Small blind amount. |
| `big_blind` | double | Big blind amount. |
| `hero_position` | text | Hero position. |
| `hero_hole_cards` | text | Space-separated Hero cards. |
| `source_file` | text | Source file path when available. |

### `players`

One row per seated player per hand.

### `actions`

One row per normalized action per hand, ordered by `order_index`.

### `results`

One row per player result per hand. `net_bb` is observed full-hand result, not EV.

## Implementation rule

Polars is used to materialize typed dataframes. DuckDB stores and queries the base tables.

