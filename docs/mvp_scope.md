# MVP Scope

## Core chain

1. GG PokerCraft hand history import.
2. Canonical hand JSON.
3. DuckDB base tables.
4. Decision nodes.
5. Spot features.
6. Basic reports.
7. Simplified action-result views.
8. Auto spot miner.
9. Issue cards.
10. Review queue.
11. GTO study cards.
12. Training cycle update.
13. `session_review.md` and Streamlit dashboard.

## Phase 0

- Position the product as a personal post-session trainer.
- Define boundaries and non-goals.
- Define canonical data contracts.
- Define reporting artifacts.
- Define dashboard v0.1.
- Add minimal tests that keep the contracts present.

## Phase 1

Build the smallest GG PokerCraft parser that emits canonical JSON. Do not feed raw hand-history text directly into analysis logic.

Required fields:

- `hand_id`
- `played_at`
- `stake`
- `table_type`
- `hero`
- `hero_hole_cards`
- `players`
- `actions`
- `board`
- `showdown`
- `results`

## Phase 2

Implement basic reports and document every statistic in `docs/stats_dictionary.md`.

## Phase 3

Implement structured spot features and a configurable query layer.

## Phase 4

Implement simplified action-result analysis with careful attribution boundaries.

## Phase 5

Mine repeated losing spots and include reliability warnings.

## Phase 6

Create issue cards and a review queue with human labels.

## Phase 7

Build a compact Streamlit dashboard with five areas:

- Session Summary
- Basic Reports
- Loss Map
- Issue Cards
- Review Queue / Training Focus

## Phase 8

Generate session artifacts:

- `session_review.md`
- `session_summary.json`
- `basic_reports.csv`
- `loss_map.csv`
- `issue_cards.json`
- `review_queue.csv`
- `gto_study_cards.md`
- `training_cycle_update.json`

