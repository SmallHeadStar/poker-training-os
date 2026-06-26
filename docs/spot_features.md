# Spot Features v0.1

## Purpose

Spot features are normalized fields used to build H2N4-style filtered reports without cloning the full H2N4 filter builder.

## Output grain

Phase 3 emits one row per Hero decision action. A row is an observation about the spot where Hero acted, not an EV claim.

## Required fields

| Field | v0.1 rule |
| --- | --- |
| `hand_id` | Canonical hand id. |
| `node_id` | Stable hand-local decision id. |
| `street` | Hero decision street. |
| `hero_position` | Parser-derived Hero position. |
| `pot_type` | Derived from preflop raise count: `limped_pot`, `single_raised_pot`, `three_bet_pot`, `four_bet_plus_pot`, or `unopened_preflop`. |
| `player_count_context` | `heads_up` or `multiway` based on active players before the decision. |
| `position_combo` | Hero position versus the most recent non-Hero actor when available. |
| `hero_ip_oop` | Approximate `ip`, `oop`, or `unknown`. |
| `preflop_line` | Coarse Hero line such as `hero_flat_vs_open`, `hero_open_faced_3bet`, `hero_3bet`, or `no_hero_vpip`. |
| `hero_hand_group` | Coarse hole-card group. |
| `made_hand_class` | v0.1 coarse class: `pair_or_better`, `no_pair`, `preflop`, or `unknown`. |
| `draw_class` | v0.1 coarse class: `flush_draw`, `backdoor_or_none`, `preflop`, or `unknown`. |
| `board_family` | Coarse board texture such as `king_high_rainbow_unpaired`. |
| `action_line_before` | Same-street action sequence before Hero's decision. |
| `facing_bet_size_bucket` | Preflop bb bucket or postflop pot-size bucket. |
| `hero_decision` | Hero action type. |
| `river_runout_class` | `river_blank_or_unknown`, `river_pairs_board`, `river_flush_completes`, or `not_river`. |
| `hand_net_bb` | Hero full-hand observed result. |

## H2N4 alignment

H2N4-style workflows depend on filtering by spot context and then showing both sample size and result. This v0.1 layer follows that report shape, but its card-classification logic is deliberately coarse until real H2N4 parity data is available.

## Limitations

- IP/OOP is approximate and should be rechecked against real hand histories.
- Made-hand and draw classes are intentionally simple.
- `hand_net_bb` is included for grouping and loss maps, but it must not be treated as decision EV.

